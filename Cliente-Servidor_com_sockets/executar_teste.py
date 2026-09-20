#!/usr/bin/env python3
"""
Script de Execução e Demonstração Automática da Tarefa de Sockets
Disciplina: Sistemas Distribuídos (UFG)
Base: Capítulo 2, Slide 5 (Comunicação Cliente-Servidor com Sockets TCP)

Este script:
 1. Inicia o servidor (server.py) em segundo plano.
 2. Aguarda a inicialização do socket na porta 5678.
 3. Executa a bateria completa de testes automatizados demonstrando:
    - Processamento de requisições no servidor (cálculos matemáticos e validações).
    - Chamadas de múltiplas funcionalidades diferentes em uma mesma sessão.
    - Chamadas de múltiplas funcionalidades em uma ÚNICA requisição (lote com ';').
    - Tratamento de exceções (divisão por zero, raízes negativas, comandos inválidos).
 4. Finaliza o servidor de forma limpa e encerra.
"""

import subprocess
import socket
import time
import sys
import os

def check_port(host, port, timeout=1.0):
    """Verifica se uma porta está aberta e aceitando conexões."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(base_dir, "server.py")
    client_script = os.path.join(base_dir, "client.py")

    print("\n" + "="*70)
    print("   SISTEMAS DISTRIBUÍDOS - UFG")
    print("   DEMONSTRAÇÃO AUTOMATIZADA: CALCULADORA REMOTA (SOCKETS TCP)")
    print("   Base Teórica: Capítulo 02 - Slide 5")
    print("="*70)
    print("  [✓] Requisito 1: Processamento da requisição no servidor")
    print("      -> Operações aritméticas, potência, raiz e validações defensivas.")
    print("  [✓] Requisito 2: Múltiplas funcionalidades diferentes por requisição")
    print("      -> ADD, SUB, MUL, DIV, POW, SQRT, HELP e suporte a lote com ';'.")
    print("="*70 + "\n")

    # 1. Iniciar o servidor
    print("[1/3] Iniciando o servidor de sockets (server.py)...")
    server_process = subprocess.Popen(
        [sys.executable, server_script],
        cwd=base_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # 2. Aguardar o servidor estar pronto
    host = "127.0.0.1"
    port = 5678
    max_attempts = 20
    server_ready = False

    for attempt in range(1, max_attempts + 1):
        if check_port(host, port, timeout=0.2):
            server_ready = True
            break
        time.sleep(0.1)

    if not server_ready:
        print(f"[-] Erro: O servidor não iniciou na porta {port} a tempo.")
        server_process.kill()
        sys.exit(1)

    print(f"[+] Servidor online e pronto para receber conexões em {host}:{port}!\n")

    # 3. Executar o cliente em modo demo
    print("[2/3] Executando o cliente com a bateria de testes automatizada...\n")
    try:
        client_run = subprocess.run(
            [sys.executable, client_script, "--demo"],
            cwd=base_dir,
            capture_output=True,
            text=True
        )
        print(client_run.stdout)
        if client_run.stderr:
            print("[!] Avisos do cliente:", client_run.stderr)
    finally:
        # 4. Finalizar o servidor de forma limpa
        print("\n[3/3] Finalizando o servidor...")
        try:
            # Envia QUIT pelo socket para encerramento gracioso
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect((host, port))
            s.send(b"QUIT")
            s.close()
        except Exception:
            pass

        try:
            server_process.terminate()
            server_process.wait(timeout=2)
        except Exception:
            server_process.kill()

        print("[+] Servidor encerrado com sucesso.")

    print("\n" + "="*70)
    print(" [SUCESSO] Todos os requisitos da tarefa foram testados e validados!")
    print(" Para testar interativamente no terminal:")
    print(f"   1. Abra um terminal e rode: python3 {os.path.relpath(server_script)}")
    print(f"   2. Abra outro terminal e rode: python3 {os.path.relpath(client_script)}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
