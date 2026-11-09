// Exemplos do seminário de Scala (Scala 3). Todos compilam e rodam.
// Compilar:  scalac -d out exemplos.scala
// Rodar:     scala -cp out seminario
import scala.concurrent.{Future, Await}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.*

// ---- Slide: opaque types + extension methods ----
object Ids:
  opaque type ClienteId = Long
  opaque type PedidoId  = Long
  def ClienteId(n: Long): ClienteId = n
  def PedidoId(n: Long): PedidoId = n
  extension (id: PedidoId) def proximo: PedidoId = id + 1

import Ids.*
def cancelar(id: PedidoId): String = s"pedido $id cancelado"
// cancelar(ClienteId(42))   // descomente: Found: ClienteId, Required: PedidoId

// ---- Slide: sealed + pattern matching ----
sealed trait Forma
case class Circulo(r: Double) extends Forma
case class Quadrado(l: Double) extends Forma
// case class Triangulo(b: Double, h: Double) extends Forma   // descomente: aviso de match não exaustivo

def area(f: Forma): Double = f match
  case Circulo(r)  => math.Pi * r * r
  case Quadrado(l) => l * l

// ---- Slide: Either ----
def div(a: Int, b: Int): Either[String, Int] =
  if b == 0 then Left("divisão por 0")
  else Right(a / b)

// ---- Slide: given / using ----
trait Codec[T]:
  def codificar(t: T): String

case class Pedido(id: Long, total: Double)

given Codec[Pedido] with
  def codificar(p: Pedido) = s"""{"id":${p.id},"total":${p.total}}"""

def enviar[T](msg: T)(using c: Codec[T]): String =
  "enviando " + c.codificar(msg)
// enviar(3.14)   // descomente: No given instance of type Codec[Double]

// ---- Slide: by-name ----
def comRetry[T](tentativas: Int)(bloco: => T): T =
  try bloco
  catch case e: Exception if tentativas > 1 =>
    println(s"falhou (${e.getMessage}), tentando de novo")
    comRetry(tentativas - 1)(bloco)

// ---- Slide: Catalyst (versão mínima) ----
sealed trait Expr
case class Literal(v: Int) extends Expr
case class Attribute(nome: String) extends Expr
case class Add(l: Expr, r: Expr) extends Expr

extension (e: Expr)
  def transform(regra: PartialFunction[Expr, Expr]): Expr =
    val filhos = e match
      case Add(l, r) => Add(l.transform(regra), r.transform(regra))
      case folha     => folha
    regra.applyOrElse(filhos, identity)

@main def seminario(): Unit =
  println("== opaque types")
  val pedido = PedidoId(7)
  println(cancelar(pedido))
  println(cancelar(pedido.proximo))

  println("== sealed")
  println(area(Circulo(1)))
  println(area(Quadrado(3)))

  println("== Either")
  println(div(10, 2))
  val r = for
    p <- div(100, 5)
    q <- div(p, 0)
  yield q
  println(r)
  println(Map("ana" -> 21).get("bob").getOrElse(0))   // Option

  println("== given / using")
  println(enviar(Pedido(1, 99.9)))

  println("== by-name")
  var chamadas = 0
  val resposta = comRetry(3) {
    chamadas += 1
    if chamadas < 3 then throw Exception("timeout")
    "resposta do servidor"
  }
  println(s"$resposta (em $chamadas chamadas)")

  println("== Futures")
  val t0 = System.nanoTime
  val f1 = Future { Thread.sleep(200); 21 }
  val f2 = Future { Thread.sleep(200); 2 }
  val total = for a <- f1; b <- f2 yield a * b
  println(Await.result(total, 2.seconds))
  println(f"tempo: ${(System.nanoTime - t0) / 1e9}%.2f s")

  println("== Catalyst")
  val tree = Add(Attribute("x"), Add(Literal(1), Literal(2)))
  println(tree.transform {
    case Add(Literal(a), Literal(b)) => Literal(a + b)
    case Add(left, Literal(0))       => left
    case Add(Literal(0), right)      => right
  })
