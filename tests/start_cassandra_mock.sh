CASSANDRA_MOCK=$1

docker run --rm --name $CASSANDRA_MOCK -d cassandra 
testcmd="docker exec $CASSANDRA_MOCK cqlsh -e 'describe keyspaces'"
echo "Waiting for DB ..."
bash -c "$testcmd" > /dev/null 2>&1 
while [ $? -gt 0 ]; do echo -n '.'; sleep 1; bash -c "$testcmd" > /dev/null 2>&1 ; done
echo
./ingest_data.sh $CASSANDRA_MOCK "$2"
