#!/usr/bin/env python3
import sys
import os

ice_lib = os.path.expanduser("~/.local/ice_install/usr/lib/python3/dist-packages")
if os.path.exists(ice_lib) and ice_lib not in sys.path:
    sys.path.insert(0, ice_lib)

import Ice
import Demo

class MultiPrinterI(Demo.Printer):
    def __init__(self, tag: str):
        self.tag = tag

    def printString(self, s, current=None):
        print(f"[{self.tag}] {s}")
        return f"{self.tag} {s}*"

    def toUpper(self, s, current=None):
        print(f"[{self.tag}] toUpper: {s}")
        return f"{self.tag} {s.upper()}"

    def add(self, a, b, current=None):
        res = a + b
        print(f"[{self.tag}] add: {a} + {b} = {res}")
        return res

    def repeatString(self, s, times, current=None):
        res = " ".join([s] * times)
        print(f"[{self.tag}] repeatString: {res}")
        return f"{self.tag} {res}"

    def shutdown(self, current=None):
        current.adapter.getCommunicator().shutdown()

def main():
    port = 11000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])

    communicator = Ice.initialize(sys.argv)
    try:
        adapter = communicator.createObjectAdapterWithEndpoints("SimpleAdapter", f"default -p {port}")
        adapter.add(MultiPrinterI("Printer1"), communicator.stringToIdentity("SimplePrinter1"))
        adapter.add(MultiPrinterI("Printer2"), communicator.stringToIdentity("SimplePrinter2"))
        adapter.activate()
        print(f"Servidor 2 pronto na porta {port}")
        sys.stdout.flush()
        communicator.waitForShutdown()
    finally:
        communicator.destroy()

if __name__ == "__main__":
    main()
