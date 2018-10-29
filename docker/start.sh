#!/bin/bash
docker stop graphsenserest
docker rm graphsenserest
hosts=""
for host in spark1 spark2
do
   hosts+=" --add-host $host:"
   h=`dig +short $host`
   hosts+=${h:-`getent hosts $host | awk '{print $1}'`}
   #echo $hosts
done
docker run $hosts -d --name graphsenserest -p 9000:9000 -it graphsenserest
#--restart=always
docker ps
