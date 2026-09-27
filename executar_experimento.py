#!/usr/bin/env python3
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
