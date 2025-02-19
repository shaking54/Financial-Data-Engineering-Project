#!/bin/bash

# Format NameNode if not already formatted
if [ ! -d "/opt/hadoop/data/nameNode/current" ]; then
    echo "Formatting NameNode..."
    hdfs namenode -format -force
fi

# Start HDFS NameNode
     &

# Wait for HDFS to be fully up
sleep 10

# Create necessary directories in HDFS
hdfs dfs -mkdir -p /data
hdfs dfs -put /data /data

# Ensure Airflow has correct ownership and permissions
hdfs dfs -chown -R airflow:supergroup /data
hdfs dfs -chmod -R 775 /data

# Keep the container running
tail -f /dev/null