#!/usr/bin/env python3
"""
Cliente Multithread de Calculadora Remota (Sockets TCP)
Disciplina: Sistemas Distribuídos
Requisitos:
- 'cada requisição do cliente deve ser enviada por uma nova thread,
   de modo que o cliente possa enviar múltiplas requisições em paralelo
   (para mais de um servidor, por exemplo)'
- 'automatizar a geração de requisições no cliente
   (por exemplo, usando um gerador de números aleatórios para gerar os dados das requisições)'
"""

import socket
import threading
import time
import argparse
import statistics
from typing import List, Tuple, Dict, Any
from constCS import HOST, PORT, BUFFER_SIZE, TIMEOUT
from gerador_requisicoes import gerar_conjunto_requisicoes

class RequestResult:
    def __init__(self, req_id: int, request: str, server: str, latency: float, success: bool, response: str = "", error: str = ""):
        self.req_id = req_id
        self.request = request
        self.server = server
        self.latency = latency
        self.success = success
        self.response = response
        self.error = error

def send_single_request(
    req_id: int,
    req_str: str,
    server_host: str,
    server_port: int,
    results: List[RequestResult],
    lock: threading.Lock,
    quiet: bool = False
):
    """
    Função executada por uma thread dedicada para enviar uma única requisição ao servidor.
    Estabelece a conexão TCP, envia a requisição, recebe a resposta e fecha a conexão.
    """
    server_addr_str = f"{server_host}:{server_port}"
    start_time = time.perf_counter()
    success = False
    response = ""
    error_msg = ""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    try:
        s.connect((server_host, server_port))
        s.sendall(req_str.encode("utf-8"))
        data = s.recv(BUFFER_SIZE)
        if data:
            response = data.decode("utf-8")
            success = response.startswith("OK:") or "OPERAÇÕES SUPORTADAS" in response or "LOTE" in response
            if not success and response.startswith("ERRO:"):
                # Resposta de erro da aplicação ainda conta como comunicação bem-sucedida com o servidor
                success = True
        else:
            error_msg = "Resposta vazia do servidor"
    except Exception as e:
        error_msg = str(e)
    finally:
        try:
            s.close()
        except Exception:
            pass
        end_time = time.perf_counter()

    latency = end_time - start_time
    result = RequestResult(req_id, req_str, server_addr_str, latency, success, response, error_msg)

    with lock:
        results.append(result)

    if not quiet:
        status_tag = "OK" if success else "FALHA"
        print(f"[Thread-{req_id:04d}] -> {server_addr_str} | '{req_str}' => [{status_tag}] ({latency*1000:.2f}ms)")

