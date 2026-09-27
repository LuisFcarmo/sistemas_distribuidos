# Sistemas Distribuídos

Repositório de atividades práticas e trabalhos da disciplina de **Sistemas Distribuídos** (UFG).

---

## 📌 Guia de Execução Rápida para o Professor

### 1. Tarefa ZeroC Ice: Novos Métodos Remotos (RPC)
> **Base Teórica:** Capítulo 3 (Exemplo 3.21 de Maarten van Steen)  
> **Repositório de Referência:** [`https://github.com/professorfabio/ice-demo`](https://github.com/professorfabio/ice-demo)

Para executar a demonstração completa da tarefa de ZeroC Ice em **um único comando** (o script sobe o servidor Ice em segundo plano, conecta o cliente, testa o método original e todos os novos métodos remotos e finaliza com segurança):

```bash
python3 executar_ice.py
```

---

### 2. Tarefa de Sockets TCP Multithread e Experimento de Desempenho
> **Base Teórica:** Capítulo 3 (Processos e Threads em Sistemas Distribuídos — Modelos de Concorrência e Dispatcher/Worker)  
> **Relato Formatado:** [`relato_experimento.md`](file:///home/luis/Desktop/sistemas_distribuidos/relato_experimento.md) | Texto para Moodle: [`RELATO_SUBMISSAO.txt`](file:///home/luis/Desktop/sistemas_distribuidos/RELATO_SUBMISSAO.txt)

Para executar o **experimento completo e comparativo de desempenho** em **um único comando** (inicia servidores, testa 500 requisições para os 3 cenários + multi-servidor e gera o relatório):

```bash
python3 executar_experimento.py
```

---

### 3. Tarefa ASR 04: Calculadora Remota Cliente-Servidor (Sockets TCP)
> **Base Teórica:** Capítulo 2, Slide 5 (Comunicação Cliente-Servidor via Sockets TCP)

Para executar a demonstração automatizada da calculadora remota da Tarefa 04:

```bash
python3 executar_sockets.py
```

---

### 4. Exemplos do Capítulo 3 (Processos e Threads)
> **Base Teórica:** Exemplos 3.3 e 3.4 (`mp.py` vs `mpthread.py`)

Para executar os exemplos comparativos de Processos vs Threads:

```bash
python3 executar_tudo.py
```

---

## 🚀 Detalhamento das Tarefas

### Tarefa: ZeroC Ice Demo (Invocação Remota de Objetos com Novos Métodos)
**Pasta:** [`ice-demo/`](file:///home/luis/Desktop/sistemas_distribuidos/ice-demo)

#### O Que Foi Feito:
Evolução do exemplo base da disciplina (`https://github.com/professorfabio/ice-demo` / Exemplo 3.21 de Maarten van Steen).
Foram adicionados à interface Slice (`Printer.ice`) e implementados no servidor e cliente os seguintes métodos:
1. **`string printString(string s);`** — Método original (retorna string com asterisco `*`).
2. **`string toUpper(string s);`** — *Novo Método 1*: Conversão e tratamento de strings em letras maiúsculas remotamente no servidor.
3. **`int add(int a, int b);`** — *Novo Método 2*: Processamento aritmético de soma executado remotamente com retorno tipado inteiro.
4. **`string repeatString(string s, int times);`** — *Novo Método 3*: Formatação e concatenação repetida de texto no servidor.
5. **`void shutdown();`** — *Novo Método 4*: Encerramento gracioso do servidor remotamente via RPC.

---

### Tarefa: Cliente-Servidor Multithread com Sockets TCP
**Pasta:** [`Cliente-Servidor_multithread/`](file:///home/luis/Desktop/sistemas_distribuidos/Cliente-Servidor_multithread)

#### Requisitos Atendidos:
1. **O servidor deve disparar uma nova thread para cada requisição recebida:**
   - Implementado em [`server_mt.py`](file:///home/luis/Desktop/sistemas_distribuidos/Cliente-Servidor_multithread/server_mt.py).
2. **Cada requisição do cliente deve ser enviada por uma nova thread (múltiplas requisições em paralelo):**
   - Implementado em [`client_mt.py`](file:///home/luis/Desktop/sistemas_distribuidos/Cliente-Servidor_multithread/client_mt.py), incluindo suporte a múltiplos servidores concorrentes.
3. **Automatizar a geração de requisições no cliente:**
   - Implementado em [`gerador_requisicoes.py`](file:///home/luis/Desktop/sistemas_distribuidos/Cliente-Servidor_multithread/gerador_requisicoes.py) com controle determinístico de semente (`seed`).
4. **Experimento de Medição e Comparação de Desempenho:**
   - Orquestrado por [`experimento.py`](file:///home/luis/Desktop/sistemas_distribuidos/Cliente-Servidor_multithread/experimento.py). O modelo multithread obteve um ganho de **~13x a 14x de speedup** sob carga realista com I/O em relação ao baseline sequencial.

---

### Tarefa ASR 04: Calculadora Remota Cliente-Servidor (Cap. 2, Slide 5)
**Pasta:** [`Cliente-Servidor_com_sockets/`](file:///home/luis/Desktop/sistemas_distribuidos/Cliente-Servidor_com_sockets)  
- Implementação da calculadora com processamento matemático (`ADD`, `SUB`, `MUL`, `DIV`, `POW`, `SQRT`), tratamento de exceções e suporte a lotes separados por ponto e vírgula.

---

### Tarefa Ch03: Exemplos do Capítulo 3 (Processos e Threads)
**Pasta:** [`Ch03(1)/`](file:///home/luis/Desktop/sistemas_distribuidos/Ch03(1))  
**Relatório:** [`relatorio_comparativo.md`](file:///home/luis/Desktop/sistemas_distribuidos/relatorio_comparativo.md)  
- Análise comparativa entre os modelos de processos independentes (`mp.py`) e threads compartilhando memória dentro de processos (`mpthread.py`).

---

## 📁 Estrutura Completa do Repositório

```text
sistemas_distribuidos/
├── ice-demo/                          # TAREFA ZEROC ICE (MÉTODOS REMOTOS RPC)
│   ├── Printer.ice                    # Contrato Slice com método original + novos métodos
│   ├── Printer_ice.py                 # Código gerado pelo compilador slice2py
│   ├── Demo/                          # Módulo gerado do Ice
│   ├── server.py                      # Servidor com implementação dos novos métodos
│   ├── client.py                      # Cliente que invoca todos os métodos remotos
│   ├── server2.py / client2.py        # Demo de múltiplos objetos registrados
│   ├── executar_teste.py              # Testador autônomo da demonstração Ice
│   └── README.md                      # Documentação detalhada da pasta
├── Cliente-Servidor_multithread/       # TAREFA SOCKETS TCP MULTITHREAD
│   ├── constCS.py                     # Constantes de rede
│   ├── calculator.py                  # Motor da calculadora com delay simulado
│   ├── gerador_requisicoes.py         # Gerador automatizado de requisições aleatórias
│   ├── server_mt.py / server_st.py    # Servidores MT e ST
│   ├── client_mt.py / client_st.py    # Clientes MT e ST
│   ├── experimento.py                 # Orquestrador do benchmark e relatórios
│   ├── resultados_experimento.json    # Dados brutos das medições
│   ├── relato_experimento.md          # Relatório do experimento em Markdown
│   ├── RELATO_SUBMISSAO.txt           # Texto do relato pronto para o Moodle
│   └── README.md                      # Documentação da pasta
├── Cliente-Servidor_com_sockets/       # Tarefa ASR 04 (Sockets TCP - Baseline Original)
│   ├── constCS.py                     # Constantes da Tarefa 04
│   ├── server.py                      # Servidor da Tarefa 04
│   ├── client.py                      # Cliente da Tarefa 04
│   ├── executar_teste.py              # Testador autônomo da Tarefa 04
│   └── README.md                      # Documentação da Tarefa 04
├── Ch03(1)/                           # Exemplos do livro (Capítulo 3)
│   └── Ch03/                          # Códigos 03-03, 03-04 e 03-21 sincronizado
├── executar_ice.py                    # Launcher na raiz para testar a tarefa ZeroC Ice
├── executar_experimento.py            # Launcher na raiz para rodar o benchmark multithread
├── executar_sockets.py                # Launcher na raiz para testar a Tarefa 04
├── executar_tudo.py                   # Launcher na raiz para rodar os exemplos do Cap. 3
├── relato_experimento.md              # Relatório completo do experimento
├── RELATO_SUBMISSAO.txt               # Texto pronto para colar na submissão
├── relatorio_comparativo.md           # Relatório comparativo do Cap. 3
├── slides.03.pdf                      # Slides da disciplina (Capítulo 3)
└── README.md                          # Guia principal do repositório
```
