"""Uso: python servidor_calculadora.py HOST_NOMES:PORTA HOST_ANUNCIADO [porta=50051]"""
import sys, grpc
import servicos_pb2 as pb, servicos_pb2_grpc as rpc
from registro import executar

class Calculadora(rpc.CalculadoraServicer):
    def Somar(self, r, c):       return pb.Numero(valor=r.a + r.b)
    def Subtrair(self, r, c):    return pb.Numero(valor=r.a - r.b)
    def Multiplicar(self, r, c): return pb.Numero(valor=r.a * r.b)
    def Dividir(self, r, c):
        if r.b == 0:
            c.abort(grpc.StatusCode.INVALID_ARGUMENT, "divisão por zero")
        return pb.Numero(valor=r.a / r.b)

if __name__ == "__main__":
    ns, host = sys.argv[1], sys.argv[2]
    porta = sys.argv[3] if len(sys.argv) > 3 else "50051"
    executar("calculadora", lambda s: rpc.add_CalculadoraServicer_to_server(Calculadora(), s), porta, host, ns)
