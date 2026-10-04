# Sistemas Distribuídos

Trabalhos e atividades práticas da disciplina de Sistemas Distribuídos (UFG).

---

## Execução Rápida

### 1. ZeroC Ice (RPC com Métodos Remotos)
Demonstração do middleware ZeroC Ice com o servant `Printer` e novos métodos remotos (`toUpper`, `add`, `repeatString`, `shutdown`):

```bash
python3 executar_ice.py
```

### 2. Sockets TCP Multithread e Experimento de Desempenho
Benchmark comparando arquiteturas multithread e single-threaded (MT+MT, ST+ST, ST+MT e multi-servidor):

```bash
python3 executar_experimento.py
```

### 2.1. ZeroC Ice Multiplataforma (Python ⇄ Java)
Cliente Java → servidor Python e cliente Python → servidor Java, com o mesmo contrato Slice:

```bash
python3 ice-multiplataforma/executar_cenarios.py
```

### 3. Calculadora Remota via Sockets TCP
Calculadora remota com operações matemáticas e suporte a lotes:

```bash
python3 executar_sockets.py
```

### 4. Processos e Threads (Capítulo 3)
Comparação entre processos independentes e threads compartilhando memória:

```bash
python3 executar_tudo.py
```

---

## Organização dos Projetos

### `ice-demo/` — ZeroC Ice RPC
Implementação da interface Slice `Printer.ice` contendo métodos para manipulação de strings, operações aritméticas e controle de ciclo de vida do servidor:
- `printString(s)`: eco da mensagem com asterisco
- `toUpper(s)`: conversão para maiúsculas no servidor
- `add(a, b)`: soma de inteiros remota
- `repeatString(s, n)`: repetição de texto
- `shutdown()`: encerramento do servidor

### `ice-multiplataforma/` — ZeroC Ice entre Python e Java
Dois cenários interoperáveis (cliente Java/servidor Python e cliente Python/servidor Java) sobre o `Printer.ice`, com discussão middleware × transporte em `RELATO_SUBMISSAO.txt`.

### `Cliente-Servidor_multithread/` — Sockets TCP Multithread
Estudo de concorrência com threads em sockets TCP:
- `server_mt.py`: servidor que cria uma thread para cada conexão recebida
- `client_mt.py`: cliente que envia requisições em threads paralelas (suporte a múltiplos servidores)
- `gerador_requisicoes.py`: gerador automatizado de operações aleatórias com seed fixa
- `experimento.py`: suite de testes que mede tempo de resposta, vazão e latência
- `relato_experimento.md`: relatório com tabelas comparativas e análise dos resultados

### `Cliente-Servidor_com_sockets/` — Calculadora Sockets TCP
Calculadora remota cliente-servidor iterativa com suporte a operações aritméticas (`ADD`, `SUB`, `MUL`, `DIV`, `POW`, `SQRT`) e validações de erro.

### `Ch03(1)/` — Exemplos de Processos e Threads
Exemplos 3.3 e 3.4 do livro de Maarten van Steen, comparando o modelo de memória de processos (`mp.py`) e threads (`mpthread.py`).

---

## Estrutura de Arquivos

```text
sistemas_distribuidos/
├── ice-demo/                          # Exemplo ZeroC Ice com novos métodos
│   ├── Printer.ice                    # Interface Slice
│   ├── Printer_ice.py                 # Código gerado via slice2py
│   ├── Demo/                          # Pacote gerado pelo compilador Slice
│   ├── server.py                      # Servidor Ice
│   ├── client.py                      # Cliente Ice
│   ├── server2.py / client2.py        # Exemplo com múltiplos objetos
│   ├── executar_teste.py              # Teste automatizado
│   └── README.md
├── Cliente-Servidor_multithread/       # Sockets TCP multithread
│   ├── constCS.py                     # Constantes de rede
│   ├── calculator.py                  # Lógica da calculadora
│   ├── gerador_requisicoes.py         # Gerador de requisições
│   ├── server_mt.py / server_st.py    # Servidores multithread e iterativo
│   ├── client_mt.py / client_st.py    # Clientes multithread e sequencial
│   ├── experimento.py                 # Script de benchmark
│   ├── resultados_experimento.json    # Dados brutos das medições
│   ├── relato_experimento.md          # Relatório em Markdown
│   ├── RELATO_SUBMISSAO.txt           # Texto do relatório para submissão
│   └── README.md
├── Cliente-Servidor_com_sockets/       # Calculadora sockets TCP (versão base)
│   ├── constCS.py
│   ├── server.py
│   ├── client.py
│   ├── executar_teste.py
│   └── README.md
├── Ch03(1)/                           # Códigos do livro (Capítulo 3)
│   └── Ch03/
├── executar_ice.py                    # Launcher para o teste do ZeroC Ice
├── executar_experimento.py            # Launcher para o experimento de sockets MT
├── executar_sockets.py                # Launcher para a calculadora de sockets
├── executar_tudo.py                   # Launcher para os exemplos do Cap. 3
├── relato_experimento.md              # Relatório comparativo de desempenho
├── RELATO_SUBMISSAO.txt               # Texto para envio
├── relatorio_comparativo.md           # Relatório do Cap. 3
├── slides.03.pdf
└── README.md
```
