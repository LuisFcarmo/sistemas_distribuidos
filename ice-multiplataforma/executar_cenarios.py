#!/usr/bin/env python3
import glob
import os
import socket
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JAVA_DIR = os.path.join(BASE_DIR, "java")
PY_DIR = os.path.join(BASE_DIR, "python")
BUILD_DIR = os.path.join(JAVA_DIR, "build")
ICE_JAR = os.path.join(BASE_DIR, "lib", "ice-3.7.6.jar")
CLASSPATH = os.pathsep.join([BUILD_DIR, ICE_JAR])
PORT = 11000

ice_home = os.path.expanduser("~/.local/ice_install/usr")
ENV = os.environ.copy()
ENV["PYTHONPATH"] = f"{PY_DIR}:{ENV.get('PYTHONPATH', '')}"
if os.path.exists(f"{ice_home}/lib/python3/dist-packages"):
    ENV["PYTHONPATH"] = f"{ice_home}/lib/python3/dist-packages:{ENV['PYTHONPATH']}"
    ENV["LD_LIBRARY_PATH"] = f"{ice_home}/lib/x86_64-linux-gnu:{ENV.get('LD_LIBRARY_PATH', '')}"

def compilar_java():
    os.makedirs(BUILD_DIR, exist_ok=True)
    fontes = glob.glob(os.path.join(JAVA_DIR, "generated", "**", "*.java"), recursive=True)
    fontes += glob.glob(os.path.join(JAVA_DIR, "*.java"))
    subprocess.run(["javac", "-cp", ICE_JAR, "-d", BUILD_DIR, *fontes], check=True)

def esperar_porta(port, timeout=10.0):
    inicio = time.perf_counter()
    while time.perf_counter() - inicio < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.3):
                return True
        except OSError:
            time.sleep(0.1)
    return False

def cenario(titulo, cmd_servidor, cmd_cliente):
    print(f"\n--- {titulo} ---")
    servidor = subprocess.Popen(cmd_servidor, env=ENV)
    try:
        if not esperar_porta(PORT):
            print("Servidor nao respondeu na porta", PORT)
            return False
        r = subprocess.run(cmd_cliente, env=ENV, capture_output=True, text=True)
        print(r.stdout, end="")
        if r.stderr:
            print(r.stderr, end="")
        return r.returncode == 0
    finally:
        servidor.terminate()
        try:
            servidor.wait(timeout=3)
        except subprocess.TimeoutExpired:
            servidor.kill()

def main():
    escolha = sys.argv[1] if len(sys.argv) > 1 else "todos"
    compilar_java()
    ok = True

    if escolha in ("1", "todos"):
        ok &= cenario(
            "Cenario 1: cliente Java, servidor Python",
            [sys.executable, os.path.join(PY_DIR, "server.py"), str(PORT)],
            ["java", "-cp", CLASSPATH, "PrinterClient", "127.0.0.1", str(PORT)],
        )
    if escolha in ("2", "todos"):
        ok &= cenario(
            "Cenario 2: cliente Python, servidor Java",
            ["java", "-cp", CLASSPATH, "PrinterServer", str(PORT)],
            [sys.executable, os.path.join(PY_DIR, "client.py"), "127.0.0.1", str(PORT)],
        )

    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
