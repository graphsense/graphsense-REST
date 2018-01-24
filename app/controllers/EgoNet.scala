package controllers

import play.api.libs.json.{Json}

import models._

class AddressEgoNet(
    incomingRelations: Iterable[AddressIncomingRelations],
    outgoingRelations: Iterable[AddressOutgoingRelations]) {

  val NodeType = "address"
  
  implicit val estimatedValueWrites = Json.writes[models.Bitcoin]
  implicit val addressSummaryWrites = Json.writes[AddressSummary]

  def incomingAddressNodes = {
    for (a <- incomingRelations)
      yield Json.obj(
        "id" -> a.srcAddress,
        "type" -> NodeType,
        "received" -> a.srcProperties.totalReceived,
        "balance" -> (a.srcProperties.totalReceived - a.srcProperties.totalSpent),
        "category" -> Category(a.srcCategory))            
  }

  def outgoingAddressNodes = {
    for (a <- outgoingRelations)
      yield Json.obj(
        "id" -> a.dstAddress,
        "type" -> NodeType,
        "received" -> a.dstProperties.totalReceived,
        "balance" -> (a.dstProperties.totalReceived - a.dstProperties.totalSpent),
        "category" -> Category(a.dstCategory))            
  }
    
  def incomingRelationEdges = {
    for(rel <- incomingRelations)
      yield Json.obj(
          "source" -> rel.srcAddress,
          "target" -> rel.dstAddress,
          "transactions" -> rel.noTransactions,
          "estimatedValue" -> rel.estimatedValue)
  }
  
  def outgoingRelationEdges = {
    for(rel <- outgoingRelations)
      yield Json.obj(
          "source" -> rel.srcAddress,
          "target" -> rel.dstAddress,
          "transactions" -> rel.noTransactions,
          "estimatedValue" -> rel.estimatedValue)
  }

  
  def construct(
      address: String,
      direction: String) = {

    val focusNode = List(Json.obj(
      "id" -> address.toString(),
      "type" -> NodeType))
    
    val nodes = direction match {
      case "in" => focusNode ++ incomingAddressNodes
      case "out" => focusNode ++ outgoingAddressNodes
      case _ => focusNode ++ incomingAddressNodes ++ outgoingAddressNodes
    }
    
    val edges = direction match {
      case "in" => incomingRelationEdges
      case "out" => outgoingRelationEdges
      case _ => incomingRelationEdges ++ outgoingRelationEdges
    }
            
    Json.obj("focusNode" -> address, "nodes" -> nodes, "edges" -> edges)
  }

}

//class ClusterEgoNet(
//    incomingObjects: (String, Option[Category], Int) => Iterable[RelatedThing[String]],
//    outgoingObjects: (String, Option[Category], Int) => Iterable[RelatedThing[String]],
//    typeName: String,
//    categories: List[Category]) {
//
//  implicit val valueWrites = Json.writes[models.Bitcoin]
//  implicit val clusterSummaryWrites = Json.writes[ClusterSummary]
//
//  def egoNet(
//      cluster: String,
//      direction: String,
//      limit: Int) = {
//    val dir =
//      direction match {
//        case "in" => Incoming
//        case "out" => Outgoing
//        case _ => Both
//      }
//    val (nodes, edges) = egoNetPart(dir, cluster, limit)
//    Json.obj("focusNode" -> cluster, "nodes" -> nodes, "edges" -> edges)
//  }
//
//  private def egoNetPart(
//      clusterOutputType: DirectionType,
//      cluster: String,
//      limit: Int): (Iterable[JsObject], List[JsObject]) = {
//
//    def relAddr(t: DirectionType) =
//      if (clusterOutputType == t || clusterOutputType == Both)
//        relClusters(t, cluster, limit)
//      else List.empty
//
//    val relatedAddressesIn = relAddr(Incoming)
//    val relatedAddressesOut = relAddr(Outgoing)
//    
//    val relatedAddresses = {
//      for (relatedAddress <- (relatedAddressesIn ++ relatedAddressesOut).view)
//      yield (relatedAddress.address, relatedAddress)
//    }.toMap
//    
//    val nodes = List(Json.obj(
//        "id" -> cluster,
//        "type" -> typeName)) ++ {
//      for (a <- relatedAddresses)
//      yield Json.obj(
//        "id" -> a._1.toString(),
//        "type" -> typeName,
//        "received" -> a._2.properties.totalReceived,
//        "balance" -> (a._2.properties.totalReceived - a._2.properties.totalSpent),
//        "category" -> Category(a._2.category))
//    }
//    
//    def edges(relatedClusters: List[RelatedThing[String]], clusterOutputType: DirectionType) =
//      for (relatedCluster <- relatedClusters)
//      yield {
//        val clusters = (relatedCluster.address, cluster)
//        val (source, target) = if (clusterOutputType == Incoming) clusters else clusters.swap
//        Json.obj(
//          "source" -> source.toString(),
//          "target" -> target.toString(),
//          "transactions" -> relatedCluster.noTransactions,
//          "value" -> relatedCluster.value)
//      }
//    (nodes, edges(relatedAddressesIn, Incoming) ++ edges(relatedAddressesOut, Outgoing))
//  }
//
//  private def relClusters(
//      clusterOutputType: DirectionType,
//      cluster: String,
//      limit: Int): List[RelatedThing[String]] = {
//
//    val numberOfSpecialNodes = math.min(5, limit / 2)
//    
//    val relClusterFunction =
//      if (clusterOutputType == Incoming) incomingObjects
//      else outgoingObjects
//    val relsPerCategory = {
//      for (category <- categories)
//      yield category -> relClusterFunction(cluster, Some(category), limit).toList
//    }.toMap
//    
//    val (reservedKnownNodes, otherKnownNodes) =
//      if (categories.contains(Explicit)) relsPerCategory(Explicit).splitAt(numberOfSpecialNodes)
//      else (List.empty, List.empty)
//    
//    val (reservedIKnownNodes, otherIKnownNodes) =
//      relsPerCategory(Implicit).splitAt(numberOfSpecialNodes)
//    
//    val specialNodes = reservedKnownNodes ++ reservedIKnownNodes
//    
//    val allOtherNodes = relsPerCategory(Unknown) ++ otherKnownNodes ++ otherIKnownNodes
//    
//    specialNodes ++ allOtherNodes.sortBy(-_.value.satoshi).take(limit - specialNodes.size)
//  }
//}
//
//
