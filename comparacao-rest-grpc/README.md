# RESTful × gRPC: comparação a partir do exemplo Employee Service

Base da análise: [RESTful-WS-Example](../RESTful-WS-Example-main) (Flask + JSON sobre HTTP) e [gRPC-WS-Example](../gRPC-WS-Example-main) (Protocol Buffers sobre HTTP/2). Os dois expõem o mesmo serviço (cadastro de funcionários: criar, consultar, atualizar, remover, listar). Os números da seção 2 foram medidos por mim; o restante é análise do código e dos modelos.

## 1. Os dois exemplos em uma frase

- **REST:** interface **genérica**. O cliente usa os verbos HTTP (`GET/PUT/POST/DELETE`) sobre URLs que identificam recursos (`/empdb/employee/201`). O formato das mensagens (JSON) não é declarado em lugar nenhum: o contrato está na cabeça de quem escreveu servidor e cliente.
- **gRPC:** interface **específica da aplicação**. Um arquivo `.proto` declara os métodos (`CreateEmployee`, `ListAllEmployees`…) e os tipos das mensagens; um compilador gera os stubs do cliente e o esqueleto do servidor.

## 2. Comparação técnica

### Modelo de programação

| | REST (exemplo) | gRPC (exemplo) |
|---|---|---|
| Paradigma | Recursos + verbos uniformes | Chamada de procedimento remoto (RPC) |
| Cliente | `requests.get(base + '/201').json()`: monta URL, escolhe o verbo, interpreta JSON à mão | `stub.GetEmployeeDataFromID(EmployeeID(id=201))`: parece chamada de método local |
| Servidor | Uma função Flask por rota, extraindo dados de `request.json` | Uma classe com um método por RPC, recebendo objetos tipados |
| Contrato | Implícito (código + documentação à parte, ex.: README/OpenAPI) | Explícito e executável (`.proto`) |
| Tipos | `id` é string no JSON; nada valida os campos | `id` é `uint32`; o stub rejeita tipos errados na serialização |

No REST do exemplo, o próprio design mostra os limites da interface genérica: atualizar o salário virou `PUT /employee/<id>/<salário>`, um "verbo" escondido no caminho, e `PUT` é usado como atualização parcial (semântica de `PATCH`). No gRPC cada operação tem nome e tipos próprios, o que é mais natural para quem pensa em operações, e menos natural para quem pensa em recursos.

### Eficiência (medido)

Servidor e cliente na mesma máquina (loopback), 2.000 chamadas sequenciais por teste, Python nos dois lados. REST: Flask (servidor de desenvolvimento) com `requests`. gRPC: `grpcio`. Script: [bench.py](bench.py).

| Operação | REST (média / p99) | gRPC (média / p99) |
|---|---|---|
| Consultar 1 funcionário | 2,27 / 2,88 ms | 0,23 / 0,65 ms |
| Listar (2 registros) | 2,23 / 2,74 ms | 0,22 / 0,52 ms |
| Listar (202 registros) | 2,67 / 3,24 ms | 0,44 / 1,05 ms |

| Tamanho da mensagem | REST (JSON) | gRPC (protobuf) |
|---|---|---|
| 1 funcionário | corpo 100 B (+148 B de cabeçalhos de resposta) | 37 B (+5 B de framing) |
| Lista de 2 | 186 B | 74 B |
| Lista de 202 | 14.186 B | 8.874 B (JSON ≈ 1,6× maior) |

Como interpretar, com ressalvas honestas:
- gRPC foi ~10× mais rápido por chamada aqui, mas **a maior parte dessa diferença vem da implementação, não do protocolo**: o servidor Flask de desenvolvimento é lento e fecha a conexão a cada resposta (`Connection: close`, conferido com `curl -i`), enquanto o servidor gRPC é em C++ com HTTP/2 persistente. Um servidor REST de produção (gunicorn, ou Go/Java/Node) reduziria bastante essa distância. Por isso, os números mostram a ordem de grandeza do exemplo, não um veredito sobre as tecnologias.
- A diferença de **tamanho** é mais estrutural: JSON repete os nomes dos campos em cada registro e escreve números como texto, enquanto o protobuf usa números de campo e inteiros em formato binário. Quanto menor e mais numérica a mensagem, maior o ganho (com os registros pequenos acima, ≈ 2,5×; na lista longa, 1,6×). Compressão HTTP (gzip) reduz parte do ganho do protobuf.
- Em rede real (como as instâncias EC2 das tarefas anteriores) a latência da rede domina e a diferença por chamada diminui; o ganho de gRPC aparece mais em alto volume de chamadas, mensagens grandes e streaming.
- gRPC também ganha em **multiplexação** (várias chamadas simultâneas numa conexão HTTP/2) e **streaming** bidirecional, que o REST clássico não oferece nativamente.

