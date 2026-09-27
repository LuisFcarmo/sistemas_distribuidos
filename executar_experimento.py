#!/usr/bin/env python3
"""
Launcher da Tarefa de Sockets Multithread na Raiz do Repositório
Disciplina: Sistemas Distribuídos (UFG)
Base Teórica: Capítulo 3 (Processos e Threads em Sistemas Distribuídos)

Executa o experimento completo de comparação de desempenho entre:
  1. Cliente MT + Servidor MT (Multithread Total)
  2. Cliente ST + Servidor ST (Single-Threaded Baseline)
  3. Cliente ST + Servidor MT (Versão Original Mista)
  4. Cliente MT + 2 Servidores MT (Multi-Servidor Concorrente)

Gera automaticamente:
  - Tabela comparativa no terminal
  - relato_experimento.md (Relatório técnico completo)
  - RELATO_SUBMISSAO.txt (Texto formatado para envio no Moodle)
  - resultados_experimento.json (Dados brutos para auditoria)
"""

import os
import sys
import subprocess

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, "Cliente-Servidor_multithread", "experimento.py")
    
    # Passa quaisquer argumentos adicionais (ex: --requests 1000)
    args = [sys.executable, script_path] + sys.argv[1:]
    result = subprocess.run(args)
    sys.exit(result.returncode)
