import os
from homework.utils import *

from aws_lambda_powertools.event_handler.api_gateway import APIGatewayRestResolver, Response


if os.environ["BACKEND"] == "better":
    config = BetterConfig()
else:
    config = Config()


app = APIGatewayRestResolver()


@app.get("/configuration")
def get_configuration() -> Response:
    c = config.get_configuration()
    return Response(status_code=201, content_type="application/json", body=json.dumps(c))


@app.put("/configuration")
def put_configuration() -> Response:
    c = config.get_configuration()
    return Response(status_code=203, content_type="application/json", body=json.dumps(c))


def handler(event, context):
    return app.resolve(event, context)
