package services

object CassandraTables {
  
  val DefaultKeyspace = "graphsense_transformed"
  
  val exchangeRates = "exchange_rates"
  
  val block = "block"
  
  val blockTransactions = "block_transactions"
  
  val transaction = "transaction"

  val address = "address"

  val addressTransactions = "address_transactions"

  val addressSummary = "address_summary"

  val addressIncomingRelations = "address_incoming_relations"

  val addressOutgoingRelations = "address_outgoing_relations"

  val addressCluster = "address_cluster"

  val addressTags = "address_tags"
  
  val cluster = "cluster"

  val clusterAddresses = "cluster_addresses"

  val clusterTags = "cluster_tags"

  val clusterIncomingRelations = "cluster_incoming_relations"

  val clusterOutgoingRelations = "cluster_outgoing_relations"
  
}