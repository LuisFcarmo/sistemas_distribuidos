const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "Scala";
pres.author = "Pedro Henrique dos Santos, Luis Cesar, Gabriel Soares";

const BG="121417", PANEL="1A1E23", BAR="232830", FG="E8E8E8", DIM="8A939C", GUT="4A525B", ACC="E8473C",
      KW="FF7A59", STR="9FD88C", COM="6B7580", NUM="C79BFF", TYP="5CC8E0", WARN="F2C14E", ERR="FF8A80";
const SANS="Arial", MONO="Courier New";
const T = (s, text, o) => s.addText(text, Object.assign({ fontFace:SANS, fontSize:20, color:FG, margin:0, valign:"top", isTextBox:true }, o));

const KEYS = new Set("val var def case class trait sealed match extends for yield if then else new object import opaque type extension given using with try catch".split(" "));
function hl(src) {
  const runs = [], lines = src.split("\n");
  lines.forEach((line, li) => {
    const re = /(\/\/.*$)|(s?"""[^]*?"""|s?"[^"]*")|(\b\d+(?:\.\d+)?\b)|(\b[A-Za-z_]\w*\b)|(\s+)|(.)/g;
    let m, parts = [];
    while ((m = re.exec(line)) !== null) {
      let color = FG, t = m[0];
      if (m[1]) color = COM; else if (m[2]) color = STR; else if (m[3]) color = NUM;
      else if (m[4]) color = KEYS.has(t) ? KW : (/^[A-Z]/.test(t) ? TYP : FG);
      parts.push({ text:t, options:{ color } });
    }
    if (!parts.length) parts.push({ text:" ", options:{ color:FG } });
    if (li < lines.length - 1) parts[parts.length-1].options.breakLine = true;
    runs.push(...parts);
  });
  return runs;
}
// painel de editor: barra com nome do arquivo, números de linha e código realçado
function editor(s, x, y, w, h, file, src, fs) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill:{color:PANEL}, line:{color:PANEL} });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h:0.42, fill:{color:BAR}, line:{color:BAR} });
  T(s, file, { x:x+0.3, y:y+0.08, w:w-0.6, h:0.28, fontFace:MONO, fontSize:12, color:DIM, valign:"middle" });
  const n = src.split("\n").length, gw = 0.55;
  const opt = { fontFace:MONO, fontSize:fs, margin:0, valign:"top", isTextBox:true, lineSpacingMultiple:1.1 };
  s.addText(Array.from({length:n}, (_, i) => ({ text:String(i+1), options:{ color:GUT, breakLine:i<n-1 } })),
    Object.assign({ x:x+0.15, y:y+0.65, w:gw-0.1, h:h-0.8, align:"right" }, opt));
  s.addText(hl(src), Object.assign({ x:x+0.15+gw+0.2, y:y+0.65, w:w-gw-0.6, h:h-0.8 }, opt));
}
function term(s, x, y, w, h, cmd, out, color, fs) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill:{color:"0B0D0F"}, line:{color:BAR, width:1} });
  T(s, [{ text:"$ "+cmd, options:{ color:DIM, breakLine:true } }, { text:" ", options:{ breakLine:true } }, { text:out, options:{ color } }],
    { x:x+0.35, y:y+0.3, w:w-0.7, h:h-0.6, fontFace:MONO, fontSize:fs||16 });
}

