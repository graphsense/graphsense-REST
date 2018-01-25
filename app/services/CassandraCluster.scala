package services

import com.datastax.driver.core.{Cluster, Row, SimpleStatement, Statement}
import com.datastax.driver.core.utils.Bytes
import javax.inject.{Inject, Singleton}
import play.api.{Configuration, Logger}
import play.api.inject.ApplicationLifecycle
import reflect.runtime.universe.TypeTag
import scala.collection.JavaConverters._
import scala.collection.SortedMap
import scala.concurrent.Future
import scala.language.implicitConversions
import scala.reflect.runtime.universe._

import Parser.Context
import models._

@Singleton
class CassandraCluster @Inject() (lifecycle: ApplicationLifecycle, conf: Configuration) {

  /** Cassandra host configuration **/
  val host = conf.getOptional[String]("cassandra.host") getOrElse "127.0.0.1"
  val keyspace = conf.getOptional[String]("cassandra.keyspace") getOrElse "graphsense_transformed"

  /** Setup cluster connection **/
  val cassandraCluster = Cluster.builder().addContactPoint(host).build()
  Logger.info(s"Connecting to keyspace $keyspace on Cassandra cluster at $host.")
  
  private val connection = cassandraCluster connect keyspace

  implicit def getHexString(c: Context, i: Int) =
    HexString(Bytes.toHexString(c getBytes i) substring 2)

  implicit def getValue(c: Context, i: Int) = Parser.parse(c getUDTValue i, Bitcoin.curried, 0)

  implicit def getVolatileValue(c: Context, i: Int): VolatileValue = {
    val rate = exchangeRates(c.parent getInt "height")
    val satoshi = c getLong i
    val bitcoin = satoshi / 1e8
    VolatileValue(satoshi, bitcoin * rate.eur, bitcoin * rate.usd)
  }

  implicit def udtToTxSummary(c: Context) = Parser.parse(c, TxSummary.curried, 0)

  implicit def udtToTxInputOutput(c: Context) = Parser.parse(c, TxInputOutput.curried, 0)

  implicit def getTxIdTime(c: Context, i: Int) = Parser.parse(c getUDTValue i, TxIdTime.curried, 0)

  implicit def getAddressSummary(c: Context, i: Int) =
    Parser.parse(c getUDTValue i, AddressSummary.curried, 0)

  implicit def getClusterSummary(c: Context, i: Int) =
    Parser.parse(c getUDTValue i, ClusterSummary.curried, 0)    

  /** Create a prepared statement for selecting given columns from a given table using a given where clause condition **/
  private def ps(columns: String, table: String, clause: String) =
    connection.prepare(queryString(columns, table, Some(clause)))

  /** Create a query string for given columns, a given table, and an optional where clause **/
  private def queryString(columns: String, table: String, clause: Option[String] = None) = {
    val query = s"select $columns from $table" + (clause match {
      case Some(s) => " where " + s
      case None => ""
    })
    println(query)
    query
  }
    
  /** Converts (field) names from camel (e.g., blockHeight) to snake case (block_height) **/
  private def snakify(name : String) = name.replaceAll("([a-z])([A-Z])", "$1_$2").toLowerCase

  /** Extracts and retuns column names of a given model type as comma separated string **/
  private def cols[T](implicit ct: TypeTag[T]) = {
    for (a <- typeOf[T].members.filter(!_.isMethod))
    yield snakify(a.name.toString.dropRight(1))
  }.toList.reverse.mkString(", ")
    
  /** Prepared statement definitions **/
  private val blockQuery = ps(cols[models.Block], "block", "height=?")

  private val transactionsQuery = ps(cols[BlockTransactions], "block_transactions", "height=?")
  
  private val transactionSearchQuery = ps("tx_hash", "transaction", "tx_prefix=?")
  
  private val transactionQuery = ps(cols[Transaction], "transaction", "tx_prefix=? and tx_hash=?")
  
  private val addressSearchQuery = ps("address", "address", "address_prefix=?")
  
  private val addressQuery = ps(cols[Address], "address", "address_prefix=? and address=?")
  
  private val tagsQuery = ps(cols[RawTag], "graphsense_raw.tag", "address=?")
  
  private val addressTransactionsQuery =
    ps(cols[AddressTransactions], "address_transactions", "address_prefix=? and address=? limit ?")

  private val addressIncomingRelationsQuery = ps(
    cols[AddressIncomingRelations],
    "address_incoming_relations",
    "dst_address_prefix=? and dst_address=? limit ?")

  private val addressOutgoingRelationsQuery = ps(
    cols[AddressOutgoingRelations],
    "address_outgoing_relations",
    "src_address_prefix=? and src_address=? limit ?")

  private val addressClusterQuery =
    ps("cluster", "address_cluster", "address_prefix=? and address=?")

  private val clusterQuery = ps(cols[models.Cluster], "cluster", "cluster=?")
  
  private val clusterTagsQuery = ps(cols[RawTag], "cluster_tags", "cluster=?")
  
  private val clusterAddressesQuery =
    ps(cols[ClusterAddresses], "cluster_addresses", "cluster=? limit ?")
  
  private val clusterIncomingRelationsQuery = ps(
    cols[ClusterIncomingRelations],
    "cluster_incoming_relations",
    "dst_cluster=? limit ?")
  