def run_multithreaded_client(
    requests: List[str],
    servers: List[Tuple[str, int]],
    quiet: bool = False,
    max_workers: int = 0
) -> Dict[str, Any]:
    """
    Dispara uma nova thread para cada requisição da lista em paralelo.
    Distribui as requisições entre os servidores disponíveis.
    """
    results: List[RequestResult] = []
    lock = threading.Lock()
    threads: List[threading.Thread] = []

    num_servers = len(servers)
    total_reqs = len(requests)

    start_wall_time = time.perf_counter()

    # Cria e inicia uma nova thread para cada requisição
    for i, req in enumerate(requests):
        target_server = servers[i % num_servers]
        t = threading.Thread(
            target=send_single_request,
            args=(i + 1, req, target_server[0], target_server[1], results, lock, quiet),
            name=f"ReqThread-{i+1}"
        )
        threads.append(t)
        t.start()

    # Aguarda a finalização de todas as threads disparadas
    for t in threads:
        t.join()

    total_wall_time = time.perf_counter() - start_wall_time

    # Compilação das métricas estatísticas
    latencies_ms = [r.latency * 1000 for r in results]
    success_count = sum(1 for r in results if r.success)

    mean_lat = statistics.mean(latencies_ms) if latencies_ms else 0.0
    stdev_lat = statistics.stdev(latencies_ms) if len(latencies_ms) > 1 else 0.0
    min_lat = min(latencies_ms) if latencies_ms else 0.0
    max_lat = max(latencies_ms) if latencies_ms else 0.0
    sorted_lat = sorted(latencies_ms) if latencies_ms else [0.0]
    p50 = sorted_lat[int(len(sorted_lat) * 0.50)]
    p95 = sorted_lat[int(len(sorted_lat) * 0.95)]
    p99 = sorted_lat[min(int(len(sorted_lat) * 0.99), len(sorted_lat) - 1)]

    throughput = total_reqs / total_wall_time if total_wall_time > 0 else 0.0

    return {
        "total_requests": total_reqs,
        "success_count": success_count,
        "success_rate": (success_count / total_reqs * 100.0) if total_reqs > 0 else 0.0,
        "total_time_s": total_wall_time,
        "throughput_req_s": throughput,
        "latency_mean_ms": mean_lat,
        "latency_stdev_ms": stdev_lat,
        "latency_min_ms": min_lat,
        "latency_max_ms": max_lat,
        "latency_p50_ms": p50,
        "latency_p95_ms": p95,
        "latency_p99_ms": p99,
        "servers_used": [f"{s[0]}:{s[1]}" for s in servers],
        "mode": "MULTITHREAD"
    }

def parse_servers(servers_arg: str) -> List[Tuple[str, int]]:
    servers = []
    for item in servers_arg.split(","):
        item = item.strip()
        if not item:
            continue
        if ":" in item:
            h, p = item.split(":")
            servers.append((h, int(p)))
        else:
            servers.append((item, PORT))
    return servers if servers else [(HOST, PORT)]

def main():
    parser = argparse.ArgumentParser(description="Cliente Multithread - Sistemas Distribuídos")
    parser.add_argument("--requests", type=int, default=100, help="Quantidade de requisições a gerar e enviar em paralelo (padrão: 100)")
    parser.add_argument("--servers", default=f"{HOST}:{PORT}", help="Lista de servidores separados por vírgula (ex: 127.0.0.1:5678,127.0.0.1:5679)")
    parser.add_argument("--seed", type=int, default=42, help="Semente para o gerador pseudo-aleatório de requisições (padrão: 42)")
    parser.add_argument("--quiet", action="store_true", help="Suprime logs individuais de requisições")
    args = parser.parse_args()

    servers = parse_servers(args.servers)
    print(f"[*] Gerando {args.requests} requisições aleatórias automatizadas (seed={args.seed})...")
    req_list = gerar_conjunto_requisicoes(args.requests, seed=args.seed)

    print(f"[*] Disparando {args.requests} requisições em threads paralelas para {len(servers)} servidor(es): {servers}")
    metrics = run_multithreaded_client(req_list, servers, quiet=args.quiet)

    print("\n" + "="*60)
    print("   RESULTADOS DO CLIENTE MULTITHREAD")
    print("="*60)
    print(f" Requisições enviadas   : {metrics['total_requests']}")
    print(f" Sucessos               : {metrics['success_count']} ({metrics['success_rate']:.1f}%)")
    print(f" Tempo Total            : {metrics['total_time_s']:.4f} s")
    print(f" Vazão (Throughput)     : {metrics['throughput_req_s']:.2f} req/s")
    print(f" Latência Média         : {metrics['latency_mean_ms']:.2f} ms (±{metrics['latency_stdev_ms']:.2f} ms)")
    print(f" Latência Mín / Máx     : {metrics['latency_min_ms']:.2f} ms / {metrics['latency_max_ms']:.2f} ms")
    print(f" Percentis (p50/p95/p99): {metrics['latency_p50_ms']:.2f} ms / {metrics['latency_p95_ms']:.2f} ms / {metrics['latency_p99_ms']:.2f} ms")
    print("="*60)

if __name__ == "__main__":
    main()
