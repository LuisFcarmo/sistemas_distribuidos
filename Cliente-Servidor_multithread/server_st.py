#!/usr/bin/env python3
import socket
import sys
import argparse
from constCS import HOST, PORT, BACKLOG, BUFFER_SIZE
from calculator import process_request

class SingleThreadedServer:
    def __init__(self, host: str = HOST, port: int = PORT, delay: float = 0.0, quiet: bool = False):
        self.host = host
        self.port = port
        self.delay = delay
        self.quiet = quiet
        self.running = False
        self.server_socket = None
        self.total_requests = 0

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(BACKLOG)
        self.running = True

        print(f"Servidor single-threaded ouvindo em {self.host}:{self.port}")

        try:
            while self.running:
                try:
                    conn, addr = self.server_socket.accept()
                except OSError:
                    break

                try:
                    while self.running:
                        data = conn.recv(BUFFER_SIZE)
                        if not data:
                            break

                        req = data.decode("utf-8")
                        if not self.quiet:
                            print(f"[MainThread] REQ de {addr[0]}:{addr[1]} -> '{req.strip()}'")

                        # Processa sequencialmente na própria thread principal
                        resp = process_request(req, simulated_delay=self.delay)
                        conn.sendall(resp.encode("utf-8"))

                        self.total_requests += 1

                        if req.strip().upper() == "QUIT":
                            break
                except Exception as e:
                    if not self.quiet and self.running:
                        print(f"[!] Erro no tratamento do cliente {addr}: {e}")
                finally:
                    try:
                        conn.close()
                    except Exception:
                        pass

        except KeyboardInterrupt:
            print("\n[*] Encerrando servidor single-threaded...")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
        print(f"[*] Servidor single-threaded finalizado. Total de requisições atendidas: {self.total_requests}")

def main():
    parser = argparse.ArgumentParser(description="Servidor Single-Threaded - Sistemas Distribuídos")
    parser.add_argument("--host", default=HOST, help="Endereço de escuta (padrão: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=PORT, help=f"Porta do serviço (padrão: {PORT})")
    parser.add_argument("--delay", type=float, default=0.0, help="Atraso simulado de processamento/IO em segundos (padrão: 0.0)")
    parser.add_argument("--quiet", action="store_true", help="Suprime logs por requisição (recomendado para benchmarks)")
    args = parser.parse_args()

    server = SingleThreadedServer(host=args.host, port=args.port, delay=args.delay, quiet=args.quiet)
    server.start()

if __name__ == "__main__":
    main()
