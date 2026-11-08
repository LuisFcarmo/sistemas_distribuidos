"""Cliente. Uso: python cliente.py HOST_NOMES:PORTA
Descobre os serviços no Serviço de Nomes (lookup) e chama os dois. Também exercita o próprio serviço de nomes."""
import sys, grpc
import nomes_pb2 as npb, nomes_pb2_grpc as nrpc
import servicos_pb2 as pb, servicos_pb2_grpc as rpc

ns = nrpc.NameServiceStub(grpc.insecure_channel(sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1:50050"))

def descobrir(nome):
    end = ns.Lookup(npb.Nome(nome=nome), timeout=5).endereco
    print(f"lookup('{nome}') -> {end}")
    return grpc.insecure_channel(end)

def tentar(descricao, f):
    try:
        print(f"  {descricao} = {f()}")
    except grpc.RpcError as e:
        print(f"  {descricao} -> ERRO {e.code().name}: {e.details()}")

calc = rpc.CalculadoraStub(descobrir("calculadora"))
txt = rpc.TextoStub(descobrir("texto"))

print("Calculadora:")
tentar("7 + 5", lambda: calc.Somar(pb.Operandos(a=7, b=5)).valor)
tentar("7 - 5", lambda: calc.Subtrair(pb.Operandos(a=7, b=5)).valor)
tentar("7 * 5", lambda: calc.Multiplicar(pb.Operandos(a=7, b=5)).valor)
tentar("7 / 2", lambda: calc.Dividir(pb.Operandos(a=7, b=2)).valor)
tentar("7 / 0", lambda: calc.Dividir(pb.Operandos(a=7, b=0)).valor)
print("Texto:")
m = pb.Mensagem(texto="sistemas distribuidos com gRPC")
tentar("maiusculas", lambda: txt.Maiusculas(m).texto)
tentar("inverter", lambda: txt.Inverter(m).texto)
tentar("contar", lambda: (lambda c: f"{c.palavras} palavras, {c.caracteres} caracteres")(txt.ContarPalavras(m)))

print("Serviço de nomes (bind/rebind/unbind/lookup):")
tentar("bind 'teste'", lambda: ns.Bind(npb.Registro(nome="teste", endereco="1.2.3.4:1"), timeout=5).mensagem)
tentar("bind 'teste' de novo", lambda: ns.Bind(npb.Registro(nome="teste", endereco="1.2.3.4:1"), timeout=5).mensagem)
tentar("rebind 'teste'", lambda: ns.Rebind(npb.Registro(nome="teste", endereco="5.6.7.8:2"), timeout=5).mensagem)
tentar("lookup 'teste'", lambda: ns.Lookup(npb.Nome(nome="teste"), timeout=5).endereco)
tentar("unbind 'teste'", lambda: ns.Unbind(npb.Nome(nome="teste"), timeout=5).mensagem)
tentar("lookup 'teste'", lambda: ns.Lookup(npb.Nome(nome="teste"), timeout=5).endereco)
tentar("rebind inexistente", lambda: ns.Rebind(npb.Registro(nome="nada", endereco="x:1"), timeout=5).mensagem)
