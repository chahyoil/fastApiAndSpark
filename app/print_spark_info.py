import subprocess
import os
import sys
import pyspark
from pyspark.sql import SparkSession

def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing {command}: {str(e)}"

def get_spark_config():
    try:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()
        return {
            "Spark Master": spark.sparkContext.master,
            "App Name": spark.sparkContext.appName,
            "Executor Instances": spark.sparkContext._conf.get("spark.executor.instances", "Not set"),
            "Executor Cores": spark.sparkContext._conf.get("spark.executor.cores", "Not set"),
            "Executor Memory": spark.sparkContext._conf.get("spark.executor.memory", "Not set"),
        }
    except Exception as e:
        return f"Error getting Spark config: {str(e)}"

def get_installed_packages():
    return run_command("pip list")

def get_java_version():
    return run_command("java -version 2>&1")

def get_scala_version():
    return run_command("scala -version 2>&1")

def get_spark_version():
    return run_command("spark-submit --version 2>&1")

def get_pyspark_version():
    return f"PySpark version: {pyspark.__version__}"

def get_python_version():
    return sys.version

def get_spark_home():
    return os.environ.get('SPARK_HOME', 'SPARK_HOME not set')

def get_hadoop_version():
    return run_command("hadoop version 2>&1")

def main():
    print("\nSpark Configuration:")
    spark_config = get_spark_config()
    for key, value in spark_config.items():
        print(f"{key}: {value}")
    
    print("\nInstalled Python Packages:")
    print(get_installed_packages())

    print("=== Spark and Related Technologies Information ===")
    print("\nJava Version:")
    print(get_java_version())
    
    print("\nScala Version:")
    print(get_scala_version())
    
    print("\nSpark Version:")
    print(get_spark_version())
    
    print("\nPySpark Version:")
    print(get_pyspark_version())
    
    print("\nPython Version:")
    print(get_python_version())
    
    print("\nSPARK_HOME:")
    print(get_spark_home())
    
    print("\nHadoop Version:")
    print(get_hadoop_version())
    
    print("\nEnvironment Variables:")
    for key, value in os.environ.items():
        if 'SPARK' in key or 'JAVA' in key or 'SCALA' in key or 'HADOOP' in key:
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()