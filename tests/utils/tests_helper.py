"""
Helper for test
"""

import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark_fixture():
    """
    Spark Session builder
    """

    spark = SparkSession.builder.appName("Unit Test").getOrCreate()
    return spark
