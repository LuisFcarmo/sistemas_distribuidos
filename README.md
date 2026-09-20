# Sistemas Distribuídos

Repositório de atividades práticas e trabalhos da disciplina de **Sistemas Distribuídos**.

---

## 📌 Guia de Execução Rápida para o Professor

### 1. Tarefa de Sockets TCP (Calculadora Remota Cliente-Servidor)
> **Base Teórica:** Capítulo 2, Slide 5 (Comunicação Cliente-Servidor via Sockets TCP)

Para executar toda a demonstração automatizada da tarefa de sockets em **um único comando** (o script sobe o servidor em segundo plano, conecta o cliente, testa todas as funcionalidades e desliga o servidor de forma limpa):

```bash
python3 executar_sockets.py
```

---

## 🚀 Detalhamento das Tarefas

### Tarefa 1: Evolução do Exemplo Cliente-Servidor com Sockets (Cap. 2, Slide 5)
**Pasta:** [`Cliente-Servidor_com_sockets/`](file:///home/luis/Desktop/sistemas_distribuidos/Cliente-Servidor_com_sockets)

#### Requisitos da Tarefa e Como Foram Atendidos:
1. **Acrescentar processamento da requisição no servidor:**
   - O exemplo original do slide apenas devolvia o texto com um asterisco (`*`).
   - Foi implementado um serviço de **Calculadora Remota**: o servidor recebe a operação em formato textual, faz o parsing, valida os parâmetros, executa os cálculos aritméticos/matemáticos (`ADD`, `SUB`, `MUL`, `DIV`, `POW`, `SQRT`) e trata erros defensivamente (divisão por zero, raízes negativas, tipos inválidos).

2. **Permitir que o cliente chame mais de uma funcionalidade diferente no servidor a cada requisição:**
   - O cliente mantém uma conexão persistente e permite ao usuário alternar entre qualquer uma das operações suportadas (`ADD`, `SUB`, `MUL`, `DIV`, `POW`, `SQRT`, `HELP`, etc.).
   - Além disso, foi adicionado suporte a **lotes de operações na mesma requisição** separadas por ponto e vírgula (exemplo: `ADD 100 250 ; MUL 7 8 ; SQRT 81 ; POW 3 4`), atendendo a ambas as interpretações do requisito.

#### Modos de Execução da Tarefa 1:
- **Modo Automático (1 comando):**
  ```bash
  python3 executar_sockets.py
  ```
  *(ou dentro da pasta: `cd Cliente-Servidor_com_sockets && python3 executar_teste.py`)*

- **Modo Interativo (Manual em 2 terminais):**
  - Terminal 1 (Servidor):
    ```bash
    cd Cliente-Servidor_com_sockets
    python3 server.py
    ```
  - Terminal 2 (Cliente):
    ```bash
    cd Cliente-Servidor_com_sockets
    python3 client.py
    ```

---

### Tarefa 2: Exemplos do Capítulo 3 (Processos e Threads)
**Pasta:** [`Ch03(1)/`](file:///home/luis/Desktop/sistemas_distribuidos/Ch03(1))  
**Relatório:** [`relatorio_comparativo.md`](file:///home/luis/Desktop/sistemas_distribuidos/relatorio_comparativo.md)

Para executar os exemplos 3.3 e 3.4 e gerar o relatório comparativo de saídas reais:
```bash
python3 executar_tudo.py
```

---

## 📁 Estrutura do Repositório

```text
sistemas_distribuidos/
├── Cliente-Servidor_com_sockets/       # Tarefa de Sockets TCP (Capítulo 2)
│   ├── constCS.py                     # Constantes de rede (HOST, PORT)
│   ├── server.py                      # Servidor com processamento matemático
│   ├── client.py                      # Cliente interativo e modo demo
│   ├── executar_teste.py              # Script autônomo de testes para o professor
│   └── README.md                      # Documentação detalhada da calculadora
├── Ch03(1)/                           # Códigos e exemplos do Capítulo 3
│   └── Ch03/                          # Exemplos 03-03 (mp.py), 03-04 (mpthread.py), etc.
├── executar_sockets.py                # Launcher na raiz para testar a tarefa de sockets
├── executar_tudo.py                   # Script para execução dos exemplos do Cap. 3
├── relatorio_comparativo.md           # Relatório comparativo (Processos vs Threads)
├── slides.03.pdf                      # Slides de apoio
└── README.md                          # Guia principal do repositório
```
