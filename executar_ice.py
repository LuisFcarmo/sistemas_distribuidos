#!/usr/bin/env python3
"""
Launcher da Tarefa ZeroC Ice na Raiz do Repositório
Disciplina: Sistemas Distribuídos (UFG)
"""
import os
import sys
import subprocess

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, "ice-demo", "executar_teste.py")
    result = subprocess.run([sys.executable, script_path] + sys.argv[1:])
    sys.exit(result.returncode)
