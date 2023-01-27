#!/bin/bash

datadir=`dirname $0`/data
CASSANDRA_MOCK=$1
ORGANIZATION=$2
data=""
if [ ! -z "$3" ]; then
    for f in $3; do
        case $f in cassandra/*)
            data="$data $f"
        esac
    done
fi
MOCK_CMD="docker exec $CASSANDRA_MOCK cqlsh"

TAG=develop
ETHTAG=feature/token-flows

if [ -z "$ORGANIZATION" ]; then
    echo 'Please set env var $ORGANIZATION'
    exit 1
fi

UTXO_RAW_SCHEMA="https://raw.githubusercontent.com/$ORGANIZATION/graphsense-blocksci/$TAG/scripts/"
UTXO_TRANSFORMED_SCHEMA="https://raw.githubusercontent.com/$ORGANIZATION/graphsense-transformation/$TAG/scripts/"
ETH_RAW_SCHEMA="https://raw.githubusercontent.com/$ORGANIZATION/graphsense-ethereum-etl/$TAG/scripts/"
ETH_TRANSFORMED_SCHEMA="https://raw.githubusercontent.com/$ORGANIZATION/graphsense-ethereum-transformation/$ETHTAG/scripts/"

function schema() {
  temp=`mktemp`
  echo "Fetching $1 ..."
  if [ "${1:0:4}" = "http" ]; then
      curl -Ls $1 > $temp
  else
      cp $1 $temp
  fi

  for c in $3; do
    create $temp $2 $c
  done
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
        #echo $line
        #line=`echo "$line" | sed -e 's/^[ \t\n\s]*//' | sed -e 's/[ \t\s\n]*$//'`
        [ -z "`echo $line | xargs`" ] && continue
        #echo "INSERT INTO $2 JSON '$line';"
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
schema "`dirname $0`/schemas/schema.cql" btc "btc ltc"
schema "`dirname $0`/schemas/schema_eth.cql" eth eth

for filename in $data; do
  insert_data $filename `basename $filename`
done
