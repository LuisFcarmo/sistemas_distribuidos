"""Uso: python servidor_texto.py HOST_NOMES:PORTA HOST_ANUNCIADO [porta=50052]"""
import sys
import servicos_pb2 as pb, servicos_pb2_grpc as rpc
from registro import executar

class Texto(rpc.TextoServicer):
    def Maiusculas(self, r, c):     return pb.Mensagem(texto=r.texto.upper())
    def Inverter(self, r, c):       return pb.Mensagem(texto=r.texto[::-1])
    def ContarPalavras(self, r, c): return pb.Contagem(palavras=len(r.texto.split()), caracteres=len(r.texto))

if __name__ == "__main__":
    ns, host = sys.argv[1], sys.argv[2]
    porta = sys.argv[3] if len(sys.argv) > 3 else "50052"
    executar("texto", lambda s: rpc.add_TextoServicer_to_server(Texto(), s), porta, host, ns)
