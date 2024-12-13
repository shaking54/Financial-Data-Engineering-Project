# Financial Data Engineering Project

This project involves building a robust **Data Warehouse** for the finance and banking sector. The focus is on designing a scalable architecture, implementing ETL pipelines, and leveraging **PySpark** for data processing. The outcome is an end-to-end solution for analytics and reporting on financial data.

## 🚀 **Objectives**
- Design and implement a **Data Warehouse** to store and organize financial data.
- Develop **ETL pipelines** to ingest, transform, and load data.
- Use **PySpark** for distributed data processing.
- Enable financial insights and analytics through optimized querying.

---

## 📂 **Project Structure**

```
finance-data-engineering-project/
├── data/               # Raw and processed data files
├── notebooks/          # Jupyter notebooks for exploration and prototyping
├── etl/                # PySpark scripts for ETL processing
├── models/             # Data modeling files (e.g., dbt or SQL scripts)
├── dags/               # Apache Airflow DAGs for pipeline orchestration
├── sql_queries/        # SQL scripts for analytics and reporting
├── config/             # Configuration files
├── docs/               # Project documentation
└── README.md           # Project overview (this file)
```

---

## 🛠 **Technologies**

| Technology          | Purpose                                    |
|---------------------|--------------------------------------------|
| **PySpark**         | Distributed data processing               |
| **Apache Airflow**  | ETL pipeline orchestration                |
| **PostgreSQL**      | Data Warehouse                            |
| **dbt**             | Data modeling and schema management       |
| **Python**          | General-purpose programming               |
| **Tableau / Power BI** | Data visualization                      |

---

## 📊 **Data Model**
The data model follows a **Star Schema** design for efficient querying and reporting:

### **Fact Table**
- **Transactions**: Records of financial transactions.
  - Columns: `transaction_id`, `account_id`, `date`, `amount`, `type`, `merchant_id`

### **Dimension Tables**
- **Customers**: Details about account holders.
  - Columns: `customer_id`, `name`, `email`, `dob`, `country`
- **Accounts**: Information about customer accounts.
  - Columns: `account_id`, `customer_id`, `account_type`, `balance`
- **Merchants**: Information about merchants where transactions occur.
  - Columns: `merchant_id`, `name`, `category`, `location`
- **Time**: A calendar table for time-based analysis.
  - Columns: `date`, `day`, `month`, `year`, `quarter`

---

## 🔄 **ETL Pipeline Overview**

1. **Extract**: Ingest raw financial data from CSV files or APIs.
2. **Transform**: Clean, aggregate, and normalize data using PySpark.
   - Tasks: Handle missing values, perform currency conversions, generate fraud detection flags.
3. **Load**: Load the transformed data into a PostgreSQL Data Warehouse.

### Example PySpark Workflow
```python
from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder \ 
    .appName("Financial ETL") \ 
    .getOrCreate()

# Read raw data
transactions_df = spark.read.csv("data/transactions.csv", header=True, inferSchema=True)

# Transformation: Currency conversion
transactions_df = transactions_df.withColumn("amount_usd", transactions_df["amount"] * 1.1)

# Write to PostgreSQL
transactions_df.write \ 
    .format("jdbc") \ 
    .option("url", "jdbc:postgresql://localhost:5432/finance_dw") \ 
    .option("finance_dw", "fact_transactions") \ 
    .option("user", "username") \ 
    .option("password", "password") \ 
    .save()
```

---

## 🛠️ **Setup Instructions**

### **Prerequisites**
1. Install **Python** (>= 3.8) and **Java** (for PySpark).
2. Set up a **PostgreSQL** instance.
3. Install dependencies:
   ```bash
   pip install pyspark airflow dbt psycopg2
   ```

### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/finance-data-engineering-project.git
   cd finance-data-engineering-project
   ```
2. Configure the database connection:
   - Create a `.env` file in the project root with the following content:
     ```env
     POSTGRES_HOST=postgres
     POSTGRES_PORT=5432
     POSTGRES_DB=finance_dw
     POSTGRES_USER=username
     POSTGRES_PASSWORD=password
     ```
   - Ensure the same `.env` file is used by your backend and `docker-compose.yml`.
3. Run Docker Compose:
   ```bash
   docker-compose --env-file .env up -d
   ```
4. Run a sample PySpark ETL job:
   ```bash
   python etl/transactions_etl.py
   ```
5. Start Apache Airflow:
   ```bash
   airflow webserver
   airflow scheduler
   ```
6. Test your pipeline using Airflow DAGs.

---

## 📈 **Analytics and Visualization**
- Use SQL queries to generate insights, such as:
  - **Total transactions per day**:
    ```sql
    SELECT date, COUNT(*) AS total_transactions 
    FROM fact_transactions 
    GROUP BY date;
    ```
  - **Top customers by spending**.
- Visualize data in Tableau or Power BI for interactive dashboards.

---

## 📚 **Future Enhancements**
- Implement real-time data ingestion using Kafka.
- Add machine learning for fraud detection.
- Migrate to a cloud-based Data Warehouse (e.g., Snowflake, Redshift).
