package controllers

import javax.inject.{Inject, Singleton}
import play.api.libs.json.{JsObject, Json, Writes}
import play.api.mvc.{AbstractController, ControllerComponents}

import models._
import services.CassandraCluster

@Singleton
class BlockController @Inject()(comp: ControllerComponents, cc: CassandraCluster)
    extends AbstractController(comp) {

  def index = Action(Ok("This is the GraphSense REST API."))

  implicit val hexStringWrites = new Writes[HexString] {
    def writes(hexString: HexString) = Json.toJson(hexString.hex)
  }
  implicit val valueWrites = Json.writes[Bitcoin]
  implicit val volatileValueWrites = Json.writes[VolatileValue]
  implicit val txSummaryWrites = Json.writes[TxSummary]
  implicit val txInputOutputWrites = Json.writes[TxInputOutput]
  implicit val txIdTimeWrites = Json.writes[TxIdTime]
  implicit val addressSummaryWrites = Json.writes[AddressSummary]
  implicit val blockWrites = Json.writes[Block]
  implicit val transactionWrites = Json.writes[Transaction]
  implicit val richTransactionWrites = Json.writes[BlockTransactions]
  implicit val addressTransactionsWrites = Json.writes[AddressTransactions]
  implicit val addressWrites = Json.writes[Address]
  implicit val rawTagsWrites = Json.writes[RawTag]
  implicit val addressIncomingRelationsWrites = Json.writes[AddressIncomingRelations]
  implicit val addressOutgoingRelationsWrites = Json.writes[AddressOutgoingRelations]
  implicit val entityWrites = Json.writes[Cluster]
  implicit val clusterAddressesWrites = Json.writes[ClusterAddresses]

  def block(height: Int) = generalAction(cc.block(height))

  def transactions(height: Int) = generalAction(cc.transactions(height))
  
  def transaction(hash: String) = generalAction(cc.transaction(hash))
  
  def address(address: String) = generalAction(cc.address(address).map(bitcoinFlowToJson(_)))
  
  def tags(address: String) = generalAction(cc.tags(address))
  
  def implicitTags(address: String) = generalAction(cc.implicitTags(address))
  
  def clusterTags(cluster: Int) = generalAction(cc.clusterTags(cluster))
  
  def addressTransactions(address: String, limit: Int) =
    generalAction(cc.addressTransactions(address, limit))
  
  def clusterByAddress(address: String) = generalAction(cc.cluster(address).map(bitcoinFlowToJson(_)))

  def cluster(cluster: Int) = generalAction(bitcoinFlowToJson(cc.cluster(cluster)))

  def addresses(entity: Int, limit: Int) =
    generalAction(cc.addresses(entity, limit).map(bitcoinFlowToJson(_)))

  def addressEgoNet(
      address: String,
      direction: String,
      limit: Int) = generalAction {
    val egoNet = new AddressEgoNet(
      cc.addressIncomingRelations(address, limit),
      cc.addressOutgoingRelations(address, limit),
      )
    egoNet.construct(address, direction)
  }

  def clusterEgoNet(
      cluster: String,
      direction: String,
      limit: Int) = generalAction {
    val egoNet = new ClusterEgoNet(
      cc.clusterIncomingRelations(cluster, limit),
      cc.clusterOutgoingRelations(cluster, limit),
      )
    egoNet.construct(cluster, direction)
  }

  def search(expression: String, limit: Int) = generalAction {
    def whenPatternMatches(pattern: String, f: (String) => Iterable[String]) = {
      for {
        term <- pattern.r.findFirstIn(expression).toList
        result <- f(term take 5)
        if result.startsWith(expression)
      } yield result
    }.take(limit)
    Json.obj(
      "addresses" -> whenPatternMatches("^[13][1-9A-HJ-NP-Za-km-z]*$", cc.addressSearch),
      "transactions" -> whenPatternMatches("^[0-9a-f]+$", cc.transactionSearch))
  }

  def bitcoinFlowToJson[T <: BitcoinFlow](bitcoinFlow: T)(implicit writes: Writes[T]): JsObject =
    Json.toJson(bitcoinFlow).as[JsObject] ++
      Json.obj("balance" -> bitcoinFlow.balance(cc.exchangeRates.last._2))

  def generalAction[T](responseObject: T)(implicit writes: Writes[T]) = Action {
    Ok(Json.toJson(responseObject))
  }

}
