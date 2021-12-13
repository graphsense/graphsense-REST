CASSANDRA_MOCK=$1

./start_cassandra_mock.sh $CASSANDRA_MOCK
./ingest_data.sh $CASSANDRA_MOCK "$2"
