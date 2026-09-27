#!/usr/bin/env python3
import subprocess
import socket
import time
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ice_lib = os.path.expanduser("~/.local/ice_install/usr/lib/python3/dist-packages")
ice_bin = os.path.expanduser("~/.local/ice_install/usr/bin")
ice_lib_native = os.path.expanduser("~/.local/ice_install/usr/lib/x86_64-linux-gnu")

ENV = os.environ.copy()
if os.path.exists(ice_lib):
    ENV["PYTHONPATH"] = f"{ice_lib}:{BASE_DIR}:{ENV.get('PYTHONPATH', '')}"
if os.path.exists(ice_lib_native):
    ENV["LD_LIBRARY_PATH"] = f"{ice_lib_native}:{ENV.get('LD_LIBRARY_PATH', '')}"
if os.path.exists(ice_bin):
    ENV["PATH"] = f"{ice_bin}:{ENV.get('PATH', '')}"

def wait_for_port(host="127.0.0.1", port=11000, timeout=5.0):
    start = time.perf_counter()
    while time.perf_counter() - start < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            s.connect((host, port))
            s.close()
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            time.sleep(0.05)
    return False

def main():
    port = 11000
    server_script = os.path.join(BASE_DIR, "server.py")
    client_script = os.path.join(BASE_DIR, "client.py")

    print(f"Iniciando servidor Ice na porta {port}...")
    server_proc = subprocess.Popen([sys.executable, server_script, str(port)], env=ENV)

    if not wait_for_port("127.0.0.1", port, timeout=5.0):
        print("Erro: Servidor nao respondeu na porta", port)
        server_proc.kill()
        sys.exit(1)

    try:
        print("Executando cliente...")
        client_run = subprocess.run(
            [sys.executable, client_script, "127.0.0.1", str(port)],
            env=ENV,
            capture_output=True,
            text=True
        )
        print(client_run.stdout)
        if client_run.stderr:
            print("Avisos:", client_run.stderr)
    finally:
        try:
            server_proc.terminate()
            server_proc.wait(timeout=2.0)
        except Exception:
            server_proc.kill()
        print("Servidor encerrado.")

if __name__ == "__main__":
    main()
