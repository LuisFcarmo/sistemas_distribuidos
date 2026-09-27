# Cliente-Servidor Multithread com Sockets TCP

**Disciplina:** Sistemas Distribuídos — UFG  
**Base Teórica:** Capítulo 3 (Processos e Threads em Sistemas Distribuídos — Modelos de Concorrência e Dispatcher/Worker)  
**Evolução de:** Tarefa ASR 04 (Calculadora Remota Cliente-Servidor via Sockets TCP)

---

## 1. Componentes Implementados

| Componente | Descrição | Arquivo |
| :--- | :--- | :--- |
| **Servidor multithread** | O servidor aceita conexões no loop principal e dispara uma nova thread para atender cada conexão. | `server_mt.py` |
| **Cliente multithread** | Dispara uma thread por requisição em paralelo. Suporta múltiplos servidores. | `client_mt.py` |
| **Gerador de requisições** | Gera requisições aleatórias (`ADD`, `SUB`, `MUL`, `DIV`, `POW`, `SQRT`) com controle de semente (`seed`). | `gerador_requisicoes.py` |
| **Experimento de desempenho** | Executa baterias de testes comparando os cenários MT e ST, calculando métricas e relatórios. | `experimento.py` |

---

## 2. Estrutura dos Arquivos

```text
Cliente-Servidor_multithread/
├── constCS.py                 # Constantes de rede (IP, portas 5678/5679, backlog, buffers)
├── calculator.py              # Motor matemático da calculadora (operações, validações e delay simulado)
├── gerador_requisicoes.py     # Gerador de requisições aleatórias reproduzíveis
├── server_mt.py               # Servidor multithread (thread por requisição)
├── server_st.py               # Servidor single-threaded iterativo (baseline da Tarefa 04)
├── client_mt.py               # Cliente multithread (thread por requisição e multi-servidor)
├── client_st.py               # Cliente single-threaded sequencial (baseline da Tarefa 04)
├── experimento.py             # Orquestrador automatizado do benchmark comparativo
├── resultados_experimento.json# Dados brutos salvos da última bateria de testes
├── relato_experimento.md      # Relatório técnico completo formatado em Markdown
├── RELATO_SUBMISSAO.txt       # Texto formatado pronto para envio no Moodle/Classroom
└── README.md                  # Este guia de documentação
```

---

## 3. Guia de Execução

### Opção 1: Execução Automática do Experimento de Desempenho (Recomendado)

Na raiz do repositório ou nesta pasta, execute:
```bash
python3 experimento.py --requests 500
```
*Ou a partir da raiz do repositório:*
```bash
python3 executar_experimento.py
```

O script cuidará de:
1. Subir os servidores em segundo plano de forma isolada.
2. Disparar a carga de testes para os 4 cenários (MT+MT, ST+ST, ST+MT, MT+2xMT).
3. Exibir a tabela formatada no terminal.
4. Salvar os relatórios `relato_experimento.md` e `RELATO_SUBMISSAO.txt`.

---

### Opção 2: Execução Manual / Interativa

#### 1. Iniciar o Servidor Multithread:
```bash
python3 server_mt.py --port 5678
```

#### 2. Disparar o Cliente Multithread:
- **Disparando 100 requisições paralelas:**
  ```bash
  python3 client_mt.py --requests 100
  ```

- **Disparando para múltiplos servidores em paralelo:**
  Em outro terminal, abra um segundo servidor:
  ```bash
  python3 server_mt.py --port 5679
  ```
  E execute o cliente distribuindo as requisições:
  ```bash
  python3 client_mt.py --requests 200 --servers 127.0.0.1:5678,127.0.0.1:5679
  ```