const REFS = {
  "parte 1 · o que é": "Livro oficial do Scala 3: https://docs.scala-lang.org/scala3/book/introduction.html | Scala para quem vem de Python: https://docs.scala-lang.org/scala3/book/scala-for-python-devs.html",
  "parte 1 · opaque types": "Opaque types: https://docs.scala-lang.org/scala3/book/types-opaque-types.html | Extension methods: https://docs.scala-lang.org/scala3/book/ca-extension-methods.html",
  "parte 1 · pattern matching": "ADTs e sealed: https://docs.scala-lang.org/scala3/book/types-adts-gadts.html | Pattern matching: https://docs.scala-lang.org/tour/pattern-matching.html",
  "parte 2 · erros como valores": "Tratamento funcional de erros (Option, Either): https://docs.scala-lang.org/scala3/book/fp-functional-error-handling.html",
  "parte 2 · given / using": "Parâmetros de contexto: https://docs.scala-lang.org/scala3/book/ca-context-parameters.html | Type classes: https://docs.scala-lang.org/scala3/book/ca-type-classes.html",
  "parte 2 · parâmetros by-name": "By-name parameters: https://docs.scala-lang.org/tour/by-name-parameters.html",
  "parte 2 · concorrência": "Futures (guia oficial): https://docs.scala-lang.org/overviews/core/futures.html | Concorrência no livro do Scala 3: https://docs.scala-lang.org/scala3/book/concurrency.html",
  "parte 3 · atores": "Atores no Apache Pekko: https://pekko.apache.org/docs/pekko/current/typed/actors.html | Mudança de licença do Akka: https://www.lightbend.com/blog/why-we-are-changing-the-license-for-akka",
  "parte 3 · spark": "Artigo original do Spark (RDDs), seções 2 e 3: https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf | Guia de RDDs: https://spark.apache.org/docs/latest/rdd-programming-guide.html",
  "parte 3 · spark sql": "Post da Databricks sobre o Catalyst: https://www.databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html | Artigo do Spark SQL: https://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf",
  "parte 3 · kafka": "Proposta de reescrita dos clientes: https://cwiki.apache.org/confluence/display/KAFKA/Client+Rewrite | KIP-751: https://cwiki.apache.org/confluence/display/KAFKA/KIP-751%3A+Drop+support+for+Scala+2.12+in+Kafka+4.0+%28deprecate+in+3.0%29",
  "parte 3 · críticas": "Compatibilidade Scala 2 x 3: https://docs.scala-lang.org/scala3/guides/migration/compatibility-intro.html",
};
let n = 0;
function slide(label, title) {
  const s = pres.addSlide(); s.background = { color:BG }; n++;
  if (label && REFS[label]) { const orig = s.addNotes.bind(s); s.addNotes = (txt) => orig(txt + "\n\nPARA ESTUDAR: " + REFS[label].split(" | ").join("\n")); }
  if (label) T(s, label, { x:0.7, y:0.55, w:8, h:0.35, fontFace:MONO, fontSize:14, color:ACC });
  if (title) T(s, title, { x:0.7, y:0.95, w:11.9, h:0.85, fontSize:36, bold:true, valign:"middle" });
  if (n > 1) T(s, String(n).padStart(2,"0"), { x:12.0, y:6.95, w:0.6, h:0.3, fontFace:MONO, fontSize:12, color:DIM, align:"right" });
  return s;
}
function divider(num, name, who, topics, notes) {
  const s = pres.addSlide(); s.background = { color:ACC }; n++;
  T(s, num, { x:0.7, y:0.4, w:6, h:3.0, fontSize:200, bold:true, color:"F07A70" });
  T(s, name, { x:0.7, y:3.3, w:11.9, h:1.2, fontSize:60, bold:true, color:BG });
  T(s, who, { x:0.75, y:4.5, w:11.9, h:0.5, fontSize:22, color:BG });
  T(s, topics, { x:0.75, y:5.6, w:11.9, h:0.5, fontFace:MONO, fontSize:16, color:"3A0F0B" });
  s.addNotes(notes);
}

// 1 — abertura
let s = slide();
T(s, "Scala", { x:0.7, y:1.5, w:7, h:1.8, fontSize:110, bold:true });
T(s, "tipos fortes, código funcional\ne concorrência na JVM", { x:0.75, y:3.35, w:7, h:1.2, fontSize:24, color:DIM });
T(s, "Pedro Henrique dos Santos   ·   Luis Cesar   ·   Gabriel Soares", { x:0.75, y:5.7, w:8, h:0.4, fontSize:16 });
T(s, "Sistemas Distribuídos · 25.11.2026", { x:0.75, y:6.1, w:8, h:0.4, fontFace:MONO, fontSize:14, color:ACC });
editor(s, 8.2, 1.4, 4.45, 3.9, "Seminario.scala", 'case class Seminario(\n  tema: String,\n  grupo: List[String]\n)\n\nval hoje = Seminario(\n  "Scala",\n  List("Pedro", "Luis",\n       "Gabriel")\n)', 14);
s.addNotes("PEDRO. Abertura: três partes. Fundamentos (Pedro), segurança no código (Luis) e Scala na prática, com concorrência e distribuição (Gabriel). O código ao lado é Scala válido.");

// 2 — divisória 1
divider("1", "Tipos a seu favor", "Pedro Henrique dos Santos", "o que é  ·  opaque types  ·  sealed", "PEDRO apresenta a parte 1.");

// 3 — o que é
s = slide("parte 1 · o que é", null);
T(s, [{ text:"Uma linguagem da JVM que mistura " }, { text:"objetos", options:{ color:ACC } }, { text:" e " },
      { text:"funções", options:{ color:ACC } }, { text:", com tipos verificados na compilação." }],
  { x:0.7, y:1.4, w:11.5, h:2.4, fontSize:42, bold:true });
