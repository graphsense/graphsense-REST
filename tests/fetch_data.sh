#!/bin/bash

outdir=`dirname $0`/data/
raw_src=btc_raw_prod
raw_dst=btc_raw

bucket_size=25000

transformed_src=btc_transformed_20201007
transformed_dst=btc_transformed

CASSANDRA_HOST=192.168.243.101

function fetch() {
  typ=$1
  table=$2
  filter=$3
  append=$4
  if [ "$typ" == "raw" ]; then
    src=$raw_src
    dst=$raw_dst
  elif [ "$typ" == "transformed" ]; then
    src=$transformed_src
    dst=$transformed_dst
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
fetch raw         block               "where height in ($blocks)"
fetch raw         block_transactions  "where height in ($blocks)"
fetch transformed address           "where address_prefix in ('3Hrnn','1Arch') and address in ($addresses)"
#fetch transformed address           "where address_prefix in ('17DfZ') and address in ('17DfZja1713S3JRWA9jaebCKFM5anUh7GG')" append
address_id=`head -n 1 $outdir$transformed_dst.address | jq ".address_id" -`
address_id_group=`expr $address_id \/ $bucket_size`
fetch transformed address_transactions           "where address_id=$address_id and address_id_group=$address_id_group"
address_id=10102718
address_id_group=`expr $address_id \/ $bucket_size`
#fetch transformed address_transactions           "where address_id=$address_id and address_id_group=$address_id_group" append
while read line; do
  blocks=$blocks,`echo $line | jq .height -`
done < $outdir$transformed_dst.address_transactions
fetch transformed address_tags "where address in ($addresses)"
fetch transformed exchange_rates      "where height in ($blocks)"
fetch transformed address_incoming_relations "where dst_address_id=$address_id and dst_address_id_group=$address_id_group limit 2"
fetch transformed address_outgoing_relations "where src_address_id=$address_id and src_address_id_group=$address_id_group limit 2"
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
fetch transformed address_by_id_group "where address_id in ($address_id) and address_id_group in ($address_id_group)"
fetch transformed address_cluster "where address_id_group in ($address_id_group) and address_id in ($address_id)"
cluster_id=-1
cluster_id_group=-1
while read line; do
  cid=`echo $line | jq ".cluster"`
  cluster_id=$cluster_id,$cid
  cluster_id_group=$cluster_id_group,`expr $cid \/ $bucket_size`
done < $outdir$transformed_dst.address_cluster
fetch transformed cluster "where cluster_group in ($cluster_id_group) and cluster in ($cluster_id)"
fetch transformed cluster_tags "where cluster_group=705 and cluster=17642138 limit 2"
cluster_id=17642138
cluster_id_group=705
fetch transformed cluster_incoming_relations "where dst_cluster=$cluster_id and dst_cluster_group=$cluster_id_group limit 2"
fetch transformed cluster_outgoing_relations "where src_cluster=$cluster_id and src_cluster_group=$cluster_id_group limit 2"
fetch transformed cluster_addresses "where cluster_group=705 and cluster=17642138 limit 2"
address_id=-1
address_id_group=-1
while read line; do
  aid=`echo $line | jq ".address_id"`
  address_id=$address_id,$aid
  address_id_group=$address_id_group,`expr $aid \/ $bucket_size`
done < $outdir$transformed_dst.cluster_addresses
#fetch transformed address_by_id_group "where address_id_group in ($address_id_group) and address_id in ($address_id) limit 2" append
cluster_id=2818641
cluster_id_group=`expr $cluster_id / $BUCKET_SIZE`
fetch transformed cluster "where cluster_group in ($cluster_id_group) and cluster in ($cluster_id)"
