#!/bin/bash

datadir=`dirname $0`/data
TAGSTORE_MOCK=$1
data=""
if [ ! -z "$2" ]; then
    for f in $2; do
        case $f in tagstore/*)
            data="$data $f"
        esac
    done
fi
MOCK_CMD="docker exec $TAGSTORE_MOCK psql -U tagstore -d tagstore"

TAG=develop

SCHEMA="https://raw.githubusercontent.com/graphsense/graphsense-tagpack-tool/$TAG/tagpack/db/tagstore_schema.sql"

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