const flow = ["Codigo.scala", "scalac", "bytecode", "JVM"];
flow.forEach((f, i) => {
  const x = 0.7 + i*3.1;
  s.addShape(pres.shapes.RECTANGLE, { x, y:4.3, w:2.4, h:0.8, fill:{color: i==1?ACC:PANEL}, line:{color: i==1?ACC:BAR, width:1} });
  T(s, f, { x, y:4.3, w:2.4, h:0.8, fontFace:MONO, fontSize:18, align:"center", valign:"middle", color: i==1?BG:FG, bold: i==1 });
  if (i < 3) s.addShape(pres.shapes.LINE, { x:x+2.5, y:4.7, w:0.5, h:0, line:{ color:DIM, width:1.5, endArrowType:"triangle" } });
});
T(s, "Roda em qualquer JVM e usa bibliotecas Java diretamente. Exemplos em Scala 3.", { x:0.7, y:5.6, w:11.9, h:0.5, fontSize:18, color:DIM });
s.addNotes("PEDRO. Sem histórico. Três pontos: roda na JVM, mistura orientação a objetos com programação funcional e é tipada estaticamente.");

// N1 — opaque types
s = slide("parte 1 · opaque types", "IDs que o compilador não deixa misturar");
editor(s, 0.7, 2.05, 7.2, 4.4, "Ids.scala", 'object Ids:\n  opaque type ClienteId = Long\n  opaque type PedidoId  = Long\n  def ClienteId(n: Long): ClienteId = n\n  def PedidoId(n: Long): PedidoId = n\n  extension (id: PedidoId)\n    def proximo: PedidoId = id + 1\n\ndef cancelar(id: PedidoId) = ...\n\ncancelar(PedidoId(7))     // ok\ncancelar(ClienteId(42))   // não compila', 15);
term(s, 8.2, 2.05, 4.4, 1.9, "scalac Ids.scala", "Found:    ClienteId\nRequired: PedidoId", ERR, 16);
T(s, [{ text:"Custo zero", options:{ bold:true, color:FG, breakLine:true } },
      { text:"Em execução os dois são só Long. A diferença existe apenas para o compilador.", options:{ color:DIM, breakLine:true } },
      { text:" ", options:{ breakLine:true } },
      { text:"extension", options:{ bold:true, color:FG, fontFace:MONO, breakLine:true } },
      { text:"Acrescenta métodos a um tipo sem alterá-lo nem criar um objeto embrulhando.", options:{ color:DIM } }],
  { x:8.2, y:4.25, w:4.4, h:2.3, fontSize:16 });
s.addNotes("PEDRO. O bug clássico em sistemas distribuídos: trocar um ID por outro, porque os dois são números. Com opaque type, ClienteId e PedidoId são tipos diferentes para o compilador, mas em execução viram só Long, sem objeto extra e sem custo. Só dentro do object Ids se sabe que é Long. O erro à direita é o real do Scala 3.3 (simplificado: ele também mostra o nome do pacote). extension adiciona o método proximo ao PedidoId. Detalhe para guardar: o 2.seconds que vai aparecer no slide de Futures também é um extension method.");

// 7 — sealed
s = slide("parte 1 · pattern matching", "O compilador conhece todos os casos");
editor(s, 0.7, 2.1, 7.2, 3.9, "Formas.scala", 'sealed trait Forma\ncase class Circulo(r: Double) extends Forma\ncase class Quadrado(l: Double) extends Forma\ncase class Triangulo(b: Double, h: Double)\n  extends Forma\n\ndef area(f: Forma) = f match\n  case Circulo(r)  => math.Pi * r * r\n  case Quadrado(l) => l * l', 16);
term(s, 8.2, 2.1, 4.4, 3.9, "scalac Formas.scala", "Pattern Match\nExhaustivity Warning\n\nmatch may not be\nexhaustive.\n\nIt would fail on:\n  Triangulo(_, _)", WARN, 16);
s.addNotes("LUIS. sealed obriga todos os subtipos a ficarem no mesmo arquivo, então o compilador conhece a lista inteira. Ao criar Triangulo, todo match que não o trata gera esse aviso (saída real do scalac). Num sistema grande, ele aponta exatamente o que precisa mudar. Passar para o Luis.");

// 6 — divisória 2
divider("2", "Código que vira linguagem", "Luis Cesar", "erros como valores  ·  given / using  ·  by-name  ·  futures", "LUIS apresenta a parte 2.");

