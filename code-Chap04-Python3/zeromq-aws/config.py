"""Configuração central. Sobrescreva com variáveis de ambiente (IPs das instâncias AWS)."""
import os

BIND = "0.0.0.0"  # servidores escutam em todas as interfaces

# Req/Rep
SERVER_HOST = os.environ.get("SERVER_HOST", "127.0.0.1")
REP_PORT = os.environ.get("REP_PORT", "4567")

# Pub/Sub
PUB_HOST = os.environ.get("PUB_HOST", "127.0.0.1")
PUB_PORT = os.environ.get("PUB_PORT", "4569")

# Pipeline (duas fontes de tarefas + um coletor de resultados)
SRC1 = os.environ.get("SRC1", "127.0.0.1")
SRC2 = os.environ.get("SRC2", "127.0.0.1")
SRC1_PORT = os.environ.get("SRC1_PORT", "4570")
SRC2_PORT = os.environ.get("SRC2_PORT", "4571")
SINK_HOST = os.environ.get("SINK_HOST", "127.0.0.1")
SINK_PORT = os.environ.get("SINK_PORT", "4572")
