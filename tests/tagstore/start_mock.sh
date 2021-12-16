MOCK_DB=$1

docker run --rm --name $MOCK_DB -e POSTGRES_USER=tagstore -e POSTGRES_PASSWORD=pw -e POSTGRES_DB=tagstore -d postgres:14-alpine
testcmd="docker exec $MOCK_DB pg_isready"
echo "Waiting for DB ..."
bash -c "$testcmd" > /dev/null 2>&1 
while [ $? -gt 0 ]; do echo -n '.'; sleep 1; bash -c "$testcmd" > /dev/null 2>&1 ; done
echo
`dirname $0`/ingest_data.sh $MOCK_DB "$2"
exit $?
