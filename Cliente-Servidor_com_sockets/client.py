from socket import *
from constCS import *
import sys

def print_menu():
    print("\n" + "="*45)
    print("   CALCULADORA REMOTA - CLIENTE (Sockets TCP)")
    print("="*45)
    print(" 1. Soma (ADD a b)")
    print(" 2. Subtração (SUB a b)")
    print(" 3. Multiplicação (MUL a b)")
    print(" 4. Divisão (DIV a b)")
    print(" 5. Potenciação (POW a b)")
    print(" 6. Raiz Quadrada (SQRT a)")
    print(" 7. Ajuda do Servidor (HELP)")
    print(" 8. Comando Livre (digitar manualmente)")
    print(" 0. Sair (QUIT)")
    print("="*45)

def run_interactive_client():
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        print(f"[+] Conectado com sucesso ao servidor {HOST}:{PORT}")
    except Exception as e:
        print(f"[-] Erro ao conectar ao servidor ({HOST}:{PORT}): {e}")
        return

    try:
        while True:
            print_menu()
            opcao = input("Escolha uma opção (0-8): ").strip()

            if opcao == "0":
                s.send("QUIT".encode("utf-8"))
                resposta = s.recv(1024).decode("utf-8")
                print(f"[Servidor]: {resposta}")
                break

            elif opcao == "1":
                a = input("Digite o primeiro número (a): ").strip()
                b = input("Digite o segundo número (b): ").strip()
                cmd = f"ADD {a} {b}"

            elif opcao == "2":
                a = input("Digite o primeiro número (a): ").strip()
                b = input("Digite o segundo número (b): ").strip()
                cmd = f"SUB {a} {b}"

            elif opcao == "3":
                a = input("Digite o primeiro número (a): ").strip()
                b = input("Digite o segundo número (b): ").strip()
                cmd = f"MUL {a} {b}"

            elif opcao == "4":
                a = input("Digite o numerador (a): ").strip()
                b = input("Digite o denominador (b): ").strip()
                cmd = f"DIV {a} {b}"

            elif opcao == "5":
                a = input("Digite a base (a): ").strip()
                b = input("Digite o expoente (b): ").strip()
                cmd = f"POW {a} {b}"

            elif opcao == "6":
                a = input("Digite o número (a): ").strip()
                cmd = f"SQRT {a}"

            elif opcao == "7":
                cmd = "HELP"

            elif opcao == "8":
                cmd = input("Digite o comando (ex: ADD 15 30): ").strip()

            else:
                print("[!] Opção inválida. Tente novamente.")
                continue

            # Envia requisição para o servidor
            s.send(cmd.encode("utf-8"))

            # Recebe a resposta processada
            data = s.recv(1024)
            if not data:
                print("[-] Servidor fechou a conexão inesperadamente.")
                break

            resposta = data.decode("utf-8")
            print("\n>>> RESPOSTA DO SERVIDOR:")
            print(resposta)

    except KeyboardInterrupt:
        print("\n[*] Cliente encerrado pelo usuário.")
    finally:
        s.close()
        print("[*] Conexão encerrada.")

def run_automated_demo():
    """Executa uma bateria de testes demonstrando várias funcionalidades diferentes."""
    print("==================================================")
    print(" MODO DEMO: Testando múltiplas funcionalidades...")
    print("==================================================")
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        print(f"[+] Conectado a {HOST}:{PORT}\n")
    except Exception as e:
        print(f"[-] Falha ao conectar: {e}")
        return

    test_commands = [
        ("Soma de 25 + 17", "ADD 25 17"),
        ("Subtração de 100 - 37", "SUB 100 37"),
        ("Multiplicação de 12 * 8", "MUL 12 8"),
        ("Divisão de 45 / 9", "DIV 45 9"),
        ("Divisão por zero (Tratamento de erro)", "DIV 10 0"),
        ("Potência de 2 ^ 10", "POW 2 10"),
        ("Raiz quadrada de 144", "SQRT 144"),
        ("Raiz quadrada de número negativo (Tratamento de erro)", "SQRT -25"),
        ("Comando inválido / Desconhecido", "FATORIAL 5"),
        ("Consulta de ajuda", "HELP"),
        ("Encerramento da sessão", "QUIT")
    ]

    try:
        for desc, cmd in test_commands:
            print(f"--> [Envio] {desc} -> Requisição: '{cmd}'")
            s.send(cmd.encode("utf-8"))
            resp = s.recv(1024).decode("utf-8")
            print(f"<-- [Resposta do Servidor]:\n{resp}\n" + "-"*40)
    finally:
        s.close()
        print("[*] Demo finalizada com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_automated_demo()
    else:
        run_interactive_client()
