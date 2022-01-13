#!/bin/bash

datadir=`dirname $0`/data
CASSANDRA_MOCK=$1
data=""
if [ ! -z "$2" ]; then
    for f in $2; do
        case $f in cassandra/*)
            data="$data $f"
        esac
    done
fi
MOCK_CMD="docker exec $CASSANDRA_MOCK cqlsh"

TAG=develop

UTXO_RAW_SCHEMA="https://raw.githubusercontent.com/graphsense/graphsense-blocksci/$TAG/scripts/"
UTXO_TRANSFORMED_SCHEMA="https://raw.githubusercontent.com/graphsense/graphsense-transformation/$TAG/scripts/"
ETH_RAW_SCHEMA="https://raw.githubusercontent.com/graphsense/graphsense-ethereum-etl/$TAG/scripts/"
ETH_TRANSFORMED_SCHEMA="https://raw.githubusercontent.com/graphsense/graphsense-ethereum-transformation/$TAG/scripts/"

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
  replaced=`mktemp`
  echo "Replace $search by $replace ..."
  sed "s/$search/$replace/g" $temp > $replaced
  echo "Remove DROP ..."
  sed -i -r "s/^DROP KEYSPACE.+//" $replaced
  echo "Copy to mockup database ..."
  docker cp $replaced $CASSANDRA_MOCK:/
  echo "Creating schema ..."
  $MOCK_CMD -f /`basename $replaced`
  rm $replaced
}

function insert_data () {
    echo "Insert test data from file $1 into Cassandra table $2..."
    $MOCK_CMD -e "TRUNCATE TABLE $2;"
    while IFS= read -r line
    do
        #line=`echo "$line" | sed -e 's/^[ \t\n\s]*//' | sed -e 's/[ \t\s\n]*$//'`
        [ -z "`echo $line | xargs`" ] && continue
        $MOCK_CMD -e "INSERT INTO $2 JSON '$line';"
        if [ $? -ne 0 ]; then
            exit 1
        fi
        echo "Inserted test data record"
    done <"$1"
}

for filename in $data; do
    table=`basename $filename`
    echo "Drop table $table ...";
    $MOCK_CMD -e "DROP TABLE $table;"
done

schema "$UTXO_RAW_SCHEMA/schema.cql" graphsense "btc_raw ltc_raw"
schema "$UTXO_TRANSFORMED_SCHEMA/schema_transformed.cql" btc "btc ltc"
schema "$ETH_RAW_SCHEMA/schema.cql" eth eth
schema "$ETH_TRANSFORMED_SCHEMA/schema_transformed.cql" eth eth
tagpacks

for filename in $data; do
  insert_data $filename `basename $filename`
done