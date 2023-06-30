import json
from datetime import datetime
import boto3


DEFAULT_NAMESPACE = "NAMEsspace"


class Config:

    def __init__(self, minimum_poll_interval_s: int = 10):
        self.minimum_poll_interval_s = minimum_poll_interval_s
        self.s3 = boto3.client("s3")
        self._changed_value = None
        self._last_time = None

    def get_configuration(self) -> dict:

        # if self._next_token is None:
        #     self._next_token = self._start_session()

        # broken cache logic
        # if datetime.utcnow() >= self._next_update_time:
        #     raw_configuration = self._make_request()
        #     if len(raw_configuration) > 0:
        #         logger.info("Configuration update received")
        #         self._last_response = parse_configuration(raw_configuration)

        return json.loads(self.s3.get_object(Bucket="Bucket", Key="key")['Body'].read())

    def put_configuration(self, dict) -> None:
        self.s3.put_object(Bucket="Bucket", Key="key", Body=json.dumps(dict))


class BetterConfig:

    def __init__(self):
        self.ssm = boto3.client('ssm')

    def get_configuration(self, namespace: str) -> dict:
        return json.loads(self.ssm.get_parameter(Name="Parameter")['Parameter']['Value'])

    def put_configuration(self, dict) -> None:
        self.ssm.put_parameter(Name="Parameter", Value=json.dumps(dict), Type="string")
