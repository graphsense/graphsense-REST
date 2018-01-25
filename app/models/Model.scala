package models

import play.api.libs.json.{Json, JsObject}

case class HexString(hex: String)

trait BitcoinFlow {
  val totalReceived: Bitcoin
  val totalSpent: Bitcoin
  def balance(rate: ExchangeRates): Bitcoin = {
    val satoshi = totalReceived.satoshi - totalSpent.satoshi
    val bitcoin = satoshi / 1e8
    Bitcoin(satoshi, bitcoin * rate.eur, bitcoin * rate.usd)
  }
}

case class TxSummary(
    txHash: HexString,
    noInputs: Int,
    noOutputs: Int,
    totalInput: VolatileValue,
    totalOutput: VolatileValue)

case class TxInputOutput(
    address: Option[String],
    value: Option[VolatileValue])

case class TxIdTime(
    height: Int,
    txHash: HexString,
    timestamp: Int)

case class VolatileValue(
    satoshi: Long,
    eur: Double,
    usd: Double)

case class Bitcoin(
    satoshi: Long,
    eur: Double,
    usd: Double) {
  
    def toJson = {
      Json.obj(
          "satoshi" -> satoshi,
          "eur" -> eur,
          "usd" -> usd)
    }
}

case class AddressSummary(
    totalReceived: Long,
    totalSpent: Long)

case class ClusterSummary(
    noAddresses: Int,
    totalReceived: Long,
    totalSpent: Long)

case class RawTag(
    address: String,
    tag: String,
    tagUri: String,
    description: String,
    actorCategory: String,
    source: String,
    sourceUri: String,
    timestamp: Int)

case class ExchangeRates(
    height: Int,
    eur: Double,
    usd: Double)

case class Block(
    height: Int,
    blockHash: HexString,
    timestamp: Int,
    noTransactions: Int)

case class BlockTransactions(
    height: Int,
    txs: Seq[TxSummary])

case class TransactionHash(txHash: HexString)

case class Transaction(
    txHash: HexString,
    height: Int,
    timestamp: Int,
    coinbase: Boolean,
    totalInput: VolatileValue,
    totalOutput: VolatileValue,
    inputs: Seq[TxInputOutput],
    outputs: Seq[TxInputOutput])

case class Address(
    address: String,
    noIncomingTxs: Int,
    noOutgoingTxs: Int,
    firstTx: TxIdTime,
    lastTx: TxIdTime,
    totalReceived: Bitcoin,
    totalSpent: Bitcoin) extends BitcoinFlow

case class AddressTransactions(
    address: String,
    txHash: HexString,
    value: Option[VolatileValue],
    height: Int,
    timestamp: Int)

trait AddressRelation{
    def id(): String
    def toJsonNode(): JsObject
}

case class AddressIncomingRelations(
    dstAddress: String,
    srcAddress: String,
    srcCategory: Int,
    srcProperties: AddressSummary,
    noTransactions: Int,
    estimatedValue: Bitcoin) extends AddressRelation {
  
    override def id(): String = { srcAddress }
  
    override def toJsonNode: JsObject = {
      Json.obj(
        "id" -> id(),
        "type" -> "address",
        "received" -> srcProperties.totalReceived,
        "balance" -> (srcProperties.totalReceived - srcProperties.totalSpent),
        "category" -> Category(srcCategory))            
    }
  
    def toJsonEdge = {
      Json.obj(
          "source" -> srcAddress,
          "target" -> dstAddress,
          "transactions" -> noTransactions,
          "estimatedValue" -> estimatedValue.toJson)
    }
  
}

case class AddressOutgoingRelations(
    srcAddress: String,
    dstAddress: String,
    dstCategory: Int,
    dstProperties: AddressSummary,
    noTransactions: Int,
    estimatedValue: Bitcoin) extends AddressRelation {
  
    override def id(): String = { dstAddress }

    override def toJsonNode: JsObject = {
      Json.obj(
        "id" -> id(),
        "type" -> "address",
        "received" -> dstProperties.totalReceived,
        "balance" -> (dstProperties.totalReceived - dstProperties.totalSpent),
        "category" -> Category(dstCategory))            
    }
    
    def toJsonEdge = {
      Json.obj(
          "source" -> srcAddress,
          "target" -> dstAddress,
          "transactions" -> noTransactions,
          "estimatedValue" -> estimatedValue.toJson)
    }
  
  
}

case class Cluster(
    cluster: Int,
    noAddresses: Int,
    noIncomingTxs: Int,
    noOutgoingTxs: Int,
    firstTx: TxIdTime,
    lastTx: TxIdTime,
    totalReceived: Bitcoin,
    totalSpent: Bitcoin) extends BitcoinFlow

case class ClusterAddresses(
    cluster: Int,
    address: String,
    noIncomingTxs: Int,
    noOutgoingTxs: Int,
    firstTx: TxIdTime,
    lastTx: TxIdTime,
    totalReceived: Bitcoin,
    totalSpent: Bitcoin) extends BitcoinFlow

case class ClusterIncomingRelations(
    dstCluster: String,
    srcCluster: String,
    srcCategory: Int,
    srcProperties: ClusterSummary,
    noTransactions: Int,
    value: Bitcoin)

case class ClusterOutgoingRelations(
    srcCluster: String,
    dstCluster: String,
    dstCategory: Int,
    dstProperties: ClusterSummary,
    noTransactions: Int,
    value: Bitcoin)

