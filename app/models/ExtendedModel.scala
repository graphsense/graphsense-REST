package models

object Category extends Enumeration {
  type Category = Value
  val Unknown, Implicit, Explicit, Manual  = Value

  def fromString(value: String) =
    Category.values.find(_.toString.toLowerCase == value.toLowerCase)

  def code(category: Category) =
    category match {
      case Unknown => 0
      case Implicit => 1
      case Explicit => 2
      case Manual => 3
    }
}

object AddressOutputType extends Enumeration {
  type AddressOutputType = Value
  val Incoming, Outgoing, Both = Value
}
