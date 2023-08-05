from functools import wraps
from flask import request, make_response, jsonify
import json
import uuid
import logging
import time
import redis


def jwt_redis_auth(redis_instance, channel_name):
    def funct_decorator(org_function):
        @wraps(org_function)
        def authorize():
            """
            Authorization method that runs before all request to check if upcoming request
            is authorized in the system.
            """
            logging.info("Authorization")
            token = request.headers.get("Authorization")
            if token:
                token = token.replace("Bearer ", "")
            else:
                logging.error("Bearer Token was not found.")
                return (
                    make_response(
                        jsonify(
                            {
                                "message": "Token is missing",
                                "statusCode": 401,
                            }
                        )
                    ),
                    401,
                )

            request_id = str(uuid.uuid4())

            try:
                logging.info("Connecting to Redis Server")
                redis_client = redis_instance.client()
                pubsub = redis_client.pubsub()
                pubsub.subscribe(channel_name + ".reply")

                logging.info("Publishing message to Redis server for token validation.")
                redis_client.publish(
                    channel_name,
                    json.dumps(
                        {
                            "pattern": {"role": "auth", "cmd": "validate"},
                            "data": {"jwt": token},
                            "id": request_id,
                        }
                    ),
                )

                try:
                    timeout = time.time() + 5
                    logging.info("Waiting for Redis response.")
                    for message in pubsub.listen():
                        if message["type"] == "message":
                            data = json.loads(message["data"].decode("utf-8"))
                            if data["response"] is False and data["id"] == request_id:
                                logging.info("Redis response - Token is invalid")
                                return (
                                    make_response(
                                        jsonify(
                                            {
                                                "message": "Unauthorized",
                                                "statusCode": 401,
                                            }
                                        )
                                    ),
                                    401,
                                )
                            elif data["id"] == request_id:
                                logging.info("Redis response - Token is valid")
                                break
                        if time.time() > timeout:
                            raise TimeoutError
                except TimeoutError:
                    logging.error(
                        "Haven't received any answer from Redis for 5 seconds."
                    )
                    return (
                        make_response(
                            jsonify(
                                {
                                    "message": "Gateway Timeout",
                                    "statusCode": 504,
                                }
                            )
                        ),
                        504,
                    )
                pubsub.unsubscribe(channel_name + ".reply")
            except redis.exceptions.ConnectionError:
                logging.error("Redis refused to connect.")
                return (
                    make_response(
                        jsonify(
                            {
                                "message": "Bad Gateway",
                                "statusCode": 502,
                            }
                        )
                    ),
                    502,
                )
            return org_function()

        return authorize

    return funct_decorator
