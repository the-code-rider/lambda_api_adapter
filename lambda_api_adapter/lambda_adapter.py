from fastapi import FastAPI, Header
from typing import Callable
import functools


def lambda_to_fastapi_route(path: str = "/test-lambda", event_source: str = "api_gateway"):
    """
    A decorator to convert an AWS Lambda handler to a FastAPI route.

    :param event_source:
    :param path: Path at which the FastAPI endpoint will be available.
    """

    def decorator(lambda_handler: Callable):
        app = FastAPI()

        @app.post(path)
        async def lambda_endpoint(request_body: dict, header:  list[str] | None = Header(default=None)):

            event = _get_event_from_body(request_body, header, event_source)

            context = {}  # Simulate an empty AWS Lambda context object

            # Invoke the Lambda function
            response = lambda_handler(event, context)

            # Convert Lambda response to FastAPI response format
            return {
                "statusCode": response.get("statusCode", 200),
                "body": response.get("body", ""),
                "headers": response.get("headers", {})
            }

        @functools.wraps(lambda_handler)
        def wrapper(*args, **kwargs):
            return lambda_handler(*args, **kwargs)

        # Attach FastAPI app to the wrapper function so it can be accessed outside
        wrapper.app = app
        return wrapper

    return decorator


def _get_event_from_body(body, header, event_source):
    if event_source == 'cloudwatch':
        event = _cloudwatch_event(body)
    elif event_source == 'sqs':
        event = _sqs_event(body)
    else:
        raise ValueError(f"Unsupported Event Source: {event_source}. Supported Event Sources: 1. cloudwatch 2. sqs")

    return event


# def _api_gateway_event(body, header):
    # event = {
    #     "body": body,
    #     "httpMethod": "POST",
    #     "headers": dict(header),
    #     "path": request.url.path,
    #     "queryStringParameters": dict(request.query_params)
    # }
    # # if 'headers'
    # return event

def _cloudwatch_event(body):
    event = {
        "awslogs": {
            "data": body
        }
    }
    return event


def _sqs_event(body):
    event = {
        "Records": [
            {
                "body": body,
                "eventSource": "aws:sqs",
                "messageId": "example-message-id",
                "receiptHandle": "example-receipt-handle"
            }
        ]
    }
    return event
