"""Uso: python subscriber.py [N_MENSAGENS] [TOPICO ...]   ex.: subscriber.py 6 TEMP LOAD"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import zmq
from config import *

n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
topics = sys.argv[2:] or ["TIME"]
ctx = zmq.Context()
s = ctx.socket(zmq.SUB)
s.connect(f"tcp://{PUB_HOST}:{PUB_PORT}")
for t in topics:
    s.setsockopt_string(zmq.SUBSCRIBE, t)
print("assinando:", topics)
for _ in range(n):
    print(s.recv_string())
