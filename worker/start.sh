# # start ssh server
/usr/sbin/sshd

# start hadoop
$HADOOP_HOME/bin/hdfs --daemon start datanode

$HADOOP_HOME/bin/yarn --daemon start nodemanager

$SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker -c $CORES -m $MEMORY spark://$MASTER_CONTAINER_NAME:7077