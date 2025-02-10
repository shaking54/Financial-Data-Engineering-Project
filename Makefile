# Paths
SPARK_COMPOSE=docker/docker-compose.spark.yaml
HDFS_COMPOSE=docker/docker-compose.hdfs.yaml
AIRFLOW_COMPOSE=docker/docker-compose.airflow.yaml
WAREHOUSE_COMPOSE=docker/docker-compose.warehouse.yaml

.PHONY: spark-start spark-stop hadoop-start hadoop-stop airflow-start airflow-stop all-start all-stop

# Spark
spark-start:
	docker compose --env-file .env -f $(SPARK_COMPOSE) up -d

spark-stop:
	docker compose -f $(SPARK_COMPOSE) down

# Hadoop
hdfs-start:
	docker compose --env-file .env -f $(HDFS_COMPOSE) up -d

hdfs-stop:
	docker compose -f $(HADOOP_COMPOSE) down

# Airflow
airflow-start:
	docker compose --env-file .env -f $(AIRFLOW_COMPOSE) up -d

airflow-stop:
	docker compose -f $(AIRFLOW_COMPOSE) down

#Warehouse	
warehouse-start:
	docker compose --env-file .env -f $(WAREHOUSE_COMPOSE) up -d

warehouse-stop:
	docker compose -f $(WAREHOUSE_COMPOSE) down

# Start/Stop all services
all-start: spark-start hadoop-start airflow-start warehouse-start
all-stop: spark-stop hadoop-stop airflow-stop warehouse-stop
