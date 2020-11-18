CASSANDRA_MOCK=$1

docker rm -f $CASSANDRA_MOCK > /dev/null 2>&1
./start_cassandra_mock.sh $CASSANDRA_MOCK
./ingest_data.sh $CASSANDRA_MOCK
