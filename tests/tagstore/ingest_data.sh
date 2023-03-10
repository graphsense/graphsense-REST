#!/bin/bash

datadir=`dirname $0`/data
TAGSTORE_MOCK=$1
ORGANIZATION=${2:$ORGANIZATION}
MOCK_CMD="docker exec $TAGSTORE_MOCK psql -U tagstore -d tagstore"

TAG=feature/actor_support

if [ -z "$ORGANIZATION" ]; then
    echo 'Please set env var $ORGANIZATION'
    exit 1
fi

SCHEMA="https://raw.githubusercontent.com/$ORGANIZATION/graphsense-tagpack-tool/$TAG/src/tagpack/db/tagstore_schema.sql"

function schema() {
  temp=`mktemp`
  echo "Fetching $1 ..."
  curl -Ls $1 > $temp

  create $temp 
  rm $temp
}

function create() {
  temp=$1
  $MOCK_CMD -c "drop schema if exists tagstore cascade"
  echo "Copy to mockup database ..."
  docker cp $temp $TAGSTORE_MOCK:/
  echo "Creating schema ..."
  $MOCK_CMD -f /`basename $temp`
}

function insert_data () {
    echo "Insert test data from file $1 into Postgres ..."
    docker cp $1 $TAGSTORE_MOCK:/
    $MOCK_CMD -f /`basename $1`
}

schema "$SCHEMA" 

for filename in $datadir/*; do
  insert_data $filename 
done
