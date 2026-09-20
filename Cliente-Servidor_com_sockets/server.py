from socket import *
from constCS import *
import math

def process_request(request_str: str) -> str:
    """
    Processa a requisição do cliente e retorna a resposta formatada.
    Protocolo de requisição: OPERACAO [ARG1] [ARG2]
    Exemplos:
      - ADD 10 5
      - SUB 20 4
      - MUL 6 7
      - DIV 100 5
      - POW 2 8
      - SQRT 144
      - HELP
      - QUIT
    """
    request_str = request_str.strip()
    if not request_str:
        return "ERRO: Requisição vazia."

    tokens = request_str.split()
    op = tokens[0].upper()
    args = tokens[1:]

    if op == "HELP":
        return (
            "OPERAÇÕES SUPORTADAS:\n"
            "  ADD <a> <b>    -> Soma a + b\n"
            "  SUB <a> <b>    -> Subtração a - b\n"
            "  MUL <a> <b>    -> Multiplicação a * b\n"
            "  DIV <a> <b>    -> Divisão a / b\n"
            "  POW <a> <b>    -> Potenciação a ^ b\n"
            "  SQRT <a>       -> Raiz quadrada de a\n"
            "  HELP           -> Mostra esta ajuda\n"
            "  QUIT           -> Encerra a conexão"
        )

    if op == "QUIT":
        return "OK: Conexão encerrada pelo cliente."

    # Operação unária (1 argumento): SQRT
    if op == "SQRT":
        if len(args) != 1:
            return "ERRO: Operação SQRT requer exatamente 1 parâmetro. Ex: SQRT 16"
        try:
            val = float(args[0])
            if val < 0:
                return "ERRO: Não é possível calcular raiz quadrada de número negativo."
            res = math.sqrt(val)
            # Se for inteiro, formata como inteiro
            return f"OK: {int(res) if res.is_integer() else res}"
        except ValueError:
            return f"ERRO: Parâmetro '{args[0]}' não é um número válido."

    # Operações binárias (2 argumentos): ADD, SUB, MUL, DIV, POW
    if op in ("ADD", "SUB", "MUL", "DIV", "POW"):
        if len(args) != 2:
            return f"ERRO: Operação {op} requer exatamente 2 parâmetros. Ex: {op} 10 5"
        try:
            num1 = float(args[0])
            num2 = float(args[1])
        except ValueError:
            return "ERRO: Os parâmetros devem ser valores numéricos válidos."

        if op == "ADD":
            res = num1 + num2
        elif op == "SUB":
            res = num1 - num2
        elif op == "MUL":
            res = num1 * num2
        elif op == "DIV":
            if num2 == 0:
                return "ERRO: Divisão por zero não é permitida."
            res = num1 / num2
        elif op == "POW":
            try:
                res = math.pow(num1, num2)
            except OverflowError:
                return "ERRO: Resultado gerou overflow numérico."

        return f"OK: {int(res) if res.is_integer() else res}"

    return f"ERRO: Operação desconhecida '{op}'. Digite HELP para ver os comandos disponíveis."

def main():
    s = socket(AF_INET, SOCK_STREAM)
    # Permite reuso rápido da porta após encerramento do processo
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"[*] Servidor de Calculadora Remota iniciado em {HOST}:{PORT}")
    print("[*] Aguardando conexões de clientes...")

    try:
        while True:
            conn, addr = s.accept()
            print(f"[+] Conexão aceita de {addr[0]}:{addr[1]}")

            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"[-] Cliente {addr[0]}:{addr[1]} encerrou a conexão.")
                    break

                req = data.decode("utf-8")
                print(f"[REQ de {addr[0]}:{addr[1]}]: {req.strip()}")

                resp = process_request(req)
                conn.send(resp.encode("utf-8"))

                if req.strip().upper() == "QUIT":
                    print(f"[-] Cliente {addr[0]}:{addr[1]} solicitou QUIT.")
                    break

            conn.close()
    except KeyboardInterrupt:
        print("\n[*] Servidor encerrado pelo usuário (Ctrl+C).")
    finally:
        s.close()

if __name__ == "__main__":
    main()
