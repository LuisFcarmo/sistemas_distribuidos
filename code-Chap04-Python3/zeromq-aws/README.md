# ZeroMQ (pyzmq) – Figs. 4.21, 4.22 e 4.23 estendidas

Os três padrões de comunicação do ZeroMQ do livro (Tanenbaum & van Steen, cap. 4), com novas funcionalidades e IPs configuráveis para rodar em várias máquinas (AWS EC2).

| Fig. | Padrão | Pasta |
|------|--------|-------|
| 4.21 | Request/Reply (REQ/REP) | `reqrep/` |
| 4.22 | Publish/Subscribe (PUB/SUB) | `pubsub/` |
| 4.23 | Pipeline (PUSH/PULL) | `pipeline/` |

## Instalação (em cada máquina)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # pyzmq
```

## Configuração

Os endereços ficam em `config.py` e são sobrescritos por variáveis de ambiente (padrão: `127.0.0.1`, então tudo roda localmente sem configurar nada). Servidores fazem `bind` em `0.0.0.0`; clientes usam o IP **privado** (mesma VPC) ou público da instância.

| Variável | Significado |
|---|---|
| `SERVER_HOST`, `REP_PORT` (4567) | servidor Req/Rep |
| `PUB_HOST`, `PUB_PORT` (4569) | publisher |
| `SRC1`, `SRC2`, `SRC1_PORT` (4570), `SRC2_PORT` (4571) | fontes de tarefas |
| `SINK_HOST`, `SINK_PORT` (4572) | coletor de resultados |

**AWS:** no Security Group libere as portas TCP 4567–4572 (entrada) entre as instâncias.

## O que foi acrescentado

**Mudanças gerais:** IPs via ambiente (antes fixos no código); `bind` em `0.0.0.0`; mensagens em **JSON** (antes `pickle`, que executa código arbitrário ao desserializar dados de rede).

**Req/Rep** – servidor com vários comandos (antes só "acrescenta `*`"): `ECHO`, `UPPER`, `REVERSE`, `ADD` (soma números), `TIME`, `STATS` (contagem de uso por comando) e `STOP`. Respostas `{ok, result|error}`; comando desconhecido ou JSON inválido não derruba o servidor. Cliente com timeout de 5 s.

**Pub/Sub** – publisher publica três tópicos (`TIME`, `TEMP` simulado, `LOAD` = load average real da máquina). O subscriber escolhe tópicos e quantidade de mensagens pela linha de comando.

**Pipeline** – os workers agora enviam o resultado (`workload²`) a um novo programa **sink**, que agrega e mostra quantos resultados cada worker processou (balanceamento de carga). O número de tarefas é configurável (`N_TASKS`).

## Execução

### Req/Rep
```bash
# máquina A
python reqrep/server.py
# máquina B
export SERVER_HOST=<IP_A>
python reqrep/client.py ADD 1 2 3.5      # 6.5
python reqrep/client.py UPPER ola mundo  # OLA MUNDO
python reqrep/client.py STATS
python reqrep/client.py STOP
```

### Pub/Sub
```bash
# máquina A
python pubsub/publisher.py
# máquina B
export PUB_HOST=<IP_A>
python pubsub/subscriber.py 6 TEMP LOAD   # 6 mensagens dos tópicos TEMP e LOAD
```

### Pipeline (4 máquinas, por exemplo)
```bash
export SRC1=<IP_A> SRC2=<IP_B> SINK_HOST=<IP_D>   # em todas as máquinas
# D:  python pipeline/sink.py
# A:  python pipeline/tasksrc.py 1
# B:  python pipeline/tasksrc.py 2
# C:  python pipeline/taskwork.py w1      (pode haver vários workers, em várias máquinas)
```
Inicie o sink e os workers antes das fontes (as fontes esperam 2 s).

## Testes realizados

Também testado localmente (processos separados em localhost) antes do teste na AWS.

### Teste em instâncias EC2 (AWS, us-east-1, 08/11/2026)

3 instâncias `t3.micro` (Amazon Linux 2023, Python 3 + `venv` + `pyzmq` 27.3.0) na mesma VPC. Security Group: TCP 4567–4572 liberado apenas entre as instâncias e SSH só do meu IP. Comunicação pelos IPs privados.

| Máquina | IP privado | Papel |
|---|---|---|
| A | 172.31.25.102 | server Req/Rep, publisher, sink, fonte 1 |
| B | 172.31.16.245 | client Req/Rep, subscriber, fonte 2 |
| C | 172.31.27.232 | 2 workers (`w1`, `w2`) |

**Req/Rep** (servidor em A, cliente em B, `SERVER_HOST=172.31.25.102`):
```
$ client.py ADD 1 2 3.5       -> 6.5
$ client.py UPPER ola mundo   -> OLA MUNDO
$ client.py REVERSE abc       -> cba
$ client.py TIME              -> Sun Nov  8 23:27:56 2026
$ client.py STATS             -> {'ADD': 1, 'UPPER': 1, 'REVERSE': 1, 'TIME': 1, 'STATS': 1}
$ client.py FOO               -> ERRO: comando desconhecido: FOO
$ client.py STOP              -> encerrando
```

**Pub/Sub** (publisher em A, subscriber em B com `subscriber.py 6 TEMP LOAD`): recebeu apenas os tópicos assinados.
```
TEMP 30.0 / LOAD 0.02 / TEMP 34.6 / LOAD 0.02 / TEMP 23.0 / LOAD 0.01
```

**Pipeline** (`N_TASKS=15` em cada fonte): o sink em A recebeu os 30 resultados vindos de workers em outra máquina, com carga dividida igualmente:
```
#30 resultado 400 (fonte 2, worker w2) | por worker: {'w1': 14, 'w2': 16}
```
(o último `tail` capturado mostra o balanceamento ao final: 30 tarefas = 14 + 16.)

As instâncias, o Security Group e o key pair foram removidos após os testes.
