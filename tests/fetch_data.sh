#!/bin/bash

outdir=`dirname $0`/data/
raw_src=btc_raw_prod
raw_dst=btc_raw

bucket_size=25000

transformed_src=btc_transformed_20201007
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
  out=$outdir$dst.$table
  if [ -s "$out" ]; then
    echo "$out is not empty"
    return
  fi
  echo "Fetching data from $src.$table $filter ..."
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

blocks="1,2"
addresses="'3Hrnn1UN78uXgLNvtqVXMjHwB41PmX66X4','3Hrnn2xbNUBDfqgLQh6CwfutAm9dfVq67u','1Archive1n2C579dMsAu3iC6tWzuQJz8dN'"
run raw         block               "where height in ($blocks)"
run raw         block_transactions  "where height in ($blocks)"
run transformed address           "where address_prefix in ('3Hrnn','1Arch') and address in ($addresses)"
address_id=`head -n 1 $outdir$transformed_dst.address | jq ".address_id" -`
address_id_group=`expr $address_id \/ $bucket_size`
run transformed address_transactions           "where address_id=$address_id and address_id_group=$address_id_group"
while read line; do
  blocks=$blocks,`echo $line | jq .height -`
done < $outdir$transformed_dst.address_transactions
run transformed address_tags "where address in ($addresses)"
run transformed exchange_rates      "where height in ($blocks)"
run transformed address_incoming_relations "where dst_address_id=$address_id and dst_address_id_group=$address_id_group limit 2"
run transformed address_outgoing_relations "where src_address_id=$address_id and src_address_id_group=$address_id_group limit 2"
while read line; do
  aid=`echo $line | jq ".src_address_id"`
  address_id=$address_id,$aid
  address_id_group=$address_id_group,`expr $aid \/ $bucket_size`
done < $outdir$transformed_dst.address_incoming_relations
while read line; do
  aid=`echo $line | jq ".dst_address_id"`
  address_id=$address_id,$aid
  address_id_group=$address_id_group,`expr $aid \/ $bucket_size`
done < $outdir$transformed_dst.address_outgoing_relations
echo "address_ids $address_id"
echo "address_id_groups $address_id_group"
run transformed address_by_id_group "where address_id in ($address_id) and address_id_group in ($address_id_group)"
run transformed address_cluster "where address_id_group in ($address_id_group) and address_id in ($address_id)"
cluster_id=-1
cluster_id_group=-1
while read line; do
  cid=`echo $line | jq ".cluster"`
  cluster_id=$cluster_id,$cid
  cluster_id_group=$cluster_id_group,`expr $cid \/ $bucket_size`
done < $outdir$transformed_dst.address_cluster
run transformed cluster "where cluster_group in ($cluster_id_group) and cluster in ($cluster_id)"
run transformed cluster_tags "where cluster_group=705 and cluster=17642138 limit 2"
