# Serviço de Nomes + serviços remotos em gRPC

Dois serviços de aplicação (**Calculadora** e **Texto**) em processos/máquinas diferentes, um **Serviço de Nomes** (`bind`, `lookup`, `unbind`, `rebind`) e um cliente que descobre os endereços dos serviços via lookup. Tudo em gRPC (Python).

```
                 ┌──────────────────┐
   1. bind  ───► │ Serviço de Nomes │ ◄─── 2. lookup("calculadora")
 (ao subir)      │   (porta 50050)  │          lookup("texto")
                 └──────────────────┘                 ▲
 ┌────────────┐  ┌────────────┐                       │
 │Calculadora │  │   Texto    │ ◄── 3. chamadas ── Cliente
 │  :50051    │  │   :50052   │     (endereço descoberto)
 └────────────┘  └────────────┘
```

## Arquivos

| Arquivo | Função |
|---|---|
| `nomes.proto` | `NameService`: `Bind`, `Lookup`, `Unbind`, `Rebind` |
| `servicos.proto` | `Calculadora` (Somar, Subtrair, Multiplicar, Dividir) e `Texto` (Maiusculas, Inverter, ContarPalavras) |
| `servidor_nomes.py` | implementação do serviço de nomes (tabela em memória, com lock) |
| `servidor_calculadora.py`, `servidor_texto.py` | serviços de aplicação |
| `registro.py` | ciclo de vida do servidor: `bind` ao subir (ou `rebind` se o nome já existia) e `unbind` ao receber Ctrl+C/SIGTERM |
| `cliente.py` | faz `lookup` dos dois serviços, chama-os e exercita as 4 operações do serviço de nomes |
| `*_pb2*.py` | código gerado pelo protoc (já incluído) |

### Semântica do serviço de nomes (via códigos de status gRPC)

| Operação | Sucesso | Erro |
|---|---|---|
| `Bind(nome, endereco)` | registra | `ALREADY_EXISTS` se o nome já existe |
| `Lookup(nome)` | devolve `host:porta` | `NOT_FOUND` |
| `Unbind(nome)` | remove | `NOT_FOUND` |
| `Rebind(nome, endereco)` | troca o endereço | `NOT_FOUND` se o nome não existe |

A `Calculadora.Dividir` devolve `INVALID_ARGUMENT` em divisão por zero.

## Instalação (em cada máquina)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
Para regenerar os stubs após editar os `.proto`:
`python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. nomes.proto servicos.proto`

## Execução

Máquina de nomes (N), calculadora (C), texto (T) e cliente (K). Use os IPs privados na AWS (mesma VPC). O segundo argumento dos servidores é o IP que será **registrado** no serviço de nomes (o IP da própria máquina).

```bash
# N
python servidor_nomes.py                                  # porta 50050
# C
python servidor_calculadora.py <IP_N>:50050 <IP_C>        # porta 50051
# T
python servidor_texto.py <IP_N>:50050 <IP_T>              # porta 50052
# K
python cliente.py <IP_N>:50050
```
Tudo local: use `127.0.0.1` em todos. Ctrl+C num servidor faz `unbind` automático. **AWS:** libere TCP 50050–50052 entre as instâncias no Security Group.

## Testes

### Local (4 processos em localhost) e AWS (4 instâncias EC2, us-east-1, 08/11/2026)

| Máquina | IP privado | Papel |
|---|---|---|
| N | 172.31.23.145 | serviço de nomes |
| C | 172.31.31.114 | calculadora |
| T | 172.31.27.217 | texto |
| K | 172.31.30.201 | cliente |

Saída do cliente em K:
```
lookup('calculadora') -> 172.31.31.114:50051
lookup('texto') -> 172.31.27.217:50052
Calculadora:
  7 + 5 = 12.0
  7 - 5 = 2.0
  7 * 5 = 35.0
  7 / 2 = 3.5
  7 / 0 -> ERRO INVALID_ARGUMENT: divisão por zero
Texto:
  maiusculas = SISTEMAS DISTRIBUIDOS COM GRPC
  inverter = CPRg moc sodiubirtsid sametsis
  contar = 4 palavras, 30 caracteres
Serviço de nomes (bind/rebind/unbind/lookup):
  bind 'teste' = registrado
  bind 'teste' de novo -> ERRO ALREADY_EXISTS: 'teste' já registrado (use rebind)
  rebind 'teste' = atualizado
  lookup 'teste' = 5.6.7.8:2
  unbind 'teste' = removido
  lookup 'teste' -> ERRO NOT_FOUND: 'teste' não encontrado
  rebind inexistente -> ERRO NOT_FOUND: 'nada' não encontrado (use bind)
```

Log do serviço de nomes em N (mostra os binds dos servidores, os lookups do cliente e o unbind automático ao encerrar):
```
[bind]   calculadora -> 172.31.31.114:50051
[bind]   texto -> 172.31.27.217:50052
[lookup] calculadora -> 172.31.31.114:50051
[lookup] texto -> 172.31.27.217:50052
...
[unbind] calculadora      <- após Ctrl+C no servidor
[unbind] texto
```
As instâncias foram encerradas após o teste.

## Limitações

Tabela de nomes só em memória (reiniciar o serviço de nomes perde os registros) e canais sem TLS. Se um servidor cair sem fazer `unbind`, o registro fica obsoleto; ao reiniciar ele faz `rebind` automaticamente.
