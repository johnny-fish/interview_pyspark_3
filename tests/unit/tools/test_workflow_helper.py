"Test workflow helper"

from datetime import date, datetime
from pyspark.testing.utils import assertDataFrameEqual
from etl.tools.workflow_helper import enhance_df_with_technical_info, Partition
from tests.utils.tests_helper import spark_fixture

def test_enhance_df_with_technical_info_day(spark_fixture):
    "Test addition function"

    # GIVEN
    input_data = [(1, 'abaaba'), (2, 'blabla')]
    input_df = spark_fixture.createDataFrame(input_data, ['id', 'name'])

    partition_type = Partition.DAY
    date_value = datetime(2001, 2, 3)
    technical_field, expeced_technical_value = '_logical_date', date(date_value.year, date_value.month, date_value.day)
    
    expected_data = [(1, 'abaaba', expeced_technical_value), (2, 'blabla', expeced_technical_value)]
    expected_df = spark_fixture.createDataFrame(expected_data, ['id', 'name', technical_field])

    # WHEN
    result_df = enhance_df_with_technical_info(input_df, partition_type, date_value, technical_field)

    # THEN
    assertDataFrameEqual(result_df, expected_df)
    
def test_enhance_df_with_technical_info_month(spark_fixture):
    "Test addition function"

    # GIVEN
    input_data = [(1, 'abaaba'), (2, 'blabla')]
    input_df = spark_fixture.createDataFrame(input_data, ['id', 'name'])

    partition_type = Partition.MONTH
    date_value = datetime(2001, 2, 3)
    technical_field, expeced_technical_value = '_logical_date', date(date_value.year, date_value.month, 1)
    
    expected_data = [(1, 'abaaba', expeced_technical_value), (2, 'blabla', expeced_technical_value)]
    expected_df = spark_fixture.createDataFrame(expected_data, ['id', 'name', technical_field])

    # WHEN
    result_df = enhance_df_with_technical_info(input_df, partition_type, date_value, technical_field)

    # THEN
    assertDataFrameEqual(result_df, expected_df)

def test_enhance_df_with_technical_info_year(spark_fixture):
    "Test addition function"

    # GIVEN
    input_data = [(1, 'abaaba'), (2, 'blabla')]
    input_df = spark_fixture.createDataFrame(input_data, ['id', 'name'])

    partition_type = Partition.YEAR
    date_value = datetime(2001, 2, 3)
    technical_field, expeced_technical_value = '_logical_date', date(date_value.year, 1, 1)
    
    expected_data = [(1, 'abaaba', expeced_technical_value), (2, 'blabla', expeced_technical_value)]
    expected_df = spark_fixture.createDataFrame(expected_data, ['id', 'name', technical_field])

    # WHEN
    result_df = enhance_df_with_technical_info(input_df, partition_type, date_value, technical_field)

    # THEN
    assertDataFrameEqual(result_df, expected_df)
