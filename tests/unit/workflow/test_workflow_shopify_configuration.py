"Test workflow of Shopify configuration data"

from pyspark.testing.utils import assertDataFrameEqual
from etl.workflow.workflow_shopify_configuration import transform_shopify_configuration
from tests.utils.tests_helper import spark_fixture

class TestWorkflowShipifyConfiguration():
    "Test workflow of Shopify configuration data"

    def test_transform_shopify_configuration(self, spark_fixture):
        "Test addition function"

        # GIVEN
        input_df = spark_fixture.read.option("delimiter", ",") \
            .option("header", True) \
            .option("inferSchema","true") \
            .csv("tests/data/shopify_configuration_input.csv")

        expected_df = spark_fixture.read.option("delimiter", ",") \
            .option("header", True) \
            .option("inferSchema","true") \
            .csv("tests/data/shopify_configuration_expected.csv")

        # WHEN
        transformed_df = transform_shopify_configuration(input_df)

        # THEN
        assertDataFrameEqual(transformed_df, expected_df)
