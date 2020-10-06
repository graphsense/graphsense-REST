#!/bin/bash

datadir=`dirname $0`/data
CASSANDRA_MOCK=$1
MOCK_CMD="docker exec $CASSANDRA_MOCK cqlsh"

function schema() {
  temp=`mktemp`
  echo "Fetching $1 ..."
  curl -Ls https://raw.githubusercontent.com/graphsense/graphsense-transformation/master/scripts/$1 > $temp

  echo "Copy to mockup database ..."
  docker cp $temp $CASSANDRA_MOCK:/
  echo "Creating schema ..."
  $MOCK_CMD -f /`basename $temp`
  rm $temp
}

function insert_data () {
    echo "Insert test data from file $1 into Cassandra table $2..."
    while IFS= read -r line
    do
        #line=`echo "$line" | sed -e 's/^[ \t\n\s]*//' | sed -e 's/[ \t\s\n]*$//'`
        [ -z "`echo $line | xargs`" ] && continue
        $MOCK_CMD -e "INSERT INTO $2 JSON '$line';"
        echo "Inserted test data record"
    done <"$1"
}

schema "schema_raw.cql"
schema "schema_transformed.cql"

for filename in $datadir/*; do
  insert_data $filename `basename $filename`
done
