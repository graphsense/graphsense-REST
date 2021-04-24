#!/bin/bash

outdir=`dirname $0`/data/
#raw_src=_prod
raw_src=  # empty for eth_raw
tagpacks_src=_prod

bucket_size=25000

transformed_src=_20210326_fxr

CASSANDRA_HOST=192.168.243.101

function fetch() {
  currency=$1
  typ=$2
  table=$3
  filter=$4
  append=$5
  dst=$typ
  if [ "$typ" == "raw" ]; then
    src=$raw_src
  elif [ "$typ" == "transformed" ]; then
    src=$transformed_src
  elif [ "$typ" == "tagpacks" ]; then
    src=$tagpacks_src
  fi
  src=$typ$src
  if [ ! -z "$currency" ]; then
    src=${currency}_$src
    dst=${currency}_$dst
  fi
  out=$outdir$dst.$table
  if [ -z "$append" -a -s "$out" ]; then
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
  cmd="cat $temp | tail -n+4 | head -n-2 | sed 's/\x1B\[[0-9;]\{1,\}[A-Za-z]//g'"
  if [ -z "$append" ]; then
    bash -c "$cmd" > $out
  else
    bash -c "$cmd" >> $out
  fi
  rm $temp
}

blocks="1,2"
addresses="'3Hrnn1UN78uXgLNvtqVXMjHwB41PmX66X4','3Hrnn2xbNUBDfqgLQh6CwfutAm9dfVq67u','1Archive1n2C579dMsAu3iC6tWzuQJz8dN'"
fetch btc raw         block               "where height in ($blocks)"
fetch btc raw         block_transactions  "where height in ($blocks)"
fetch btc transformed address           "where address_prefix in ('3Hrnn','1Arch') and address in ($addresses)"
#fetch btc transformed address           "where address_prefix in ('17DfZ') and address in ('17DfZja1713S3JRWA9jaebCKFM5anUh7GG')" append
address_id=`head -n 1 $outdir$transformed_dst.address | jq ".address_id" -`
address_id_group=`expr $address_id \/ $bucket_size`
fetch btc transformed address_transactions           "where address_id=$address_id and address_id_group=$address_id_group"
address_id=10102718
address_id_group=`expr $address_id \/ $bucket_size`
#fetch btc transformed address_transactions           "where address_id=$address_id and address_id_group=$address_id_group" append
while read line; do
  blocks=$blocks,`echo $line | jq .height -`
done < $outdir$transformed_dst.address_transactions
fetch btc transformed address_tags "where address in ($addresses)"
fetch btc transformed exchange_rates      "where height in ($blocks)"
fetch btc transformed address_incoming_relations "where dst_address_id=$address_id and dst_address_id_group=$address_id_group limit 2"
fetch btc transformed address_outgoing_relations "where src_address_id=$address_id and src_address_id_group=$address_id_group limit 2"
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
fetch btc transformed address_by_id_group "where address_id in ($address_id) and address_id_group in ($address_id_group)"
fetch btc transformed address_cluster "where address_id_group in ($address_id_group) and address_id in ($address_id)"
cluster_id=-1
cluster_id_group=-1
while read line; do
  cid=`echo $line | jq ".cluster"`
  cluster_id=$cluster_id,$cid
  cluster_id_group=$cluster_id_group,`expr $cid \/ $bucket_size`
done < $outdir$transformed_dst.address_cluster
fetch btc transformed cluster "where cluster_group in ($cluster_id_group) and cluster in ($cluster_id)"
fetch btc transformed cluster_tags "where cluster_group=705 and cluster=17642138 limit 2"
cluster_id=17642138
cluster_id_group=705
fetch btc transformed cluster_incoming_relations "where dst_cluster=$cluster_id and dst_cluster_group=$cluster_id_group limit 2"
fetch btc transformed cluster_outgoing_relations "where src_cluster=$cluster_id and src_cluster_group=$cluster_id_group limit 2"
fetch btc transformed cluster_addresses "where cluster_group=705 and cluster=17642138 limit 2"
address_id=-1
address_id_group=-1
while read line; do
  aid=`echo $line | jq ".address_id"`
  address_id=$address_id,$aid
  address_id_group=$address_id_group,`expr $aid \/ $bucket_size`
done < $outdir$transformed_dst.cluster_addresses
#fetch btc transformed address_by_id_group "where address_id_group in ($address_id_group) and address_id in ($address_id) limit 2" append
fetch btc raw transaction "limit 2"
fetch btc transformed tag_by_label "limit 2"
fetch ltc transformed tag_by_label "limit 2"
fetch "" tagpacks taxonomy_by_key ""
fetch "" tagpacks concept_by_taxonomy_id ""
fetch btc transformed configuration ""
fetch ltc transformed configuration ""
fetch eth transformed configuration ""
fetch eth transformed summary_statistics ""
fetch eth raw block "limit 3"
fetch eth transformed address "limit 2"
fetch eth transformed address_ids_by_address_prefix "limit 2"
fetch eth transformed address_ids_by_address_id_group "limit 2"
fetch eth transformed exchange_rates "limit 2"
fetch eth transformed address_tags "limit 2"
fetch eth transformed transaction_ids_by_transaction_id_group "limit 2"
fetch eth transformed transaction_ids_by_transaction_prefix "limit 2"

