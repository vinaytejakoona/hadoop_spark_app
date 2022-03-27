
This repo lets us create local spark cluster, hadoop cluster and yarn cluster in docker containers. We need to install just docker and docker-compose to use it.

# clone the repo

git clone https://github.com/vinaytejakoona/hadoop_spark_app.git

# Build docker images

If you don't want to build you can pull pre built images from docker hub (see next step)

Be in hadoop_spark_app directory to run docker-compose commands without needing to pass the path to yml file

cd hadoop_spark_app
docker-compose build

# Pull from docker hub

To use prebuilt images pull them from docker hub and re tag them

docker pull vinaytejakoona/base:latest
docker pull vinaytejakoona/master:latest
docker pull vinaytejakoona/worker:latest

docker tag vinaytejakoona/base:latest base:lastest
docker tag vinaytejakoona/master:latest master:latest
docker tag vinaytejakoona/worker:latest worker:latest

# Starting services

docker-compose up -d

It starts 2 containers : master, worker

| container | services |
| ------    | ------   |
| master    | Spark Master, Hadoop Namenode, Yarn ResourceManager |
| worker    | Spark Worker, Hadoop Datanode, Yarn NodeManager     |

All containers start in a docker bridge network named dockernet. This provides an isolated network and also allows containers to connect to each other.

# Scaling workers

you can add any number of workers depending on your available hardware resources.

docker-compose up -d --scale worker=2

# Start base container and Exec into container

We can use base container to submit workloads to cluster

With below command, present working directory is bind mounted to base container and it is available as local_mount directory inside container. This allows us to edit any file from outside container and changes would be available inside container. 


docker run -it --name base --network hadoopsparkapp_dockernet -p 4040:4040 -v $(pwd)/.:/local_mount base bash

if container already exists but it is not running use below commands

docker restart base 
docker exec -it base bash

# Put data on hdfs

hdfs dfs -put sampledata.txt /

hdfs dfs -ls /

hdfs dfs -cat /sampledata.txt


# Submit spark script to spark master

The script test_spark.py reads text data in hdfs and writes word counts to hdfs
```
cd local_mount

$SPARK_HOME/bin/spark-submit --conf spark.executor.memory=500M --conf spark.executor.cores=1 --master spark://master:7077  test_spark.py
```

you can check output using  : hdfs dfs -cat /output/part-*


# UI links

| service | link |
| ------  | ------ |
| spark master    |  https://<master-container-ip>:8080 |
| hadoop namenode |  https:/<master-container-ip>:9870  |
| yarn            |  https:/<master-container-ip>:8088  |


# Shutdown containers

Be in hadoop_spark_app directory

```
cd ..  
docker-compose down

```
# Extra

## generate sample text 

Follow below steps to generate random text data in hdfs as hadoop sequenceFile format

hadoop jar hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.2.jar randomtextwriter -D mapreduce.randomtextwriter.totalbytes=10 /generated

## Submit spark script to yarn 

```
cd local_mount

$SPARK_HOME/bin/spark-submit --conf spark.executor.memory=500M --conf spark.executor.cores=1 --master yarn test_spark.py
```

## Start pyspark console

To run spark interactively

```
$SPARK_HOME/bin/pyspark --conf spark.executor.memory=500M --conf spark.executor.cores=1 --master spark://master:7077
```

# Credits

Following pages have been a big help in creating this repo.

https://github.com/sdesilva26/docker-spark

https://phpfog.com/creating-hadoop-docker-image/

