# # start ssh server
/usr/sbin/sshd 


# format namenode
$HADOOP_HOME/bin/hdfs namenode -format

# start hadoop
$HADOOP_HOME/bin/hdfs --daemon start namenode

$HADOOP_HOME/bin/yarn --daemon start resourcemanager

$HADOOP_HOME/bin/yarn --daemon start proxyserver

$SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master