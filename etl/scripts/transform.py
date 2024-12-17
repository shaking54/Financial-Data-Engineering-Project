from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, lit

def transform_data(params):
    input_path = params['processed']
    output_path = params['star']
                         
    spark = SparkSession.builder \
        .appName("FinancialTransactionsETL") \
        .master("local[*]") \
        .getOrCreate()

    # Load raw data
    transactions = spark.read.csv(f"{input_path}/transactions.csv", header=True, inferSchema=True)
    customers = spark.read.csv(f"{input_path}/customers.csv", header=True, inferSchema=True)
    accounts = spark.read.csv(f"{input_path}/accounts.csv", header=True, inferSchema=True)
    merchants = spark.read.csv(f"{input_path}/merchants.csv", header=True, inferSchema=True)

    # Transform Customers Dimension
    customers_transformed = customers.withColumn("country", upper(col("country")))

    # Transform Accounts Dimension
    accounts_transformed = accounts.withColumn("account_type", upper(col("account_type")))

    # Transform Merchants Dimension
    merchants_transformed = merchants.withColumn("category", upper(col("category")))

    # Transform Transactions Fact Table
    transactions_transformed = transactions.withColumn("type", upper(col("type")))

    # Save to processed directory
    customers_transformed.write.option("header", "true").csv(f"{output_path}/customers", mode="overwrite")
    accounts_transformed.write.option("header", "true").csv(f"{output_path}/accounts", mode="overwrite")
    merchants_transformed.write.option("header", "true").csv(f"{output_path}/merchants", mode="overwrite")
    transactions_transformed.write.option("header", "true").csv(f"{output_path}/transactions", mode="overwrite")

    spark.stop()

if __name__ == "__main__":
    # Initialize Spark session
    params = {
        "input_path": "data/raw",
        "output_path": "data/processed"
    }
    transform_data(params)
