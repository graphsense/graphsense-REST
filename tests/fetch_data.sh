#!/bin/bash

outdir=`dirname $0`/data/
raw_src=btc_raw_prod
raw_dst=btc_raw

transformed_src=btc_transformed_20200611
transformed_dst=btc_transformed

CASSANDRA_HOST=192.168.243.101

function run() {
  typ=$1
  table=$2
  filter=$3
  if [ "$typ" == "raw" ]; then
    src=$raw_src
    dst=$raw_dst
  elif [ "$typ" == "transformed" ]; then
    src=$transformed_src
    dst=$transformed_dst
  fi
  echo "Fetching data from $src.$table where $filter ..."
  out=$outdir$dst.$table
  temp=`mktemp`
  # executing query and removing header, footer and colors
  docker run -it --rm cassandra cqlsh $CASSANDRA_HOST -e "SELECT JSON * FROM $src.$table where $filter" > $temp
  if [ $? -gt 0 ]; then
    cat $temp
    rm $temp
    exit 1
  fi
  cat $temp | tail -n+4 | head -n+2 | sed 's/\x1B\[[0-9;]\{1,\}[A-Za-z]//g'  > $out
  rm $temp
}

run raw         block               "height in (1, 2)"
run raw         block_transactions  "height=1"
run transformed exchange_rates      "height=1"
