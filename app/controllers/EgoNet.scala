package controllers

import play.api.libs.json.{Json}

import models._

class AddressEgoNet(
    focusAddress: Option[Address],
    explicitTags: Iterable[RawTag],
    implicitTags: Iterable[RawTag],
    incomingRelations: List[AddressIncomingRelations],
    outgoingRelations: List[AddressOutgoingRelations]) {

  val focusNodeCategory = if (explicitTags.nonEmpty) {
    Category.Explicit
  } else if (implicitTags.nonEmpty) {
    Category.Implicit
  } else {
    Category.Unknown
  }
  
  def focusNode = List(Json.obj(
    "id" -> focusAddress.get.address,
    "type" -> "address",
    "received" -> focusAddress.get.totalReceived.satoshi,
    "balance" -> (focusAddress.get.totalReceived.satoshi - focusAddress.get.totalSpent.satoshi),
    "category" -> focusNodeCategory))
  
  def addressNodes(addrRelations: List[AddressRelation]) = {
    val dedupNodes = {
      for (a <- addrRelations) yield (a.id, a)
    }.toMap
    dedupNodes.values
  }

  def construct(
      address: String,
      direction: String) = {
    
    val nodes = direction match {
      case "in" => focusNode ++ addressNodes(incomingRelations).map(_.toJsonNode())
      case "out" => focusNode ++ addressNodes(outgoingRelations).map(_.toJsonNode())
      case _ => focusNode ++ addressNodes(incomingRelations ++ outgoingRelations).map(_.toJsonNode())
    }
    
    val edges = direction match {
      case "in" => incomingRelations.map(_.toJsonEdge)
      case "out" => outgoingRelations.map(_.toJsonEdge)
      case _ => incomingRelations.map(_.toJsonEdge) ++ outgoingRelations.map(_.toJsonEdge)
    }
            
    Json.obj("focusNode" -> address, "nodes" -> nodes, "edges" -> edges)
  }

}

class ClusterEgoNet(
    incomingRelations: Iterable[ClusterIncomingRelations],
    outgoingRelations: Iterable[ClusterOutgoingRelations]) {
  
  implicit val valueWrites = Json.writes[models.Bitcoin]
  implicit val clusterSummaryWrites = Json.writes[ClusterSummary]

  def isNumeric(input: String): Boolean = input.forall(_.isDigit)
  
  def incomingClusterNodes = {
    for (a <- incomingRelations)
      yield Json.obj(
        "id" -> a.srcCluster,
        "type" -> (if (isNumeric(a.srcCluster)) "cluster" else "address"),
        "received" -> a.srcProperties.totalReceived,
        "balance" -> (a.srcProperties.totalReceived - a.srcProperties.totalSpent),
        "noAddresses" -> a.srcProperties.noAddresses,
        "category" -> Category(a.srcCategory))            
  }

  def outgoingClusterNodes = {
    for (a <- outgoingRelations)
      yield Json.obj(
        "id" -> a.dstCluster,
        "type" -> (if (isNumeric(a.dstCluster)) "cluster" else "address"),
        "received" -> a.dstProperties.totalReceived,
        "balance" -> (a.dstProperties.totalReceived - a.dstProperties.totalSpent),
        "noAddresses" -> a.dstProperties.noAddresses,
        "category" -> Category(a.dstCategory))            
  }
    
  def incomingRelationEdges = {
    for(rel <- incomingRelations)
      yield Json.obj(
          "source" -> rel.srcCluster,
          "target" -> rel.dstCluster,
          "transactions" -> rel.noTransactions,
          "value" -> rel.value)
  }
  
  def outgoingRelationEdges = {
    for(rel <- outgoingRelations)
      yield Json.obj(
          "source" -> rel.srcCluster,
          "target" -> rel.dstCluster,
          "transactions" -> rel.noTransactions,
          "value" -> rel.value)
  }

  
  def construct(
      cluster: String,
      direction: String) = {

    val focusNode = List(Json.obj(
      "id" -> cluster,
      "type" -> "cluster"))
    
    val nodes = direction match {
      case "in" => focusNode ++ incomingClusterNodes
      case "out" => focusNode ++ outgoingClusterNodes
      case _ => focusNode ++ incomingClusterNodes ++ outgoingClusterNodes
    }
    
    val edges = direction match {
      case "in" => incomingRelationEdges
      case "out" => outgoingRelationEdges
      case _ => incomingRelationEdges ++ outgoingRelationEdges
    }
            
    Json.obj("focusNode" -> cluster, "nodes" -> nodes, "edges" -> edges)
  }

}