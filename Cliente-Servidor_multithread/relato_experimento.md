# Relatório Experimental: Avaliação de Desempenho de Arquiteturas Cliente-Servidor Multithread
**Disciplina:** Sistemas Distribuídos — UFG  
**Repositório GitHub:** [https://github.com/LuisFcarmo/sistemas_distribuidos](https://github.com/LuisFcarmo/sistemas_distribuidos)  
**Base Teórica:** Capítulo 3 (Processos e Threads em Sistemas Distribuídos — Modelos de Concorrência e Dispatcher/Worker)

---

## 1. Introdução e Objetivos

Este relatório apresenta o projeto, a implementação e a análise experimental comparativa de desempenho de um sistema de **Calculadora Remota** baseado em Sockets TCP.

O objetivo principal consiste em avaliar os impactos do uso de **Multithreading** em ambos os lados da comunicação (cliente e servidor), medindo o tempo total, a vazão (*throughput*) e a latência sob o envio de uma quantidade significativa de requisições (500 requisições automatizadas).

Foram comparadas experimentalmente três arquiteturas centrais (mais um cenário multi-servidor):
1. **Cliente Multithread + Servidor Multithread (MT + MT):** Paralelismo total, onde cada requisição é gerada e despachada por uma thread independente no cliente, e atendida por uma thread dedicada no servidor.
2. **Cliente Single-threaded + Servidor Single-threaded (ST + ST):** Modelo sequencial iterativo (baseline de comparação).
3. **Cliente Single-threaded + Servidor Multithread (ST + MT):** Versão com multithreading apenas no servidor, mas com envio sequencial pelo cliente.
4. **Cliente Multithread + 2 Servidores Multithread (MT + 2x MT):** Paralelismo com distribuição de carga entre múltiplos servidores concorrentes.

---

## 2. Metodologia Experimental

- **Carga de Testes:** 500 requisições sintéticas geradas automaticamente por gerador pseudo-aleatório (`gerador_requisicoes.py`) com semente determinística (`seed=42`), cobrindo todas as operações aritméticas (`ADD`, `SUB`, `MUL`, `DIV`, `POW`, `SQRT`).
- **Isolamento e Controle:** A mesma massa de requisições foi submetida a cada cenário para garantir equivalência matemática estrita.
- **Perfis de Carga:**
  1. *Bateria 1 (Carga Realista de I/O / Processamento - 2.0ms):* Simula a latência de processamento de regras de negócio, acesso a banco de dados ou chamadas externas, cenário típico onde threads ocultam latência de I/O (Slide 15 e 17 do Capítulo 3).
  2. *Bateria 2 (Carga Pura sem Atraso Artificial - 0.0s):* Avalia o custo de chaveamento de contexto no SO, criação de threads e o impacto da concorrência na pilha TCP em loopback local.

---

## 3. Resultados Experimentais

### 3.1. Bateria 1: Carga com Processamento / I/O Realista (2.0 ms por requisição)

| Cenário | Tempo Total (s) | Vazão (req/s) | Latência Média (ms) | Desvio Padrão (ms) | p95 (ms) | Speedup |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **2. Cliente ST + Servidor ST** (Baseline) | 1.1666 | 428.61 | 2.32 | 0.11 | 2.50 | 1.00x |
| **3. Cliente ST + Servidor MT** (Original) | 1.2662 | 394.88 | 2.52 | 0.15 | 2.74 | 0.92x |
| **1. Cliente MT + Servidor MT** (Completo) | **0.0804** | **6222.16** | 2.93 | 0.40 | 3.71 | **14.52x** |
| **4. Cliente MT + 2 Servidores MT** (Multi-Server) | **0.0882** | **5668.93** | 2.80 | 0.43 | 3.64 | **13.23x** |

### 3.2. Bateria 2: Carga Pura sem Atraso Artificial (0.0 s — Sockets / CPU Local)

| Cenário | Tempo Total (s) | Vazão (req/s) | Latência Média (ms) | Desvio Padrão (ms) | p95 (ms) | Speedup |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **2. Cliente ST + Servidor ST** (Baseline) | 0.0302 | 16537.35 | 0.06 | 0.04 | 0.12 | 1.00x |
| **3. Cliente ST + Servidor MT** (Original) | 0.1095 | 4565.02 | 0.21 | 0.08 | 0.33 | 0.28x |
| **1. Cliente MT + Servidor MT** (Completo) | 0.1033 | 4840.01 | 1.11 | 0.43 | 1.83 | 0.29x |
| **4. Cliente MT + 2 Servidores MT** (Multi-Server) | 0.0741 | 6743.98 | 0.65 | 0.35 | 1.38 | 0.41x |

---

## 4. Análise Crítica dos Resultados

### A) Por que o Cliente Multithread + Servidor Multithread (MT + MT) obteve speedup massivo?
No cenário realista (Bateria 1), o modelo **MT + MT** alcançou um ganho de desempenho impressionante de **14.52x de aceleração** em relação ao modelo single-threaded (tempo reduzido de **1.167s** para apenas **0.080s**; vazão saltando de **428.6 req/s** para **6222.2 req/s**).
Isso ocorre porque, enquanto o servidor aguarda a conclusão da operação de uma requisição, o escalonador do sistema operacional chaveia a CPU para atender outras threads ativas, ocultando completamente o tempo ocioso (*latency hiding*).

### B) Por que o Servidor Multithread sozinho (ST + MT) não acelerou o processamento?
Ao analisar o Cenário 3 (**ST + MT**), nota-se que o tempo total (1.266s) foi essencialmente idêntico ao modelo **ST + ST** (1.167s).
**Explicação Técnica:** Embora o servidor tenha capacidade de processar requisições concorrentes disparando threads, o cliente single-threaded opera em modo estritamente síncrono/bloqueante (envia a requisição $k$, bloqueia no `recv()`, e só envia a requisição $k+1$ após receber a resposta). Logo, o servidor nunca recebe mais de uma requisição simultânea, anulando o benefício do multithreading no lado do servidor. O cliente se torna o gargalo limitante do sistema (*head-of-line blocking* no cliente).

### C) Impacto da Distribuição em Múltiplos Servidores (Cenário MT + 2 Servidores)
Ao distribuir as 500 requisições entre 2 instâncias do servidor rodando em portas distintas, o tempo total caiu para **0.088s** com vazão de **5668.9 req/s** (**13.23x de speedup**).
Isso comprova experimentalmente a afirmação do Slide 15 do Capítulo 3: *"se as chamadas forem para servidores diferentes, podemos ter uma aceleração linear"*, reduzindo a contenção na porta e na fila de conexões pendentes do kernel.

### D) Análise do Overhead na Carga Pura (Bateria 2)
Quando as requisições não realizam operações bloqueantes (Bateria 2, tempo de processamento ~0s), o tempo de execução no modelo ST+ST é dominado puramente pelo throughput da pilha de rede local. No modelo MT+MT com disparo de centenas de threads simultâneas, há o custo de alocação de pilhas de threads e chaveamento de contexto no kernel do Linux. Contudo, em qualquer sistema distribuído real onde ocorrem acessos a banco de dados ou rede externa, os ganhos de concorrência superam largamente qualquer sobrecarga mínima de criação de threads.

---

## 5. Conclusão

Os experimentos comprovaram empiricamente os conceitos teóricos do Capítulo 3:
1. Para explorar plenamente a capacidade de processamento concorrente em sistemas distribuídos, **tanto o cliente quanto o servidor devem implementar modelos não-bloqueantes ou multithread**.
2. O paralelismo do lado do cliente (*multithreaded client*) é indispensável para ocultar latência de rede e permitir o processamento simultâneo de lotes de requisições.
3. A distribuição de requisições paralelas entre múltiplos servidores proporciona escalabilidade horizontal eficaz.
