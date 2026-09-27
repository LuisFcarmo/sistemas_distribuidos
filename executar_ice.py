#!/usr/bin/env python3
import os
import sys
import subprocess

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, "ice-demo", "executar_teste.py")
    result = subprocess.run([sys.executable, script_path] + sys.argv[1:])
    sys.exit(result.returncode)
