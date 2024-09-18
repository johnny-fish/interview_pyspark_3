"""
Tools module contains reusable function
"""
from enum import Enum
from datetime import datetime, date
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

class Partition(Enum):
    "Partition Enum"
    DAY = "DAY"
    MONTH = "MONTH"
    YEAR = "YEAR"

def cast_datetime_to_str(date_value:datetime, partition_type: Partition) -> date:
    """
    Transformation of shopify configuration data
    :param date_value: date value
    :type date_value: datetime
    :param partition_type: granularity of partition
    :type partition_type: Partition
    :return: date of partition
    :rtype: date
    """
    if partition_type == Partition.DAY:
        return date_value.date()
    elif partition_type == Partition.MONTH:
        return date(date_value.year, date_value.month, 1)
    elif partition_type == Partition.YEAR:
        return date(date_value.year, 1, 1)

def enhance_df_with_technical_info(
    dataframe: DataFrame,
    partition_type:Partition,
    date_value: datetime,
    technical_field:str='_logical_date') -> DataFrame:
    """
    Transformation of shopify configuration data
    :param dataframe: input
    :type dataframe: DataFrame
    :param partition_type: granularity of partition
    :type partition_type: Partition
    :param date_value: date value
    :type date_value: datetime
    :param technical_field: name of the new field
    :type technical_field: str
    :return: datafram with new technical field
    :rtype: DataFrame
    """
    partition_value = F.lit(cast_datetime_to_str(date_value, partition_type))
    enhance_df = dataframe.withColumn(technical_field, partition_value)

    return enhance_df
