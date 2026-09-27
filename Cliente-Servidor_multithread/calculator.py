# calculator.py
"""
Módulo de processamento de operações matemáticas da Calculadora Remota.
Evolução direta da Tarefa ASR 04 (Sockets TCP).
"""

import math
import time

def process_single_request(request_str: str) -> str:
    """
    Processa uma única operação do protocolo: OPERACAO [ARG1] [ARG2]
    Suporta: ADD, SUB, MUL, DIV, POW, SQRT, HELP, QUIT
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

def process_request(request_str: str, simulated_delay: float = 0.0) -> str:
    """
    Processa a requisição do cliente e retorna a resposta formatada.
    Permite chamar tanto uma funcionalidade única quanto lote separado por ';'.
    O parâmetro simulated_delay permite simular tempo de processamento/I/O no servidor.
    """
    if simulated_delay > 0:
        time.sleep(simulated_delay)

    request_str = request_str.strip()
    if not request_str:
        return "ERRO: Requisição vazia."

    # Suporte a lote de operações na mesma requisição
    if ";" in request_str:
        sub_reqs = [r.strip() for r in request_str.split(";") if r.strip()]
        if len(sub_reqs) > 1:
            res_list = [f"  • [{sub}] => {process_single_request(sub)}" for sub in sub_reqs]
            return "LOTE DE OPERAÇÕES PROCESSADO:\n" + "\n".join(res_list)

    return process_single_request(request_str)
