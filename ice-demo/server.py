#!/usr/bin/env python3
"""
Servidor ZeroC Ice - Exemplo Printer com Novos Métodos Remotos
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

class PrinterI(Demo.Printer):
    """
    Servant que implementa a interface Demo.Printer definida em Printer.ice.
    Contém o método original (printString) e novos métodos remotos adicionados.
    """

    def printString(self, s, current=None):
        """Método original: exibe no servidor e retorna s com asterisco (*)"""
        print(f"[Servidor] Executando printString('{s}')")
        return s + "*"

    def toUpper(self, s, current=None):
        """Novo Método 1: converte o texto para letras maiúsculas remotamente"""
        print(f"[Servidor] Executando toUpper('{s}')")
        return s.upper()

    def add(self, a, b, current=None):
        """Novo Método 2: efetua a soma de dois números inteiros remotamente"""
        resultado = a + b
        print(f"[Servidor] Executando add({a}, {b}) => {resultado}")
        return resultado

    def repeatString(self, s, times, current=None):
        """Novo Método 3: repete uma string 'times' vezes remotamente"""
        resultado = " ".join([s] * times)
        print(f"[Servidor] Executando repeatString('{s}', {times}) => '{resultado}'")
        return resultado

    def shutdown(self, current=None):
        """Novo Método 4: encerramento gracioso do servidor"""
        print("[Servidor] Requisição de shutdown recebida. Encerrando communicator...")
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
        printer_servant = PrinterI()
        adapter.add(printer_servant, communicator.stringToIdentity("SimplePrinter"))
        adapter.activate()

        print(f"[*] Servidor ZeroC Ice ativo na porta {port}")
        print("[*] Objeto 'SimplePrinter' registrado no Object Adapter.")
        print("[*] Aguardando invocações de métodos remotos (Ctrl+C para encerrar)...")
        sys.stdout.flush()

        communicator.waitForShutdown()
    except KeyboardInterrupt:
        print("\n[*] Servidor encerrado pelo usuário.")
    finally:
        communicator.destroy()
        print("[*] Communicator finalizado com sucesso.")

if __name__ == "__main__":
    main()
