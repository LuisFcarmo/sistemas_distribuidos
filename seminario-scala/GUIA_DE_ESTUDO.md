# Guia de estudo: seminário de Scala

Para cada slide: a ideia em uma frase, como explicar, a pergunta mais provável do professor e onde estudar.
Todo o código está em `exemplos.scala` e roda com Scala 3:

```bash
scalac -d out exemplos.scala
scala -cp out seminario
```

Para ver os erros do compilador mostrados nos slides, descomente as linhas marcadas com `// descomente` no arquivo.

Ponto de partida para quem vem de Python: [Scala para desenvolvedores Python](https://docs.scala-lang.org/scala3/book/scala-for-python-devs.html) (página oficial que compara as duas linguagens lado a lado).

---

## Parte 1 · Pedro

### O que é Scala
- **Em uma frase:** linguagem da JVM que mistura orientação a objetos e programação funcional, com tipos verificados na compilação.
- **Como explicar:** o `scalac` gera bytecode Java, então o programa roda em qualquer JVM e usa qualquer biblioteca Java. Os tipos são inferidos: quase não se escreve tipo, mas o compilador confere todos.
- **Pergunta provável:** *"Por que não usar Java direto?"* Scala tem inferência de tipos, pattern matching, funções como valores e os recursos dos próximos slides, com código bem mais curto. E continua usando as bibliotecas Java.
- **Pergunta provável:** *"Scala 2 ou 3?"* Os exemplos são Scala 3 (lançado em 2021), que trouxe sintaxe por indentação, `given`/`using` no lugar dos antigos `implicit`, e `opaque type`.
- **Estudar:** [livro oficial do Scala 3](https://docs.scala-lang.org/scala3/book/introduction.html)

### Opaque types e extension methods
- **Em uma frase:** dois IDs que são `Long` por baixo viram tipos diferentes para o compilador, sem custo nenhum em execução.
- **Como explicar:** o bug clássico em sistema distribuído é passar o ID do cliente onde se esperava o do pedido. Fora do `object Ids`, ninguém sabe que é `Long`, então misturar não compila. Em execução, são só `Long`. `extension` acrescenta um método (`proximo`) a um tipo sem alterá-lo.
- **Pergunta provável:** *"Por que não `case class ClienteId(v: Long)`?"* Funciona, mas cria um objeto a cada ID em execução. O opaque type some depois da compilação.
- **Pergunta provável:** *"E `type ClienteId = Long`?"* Isso é só um apelido: o compilador trata como o mesmo tipo, e a mistura passaria.
- **Gancho:** o `2.seconds` do slide de Futures também é um extension method sobre `Int`.
- **Estudar:** [opaque types](https://docs.scala-lang.org/scala3/book/types-opaque-types.html) · [extension methods](https://docs.scala-lang.org/scala3/book/ca-extension-methods.html)

### sealed e pattern matching
- **Em uma frase:** com `sealed`, o compilador conhece todos os subtipos e avisa quando um `match` esquece algum.
- **Como explicar:** `sealed` obriga todos os subtipos de `Forma` a estarem no mesmo arquivo. Ao criar `Triangulo`, todo `match` que não o trata gera o aviso "match may not be exhaustive". Num sistema grande, isso aponta exatamente o que precisa mudar.
- **Pergunta provável:** *"E se não for sealed?"* As subclasses podem estar em qualquer arquivo, então o compilador não consegue checar se o `match` cobre todos os casos.
- **Pergunta provável:** *"É erro ou aviso?"* Aviso. Com a opção `-Werror`, avisos viram erro e o programa não compila.
- **Estudar:** [ADTs e sealed](https://docs.scala-lang.org/scala3/book/types-adts-gadts.html) · [pattern matching](https://docs.scala-lang.org/tour/pattern-matching.html)

---

## Parte 2 · Luis

### Either e Option
- **Em uma frase:** a possibilidade de falha aparece no tipo de retorno, e não escondida numa exceção.
- **Como explicar:** `div` devolve `Right(valor)` ou `Left(erro)`. Quem chama vê pela assinatura que pode falhar. O `for` encadeia as operações e para no primeiro `Left`, sem um `if` para cada passo. `Option` é `Some(valor)` ou `None` e substitui o `null`.
- **Pergunta provável:** *"Diferença entre Option e Either?"* `Option` só diz se tem valor. `Either` também diz por que falhou.
- **Pergunta provável:** *"E as exceções?"* Continuam existindo (vêm do Java), mas não aparecem na assinatura. `scala.util.Try` transforma uma exceção em valor.
- **Estudar:** [tratamento funcional de erros](https://docs.scala-lang.org/scala3/book/fp-functional-error-handling.html)

### given / using (type classes)
- **Em uma frase:** o compilador escolhe, pelo tipo da mensagem, qual serializador usar, e se não houver nenhum o programa não compila.
- **Como explicar:** `Codec[T]` diz como transformar um `T` em texto. `given` registra a implementação para `Pedido`. `using` pede ao compilador que encontre o `Codec` certo e o passe sozinho. Para `Double` não existe nenhum, então o erro aparece na compilação, e não quando a mensagem já está na rede.
- **Pergunta provável:** *"E se houver dois `given` para o mesmo tipo?"* Também não compila: "Ambiguous given instances" (testado no Scala 3.3).
- **Pergunta provável:** *"É injeção de dependência?"* Parecido, mas resolvido em compilação, pelo tipo, sem framework.
- **Estudar:** [parâmetros de contexto](https://docs.scala-lang.org/scala3/book/ca-context-parameters.html) · [type classes](https://docs.scala-lang.org/scala3/book/ca-type-classes.html)

### Parâmetros by-name
- **Em uma frase:** com `=> T`, o bloco não é executado na chamada e roda de novo cada vez que é usado, o que permite criar estruturas que parecem palavra-chave da linguagem.
- **Como explicar:** normalmente o argumento é calculado antes da chamada. Com by-name, `comRetry(3) { ... }` reexecuta o bloco a cada tentativa. Em sistemas distribuídos, repetir uma chamada que deu timeout é rotina.
- **Pergunta provável:** *"Qual a diferença de passar uma função `() => T`?"* Por baixo é parecido (vira uma função sem parâmetros), mas quem chama escreve só o bloco, sem `() =>`.
- **Pergunta provável:** *"É o mesmo que `lazy val`?"* Não. `lazy val` calcula uma vez e guarda. By-name recalcula a cada uso, que é o que o retry precisa.
- **Estudar:** [by-name parameters](https://docs.scala-lang.org/tour/by-name-parameters.html)

### Futures
- **Em uma frase:** `Future` começa a rodar assim que é criado, em threads de verdade, e os resultados se combinam com `for`.
- **Como explicar:** `f1` e `f2` são criados antes do `for`, então rodam ao mesmo tempo. O tempo medido foi 0,22 s, e não 0,4 s. Se fossem criados dentro do `for`, rodariam um depois do outro.
- **Pergunta provável:** *"O `Await` bloqueia?"* Sim. Ele só aparece no exemplo para imprimir o resultado. Em código real, os Futures são compostos com `map`/`for` sem bloquear.
- **Pergunta provável:** *"Quem executa?"* Um `ExecutionContext`, que é um pool de threads. O `global` usa um pool com um número de threads próximo ao de núcleos da máquina.
- **Estudar:** [guia oficial de Futures](https://docs.scala-lang.org/overviews/core/futures.html) · [concorrência no livro do Scala 3](https://docs.scala-lang.org/scala3/book/concurrency.html)

---

## Parte 3 · Gabriel

### Atores
- **Em uma frase:** cada ator tem estado privado e só conversa por mensagens, então não há estado compartilhado nem lock.
- **Como explicar:** é a troca de mensagens assíncrona da disciplina (ZeroMQ, gRPC), só que no nível da linguagem. O ator do outro lado pode estar em outra máquina, e a mensagem é enviada da mesma forma.
- **Pergunta provável:** *"Por que citar o Pekko?"* Em 2022 o Akka passou a ter licença comercial (BSL). O Apache Pekko é o fork aberto, mantido pela Apache.
- **Estudar:** [atores no Apache Pekko](https://pekko.apache.org/docs/pekko/current/typed/actors.html) · [anúncio da mudança de licença do Akka](https://www.lightbend.com/blog/why-we-are-changing-the-license-for-akka)

### Spark: o código viaja até os dados
- **Em uma frase:** a função passada ao `filter` é serializada e enviada pela rede para cada máquina, que a executa sobre a sua parte dos dados.
- **Como explicar:** no artigo original do Spark, os autores dizem que o Scala representa cada closure como um objeto Java, que pode ser serializado e carregado em outro nó. E explicam a escolha: "concisão (conveniente para uso interativo) e eficiência (por causa da tipagem estática)". Hoje cerca de 70% do repositório do Spark é Scala.
- **Pergunta provável:** *"E se a closure usar algo que não dá para serializar?"* O Spark falha com o erro "Task not serializable", um dos mais comuns para quem começa.
- **Pergunta provável:** *"E o PySpark?"* Ele conversa com a JVM do Spark por uma ponte (Py4J). O motor continua sendo Scala.
- **Estudar:** [artigo original do Spark (RDDs), NSDI 2012](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf) (seções 2 e 3) · [guia de RDDs](https://spark.apache.org/docs/latest/rdd-programming-guide.html)

### Catalyst: o otimizador do Spark SQL
- **Em uma frase:** a consulta vira uma árvore de objetos imutáveis, e cada regra de otimização é um `case` de pattern matching.
- **Como explicar:** a regra `case Add(Literal(a), Literal(b)) => Literal(a + b)` acha uma soma de duas constantes e calcula antes de executar: `x + (1 + 2)` vira `x + 3`. É o pattern matching da parte 1 no coração de um sistema distribuído. A versão mínima no `exemplos.scala` imprime `Add(Attribute(x),Literal(3))`.
- **Pergunta provável:** *"O código real é assim?"* O real tem mais detalhes (tipos, posições na consulta), mas as regras têm exatamente essa forma. As três do slide são do artigo dos criadores.
- **Estudar:** [post da Databricks sobre o Catalyst](https://www.databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html) · [artigo do Spark SQL, SIGMOD 2015](https://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf)

### Kafka: nasceu em Scala e migra para Java
- **Em uma frase:** o Kafka nasceu em Scala, reescreveu os clientes em Java por problemas do próprio Scala, e hoje escreve código novo em Java.
- **Como explicar:**
  - Aberto pelo LinkedIn em 2011.
  - Producer em Java na 0.8.2, consumer na 0.9.
  - Clientes Scala removidos na 2.0.
  - Na 4.0, só Scala 2.13.
  - Os motivos estão na proposta oficial de reescrita: versões do Scala incompatíveis entre si, classes Scala vazando na API usada em Java, Javadoc ruim e stack traces difíceis.
  - Hoje cerca de 8% do repositório é Scala, mas `ReplicaManager`, `KafkaApis` e `LogManager` (núcleo do broker) ainda são arquivos `.scala`.
- **Pergunta provável:** *"Então o Kafka não usa mais Scala?"* Usa no núcleo do broker. O que mudou é que código novo, como o KRaft (que substituiu o ZooKeeper), é escrito em Java.
- **Estudar:** [proposta de reescrita dos clientes](https://cwiki.apache.org/confluence/display/KAFKA/Client+Rewrite) · [KIP-751: fim do Scala 2.12 no Kafka 4.0](https://cwiki.apache.org/confluence/display/KAFKA/KIP-751%3A+Drop+support+for+Scala+2.12+in+Kafka+4.0+%28deprecate+in+3.0%29) · [notas de upgrade do Kafka 2.0](https://kafka.apache.org/20/getting-started/upgrade/)

### Críticas
- **A favor:** erros de tipo e casos esquecidos param na compilação, imutabilidade facilita concorrência e todo o ecossistema Java fica disponível.
- **Contra:** curva de aprendizado alta, compilação lenta, comunidade pequena e versões incompatíveis entre si. O caso do Kafka mostra esse último ponto na prática.
- **Pergunta provável:** *"Vocês usariam Scala?"* Resposta honesta: para scripts e análise de dados, Python é mais produtivo. Scala compensa em sistemas grandes, com muita concorrência ou processamento distribuído, onde o compilador evita erros caros.
- **Estudar:** [compatibilidade entre Scala 2 e 3](https://docs.scala-lang.org/scala3/guides/migration/compatibility-intro.html)

---

## O que não foi executado

O código do Spark nos slides é o exemplo do artigo original e não foi rodado, porque exigiria instalar o Spark. Todo o resto foi compilado e executado com Scala 3.3.4, e as mensagens de erro nos slides são as saídas reais do compilador.
