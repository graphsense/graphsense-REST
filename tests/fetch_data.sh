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
  echo "Fetching data from $src.$table $filter ..."
  out=$outdir$dst.$table
  temp=`mktemp`
  # executing query and removing header, footer and colors
  docker run -it --rm cassandra cqlsh $CASSANDRA_HOST -e "SELECT JSON * FROM $src.$table $filter" > $temp
  if [ $? -gt 0 ]; then
    cat $temp
    rm $temp
    exit 1
  fi
  cat $temp | tail -n+4 | head -n-2 | sed 's/\x1B\[[0-9;]\{1,\}[A-Za-z]//g'  > $out
  rm $temp
}

# hard code statistics:
echo $outdir$transformed_dst.summary_statistics
cat << EOF > $outdir$transformed_dst.summary_statistics
{"no_blocks": 3, "bucket_size": 25000, "no_address_relations": 3906549689, "no_addresses": 660644759, "no_clusters": 318170948, "no_tags": 6954, "no_transactions": 538169236, "timestamp": 1591915024}
EOF
blocks="(1,2)"
run raw         block               "where height in $blocks"
run raw         block_transactions  "where height in $blocks"
run transformed exchange_rates      "where height in $blocks"
run transformed address           "limit 3"
