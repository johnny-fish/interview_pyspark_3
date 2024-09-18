"""
Module for Shopify configuration data
"""
from pyspark.sql import DataFrame
import pyspark.sql.functions as F

def transform_shopify_configuration(input_dataframe: DataFrame) -> DataFrame:
    """
    Transformation of shopify configuration data
    :param input_dataframe: input
    :type input_dataframe: DataFrame
    :return: after apply transformation
    :rtype: DataFrame
    """

    output = input_dataframe \
        .filter(F.col("application_id").isNotNull()) \
        .withColumn("has_specific_prefix", \
                    F.when(F.col("index_prefix") != "shopify_", \
                           F.lit(True)) \
                    .otherwise(F.lit(False)))

    return output
