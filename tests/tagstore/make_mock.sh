MOCK_DB=$1

./start_mock.sh $MOCK_DB
./ingest_data.sh $MOCK_DB "$2"
