"""Serviço de Nomes. Uso: python servidor_nomes.py [porta]"""
import sys, threading
from concurrent import futures
import grpc
import nomes_pb2 as pb, nomes_pb2_grpc as rpc

class NameService(rpc.NameServiceServicer):
    def __init__(self):
        self.tabela, self.lock = {}, threading.Lock()

    def Bind(self, req, ctx):
        with self.lock:
            if req.nome in self.tabela:
                ctx.abort(grpc.StatusCode.ALREADY_EXISTS, f"'{req.nome}' já registrado (use rebind)")
            self.tabela[req.nome] = req.endereco
        print(f"[bind]   {req.nome} -> {req.endereco}", flush=True)
        return pb.Resposta(mensagem="registrado")

    def Lookup(self, req, ctx):
        with self.lock:
            end = self.tabela.get(req.nome)
        if end is None:
            ctx.abort(grpc.StatusCode.NOT_FOUND, f"'{req.nome}' não encontrado")
        print(f"[lookup] {req.nome} -> {end}", flush=True)
        return pb.Endereco(endereco=end)

    def Unbind(self, req, ctx):
        with self.lock:
            if self.tabela.pop(req.nome, None) is None:
                ctx.abort(grpc.StatusCode.NOT_FOUND, f"'{req.nome}' não encontrado")
        print(f"[unbind] {req.nome}", flush=True)
        return pb.Resposta(mensagem="removido")

    def Rebind(self, req, ctx):
        with self.lock:
            if req.nome not in self.tabela:
                ctx.abort(grpc.StatusCode.NOT_FOUND, f"'{req.nome}' não encontrado (use bind)")
            self.tabela[req.nome] = req.endereco
        print(f"[rebind] {req.nome} -> {req.endereco}", flush=True)
        return pb.Resposta(mensagem="atualizado")

if __name__ == "__main__":
    porta = sys.argv[1] if len(sys.argv) > 1 else "50050"
    srv = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    rpc.add_NameServiceServicer_to_server(NameService(), srv)
    srv.add_insecure_port(f"0.0.0.0:{porta}")
    srv.start()
    print("Serviço de Nomes na porta", porta, flush=True)
    srv.wait_for_termination()
