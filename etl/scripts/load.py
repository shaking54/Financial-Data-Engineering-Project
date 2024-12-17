from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, lit

def load_data(params):
    input_path = params['star']
    db_url = params['db_url']
    db_properties = params['db_properties']
    spark_host = params['spark_host']
    
    spark = SparkSession.builder \
                        .appName("FinancialTransactionsETL") \
                        .master(spark_host) \
                        .config("spark.jars.packages", "org.postgresql:postgresql:42.2.5") \
                        .getOrCreate()

    # Load transformed data
    transactions = spark.read.csv(f"{input_path}/transactions")
    customers = spark.read.csv(f"{input_path}/customers",header=True, inferSchema=True)
    accounts = spark.read.csv(f"{input_path}/accounts",header=True, inferSchema=True)
    merchants = spark.read.csv(f"{input_path}/merchants",header=True, inferSchema=True)

    transactions.show()
    customers.show()
    accounts.show()
    merchants.show()

    # Write to database
    transactions.write.jdbc(db_url, f"fact_transactions", mode="append", properties=db_properties)
    customers.write.jdbc(db_url, f"dim_customers", mode="append", properties=db_properties)
    accounts.write.jdbc(db_url, f"dim_accounts", mode="append", properties=db_properties)
    merchants.write.jdbc(db_url, f"dim_merchants", mode="append", properties=db_properties)

    # Write to PostgreSQL
    # transactions.write \
    #     .format("jdbc") \
    #     .option("driver", "org.postgresql.Driver") \
    #     .option("url", "jdbc:postgresql://postgres:5432/finance_dw") \
    #     .option("dbtable", "fact_transactions") \
    #     .option("user", "postgres") \
    #     .option("password", "postgres") \
    #     .mode("append") \
    #     .save()
    spark.stop()


if __name__ == "__main__":
    db_url = "jdbc:postgresql://localhost:5432/finance_dw"
    db_properties = {"user": "postgres", "password": "postgres", "driver": "org.postgresql.Driver"}
    load_data("data/star", db_url, db_properties)
