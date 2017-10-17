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
  implicit val entityWrites = Json.writes[Entity]
  implicit val clusterAddressesWrites = Json.writes[ClusterAddresses]

  def block(height: Int) = generalAction(cc.block(height))
  def transactions(height: Int) = generalAction(cc.transactions(height))
  def transaction(hash: String) = generalAction(cc.transaction(hash))
  def address(address: String) = generalAction(cc.address(address).map(bitcoinFlowToJson(_)))
  def tags(address: String) = generalAction(cc.tags(address))
  def implicitTags(address: String) = generalAction(cc.implicitTags(address))
  def clusterTags(entity: Long) = generalAction(cc.clusterTags(entity))
  def addressTransactions(address: String, limit: Int) =
    generalAction(cc.addressTransactions(address, limit))
  def inRelations(address: String, category: String, limit: Int) =
    generalAction(cc.addressIncomingRelations(address, Category.fromString(category), limit))
  def outRelations(address: String, category: String, limit: Int) =
    generalAction(cc.addressOutgoingRelations(address, Category.fromString(category), limit))
  def entityByAddress(address: String) = generalAction(cc.entity(address).map(bitcoinFlowToJson(_)))
  def entity(entity: Long) = generalAction(bitcoinFlowToJson(cc.entity(entity)))
  def addresses(entity: Long, limit: Int) =
    generalAction(cc.addresses(entity, limit).map(bitcoinFlowToJson(_)))
  def egoNet(
      address: String,
      direction: String,
      minAvgValue: Long,
      limit: Int) = generalAction {
    import models.Category._
    val egoNet = new EgoNet[String](
      cc.addressIncomingRelations,
      cc.addressOutgoingRelations,
      "address",
      List(Explicit, Implicit, Unknown))
    egoNet.egoNet(address, direction, limit)
  }
  def clusterEgoNet(
      entity: Long,
      direction: String,
      minAvgValue: Long,
      limit: Int) = generalAction {
    import models.Category._
    val egoNet = new EgoNet[Long](
      cc.clusterIncomingRelations,
      cc.clusterOutgoingRelations,
      "cluster",
      List(Explicit, Implicit, Unknown))
    egoNet.egoNet(entity, direction, limit)
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
