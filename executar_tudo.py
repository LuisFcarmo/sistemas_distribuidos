#!/usr/bin/env python3
import subprocess
import os
import sys

def run_script(rel_path, title):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, rel_path)
    print(f"\n{'='*60}")
    print(f" Executando: {title} ({rel_path})")
    print(f"{'='*60}")
    
    result = subprocess.run([sys.executable, full_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Erros:", result.stderr)
    return result.stdout

def main():
    print("Iniciando a execução dos exemplos do Capítulo 3...")
    out_3_3 = run_script("Ch03(1)/Ch03/03-03/mp.py", "Exemplo 3.3 - Processos (mp.py)")
    out_3_4 = run_script("Ch03(1)/Ch03/03-04/mpthread.py", "Exemplo 3.4 - Threads e Processos (mpthread.py)")

    report_content = f"""# Relatório de Comparação: Exemplos 3.3 e 3.4 (Capítulo 3)
**Disciplina:** Sistemas Distribuídos

---

## 1. Saídas Reais da Execução

### Exemplo 3.3 (`03-03/mp.py`) — Processos
```text
{out_3_3.strip()}
```

### Exemplo 3.4 (`03-04/mpthread.py`) — Threads & Processos
```text
{out_3_4.strip()}
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
"""

    report_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "relatorio_comparativo.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\n{'='*60}")
    print(f" [OK] Relatório gerado com sucesso em:")
    print(f" {report_file}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
