import random
from typing import List

def gerar_requisicao_aleatoria(rng: random.Random = None) -> str:
    """Gera uma string de requisição sintaticamente válida com valores aleatórios."""
    if rng is None:
        rng = random.Random()

    operacoes = ["ADD", "SUB", "MUL", "DIV", "POW", "SQRT"]
    op = rng.choice(operacoes)

    if op == "SQRT":
        val = rng.randint(1, 10000)
        return f"SQRT {val}"

    if op == "POW":
        base = rng.randint(1, 20)
        exp = rng.randint(1, 5)
        return f"POW {base} {exp}"

    if op == "DIV":
        a = rng.randint(1, 5000)
        b = rng.randint(1, 200) # Evita divisão por zero para fluxos normais
        return f"DIV {a} {b}"

    # ADD, SUB, MUL
    a = rng.randint(1, 10000)
    b = rng.randint(1, 10000)
    return f"{op} {a} {b}"

def gerar_conjunto_requisicoes(quantidade: int, seed: int = 42) -> List[str]:
    """
    Gera uma lista com N requisições determinísticas para permitir
    comparações justas entre diferentes arquiteturas de clientes e servidores.
    """
    rng = random.Random(seed)
    return [gerar_requisicao_aleatoria(rng) for _ in range(quantidade)]
