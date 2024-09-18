"""
Main to process Shopify configuration data
"""

import argparse
from datetime import datetime
from pyspark.sql import SparkSession
from etl.workflow.workflow_shopify_configuration import transform_shopify_configuration
from etl.tools.workflow_helper import enhance_df_with_technical_info, Partition

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Shopify configutation")
    parser.add_argument("--s3_bucket", required=True) 
    parser.add_argument("--logical_date", required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--aws_key_id", required=True)
    parser.add_argument("--aws_key_secret", required=True)
    parser.add_argument("--psql_ip", required=True)
    parser.add_argument("--psql_db", required=True)
    parser.add_argument("--psql_table", required=True)
    parser.add_argument("--psql_user", required=True)
    parser.add_argument("--psql_pwd", required=True)

    args = parser.parse_args()

    # Create a SparkSession
    spark = SparkSession.builder \
        .appName(f"Process Shopify configutation file: {args.filename}") \
        .getOrCreate()

    # Set S3 cred
    spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", args.aws_key_id)
    spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", args.aws_key_secret)
    # Import S3 FileSystem jar
    spark._jsc.hadoopConfiguration().set("fs.s3a.impl","org.apache.hadoop.fs.s3a.S3AFileSystem")

    # Read csv from S3
    input_df = spark.read.option("delimiter", ",") \
        .option("header", True) \
        .option("inferSchema", "true") \
        .csv(f"s3a://{args.s3_bucket}/{args.filename}")

    transform_df = transform_shopify_configuration(input_df)
    enhance_with_technical_field_df = enhance_df_with_technical_info(
        transform_df,
        Partition.DAY,
        datetime.strptime(args.logical_date, "%Y-%m-%d"))

    enhance_with_technical_field_df.show()
    enhance_with_technical_field_df.printSchema()
    enhance_with_technical_field_df \
        .write.mode("append") \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{args.psql_ip}:5432/{args.psql_db}") \
        .option("driver", "org.postgresql.Driver").option("dbtable", args.psql_table) \
        .option("user", args.psql_user).option("password", args.psql_pwd).save()

    spark.stop()
