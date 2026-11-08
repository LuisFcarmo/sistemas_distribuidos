"""Uso: python client.py COMANDO [args...]   ex.: client.py ADD 1 2 3"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import zmq
from config import *

if len(sys.argv) < 2:
    sys.exit(__doc__)
ctx = zmq.Context()
s = ctx.socket(zmq.REQ)
s.setsockopt(zmq.RCVTIMEO, 5000)   # timeout: não bloqueia para sempre se o servidor cair
s.setsockopt(zmq.LINGER, 0)
s.connect(f"tcp://{SERVER_HOST}:{REP_PORT}")
s.send_json({"cmd": sys.argv[1], "args": sys.argv[2:]})
try:
    r = s.recv_json()
except zmq.Again:
    sys.exit("timeout: servidor não respondeu (verifique IP e Security Group)")
print(r["result"] if r["ok"] else "ERRO: " + r["error"])
