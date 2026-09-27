#!/usr/bin/env python3
"""
Script de Demonstração e Teste Automatizado da Tarefa ZeroC Ice
Disciplina: Sistemas Distribuídos - UFG
Inicia o servidor em segundo plano, executa o cliente com todos os métodos novos e encerra de forma limpa.
"""

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

    print("\n" + "="*70)
    print("   SISTEMAS DISTRIBUÍDOS - UFG")
    print("   DEMONSTRAÇÃO AUTOMATIZADA: ZEROC ICE RPC COM NOVOS MÉTODOS")
    print("   Base: Capítulo 03 - Exemplo 3.21 e https://github.com/professorfabio/ice-demo")
    print("="*70)
    print("  [✓] Método Original: printString(s)")
    print("  [✓] Novo Método 1:   toUpper(s)        -> Conversão de texto remota")
    print("  [✓] Novo Método 2:   add(a, b)         -> Processamento aritmético remoto")
    print("  [✓] Novo Método 3:   repeatString(s, n)-> Formatação/repetição remota")
    print("="*70 + "\n")

    print("[1/3] Iniciando o servidor Ice (server.py) em segundo plano...")
    server_proc = subprocess.Popen([sys.executable, server_script, str(port)], env=ENV)

    if not wait_for_port("127.0.0.1", port, timeout=5.0):
        print("[-] Erro: O servidor Ice não respondeu na porta", port)
        server_proc.kill()
        sys.exit(1)

    print(f"[+] Servidor Ice pronto e aceitando invocações na porta {port}!\n")

    try:
        print("[2/3] Executando o cliente Ice (client.py) invocando todos os métodos...\n")
        client_run = subprocess.run(
            [sys.executable, client_script, "127.0.0.1", str(port)],
            env=ENV,
            capture_output=True,
            text=True
        )
        print(client_run.stdout)
        if client_run.stderr:
            print("[!] Avisos do cliente:", client_run.stderr)
    finally:
        print("[3/3] Finalizando o servidor...")
        try:
            server_proc.terminate()
            server_proc.wait(timeout=2.0)
        except Exception:
            server_proc.kill()
        print("[+] Servidor finalizado com sucesso.")

    print("\n" + "="*70)
    print(" [SUCESSO] Todos os métodos remotos foram testados com êxito!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
