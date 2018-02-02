package controllers

import javax.inject.{Inject, Singleton}
import play.api.libs.json.{JsObject, Json, Writes}
import play.api.mvc.{AbstractController, ControllerComponents}

import models._
import services.CassandraCluster

@Singleton
class BlockController @Inject()(comp: ControllerComponents, cc: CassandraCluster)
    extends AbstractController(comp) {

  implicit val hexStringWrites = new Writes[HexString] {
    def writes(hexString: HexString) = Json.toJson(hexString.hex)
  }
  implicit val txIdTimeWrites = Json.writes[TxIdTime]  
  implicit val valueWrites = Json.writes[Bitcoin]  
  implicit val volatileValueWrites = Json.writes[VolatileValue]
  implicit val txSummaryWrites = Json.writes[TxSummary]
  implicit val txInputOutputWrites = Json.writes[TxInputOutput]
  implicit val addressSummaryWrites = Json.writes[AddressSummary]
  implicit val blockWrites = Json.writes[Block]
  implicit val transactionWrites = Json.writes[Transaction]
  implicit val richTransactionWrites = Json.writes[BlockTransactions]
  implicit val addressTransactionsWrites = Json.writes[AddressTransactions]
  implicit val addressWrites = Json.writes[Address]
  implicit val addressTagWrites = Json.writes[AddressTag]
  implicit val clusterWrites = Json.writes[Cluster]
  implicit val addressIncomingRelationsWrites = Json.writes[AddressIncomingRelations]
  implicit val addressOutgoingRelationsWrites = Json.writes[AddressOutgoingRelations]
  implicit val clusterAddressesWrites = Json.writes[ClusterAddresses]
  implicit val clusterTagsWrites = Json.writes[ClusterTag]
 
  
  /** generic response action used by all controller methods **/
  def generalAction[T](responseObject: T)(implicit writes: Writes[T]) = Action {
    Ok(Json.toJson(responseObject))
  }

  /** method for serializing Bitcoin flow traits (balance) to Json **/
  def bitcoinFlowToJson[T <: BitcoinFlow](bitcoinFlow: T)(implicit writes: Writes[T]): JsObject =
    Json.toJson(bitcoinFlow).as[JsObject] ++
      Json.obj("balance" -> bitcoinFlow.balance(cc.exchangeRates.last._2))
  
  /*
    REST INTERFACE CONTROLLER METHODS (mapped in routes file)
	*/
      
  /** / **/
  def index = Action(Ok("This is the GraphSense REST API."))      

  /** /search **/
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
      
  /** /block/:height **/
  def block(height: Int) = generalAction(cc.block(height))

  /** /block/:height/transactions **/
  def blockTransactions(height: Int) = generalAction(cc.blockTransactions(height))
  
  /** /tx/:hash **/
  def transaction(hash: String) = generalAction(cc.transaction(hash))
  
  /** /address/:address **/
  def address(address: String) = generalAction(cc.address(address).map(bitcoinFlowToJson(_)))
  
  /** /address/:address/transactions **/
  def addressTransactions(address: String, limit: Int) =
    generalAction(cc.addressTransactions(address, limit))
  
  /** /address/:address/tags **/
  def addressTags(address: String) = generalAction(cc.addressTags(address))
  
  /** /address/:address/implicitTags **/
  def addressImplicitTags(address: String) = generalAction(cc.addressImplicitTags(address))
  
  /** /address/:address/cluster **/
  def addressCluster(address: String) = generalAction(cc.addressCluster(address).map(bitcoinFlowToJson(_)))
  
  /** /address/:address/egonet **/
  def addressEgoNet(
      address: String,
      direction: String,
      limit: Int) = generalAction {
    val egoNet = new AddressEgoNet(
      cc.address(address),
      cc.addressTags(address),
      cc.addressImplicitTags(address), // TODO: refactor handling of implicit and explicit tags
      cc.addressIncomingRelations(address, limit).toList,
      cc.addressOutgoingRelations(address, limit).toList,
      )
    egoNet.construct(address, direction)
  }
  
  /** /cluster/:id **/
  def cluster(cluster: Int) = generalAction(bitcoinFlowToJson(cc.cluster(cluster)))
  
  /** /cluster/:id/addresses **/
  def clusterAddresses(cluster: Int, limit: Int) =
    generalAction(cc.clusterAddresses(cluster, limit).map(bitcoinFlowToJson(_)))
  
  /** /cluster/:id/tags **/
  def clusterTags(cluster: Int) = generalAction(cc.clusterTags(cluster))

  /** /cluster/:id/egonet **/
  def clusterEgoNet(
      cluster: Int,
      direction: String,
      limit: Int) = generalAction {
    val egoNet = new ClusterEgoNet(
      cc.cluster(cluster),
      cc.clusterTags(cluster),
      cc.clusterIncomingRelations(cluster, limit).toList,
      cc.clusterOutgoingRelations(cluster, limit).toList,
      )
    egoNet.construct(cluster, direction)
  }
}
