# This base image comes shipped with java 8 (needed for scala)
FROM openjdk:11

# Set env variables
ENV DAEMON_RUN=true
ENV SPARK_VERSION=3.2.1
ENV SPARK_HADOOP_VERSION=3.2
ENV SCALA_VERSION=2.12.3
ENV SCALA_HOME=/usr/share/scala
ENV SPARK_HOME=/spark
ENV SPARK_OPTS --driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info
ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip
ENV HADOOP_HOME=/hadoop
ENV HADOOP_VERSION=3.2.2
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV YARN_CONF_DIR=$HADOOP_HOME/etc/hadoop

# Update commands
RUN apt-get update
RUN apt-get install -y wget tar bash coreutils procps openssl openssh-server

# Install Apache Hadoop
RUN wget --no-check-certificate https://dlcdn.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz 

RUN tar -xzf hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} ${HADOOP_HOME} && \
    echo "export JAVA_HOME=$JAVA_HOME \n\
    export HDFS_NAMENODE_USER=root \n\
    export HDFS_DATANODE_USER=root \n\
    export HDFS_SECONDARYNAMENODE_USER=root \n\
    export YARN_RESOURCEMANAGER_USER=root \n\
    export YARN_NODEMANAGER_USER=root \n\
    export HADOOP_SSH_OPTS=\"-p 22\"" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo "Host * \n\
  UserKnownHostsFile /dev/null \n\
  StrictHostKeyChecking no" > /etc/ssh/ssh_config && \
    echo "UsePrivilegeSeparation no" >> /etc/ssh/sshd_config

ENV PATH=$HADOOP_HOME/bin:$PATH 


# create ssh keys for hadoop connectivity
RUN ssh-keygen -A && \
  ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
  chmod 0600 ~/.ssh/authorized_keys 
  


# Install Scala
RUN cd "/tmp" && \
    wget "https://downloads.typesafe.com/scala/${SCALA_VERSION}/scala-${SCALA_VERSION}.tgz" && \
    tar xzf "scala-${SCALA_VERSION}.tgz" && \
    mkdir "${SCALA_HOME}" && \
    rm "/tmp/scala-${SCALA_VERSION}/bin/"*.bat && \
    mv "/tmp/scala-${SCALA_VERSION}/bin" "/tmp/scala-${SCALA_VERSION}/lib" "${SCALA_HOME}" && \
    ln -s "${SCALA_HOME}/bin/"* "/usr/bin/" && \
    rm -rf "/tmp/"* && \
    mkdir -p "/usr/local/sbt"

ENV PATH=/usr/local/sbt/bin:$PATH

# Get Apache Spark
RUN wget --no-check-certificate https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz 
# Install Spark and move it to the folder "/spark" and then add this location to the PATH env variable
RUN tar -xzf spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION} /spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz
    
ENV PATH=$SPARK_HOME/bin:$PATH

# update hadoop configs
COPY configs/*xml ${HADOOP_HOME}/etc/hadoop/

EXPOSE 22 4040
