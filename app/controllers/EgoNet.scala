package controllers

import play.api.libs.json.{Json}

import models._

class AddressEgoNet(
    focusAddress: Option[Address],
    explicitTags: Iterable[AddressTag],
    implicitTags: Iterable[ClusterTag],
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
    focusCluster: Cluster,
    clusterTags: Iterable[ClusterTag],
    incomingRelations: List[ClusterIncomingRelations],
    outgoingRelations: List[ClusterOutgoingRelations]) {

  val focusNodeCategory = if (clusterTags.nonEmpty) {
    Category.Implicit
  } else {
    Category.Unknown
  }
  
  def focusNode = List(Json.obj(
    "id" -> focusCluster.cluster,
    "type" -> "cluster",
    "received" -> focusCluster.totalReceived.satoshi,
    "balance" -> (focusCluster.totalReceived.satoshi - focusCluster.totalSpent.satoshi),
    "category" -> focusNodeCategory))
  
  def clusterNodes(clusterRelations: List[ClusterRelation]) = {
    val dedupNodes = {
      for (rel <- clusterRelations) yield (rel.id, rel)
    }.toMap
    dedupNodes.values
  }

  def construct(
      cluster: Int,
      direction: String) = {
    
    val nodes = direction match {
      case "in" => focusNode ++ clusterNodes(incomingRelations).map(_.toJsonNode())
      case "out" => focusNode ++ clusterNodes(outgoingRelations).map(_.toJsonNode())
      case _ => focusNode ++ clusterNodes(incomingRelations ++ outgoingRelations).map(_.toJsonNode())
    }
    
    val edges = direction match {
      case "in" => incomingRelations.map(_.toJsonEdge)
      case "out" => outgoingRelations.map(_.toJsonEdge)
      case _ => incomingRelations.map(_.toJsonEdge) ++ outgoingRelations.map(_.toJsonEdge)
    }
            
    Json.obj("focusNode" -> cluster, "nodes" -> nodes, "edges" -> edges)
  }

}
