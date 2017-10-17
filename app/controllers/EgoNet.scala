package controllers

import play.api.libs.json.{JsObject, Json}

import models._
import models.AddressOutputType._
import models.Category._

class EgoNet[A](
    incomingObjects: (A, Option[Category], Int) => Iterable[RelatedThing[A]],
    outgoingObjects: (A, Option[Category], Int) => Iterable[RelatedThing[A]],
    typeName: String,
    categories: List[Category]) {

  implicit val valueWrites = Json.writes[models.Bitcoin]
  implicit val addressSummaryWrites = Json.writes[AddressSummary]

  def egoNet(
      address: A,
      direction: String,
      limit: Int) = {
    val dir =
      direction match {
        case "in" => Incoming
        case "out" => Outgoing
        case _ => Both
      }
    val (nodes, edges) = egoNetPart(dir, address, limit)
    Json.obj("focusNode" -> address.toString(), "nodes" -> nodes, "edges" -> edges)
  }

  private def egoNetPart(
      addressOutputType: AddressOutputType,
      address: A,
      limit: Int): (Iterable[JsObject], List[JsObject]) = {
    def relAddr(t: AddressOutputType) =
      if (addressOutputType == t || addressOutputType == Both)
        relAddresses(t, address, limit)
      else List.empty
    val relatedAddressesIn = relAddr(Incoming)
    val relatedAddressesOut = relAddr(Outgoing)
    val relatedAddresses = {
      for (relatedAddress <- (relatedAddressesIn ++ relatedAddressesOut).view)
      yield (relatedAddress.address, relatedAddress)
    }.toMap
    val nodes = List(Json.obj(
        "id" -> address.toString(),
        "type" -> typeName)) ++ {
      for (a <- relatedAddresses)
      yield Json.obj(
        "id" -> a._1.toString(),
        "type" -> typeName,
        "received" -> a._2.properties.totalReceived,
        "balance" -> (a._2.properties.totalReceived - a._2.properties.totalSpent),
        "category" -> Category(a._2.category))
    }
    def edges(relatedAddresses: List[RelatedThing[A]], addressOutputType: AddressOutputType) =
      for (relatedAddress <- relatedAddresses)
      yield {
        val addrs = (relatedAddress.address, address)
        val (source, target) = if (addressOutputType == Incoming) addrs else addrs.swap
        Json.obj(
          "source" -> source.toString(),
          "target" -> target.toString(),
          "transactions" -> relatedAddress.noTransactions,
          "estimatedValue" -> relatedAddress.estimatedValue)
      }
    (nodes, edges(relatedAddressesIn, Incoming) ++ edges(relatedAddressesOut, Outgoing))
  }

  private def relAddresses(
      addressOutputType: AddressOutputType,
      address: A,
      limit: Int): List[RelatedThing[A]] = {
    val numberOfSpecialNodes = math.min(5, limit / 2)
    val relAddrFunction =
      if (addressOutputType == Incoming) incomingObjects
      else outgoingObjects
    val relsPerCategory = {
      for (category <- categories)
      yield category -> relAddrFunction(address, Some(category), limit).toList
    }.toMap
    val (reservedKnownNodes, otherKnownNodes) =
      if (categories.contains(Explicit)) relsPerCategory(Explicit).splitAt(numberOfSpecialNodes)
      else (List.empty, List.empty)
    val (reservedIKnownNodes, otherIKnownNodes) =
      relsPerCategory(Implicit).splitAt(numberOfSpecialNodes)
    val specialNodes = reservedKnownNodes ++ reservedIKnownNodes
    val allOtherNodes = relsPerCategory(Unknown) ++ otherKnownNodes ++ otherIKnownNodes
    specialNodes ++ allOtherNodes.sortBy(-_.estimatedValue.satoshi).take(limit - specialNodes.size)
  }
}
