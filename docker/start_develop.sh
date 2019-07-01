#!/bin/bash
if [ $# -lt 1 ]; then
  echo "Usage: $0 \"<space separated list of hostnames>\""
  exit 1
fi
docker rm -f graphsense-rest
for host in $1
do
  echo $host
   hosts+=" --add-host $host:"
   h=`dig +short $host`
   hosts+=${h:-`getent hosts $host | awk '{print $1}'`}
done
docker run $hosts -d --name graphsense-rest -p 9000:9000 graphsense-rest
docker exec graphsense-rest bash -c 'cd /srv/graphsense-rest && python3 adddefaultusers.py'
docker ps