// 8 — Either
s = slide("parte 2 · erros como valores", "A falha aparece no tipo de retorno");
editor(s, 0.7, 2.1, 8.3, 3.9, "Divisao.scala", 'def div(a: Int, b: Int): Either[String, Int] =\n  if b == 0 then Left("divisão por 0")\n  else Right(a / b)\n\nval r = for\n  p <- div(100, 5)    // Right(20)\n  q <- div(p, 0)      // Left: para aqui\nyield q\n// r == Left("divisão por 0")', 16);
T(s, [{ text:"Right", options:{ color:STR, bold:true, breakLine:true } }, { text:"deu certo, segue", options:{ color:DIM, breakLine:true } }, { text:" ", options:{ breakLine:true } },
      { text:"Left", options:{ color:ERR, bold:true, breakLine:true } }, { text:"falhou, o for para", options:{ color:DIM, breakLine:true } }, { text:" ", options:{ breakLine:true } },
      { text:"Option", options:{ color:TYP, bold:true, breakLine:true } }, { text:"Some(valor) ou None, no lugar de null", options:{ color:DIM } }],
  { x:9.4, y:2.3, w:3.2, h:4.2, fontSize:19 });
s.addNotes("LUIS. Quem chama div vê pela assinatura que ela pode falhar. O for encadeia as operações e para no primeiro Left, sem um if para cada passo. Option: Map(\"ana\" -> 21).get(\"bob\") devolve None.");

// N2 — given / using
s = slide("parte 2 · given / using", "O compilador escolhe o serializador");
editor(s, 0.7, 2.05, 7.4, 4.6, "Codec.scala", 'trait Codec[T]:\n  def codificar(t: T): String\n\ncase class Pedido(id: Long, total: Double)\n\ngiven Codec[Pedido] with\n  def codificar(p: Pedido) =\n    s"""{"id":${p.id},"total":${p.total}}"""\n\ndef enviar[T](msg: T)(using c: Codec[T]) =\n  "enviando " + c.codificar(msg)\n\nenviar(Pedido(1, 99.9))\nenviar(3.14)          // não compila', 14);
term(s, 8.4, 2.05, 4.2, 2.45, "scalac Codec.scala", "No given instance of\ntype Codec[Double]\nwas found for\nparameter c", ERR, 15);
T(s, [{ text:"enviar(Pedido(1, 99.9))", options:{ fontFace:MONO, color:FG, fontSize:14, breakLine:true } },
      { text:'enviando {"id":1,"total":99.9}', options:{ fontFace:MONO, color:STR, fontSize:14, breakLine:true } },
      { text:" ", options:{ breakLine:true } },
      { text:"Esqueceu o serializador de um tipo? O erro aparece na compilação, e não quando a mensagem já está na rede.", options:{ color:DIM } }],
  { x:8.4, y:4.75, w:4.2, h:1.9, fontSize:16 });
s.addNotes("LUIS. Isso se chama type class. Codec[T] diz como transformar um T em texto para mandar pela rede. given registra a implementação para Pedido (case class é uma classe de dados imutável, com construtor, igualdade e toString prontos). using pede ao compilador que procure, pelo tipo da mensagem, o Codec certo e o passe sozinho. Para Double não existe nenhum, então o programa não compila (mensagem real do scalac). É o mesmo mecanismo que bibliotecas de JSON em Scala usam.");

// N3 — by-name
s = slide("parte 2 · parâmetros by-name", "Uma estrutura de controle em cinco linhas");
editor(s, 0.7, 2.0, 11.9, 2.4, "Retry.scala", 'def comRetry[T](tentativas: Int)(bloco: => T): T =\n  try bloco\n  catch case e: Exception if tentativas > 1 =>\n    println(s"falhou (${e.getMessage}), tentando de novo")\n    comRetry(tentativas - 1)(bloco)', 16);
T(s, [{ text:"=> T", options:{ fontFace:MONO, color:ACC, bold:true } }, { text:"  o bloco é passado sem ser executado e roda de novo a cada tentativa.", options:{ color:DIM } }],
  { x:0.7, y:4.55, w:11.9, h:0.4, fontSize:17 });
editor(s, 0.7, 5.05, 5.7, 1.75, "Cliente.scala", 'comRetry(3) {\n  chamarServidor()\n}', 16);
term(s, 6.7, 5.05, 5.9, 1.75, "scala Cliente", "falhou (timeout), tentando de novo\nfalhou (timeout), tentando de novo\nresposta do servidor", WARN, 13);
s.addNotes("LUIS. Em quase toda linguagem, o argumento é calculado antes da chamada. Com => T (by-name), o bloco só roda quando é usado, e roda de novo cada vez que aparece. Por isso comRetry(3) { ... } parece um comando da linguagem, como while, mas é uma função comum de cinco linhas. Em sistemas distribuídos, repetir uma chamada que deu timeout é rotina. A saída à direita é real: no exemplos.scala o servidor simulado falha duas vezes e responde na terceira.");

