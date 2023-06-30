import pytest
import boto3
import moto

from homework.utils import Config


@pytest.fixture(scope="function")
def powertools_env(monkeypatch):
    monkeypatch.setenv("POWERTOOLS_LOG_DEDUPLICATION_DISABLED", "true")


@pytest.fixture(scope="function")
def s3_bucket():
    with moto.mock_s3():
        s3 = boto3.resource("s3")
        bucket = s3.create_bucket(Bucket="Bucket", CreateBucketConfiguration={"LocationConstraint": "eu-west-1"})
        yield bucket


@pytest.fixture(scope="function")
def ssm_parameter():
    with moto.mock_ssm():
        ssm = boto3.client("ssm", region_name="eu-west-1")
        ssm.put_parameter(Name="Parameter", Value="{}", Type="String")


def test_handler(s3_bucket, ssm_parameter, powertools_env):
    config = Config()
    value = {"value": "value"}
    config.put_configuration(value)
