CASSANDRA_MOCK=$1
ORGANIZATION=$2

docker run --rm --name $CASSANDRA_MOCK -p 9042:9042/tcp -d cassandra 
testcmd="docker exec $CASSANDRA_MOCK cqlsh -e 'describe keyspaces'"
echo "Waiting for DB ..."
bash -c "$testcmd" > /dev/null 2>&1 
while [ $? -gt 0 ]; do echo -n '.'; sleep 1; bash -c "$testcmd" > /dev/null 2>&1 ; done
echo
`dirname $0`/ingest_data.sh $CASSANDRA_MOCK $ORGANIZATION "$3"
exit $?