// 12 — Futures
s = slide("parte 2 · concorrência", "Futures rodam em paralelo");
editor(s, 0.7, 2.05, 11.9, 3.1, "Paralelo.scala", 'val f1 = Future { Thread.sleep(200); 21 }\nval f2 = Future { Thread.sleep(200); 2 }\n\nval total = for a <- f1; b <- f2 yield a * b\n\nAwait.result(total, 2.seconds)   // 42', 18);
T(s, "f1", { x:0.7, y:5.5, w:0.5, h:0.35, fontFace:MONO, fontSize:15, color:DIM, valign:"middle" });
s.addShape(pres.shapes.RECTANGLE, { x:1.3, y:5.56, w:4.5, h:0.24, fill:{color:ACC}, line:{color:ACC} });
T(s, "f2", { x:0.7, y:5.95, w:0.5, h:0.35, fontFace:MONO, fontSize:15, color:DIM, valign:"middle" });
s.addShape(pres.shapes.RECTANGLE, { x:1.3, y:6.01, w:4.5, h:0.24, fill:{color:ACC}, line:{color:ACC} });
T(s, "0 ms", { x:1.3, y:6.4, w:1, h:0.3, fontFace:MONO, fontSize:12, color:DIM });
T(s, "200 ms", { x:5.1, y:6.4, w:1, h:0.3, fontFace:MONO, fontSize:12, color:DIM });
T(s, [{ text:"0,22 s", options:{ fontSize:44, bold:true, color:FG, breakLine:true } }, { text:"tempo medido, e não 0,4 s: as duas tarefas rodaram juntas em threads do pool", options:{ fontSize:16, color:DIM } }],
  { x:7.0, y:5.35, w:5.6, h:1.5 });
s.addNotes("GABRIEL. O 0,22 s foi medido rodando esse código. f1 e f2 são criados antes do for, por isso já começam a rodar. Se fossem criados dentro do for, rodariam um depois do outro. O 2.seconds é um extension method sobre Int, o mesmo recurso do slide de IDs. Passar para o Gabriel.");

// 11 — divisória 3
divider("3", "Na prática", "Gabriel Soares", "atores  ·  spark  ·  kafka  ·  críticas", "GABRIEL apresenta a parte 3.");

// 13 — atores
s = slide("parte 3 · atores", "Mensagens no lugar de locks");
function actor(cx, label) {
  s.addShape(pres.shapes.OVAL, { x:cx-1.15, y:2.3, w:2.3, h:2.3, fill:{color:PANEL}, line:{color:ACC, width:2} });
  T(s, label, { x:cx-1.15, y:2.95, w:2.3, h:0.5, fontSize:22, bold:true, align:"center" });
  T(s, "estado privado", { x:cx-1.15, y:3.45, w:2.3, h:0.4, fontSize:14, color:DIM, align:"center" });
}
actor(2.0, "Ator A"); actor(6.9, "Ator B");
s.addShape(pres.shapes.LINE, { x:3.3, y:3.45, w:2.3, h:0, line:{ color:ACC, width:2.5, endArrowType:"triangle" } });
T(s, "mensagem", { x:3.3, y:2.95, w:2.3, h:0.4, fontFace:MONO, fontSize:15, color:ACC, align:"center" });
T(s, "Cada ator processa uma mensagem por vez e ninguém toca no estado do outro. Sem estado compartilhado, não há condição de corrida.", { x:0.7, y:5.05, w:8.0, h:1.3, fontSize:19, color:DIM });
s.addShape(pres.shapes.RECTANGLE, { x:9.1, y:2.1, w:3.5, h:4.4, fill:{color:PANEL}, line:{color:PANEL} });
T(s, [{ text:"Akka", options:{ bold:true, color:FG, fontSize:22, breakLine:true } }, { text:" ", options:{ breakLine:true, fontSize:8 } },
      { text:"Toolkit de atores do ecossistema Scala. O ator do outro lado pode estar em outra máquina.", options:{ color:DIM, breakLine:true } },
      { text:" ", options:{ breakLine:true } },
      { text:"Desde 2022 tem licença comercial. O Apache Pekko é o fork aberto.", options:{ color:DIM } }],
  { x:9.4, y:2.4, w:2.9, h:3.9, fontSize:16 });
s.addNotes("GABRIEL. Ligação com a disciplina: é troca de mensagens assíncrona, como em ZeroMQ e gRPC, só que no nível da linguagem. A mudança de licença do Akka é um bom gancho para o debate.");

