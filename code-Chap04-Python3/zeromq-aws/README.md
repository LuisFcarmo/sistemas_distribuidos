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

Todos os cenários foram executados com sucesso **localmente** (processos separados em localhost): todos os comandos do Req/Rep (inclusive erro e `STOP`), subscriber filtrando `TEMP`/`LOAD`, e pipeline com 2 fontes × 10 tarefas e 2 workers (20 resultados recebidos no sink, 10 por worker).

Teste em instâncias EC2 distintas: _preencher aqui após executar (instâncias, IPs, saída observada)._
