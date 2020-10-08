CASSANDRA_MOCK=cassandra_mock

docker run --name $CASSANDRA_MOCK -d cassandra 
if [ $? -gt 0 ]; then
  docker start $CASSANDRA_MOCK
else
  testcmd="docker exec $CASSANDRA_MOCK cqlsh -e 'describe keyspaces'"
  echo "Waiting for DB ..."
  bash -c "$testcmd" > /dev/null 2>&1 
  while [ $? -gt 0 ]; do echo -n '.'; sleep 1; bash -c "$testcmd" > /dev/null 2>&1 ; done
  echo
  ./tests/ingest_data.sh $CASSANDRA_MOCK
fi
ip=`docker exec $CASSANDRA_MOCK cat /etc/hosts | tail -n 1 | awk '{print $1}'`
sed -i "s/CASSANDRA_MOCK_IP/$ip/" ./tests/instance/config.py 