// 14a — Spark: closures viajam até os dados
s = slide("parte 3 · spark", "O código viaja até os dados");
editor(s, 0.7, 2.05, 7.2, 3.35, "LogMining.scala", 'val lines  = spark.textFile("hdfs://...")\nval errors = lines.filter(_.startsWith("ERROR"))\nerrors.persist()\n\nerrors.filter(_.contains("HDFS"))\n      .map(_.split(\'\\t\')(3))\n      .collect()', 14);
// diagrama: driver serializa a closure e envia aos executores
const dbx = (x, y, w, h, t, hi, fs) => { s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill:{color: hi?ACC:PANEL}, line:{color: hi?ACC:BAR, width:1} });
  T(s, t, { x, y, w, h, fontFace:MONO, fontSize:fs||13, align:"center", valign:"middle", color: hi?BG:FG, bold:!!hi }); };
dbx(8.3, 3.2, 1.35, 0.65, "driver", true);
[2.15, 3.2, 4.25].forEach((y, i) => {
  dbx(11.0, y, 1.6, 0.65, "executor " + (i+1));
  s.addShape(pres.shapes.LINE, { x:9.7, y: y >= 3.2 ? 3.52 : y+0.32, w:1.25, h: Math.abs((y+0.32)-3.52) || 0.001, flipV: y < 3.2,
    line:{ color:DIM, width:1.25, endArrowType:"triangle" } });
});
T(s, "_.startsWith(\"ERROR\")", { x:8.3, y:4.15, w:2.6, h:0.35, fontFace:MONO, fontSize:12, color:STR });
T(s, "a closure vira um objeto Java serializado e vai pela rede", { x:8.3, y:4.5, w:2.6, h:0.8, fontSize:13, color:DIM });
s.addShape(pres.shapes.RECTANGLE, { x:0.7, y:5.65, w:11.9, h:1.05, fill:{color:PANEL}, line:{color:PANEL} });
T(s, [{ text:"“Escolhemos Scala pela combinação de concisão (conveniente para uso interativo) e eficiência (por causa da tipagem estática).”", options:{ color:FG, italic:true, breakLine:true } },
      { text:"Zaharia et al., artigo original do Spark (RDDs), NSDI 2012", options:{ color:DIM, fontSize:12 } }],
  { x:1.0, y:5.78, w:11.3, h:0.85, fontSize:15 });
s.addNotes("GABRIEL. Exemplo de mineração de logs tirado do artigo original do Spark (Zaharia et al., NSDI 2012, seção 2.2). O que é distribuído aqui: a função _.startsWith(\"ERROR\") é uma closure; o Scala a representa como um objeto Java, que é serializado e enviado pela rede para cada nó, que a executa sobre a sua parte do arquivo. É o código indo até os dados, e não os dados até o código. O artigo diz que nada do RDD exige uma linguagem funcional, mas Scala foi escolhida pela concisão e pela eficiência da tipagem estática. Hoje ~70% do repositório do Spark é Scala (GitHub). O PySpark conversa com essa JVM por uma ponte (Py4J).");

// 14b — Catalyst
s = slide("parte 3 · spark sql", "O otimizador do Spark SQL é pattern matching");
editor(s, 0.7, 2.05, 7.2, 2.9, "Catalyst.scala", 'tree.transform {\n  case Add(Literal(a), Literal(b)) => Literal(a + b)\n  case Add(left, Literal(0))       => left\n  case Add(Literal(0), right)      => right\n}', 13);
const NW=0.8, NH=0.55;
function node(cx, cy, t, hi) { s.addShape(pres.shapes.OVAL, { x:cx-NW/2, y:cy-NH/2, w:NW, h:NH, fill:{color: hi?ACC:PANEL}, line:{color: hi?ACC:BAR, width:1} });
  T(s, t, { x:cx-NW/2, y:cy-NH/2, w:NW, h:NH, fontFace:MONO, fontSize:14, align:"center", valign:"middle", color: hi?BG:FG, bold:!!hi }); }
function edge(px, py, cx, cy) { const y1 = py + NH/2, y2 = cy - NH/2;
  s.addShape(pres.shapes.LINE, { x:Math.min(px,cx), y:y1, w:Math.abs(cx-px)||0.001, h:y2-y1, flipH: cx<px, line:{ color:GUT, width:1.25 } }); }