### Modularidade e manutenibilidade

- **gRPC:** o `.proto` separa a interface da implementação e serve como documentação única. Os stubs são gerados, o que elimina a classe de erros "o cliente montou o JSON errado". Mudar um campo ou método quebra a compilação dos dois lados, o que é bom: o erro aparece cedo. O custo é a etapa de geração de código e as ferramentas extras (`protoc`) em todo ambiente de build. Para acrescentar o salário (como o enunciado do REST pede), muda o `.proto`, regenera-se e atualizam-se as duas pontas.
- **REST:** o servidor pode ganhar um campo sem mexer em nenhuma ferramenta, e clientes antigos continuam funcionando. Isso é rápido, mas **nada garante consistência**. O código do exemplo mostra isso: o `POST` ignora o campo `salary` enviado pelo cliente (verificado: a resposta devolve só `id`, `name` e `title`), e nenhum erro avisa. Sem contrato formal (OpenAPI/JSON Schema), a manutenção depende de disciplina e de testes.
- **Evolução compatível:** no protobuf, o número do campo identifica o dado, então é possível adicionar campos opcionais e remover os antigos sem quebrar clientes, desde que se sigam as regras. No REST, a compatibilidade é igualmente possível, mas é convenção, não regra imposta pela ferramenta.

### Abertura (openness)

- **REST** é aberto no sentido mais amplo: HTTP + JSON são padrões universais, qualquer linguagem, navegador, `curl` ou ferramenta de teste consome a API sem biblioteca especial e sem compartilhar nenhum arquivo com o servidor.
- **gRPC** também é aberto (especificação pública, ~12 linguagens com suporte oficial), mas exige que o cliente tenha o `.proto` e o gerador de código. A interoperabilidade entre linguagens é excelente dentro desse ecossistema; fora dele (um navegador, um script de shell) é mais trabalhosa.

### Transparência de distribuição

- **gRPC** aproxima-se do ideal clássico de RPC: o cliente chama `stub.GetEmployeeDataFromID(...)` como se fosse local; serialização, conexão e despacho ficam escondidos. Mas essa transparência é parcial: falhas de rede continuam existindo (o cliente precisa tratar `RpcError`, definir timeouts via *deadlines*), e o próprio gRPC expõe isso nos códigos de status.
- **REST** é **menos transparente por escolha**: o cliente sabe que está fazendo HTTP (URLs, verbos, códigos de status, cabeçalhos). Em troca, a rede fica explícita e visível, e os mecanismos da web (cache, proxies, balanceadores) funcionam sobre ela sem adaptação.

### Tratamento de erros (observado nos exemplos)

| Situação | REST (exemplo) | gRPC (exemplo) |
|---|---|---|
| Consultar id inexistente | HTTP **200** com `{"emp": []}` | erro `UNKNOWN` (exceção `IndexError` não tratada) |
| Atualizar salário de id inexistente | HTTP **500** | (operação não existe no exemplo) |
| Remover id inexistente | HTTP 200 com `{'response': 'Failure'}` | resposta `status = 'NOK'` |

Nenhum dos dois exemplos trata erros bem; são exemplos didáticos. Mas mostram a diferença conceitual: REST tem o vocabulário de códigos HTTP (404, 409, 422…) e gRPC tem o seu (`NOT_FOUND`, `INVALID_ARGUMENT`, `ALREADY_EXISTS`…, como usei no serviço de nomes da tarefa anterior). O exemplo gRPC ignora esse vocabulário e devolve strings `'OK'`/`'NOK'` no corpo, o que reinventa o que o protocolo já oferece.

## 3. Comparação ampla: onde cada tecnologia se encaixa

### APIs para aplicações de usuário final (frontend: navegador, apps)

