from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("FinancialTransactionsETL") \
    .master("spark://spark-master-2:7077") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.2.5") \
    .getOrCreate()

# Read CSV data
transactions_df = spark.read.csv("./data/transactions.csv", header=True, inferSchema=True)

# Data transformation: Add a column for USD conversion
# transactions_df = transactions_df.withColumn("amount_usd", transactions_df["amount"] * 1.1)

# Show the DataFrame
transactions_df.show()

# Write to PostgreSQL
transactions_df.write \
    .format("jdbc") \
    .option("driver", "org.postgresql.Driver") \
    .option("url", "jdbc:postgresql://postgres:5432/finance_dw") \
    .option("dbtable", "fact_transactions") \
    .option("user", "postgres") \
    .option("password", "postgres") \
    .mode("append") \
    .save()

spark.stop()
