#!/usr/bin/env python3
"""
Cliente ZeroC Ice - Invoca Métodos Remotos do Servant Printer
Disciplina: Sistemas Distribuídos - UFG
Referência: https://github.com/professorfabio/ice-demo e Maarten van Steen (Capítulo 3, Exemplo 3.21)
"""

import sys
import os

# Garante que as bibliotecas ZeroC Ice locais sejam encontradas caso instaladas em ~/.local
ice_lib = os.path.expanduser("~/.local/ice_install/usr/lib/python3/dist-packages")
if os.path.exists(ice_lib) and ice_lib not in sys.path:
    sys.path.insert(0, ice_lib)

import Ice
import Demo

def main():
    host = "127.0.0.1"
    port = 11000

    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        host = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2].isdigit():
        port = int(sys.argv[2])

    proxy_str = f"SimplePrinter:tcp -h {host} -p {port}"
    print("="*65)
    print("   CLIENTE ZEROC ICE - INVOCANDO MÉTODOS REMOTOS (RPC)")
    print("="*65)
    print(f"[*] Conectando ao proxy: '{proxy_str}'...")

    communicator = Ice.initialize(sys.argv)
    try:
        base = communicator.stringToProxy(proxy_str)
        printer = Demo.PrinterPrx.checkedCast(base)
        if not printer:
            raise RuntimeError(f"Proxy inválido ou servidor inacessível em {host}:{port}")

        print("[+] Proxy obtido e validado via checkedCast com sucesso!\n")

        # 1. Método original
        print("--> [1/4] Invocando método original 'printString':")
        txt_original = "Hello World via ZeroC Ice!"
        resp1 = printer.printString(txt_original)
        print(f"    Parâmetro enviado: '{txt_original}'")
        print(f"    Retorno do servidor: '{resp1}'\n")

        # 2. Novo Método 1: toUpper
        print("--> [2/4] Invocando NOVO método 'toUpper':")
        txt_upper = "sistemas distribuidos - ufg 2026"
        resp2 = printer.toUpper(txt_upper)
        print(f"    Parâmetro enviado: '{txt_upper}'")
        print(f"    Retorno do servidor: '{resp2}'\n")

        # 3. Novo Método 2: add
        print("--> [3/4] Invocando NOVO método 'add':")
        a, b = 35, 7
        resp3 = printer.add(a, b)
        print(f"    Parâmetros enviados: a={a}, b={b}")
        print(f"    Retorno do servidor: {resp3} (Tipo: {type(resp3).__name__})\n")

        # 4. Novo Método 3: repeatString
        print("--> [4/4] Invocando NOVO método 'repeatString':")
        palavra, vezes = "ZeroC-Ice", 3
        resp4 = printer.repeatString(palavra, vezes)
        print(f"    Parâmetros enviados: s='{palavra}', times={vezes}")
        print(f"    Retorno do servidor: '{resp4}'\n")

        print("="*65)
        print(" [SUCESSO] Todos os métodos remotos responderam perfeitamente!")
        print("="*65)

    except Exception as e:
        print(f"[-] Erro na execução do cliente: {e}")
        return 1
    finally:
        communicator.destroy()
    return 0

if __name__ == "__main__":
    sys.exit(main())
