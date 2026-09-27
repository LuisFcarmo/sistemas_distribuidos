# Sistemas Distribuídos

Repositório de atividades práticas e trabalhos da disciplina de **Sistemas Distribuídos** (UFG).

---

## 📌 Guia de Execução Rápida para o Professor

### 1. Tarefa Atual: Sockets TCP Multithread e Experimento de Desempenho
> **Base Teórica:** Capítulo 3 (Processos e Threads em Sistemas Distribuídos — Modelos de Concorrência e Dispatcher/Worker)  
> **Relato Formatado:** [`relato_experimento.md`](file:///home/luis/Desktop/sistemas_distribuidos/relato_experimento.md) | Texto para Moodle: [`RELATO_SUBMISSAO.txt`](file:///home/luis/Desktop/sistemas_distribuidos/RELATO_SUBMISSAO.txt)

Para executar o **experimento completo e comparativo de desempenho** em **um único comando** (o script inicia os servidores em segundo plano, executa os testes automatizados para os 3 cenários + multi-servidor, calcula métricas estatísticas e gera os relatórios):

```bash
python3 executar_experimento.py
```
*(Para personalizar a quantidade de requisições: `python3 executar_experimento.py --requests 1000`)*

---

### 2. Tarefa ASR 04: Calculadora Remota Cliente-Servidor (Sockets TCP)
> **Base Teórica:** Capítulo 2, Slide 5 (Comunicação Cliente-Servidor via Sockets TCP)

Para executar a demonstração automatizada da calculadora remota da Tarefa 04:

```bash
python3 executar_sockets.py
```

---

### 3. Exemplos do Capítulo 3 (Processos e Threads)
> **Base Teórica:** Exemplos 3.3 e 3.4 (`mp.py` vs `mpthread.py`)

Para executar os exemplos comparativos de Processos vs Threads:

```bash
python3 executar_tudo.py
```

---

## 🚀 Detalhamento das Tarefas

### Tarefa Atual: Cliente-Servidor Multithread com Sockets TCP
**Pasta:** [`Cliente-Servidor_multithread/`](file:///home/luis/Desktop/sistemas_distribuidos/Cliente-Servidor_multithread)

#### Requisitos da Tarefa e Como Foram Atendidos:
1. **O servidor deve disparar uma nova thread para cada requisição recebida:**
   - Implementado em [`server_mt.py`](file:///home/luis/Desktop/sistemas_distribuidos/Cliente-Servidor_multithread/server_mt.py). O loop principal aceita a conexão TCP e dispara imediatamente uma thread dedicada (`threading.Thread`) para processar a requisição e devolver a resposta ao cliente, mantendo o servidor livre para novas requisições concorrentes.
2. **Cada requisição do cliente deve ser enviada por uma nova thread (múltiplas requisições em paralelo):**
   - Implementado em [`client_mt.py`](file:///home/luis/Desktop/sistemas_distribuidos/Cliente-Servidor_multithread/client_mt.py). Cada requisição é disparada por uma thread independente, permitindo concorrência massiva. O cliente suporta ainda a distribuição balanceada de requisições para múltiplos servidores simultâneos (`--servers 127.0.0.1:5678,127.0.0.1:5679`).
3. **Automatizar a geração de requisições no cliente:**
   - Implementado em [`gerador_requisicoes.py`](file:///home/luis/Desktop/sistemas_distribuidos/Cliente-Servidor_multithread/gerador_requisicoes.py). Gera requisições pseudo-aleatórias cobrindo `ADD`, `SUB`, `MUL`, `DIV`, `POW`, `SQRT` com semente determinística para reprodutibilidade científica nos testes comparativos.
4. **Experimento de Medição e Comparação de Desempenho:**
   - O orquestrador [`experimento.py`](file:///home/luis/Desktop/sistemas_distribuidos/Cliente-Servidor_multithread/experimento.py) executa baterias com 500 requisições comparando:
     * **Cenário 1 (MT + MT):** Cliente Multithread + Servidor Multithread.
     * **Cenário 2 (ST + ST):** Cliente Single-threaded + Servidor Single-threaded (baseline da tarefa anterior).
     * **Cenário 3 (ST + MT):** Cliente Single-threaded + Servidor Multithread (versão original mista).
     * **Cenário 4 (MT + 2x MT):** Cliente Multithread distribuindo requisições entre 2 Servidores Multithread.
   - Avaliado tanto sob carga realista com processamento/I/O (ganho de **~13x a 14x de speedup**) quanto sob carga pura de rede local.

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
├── Cliente-Servidor_multithread/       # TAREFA ATUAL: Sockets TCP Multithread
│   ├── constCS.py                     # Constantes de rede (HOST, PORT, PORT_ALT, BACKLOG)
│   ├── calculator.py                  # Motor da calculadora com suporte a delay simulado
│   ├── gerador_requisicoes.py         # Gerador automatizado de requisições aleatórias
│   ├── server_mt.py                   # Servidor multithread (thread por requisição)
│   ├── server_st.py                   # Servidor single-threaded (baseline iterativo)
│   ├── client_mt.py                   # Cliente multithread (thread por requisição e multi-servidor)
│   ├── client_st.py                   # Cliente single-threaded (sequencial)
│   ├── experimento.py                 # Orquestrador do benchmark e gerador de relatórios
│   ├── resultados_experimento.json    # Dados brutos salvos da última execução
│   ├── relato_experimento.md          # Relatório técnico do experimento em Markdown
│   ├── RELATO_SUBMISSAO.txt           # Texto do relato pronto para o campo do Moodle
│   └── README.md                      # Documentação detalhada da pasta
├── Cliente-Servidor_com_sockets/       # Tarefa ASR 04 (Sockets TCP - Baseline Original)
│   ├── constCS.py                     # Constantes da Tarefa 04
│   ├── server.py                      # Servidor da Tarefa 04
│   ├── client.py                      # Cliente da Tarefa 04
│   ├── executar_teste.py              # Testador autônomo da Tarefa 04
│   └── README.md                      # Documentação da Tarefa 04
├── Ch03(1)/                           # Tarefa Ch03: Exemplos de Processos e Threads
│   └── Ch03/                          # Códigos do livro (03-03, 03-04, 03-21)
├── executar_experimento.py            # Launcher na raiz para rodar o benchmark multithread
├── executar_sockets.py                # Launcher na raiz para testar a Tarefa 04
├── executar_tudo.py                   # Launcher na raiz para rodar os exemplos do Cap. 3
├── relato_experimento.md              # Relatório completo do experimento
├── RELATO_SUBMISSAO.txt               # Texto pronto para colar na submissão
├── relatorio_comparativo.md           # Relatório comparativo do Cap. 3
├── slides.03.pdf                      # Slides da disciplina (Capítulo 3)
└── README.md                          # Guia principal do repositório
```
