#!/bin/bash
rm -rf /opt/hadoop/data/dataNode/*
rm -rf /hadoop/dfs
chown -R hadoop:hadoop /opt/hadoop/data/dataNode
chmod 775 /opt/hadoop/data/dataNode
hdfs datanode