import pytest
from utils.spark_utils import get_spark, stop_spark_session
from initialize_f1_data import initialize_f1_data

@pytest.fixture(scope="session")
def spark():
    spark = get_spark()
    initialize_f1_data(spark)

    yield spark
    stop_spark_session()
    
@pytest.fixture
def client(spark):
    from main import app
    from fastapi.testclient import TestClient
    return TestClient(app)