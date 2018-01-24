package services

import com.datastax.driver.core.{GettableData, UDTValue}
import scala.collection.JavaConverters._
import scala.language.implicitConversions

object Parser {

  private type Q[A] = (Context, Int) => A
  
  case class Context(parent: GettableData, entry: GettableData)

  implicit def contextToGettableData(c: Context) = c.entry
  implicit def gettableDataToContext(r: GettableData) = Context(r, r)
  implicit val getBool: Q[Boolean] = _ getBool _
  implicit val getInt: Q[Int] = _ getInt _
  implicit val getLong: Q[Long] = _ getLong _
  implicit val getDouble: Q[Double] = _ getDouble _
  implicit val getString: Q[String] = _ getString _
  implicit def getSeq[A](implicit converter: Context => A): Q[Seq[A]] = (c, i) =>
    c.getList(i, classOf[UDTValue]).asScala.map(Context(c.entry, _)) map converter
  implicit def getOption[A](implicit getter: (Context, Int) => A): Q[Option[A]] = (c, i) =>
    if (c isNull i) None else Some(getter(c, i))

  def parse[A, Z]
      (con: Context, fun: A => Z, pos: Int)
      (implicit a: Q[A]): Z =
    fun(a(con, pos))
  def parse[A, B, Z]
      (con: Context, fun: A => B => Z, pos: Int)
      (implicit a: Q[A], b: Q[B]): Z =
    parse(con, fun(a(con, pos)), pos+1)
  def parse[A, B, C, Z]
      (con: Context, fun: A => B => C => Z, pos: Int)
      (implicit a: Q[A], b: Q[B], c: Q[C]): Z =
    parse(con, fun(a(con, pos)), pos+1)
  def parse[A, B, C, D, Z]
      (con: Context, fun: A => B => C => D => Z, pos: Int)
      (implicit a: Q[A], b: Q[B], c: Q[C], d: Q[D]): Z =
    parse(con, fun(a(con, pos)), pos+1)
  def parse[A, B, C, D, E, Z]
      (con: Context, fun: A => B => C => D => E => Z, pos: Int)
      (implicit a: Q[A], b: Q[B], c: Q[C], d: Q[D], e: Q[E]): Z =
    parse(con, fun(a(con, pos)), pos+1)
  def parse[A, B, C, D, E, F, Z]
      (con: Context, fun: A => B => C => D => E => F => Z, pos: Int)
      (implicit a: Q[A], b: Q[B], c: Q[C], d: Q[D], e: Q[E], f: Q[F]): Z =
    parse(con, fun(a(con, pos)), pos+1)
  def parse[A, B, C, D, E, F, G, Z]
      (con: Context, fun: A => B => C => D => E => F => G => Z, pos: Int)
      (implicit a: Q[A], b: Q[B], c: Q[C], d: Q[D], e: Q[E], f: Q[F], g: Q[G]): Z =
    parse(con, fun(a(con, pos)), pos+1)
  def parse[A, B, C, D, E, F, G, H, Z]
      (con: Context, fun: A => B => C => D => E => F => G => H => Z, pos: Int)
      (implicit a: Q[A], b: Q[B], c: Q[C], d: Q[D], e: Q[E], f: Q[F], g: Q[G], h: Q[H]): Z =
    parse(con, fun(a(con, pos)), pos+1)
}