**REST tende a ser a melhor escolha.**
- Funciona nativamente no navegador (`fetch`), sem biblioteca adicional. gRPC não: os navegadores não dão controle suficiente sobre HTTP/2, então é preciso gRPC-Web e um proxy (ex.: Envoy) no meio, com limitações (sem streaming bidirecional).
- JSON é legível e depurável nas ferramentas do navegador, no `curl` e no Postman.
- Aproveita a infraestrutura da web: cache HTTP (`GET`, `ETag`, CDN), autenticação por cookie/`Authorization`, CORS.
- APIs públicas têm que ser consumidas por terceiros que não controlamos; um padrão universal e documentado (OpenAPI) reduz a barreira de entrada.
- Em apps móveis, gRPC é viável e vantajoso (mensagens menores, economia de dados e bateria, streaming), principalmente quando a equipe controla o cliente.

### APIs entre serviços (backend: microsserviços, comunicação interna)

**gRPC tende a ser a melhor escolha.**
- Alto volume de chamadas internas: menor latência e menor volume de dados fazem diferença acumulada.
- Contrato forte entre equipes diferentes: o `.proto` é a fonte única, e a geração de código em várias linguagens mantém serviços poliglotas consistentes.
- Streaming (servidor, cliente ou bidirecional), *deadlines*, cancelamento e interceptors (autenticação, tracing, métricas) são recursos de primeira classe.
- Os dois lados são nossos, então a dependência do `.proto` e do gerador de código é aceitável.

### Fatores para decidir

1. **Quem são os clientes?** Navegadores e terceiros → REST. Serviços internos que controlamos → gRPC.
2. **Padrão de comunicação:** simples pedido/resposta funciona nos dois; streaming ou comunicação bidirecional → gRPC.
3. **Desempenho:** latência, volume de chamadas e tamanho das mensagens. Meça no seu cenário: neste exemplo, parte da diferença vinha da implementação do servidor, não do protocolo.
4. **Contrato e evolução:** quanto maior o número de equipes e linguagens, maior o valor de um contrato formal e gerado (gRPC; ou REST com OpenAPI, que dá parte do mesmo benefício).
5. **Ferramentas e depuração:** REST vence em facilidade (`curl`, navegador, logs legíveis); gRPC exige ferramentas próprias (`grpcurl`, reflection) porque o conteúdo é binário.
6. **Infraestrutura:** gRPC exige HTTP/2 de ponta a ponta (balanceadores, proxies e gateways compatíveis; balanceamento por chamada, não por conexão). REST funciona praticamente em qualquer lugar.
7. **Cache e semântica web:** REST com `GET` cacheável é difícil de imitar em gRPC.
8. **Modelo mental da equipe:** o domínio é mais natural como recursos (CRUD) ou como operações (comandos, ações com regras)? Para operações complexas, RPC costuma ser mais expressivo; para CRUD sobre entidades, REST casa bem.
9. **Segurança:** ambos suportam TLS e autenticação por token; nos exemplos analisados nenhum dos dois usa TLS (`insecure_channel`, HTTP puro), o que seria inaceitável em produção.

### Não é uma escolha excludente

Combinações comuns: **gRPC internamente e REST na borda** (um gateway traduz, por exemplo com gRPC-Gateway ou transcodificação do Envoy, expondo uma API REST/JSON para o frontend a partir do mesmo `.proto`), ou REST para a API pública e gRPC entre microsserviços.

## 4. Conclusão

REST e gRPC resolvem o mesmo problema com filosofias diferentes: **REST privilegia a universalidade e a simplicidade de acesso** (interface genérica, texto, web), **gRPC privilegia o contrato forte e a eficiência** (interface específica, binário, RPC tipada). No exemplo analisado, o gRPC mostrou menores mensagens e menor latência por chamada, além de um contrato explícito que o REST não tem; o REST mostrou menor atrito de uso e evolução mais flexível, ao custo de erros silenciosos (o `POST` que descarta o salário, o `200` para um id inexistente). A escolha deve partir de quem consome a API e do que importa mais (alcance e simplicidade, ou desempenho e rigor do contrato), e não de uma preferência pela tecnologia em si.

## Apêndice: como medir

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install flask requests grpcio grpcio-tools
# gerar stubs do exemplo gRPC e subir os dois servidores (portas 5678 e 50051), depois:
python bench.py
```
Detalhes: 1 chamada de aquecimento + 2.000 medidas por teste; tempos em `time.perf_counter`; REST usa `requests.Session` (os números "sem keep-alive" ficaram próximos, pois o servidor de desenvolvimento do Flask fecha a conexão a cada resposta); tamanho gRPC = `ByteSize()` da mensagem. A medição é em loopback, com um único cliente, e deve ser lida como ordem de grandeza.
