import pytest
from utils.spark_utils import get_spark_session, stop_spark_session
from initialize_f1_data import initialize_f1_data

@pytest.fixture(scope="session")
def spark():
    spark = get_spark_session()
    initialize_f1_data()

    yield spark
    stop_spark_session()

@pytest.fixture
def client(spark):
    from main import app
    from fastapi.testclient import TestClient
    return TestClient(app)