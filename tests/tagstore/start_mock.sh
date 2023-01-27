#!/bin/bash
MOCK_DB=$1
ORGANIZATION=$2

docker run --rm --name $MOCK_DB -p 5432:5432/tcp -e POSTGRES_USER=tagstore -e POSTGRES_PASSWORD=tagstore -e POSTGRES_DB=tagstore -d postgres:14-alpine
testcmd="docker exec $MOCK_DB pg_isready"
echo "Waiting for DB ..."
bash -c "$testcmd" > /dev/null 2>&1 
while [ $? -gt 0 ]; do echo -n '.'; sleep 1; bash -c "$testcmd" > /dev/null 2>&1 ; done
echo
`dirname $0`/ingest_data.sh $MOCK_DB $ORGANIZATION "$3"
exit $?
