"""Ciclo de vida de um servidor de aplicação: sobe, faz bind no serviço de nomes e faz unbind ao sair."""
import signal, threading
from concurrent import futures
import grpc
import nomes_pb2 as pb, nomes_pb2_grpc as rpc

def executar(nome, adicionar_servicer, porta, host_anunciado, ns_addr):
    srv = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    adicionar_servicer(srv)
    srv.add_insecure_port(f"0.0.0.0:{porta}")
    srv.start()
    endereco = f"{host_anunciado}:{porta}"

    ns = rpc.NameServiceStub(grpc.insecure_channel(ns_addr))
    reg = pb.Registro(nome=nome, endereco=endereco)
    try:
        ns.Bind(reg, timeout=5)
    except grpc.RpcError as e:
        if e.code() != grpc.StatusCode.ALREADY_EXISTS:
            raise
        ns.Rebind(reg, timeout=5)   # registro antigo (ex.: queda anterior): atualiza
    print(f"'{nome}' em {endereco}, registrado em {ns_addr}", flush=True)

    parar = threading.Event()
    for s in (signal.SIGINT, signal.SIGTERM):
        signal.signal(s, lambda *_: parar.set())
    parar.wait()
    try:
        ns.Unbind(pb.Nome(nome=nome), timeout=5)
        print("unbind feito", flush=True)
    except grpc.RpcError:
        pass
    srv.stop(1)
