#!/bin/bash

datadir=`dirname $0`/data
CASSANDRA_MOCK=$1
data="$2"
MOCK_CMD="docker exec $CASSANDRA_MOCK cqlsh"

TAG=develop

UTXO_SCHEMA="https://raw.githubusercontent.com/graphsense/graphsense-transformation/$TAG/scripts/"
ETH_SCHEMA="https://raw.githubusercontent.com/graphsense/graphsense-ethereum-transformation/$TAG/scripts/"

function schema() {
  temp=`mktemp`
  echo "Fetching $1 ..."
  curl -Ls $1 > $temp

  for c in $3; do
    create $temp $2 $c
  done
  rm $temp
}

function tagpacks() {
  temp=`mktemp`
  name=tagpack_schema.cql
  echo "Fetching $name ..."
  curl -Ls https://raw.githubusercontent.com/graphsense/graphsense-tagpack-tool/$TAG/tagpack/db/$name > $temp
  create $temp KEYSPACE_NAME tagpacks
  rm $temp
}

function create() {
  temp=$1
  search=$2
  replace=$3
  echo "Replace $search by $replace ..."
  sed -i "s/$search/$replace/g" $temp
  echo "Remove DROP ..."
  sed -i -r "s/^DROP KEYSPACE.+//" $temp
  echo "Copy to mockup database ..."
  docker cp $temp $CASSANDRA_MOCK:/
  echo "Creating schema ..."
  $MOCK_CMD -f /`basename $temp`
}

function insert_data () {
    echo "Insert test data from file $1 into Cassandra table $2..."
    $MOCK_CMD -e "TRUNCATE TABLE $2;"
    while IFS= read -r line
    do
        #line=`echo "$line" | sed -e 's/^[ \t\n\s]*//' | sed -e 's/[ \t\s\n]*$//'`
        [ -z "`echo $line | xargs`" ] && continue
        $MOCK_CMD -e "INSERT INTO $2 JSON '$line';"
        echo "Inserted test data record"
    done <"$1"
}

schema "$UTXO_SCHEMA/schema_raw.cql" btc "btc ltc"
schema "$UTXO_SCHEMA/schema_transformed.cql" btc "btc ltc"
schema "$ETH_SCHEMA/schema_raw.cql" eth eth
schema "$ETH_SCHEMA/schema_transformed.cql" eth eth
tagpacks

for filename in $data; do
  insert_data $filename `basename $filename`
done
