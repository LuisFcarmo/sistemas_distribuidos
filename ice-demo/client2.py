#!/usr/bin/env python3
"""
Cliente 2 ZeroC Ice - Comunicação com Múltiplos Objetos Distribuídos
Disciplina: Sistemas Distribuídos - UFG
Referência: https://github.com/professorfabio/ice-demo (client2.py)
"""

import sys
import os

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

    communicator = Ice.initialize(sys.argv)
    try:
        base1 = communicator.stringToProxy(f"SimplePrinter1:tcp -h {host} -p {port}")
        base2 = communicator.stringToProxy(f"SimplePrinter2:tcp -h {host} -p {port}")

        p1 = Demo.PrinterPrx.checkedCast(base1)
        p2 = Demo.PrinterPrx.checkedCast(base2)

        if not p1 or not p2:
            raise RuntimeError("Não foi possível conectar a ambos os objetos!")

        print("=== Testando Objeto 1 (SimplePrinter1) ===")
        print("printString:", p1.printString("Mensagem para Objeto 1"))
        print("toUpper:    ", p1.toUpper("texto minusculo 1"))
        print("add:        ", p1.add(10, 20))

        print("\n=== Testando Objeto 2 (SimplePrinter2) ===")
        print("printString:", p2.printString("Mensagem para Objeto 2"))
        print("repeatString:", p2.repeatString("Echo", 2))
        print("add:        ", p2.add(100, 250))

    finally:
        communicator.destroy()

if __name__ == "__main__":
    main()
