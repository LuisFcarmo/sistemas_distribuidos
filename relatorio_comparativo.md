# Relatório de Comparação: Exemplos 3.3 e 3.4 (Capítulo 3)
**Disciplina:** Sistemas Distribuídos

---

## 1. Saídas Reais da Execução

### Exemplo 3.3 (`03-03/mp.py`) — Processos
```text
10:27 eve is going to sleep for 1 seconds
10:28 eve has woken up
10:27 bob is going to sleep for 2 seconds
10:29 bob has woken up
```

### Exemplo 3.4 (`03-04/mpthread.py`) — Threads & Processos
```text
eve sees shared x being 40
10:29 eve 0 is going to sleep for 13 seconds
10:29 eve 1 is going to sleep for 3 seconds
10:29 eve 2 is going to sleep for 7 seconds
10:32 eve 1 has woken up, seeing shared x being 41
10:36 eve 2 has woken up, seeing shared x being 42
10:42 eve 0 has woken up, seeing shared x being 43
eve sees shared x being 43
bob sees shared x being 40
10:29 bob 0 is going to sleep for 5 seconds
10:29 bob 1 is going to sleep for 16 seconds
10:29 bob 2 is going to sleep for 2 seconds
10:31 bob 2 has woken up, seeing shared x being 41
10:34 bob 0 has woken up, seeing shared x being 42
10:45 bob 1 has woken up, seeing shared x being 43
bob sees shared x being 43
```

---

## 2. Análise Comparativa e Respostas da Tarefa

### A) Exemplo 3.3 (Processos)
- **Comportamento:** Cria dois processos independentes (`eve` e `bob`) através de `multiprocessing.Process`.
- **Memória e Isolamento:** Cada processo roda com seu próprio espaço de endereçamento isolado no Sistema Operacional. Eles executam e dormem de forma paralela/concorrente sem compartilhar nenhuma variável de memória.

### B) Exemplo 3.4 (Threads dentro de Processos)
- **Comportamento:** Cria dois processos (`eve` e `bob`). Cada processo instancia **3 threads** (`Thread`).
- **Isolamento entre Processos:** Os processos `eve` e `bob` possuem seus próprios espaços de memória independentes. Por isso, a variável `shared_x` modificada dentro do processo `eve` **não interfere** na variável `shared_x` do processo `bob`.
- **Compartilhamento entre Threads:** As threads de um mesmo processo compartilham a mesma área de memória global. Conforme cada thread acorda (`eve 0`, `eve 1`, `eve 2`), ela enxerga os incrementos feitos pelas threads anteriores do mesmo processo (`shared_x = shared_x + 1`).

---

## 3. Resumo das Diferenças

| Característica | Processos (Exemplo 3.3) | Threads no Processo (Exemplo 3.4) |
| :--- | :--- | :--- |
| **Espaço de Memória** | Isolado / Exclusivo para cada processo | Compartilhado entre threads do mesmo processo |
| **Acesso a Variáveis Globais** | Cópias independentes | Modificação direta da mesma variável |
| **Custo de Troca de Contexto** | Mais alto (gerenciado via Kernel / MMU) | Mais leve (mesmo mapa de memória) |
| **Comunicação** | Requer IPC (Sockets, Pipes, Queues) | Direta via memória compartilhada |

---
*Relatório gerado automaticamente.*
