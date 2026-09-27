#!/usr/bin/env python3
import os
import sys
import subprocess

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, "Cliente-Servidor_com_sockets", "executar_teste.py")
    result = subprocess.run([sys.executable, script_path])
    sys.exit(result.returncode)