  private val clusterOutgoingRelationsQuery = ps(
    cols[ClusterOutgoingRelations],
    "cluster_outgoing_relations",
    "src_cluster=? limit ?")

  private def toBinary(s: String) = Bytes.fromHexString("0x" + s)

  /** All exchange rates for all blocks **/
  val exchangeRates = {
    val q = new SimpleStatement(queryString(cols[ExchangeRates], "exchange_rates"))
    val parsedRows =
      for (e <- list(q, Parser.parse(_, ExchangeRates.curried, 0)).view)
      yield (e.height, e)
    SortedMap(parsedRows.toSeq: _*)
  }
 
  private def single[T](statement: Statement, converter: Row => T) =
    converter(connection.execute(statement).one())

  private def singleOption[T](statement: Statement, converter: Row => T) = {
    val rs = connection.execute(statement)
    if (rs.isExhausted()) None else Some(converter(rs.one()))
  }

  private def list[T](statement: Statement, converter: Row => T) =
    connection.execute(statement).asScala.map(converter)

  /** Search for transaction starting with a given prefix **/
  def transactionSearch(prefix: String) =
    list(transactionSearchQuery.bind(prefix), Parser.parse(_, TransactionHash, 0)).map(_.txHash.hex)

  /** Search for address starting with a given prefix **/
  def addressSearch(prefix: String) =
    list(addressSearchQuery.bind(prefix), _ getString 0)

  /** Retrieve block with given height **/
  def block(height: Int) =
    single(blockQuery.bind(Int box height), Parser.parse(_, models.Block.curried, 0))

  /** Retrieve transactions for a given block height **/
  def transactions(height: Int) =
    single(transactionsQuery.bind(Int box height), Parser.parse(_, BlockTransactions.curried, 0))

  /** Retrieve transaction with a given hash **/
  def transaction(hash: String) =
    singleOption(
      transactionQuery.bind(hash take 5, toBinary(hash)),
      Parser.parse(_, Transaction.curried, 0))

  /** Retrieve transactions for a given address (with a given limit) **/
  def addressTransactions(address: String, limit: Int) = list(
    addressTransactionsQuery.bind(address take 5, address, Int box limit),
    Parser.parse(_, AddressTransactions.curried, 0))

  /** Retrieve statistics for a given address **/
  def address(address: String) =
    singleOption(addressQuery.bind(address take 5, address), Parser.parse(_, Address.curried, 0))

  /** Retrieve tags for a given address **/
  def addressTags(address: String) =
    list(tagsQuery.bind(address), Parser.parse(_, RawTag.curried, 0))

  /** Retrieve incoming relations for a given address (filter by category) **/
  def addressIncomingRelations(address: String, limit: Int) =
    list(
      addressIncomingRelationsQuery
        .bind(address take 5, address, Int box limit),
      Parser.parse(_, AddressIncomingRelations.curried, 0))

  /** Retrieve outgoing relations for a given address (filter by category) **/      
  def addressOutgoingRelations(address: String, limit: Int) =
    list(
      addressOutgoingRelationsQuery
        .bind(address take 5, address, Int box limit),
      Parser.parse(_, AddressOutgoingRelations.curried, 0))

  /** Retrieve the cluster id for a given address **/
  def addressCluster(address: String) =
    singleOption(addressClusterQuery.bind(address take 5, address), _ getInt 0)

  /** Retrieve statistics for a given address cluster by cluster id **/
  def cluster(cluster: Int) =
    single(clusterQuery.bind(Int box cluster), Parser.parse(_, models.Cluster.curried, 0))
  
  /** Retrieve statistics for a given address cluster by address **/
  def cluster(address: String): Option[models.Cluster] = addressCluster(address) map cluster
  
  /** Retrieve tags for a given address cluster id **/
  def clusterTags(cluster: Int) =
    list(clusterTagsQuery.bind(Int box cluster), Parser.parse(_, RawTag.curried, 0))
  
  /** Retrieve implicit tags for a given address **/
  def implicitTags(address: String) =
    addressCluster(address).toIterable.flatMap(clusterTags).filter(_.address != address)
  
  /** Retrieve addresses belonging to a certain cluster **/
  def addresses(cluster: Int, limit: Int) =
    list(
      clusterAddressesQuery.bind(Int box cluster, Int box limit),
      Parser.parse(_, ClusterAddresses.curried, 0))
  
  /** Retrieve incoming relations for a given cluster **/
  def clusterIncomingRelations(cluster: String, limit: Int) =
    list(
        clusterIncomingRelationsQuery
          .bind(cluster, Int box limit),
        Parser.parse(_, ClusterIncomingRelations.curried, 0))
      .filter(_.srcCluster != cluster) // omit cycles for the time being
  
  /** Retrieve outgoing relations for a given cluster **/
  def clusterOutgoingRelations(cluster: String, limit: Int) =
    list(
        clusterOutgoingRelationsQuery
          .bind(cluster, Int box limit),
        Parser.parse(_, ClusterOutgoingRelations.curried, 0))
      .filter(_.dstCluster != cluster) // omit cycles for the time being

  lifecycle.addStopHook { () =>
    Logger.info("Closing connections to Cassandra Cluster.")
    Future.successful{
      connection.close()
      cassandraCluster.close()
    }
  }
}
