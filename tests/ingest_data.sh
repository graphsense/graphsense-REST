#!/bin/bash

datadir=`dirname $0`/data
CASSANDRA_MOCK=$1
MOCK_CMD="docker exec $CASSANDRA_MOCK cqlsh"

TAG=develop

function schema() {
  temp=`mktemp`
  echo "Fetching $1 ..."
  curl -Ls https://raw.githubusercontent.com/graphsense/graphsense-transformation/$TAG/scripts/$1 > $temp

  create $temp btc btc
  create $temp btc ltc

}

function eth_schema() {
  temp=`mktemp`
  echo "Fetching $1 ..."
  cp /tmp/$1 $temp
  create $temp eth eth
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
  echo "Copy to mockup database ..."
  docker cp $temp $CASSANDRA_MOCK:/
  echo "Creating schema ..."
  $MOCK_CMD -f /`basename $temp`
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
eth_schema "schema_raw.cql"
eth_schema "schema_transformed.cql"
tagpacks

for filename in $datadir/*; do
  insert_data $filename `basename $filename`
done
