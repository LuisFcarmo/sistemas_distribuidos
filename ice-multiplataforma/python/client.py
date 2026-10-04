#!/usr/bin/env python3
import sys
import os

ice_lib = os.path.expanduser("~/.local/ice_install/usr/lib/python3/dist-packages")
if os.path.exists(ice_lib) and ice_lib not in sys.path:
    sys.path.insert(0, ice_lib)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
        base = communicator.stringToProxy(f"SimplePrinter:tcp -h {host} -p {port}")
        printer = Demo.PrinterPrx.checkedCast(base)
        if not printer:
            raise RuntimeError("Proxy invalido")

        print("printString: ", printer.printString("Hello World!"))
        print("toUpper:     ", printer.toUpper("sistemas distribuidos"))
        print("add:         ", printer.add(35, 7))
        print("repeatString:", printer.repeatString("ZeroC-Ice", 3))
    except Exception as e:
        print("Erro:", e)
        return 1
    finally:
        communicator.destroy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