// x + (1 + 2)
edge(9.05,2.4, 8.6,3.25); edge(9.05,2.4, 9.5,3.25); edge(9.5,3.25, 9.05,4.1); edge(9.5,3.25, 9.95,4.1);
node(9.05,2.4,"+"); node(8.6,3.25,"x"); node(9.5,3.25,"+",true); node(9.05,4.1,"1"); node(9.95,4.1,"2");
T(s, "→", { x:10.45, y:2.95, w:0.5, h:0.6, fontSize:28, color:ACC, align:"center", valign:"middle" });
edge(11.7,2.4, 11.25,3.25); edge(11.7,2.4, 12.15,3.25);
node(11.7,2.4,"+"); node(11.25,3.25,"x"); node(12.15,3.25,"3",true);
T(s, "x + (1 + 2)", { x:8.2, y:4.55, w:2.2, h:0.35, fontFace:MONO, fontSize:13, color:DIM, align:"center" });
T(s, "x + 3", { x:10.95, y:4.55, w:1.6, h:0.35, fontFace:MONO, fontSize:13, color:DIM, align:"center" });
T(s, "A consulta SQL vira uma árvore de objetos imutáveis (case classes). Cada regra de otimização é um case que procura um formato na árvore e devolve uma árvore nova. É o pattern matching da parte 1 no coração de um sistema distribuído.", { x:0.7, y:5.35, w:11.9, h:1.0, fontSize:18, color:DIM });
T(s, "Regras tiradas do artigo do Spark SQL (Armbrust et al., SIGMOD 2015). Uma versão mínima roda no exemplos.scala.", { x:0.7, y:6.45, w:11.0, h:0.35, fontSize:13, color:DIM });
s.addNotes("GABRIEL. O Catalyst é o otimizador de consultas do Spark SQL. As três regras são do artigo dos criadores (Armbrust et al., SIGMOD 2015) e do post da Databricks sobre o Catalyst. Exemplo: x+(1+2) vira x+3, porque a primeira regra encontra um Add de dois literais e soma em tempo de otimização. Por que Scala: pattern matching deixa cada regra curta e só olha os formatos que interessam; árvores imutáveis tornam o otimizador fácil de entender e depurar (palavras do próprio post). No exemplos.scala do grupo há uma versão mínima, com sealed trait Expr, que roda e imprime Add(Attribute(x),Literal(3)).");

// 14c — Kafka
s = slide("parte 3 · kafka", "Kafka nasceu em Scala e migra para Java");
const marcos = [
  ["2011", "LinkedIn abre o código. Broker e clientes em Scala."],
  ["0.8.2 / 0.9", "Producer e consumer reescritos em Java."],
  ["2.0", "Clientes Scala removidos."],
  ["4.0", "Só Scala 2.13. Código novo, como o KRaft, em Java."],
];
s.addShape(pres.shapes.LINE, { x:0.9, y:2.55, w:11.5, h:0, line:{ color:BAR, width:2 } });
marcos.forEach((m, i) => {
  const x = 0.7 + i*3.0;
  s.addShape(pres.shapes.OVAL, { x:x+0.1, y:2.43, w:0.24, h:0.24, fill:{color: i==0?ACC:FG}, line:{color: i==0?ACC:FG} });
  T(s, m[0], { x, y:2.85, w:2.8, h:0.45, fontFace:MONO, fontSize:17, bold:true, color: i==0?ACC:FG });
  T(s, m[1], { x, y:3.3, w:2.7, h:1.0, fontSize:15, color:DIM });
});
s.addShape(pres.shapes.RECTANGLE, { x:0.7, y:4.55, w:5.8, h:2.15, fill:{color:PANEL}, line:{color:PANEL} });
T(s, [{ text:"Por que os clientes saíram do Scala", options:{ bold:true, color:FG, breakLine:true } }, { text:" ", options:{ breakLine:true, fontSize:6 } },
      { text:"versões do Scala incompatíveis entre si", options:{ bullet:true, color:DIM, breakLine:true } },
      { text:"classes Scala vazando na API usada em Java", options:{ bullet:true, color:DIM, breakLine:true } },
      { text:"Javadoc ruim e stack traces difíceis de ler", options:{ bullet:true, color:DIM } }],
  { x:1.0, y:4.75, w:5.3, h:1.85, fontSize:16 });
s.addShape(pres.shapes.RECTANGLE, { x:6.8, y:4.55, w:5.8, h:2.15, fill:{color:PANEL}, line:{color:PANEL} });
T(s, [{ text:"~8%", options:{ fontSize:40, bold:true, color:FG } }, { text:"  do repositório ainda é Scala", options:{ fontSize:15, color:DIM, breakLine:true } },
      { text:"Mas o núcleo do broker continua lá:", options:{ fontSize:15, color:DIM, breakLine:true } },
      { text:"ReplicaManager.scala", options:{ fontFace:MONO, fontSize:14, color:TYP, breakLine:true } }, { text:"KafkaApis.scala  LogManager.scala", options:{ fontFace:MONO, fontSize:14, color:TYP } }],
  { x:7.1, y:4.7, w:5.3, h:1.9 });
