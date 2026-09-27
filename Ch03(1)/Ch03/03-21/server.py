#!/usr/bin/env python3
import sys
import os

ice_lib = os.path.expanduser("~/.local/ice_install/usr/lib/python3/dist-packages")
if os.path.exists(ice_lib) and ice_lib not in sys.path:
    sys.path.insert(0, ice_lib)

import Ice
import Demo

class PrinterI(Demo.Printer):
    def printString(self, s, current=None):
        print(s)
        return s + "*"

    def toUpper(self, s, current=None):
        print(f"toUpper: {s}")
        return s.upper()

    def add(self, a, b, current=None):
        print(f"add: {a} + {b} = {a + b}")
        return a + b

    def repeatString(self, s, times, current=None):
        print(f"repeatString: {s} ({times}x)")
        return " ".join([s] * times)

    def shutdown(self, current=None):
        current.adapter.getCommunicator().shutdown()

def main():
    port = 11000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])

    communicator = Ice.initialize(sys.argv)
    try:
        adapter = communicator.createObjectAdapterWithEndpoints(
            "SimpleAdapter", f"default -p {port}"
        )
        adapter.add(PrinterI(), communicator.stringToIdentity("SimplePrinter"))
        adapter.activate()
        print(f"Servidor iniciado na porta {port}")
        sys.stdout.flush()
        communicator.waitForShutdown()
    finally:
        communicator.destroy()

if __name__ == "__main__":
    main()
