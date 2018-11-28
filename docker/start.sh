#!/bin/bash
docker stop graphsenserest-python
docker rm graphsenserest-python
hosts=""
for host in spark1 spark2
do
   hosts+=" --add-host $host:"
   h=`dig +short $host`
   hosts+=${h:-`getent hosts $host | awk '{print $1}'`}
   #echo $hosts
done
docker run $hosts -d --name graphsenserest-python -p 9001:9000 -it graphsenserest-python
#--restart=always
docker ps