s.addNotes("GABRIEL. Este slide é um caso real das críticas. O Kafka foi aberto pelo LinkedIn em 2011 com broker e clientes em Scala. A proposta oficial 'Client Rewrite' (wiki do Kafka) lista os motivos para reescrever os clientes em Java: incompatibilidade entre versões do Scala, classes Scala vazando na API Java, Javadoc ruim e stack traces difíceis. O producer Java saiu na 0.8.2, o consumer na 0.9, e os clientes Scala foram removidos na 2.0. Na 4.0 (KIP-751) só Scala 2.13 é suportado, e código novo como o KRaft é escrito em Java. Hoje cerca de 8% do repositório é Scala (GitHub, nov/2026; já foi metade na 0.7), mas classes centrais do broker como ReplicaManager, KafkaApis e LogManager ainda são arquivos .scala.");

// 15 — críticas
s = slide("parte 3 · críticas", "Segurança tem custo");
const col = (x, sign, color, items) => {
  T(s, sign, { x, y:2.15, w:1, h:0.9, fontSize:54, bold:true, color });
  items.forEach((it, i) => {
    s.addShape(pres.shapes.LINE, { x, y:3.25 + i*1.05, w:5.6, h:0, line:{ color:BAR, width:1 } });
    T(s, it, { x, y:3.4 + i*1.05, w:5.6, h:0.8, fontSize:21 });
  });
};
col(0.7, "+", STR, ["Erros de tipo e casos esquecidos param na compilação", "Imutabilidade facilita concorrência", "Todo o ecossistema Java disponível"]);
col(7.0, "−", ERR, ["Curva de aprendizado alta", "Compilação lenta e comunidade pequena", "Versões incompatíveis entre si, o motivo de o Kafka ir para Java"]);
s.addNotes("GABRIEL. O professor pediu críticas positivas e negativas. A expressividade que encurta o código também pode deixá-lo difícil de ler quando se abusa de recursos avançados.");

// 16 — encerramento
s = slide();
T(s, "Perguntas?", { x:0.7, y:1.6, w:11.9, h:1.6, fontSize:88, bold:true });
T(s, [{ text:"Scala compensa quando ", options:{ color:DIM } }, { text:"correção", options:{ color:ACC } }, { text:" e ", options:{ color:DIM } }, { text:"concorrência", options:{ color:ACC } }, { text:" importam mais que a velocidade de escrever.", options:{ color:DIM } }],
  { x:0.75, y:3.5, w:11, h:1.2, fontSize:26 });
T(s, "Pedro · Luis · Gabriel", { x:0.75, y:6.0, w:8, h:0.4, fontFace:MONO, fontSize:14, color:ACC });
s.addNotes("GABRIEL fecha e abre para perguntas e debate (~10 min).");


// 18 — referências
s = slide("referências", "Para estudar cada conceito");
const L = [
  ["opaque types", "docs.scala-lang.org/scala3/book/types-opaque-types.html"],
  ["extension methods", "docs.scala-lang.org/scala3/book/ca-extension-methods.html"],
  ["sealed e pattern matching", "docs.scala-lang.org/scala3/book/types-adts-gadts.html"],
  ["Option e Either", "docs.scala-lang.org/scala3/book/fp-functional-error-handling.html"],
  ["given / using", "docs.scala-lang.org/scala3/book/ca-context-parameters.html"],
  ["by-name", "docs.scala-lang.org/tour/by-name-parameters.html"],
  ["Futures", "docs.scala-lang.org/overviews/core/futures.html"],
  ["atores (Pekko)", "pekko.apache.org/docs/pekko/current/typed/actors.html"],
  ["Spark (RDDs)", "Zaharia et al., NSDI 2012 · usenix.org"],
  ["Catalyst", "Armbrust et al., SIGMOD 2015 · blog da Databricks"],
  ["Kafka em Java", "cwiki.apache.org/confluence/display/KAFKA/Client+Rewrite"],
];
L.forEach((r, i) => {
  const y = 2.0 + i*0.42;
  T(s, r[0], { x:0.7, y, w:3.6, h:0.38, fontSize:16, bold:true, valign:"middle" });
  T(s, r[1], { x:4.4, y, w:8.2, h:0.38, fontFace:MONO, fontSize:13, color:TYP, valign:"middle" });
});
s.addNotes("Slide de apoio: mostrar só se perguntarem. Links completos no GUIA_DE_ESTUDO.md.");

pres.writeFile({ fileName: "scala-seminario.pptx" }).then(() => console.log("ok", n));
