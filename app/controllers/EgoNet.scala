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