import os
from utils.logging_utils import get_logger
import requests
import zipfile
from utils.spark_utils import get_spark

logger = get_logger(__name__)

def initialize_f1_data(spark):

    database_name = "f1_database"

    try:
        spark.sql(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        spark.sql(f"USE {database_name}")
        logger.info(f"Using database: {database_name}")
    except Exception as e:
        logger.warning(f"Failed to create or use database {database_name}: {str(e)}")
        logger.info("Using default database")
        database_name = "default"  # 기본 데이터베이스 사용
    
    base_url = "http://ergast.com/downloads/f1db_csv.zip"
    zip_file_name = "f1db_csv.zip"
    base_path = '/tmp/f1db'

    os.makedirs(base_path, exist_ok=True)
    download_and_extract(base_url, zip_file_name, base_path)

    csv_files = [f for f in os.listdir(base_path) if f.endswith('.csv')]

    for file_name in csv_files:
        file_path = os.path.join(base_path, file_name)
        table_name = file_name.split('.')[0]

        logger.info(f"Processing file: {file_path}")

        try:
            df = spark.read.option("header", "true").csv(file_path)
            
            if df.count() == 0:
                logger.warning(f"DataFrame for {file_name} is empty")
            
            spark.sql(f"DROP TABLE IF EXISTS {database_name}.{table_name}")

            # 새 테이블 생성 및 데이터 삽입
            df.write.saveAsTable(f"{database_name}.{table_name}")
            logger.info(f"Successfully created table {database_name}.{table_name}")
            
            # 샘플 데이터 확인
            sample_data = spark.sql(f"SELECT * FROM {database_name}.{table_name} LIMIT 5").collect()
            logger.info(f"Sample data from {database_name}.{table_name}:")
            for row in sample_data:
                logger.info(str(row))
        except Exception as e:
            logger.error(f"Error processing {file_name}: {str(e)}")

    logger.info("All F1 data has been initialized in Spark.")

def download_and_extract(url, file_name, extract_to):
    response = requests.get(url)
    zip_path = os.path.join(extract_to, file_name)
    with open(zip_path, 'wb') as f:
        f.write(response.content)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    os.remove(zip_path)


if __name__ == "__main__":
    initialize_f1_data()