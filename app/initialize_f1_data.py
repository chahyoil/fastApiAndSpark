import os
import logging
import requests
import zipfile
from utils.spark_utils import get_spark_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_f1_data():
    spark = get_spark_session()
    
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
            
            df.createOrReplaceTempView(table_name)
            logger.info(f"Successfully created temp view {table_name}")
            
            sample_data = spark.sql(f"SELECT * FROM {table_name} LIMIT 5").collect()
            logger.info(f"Sample data from {table_name}:")
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