"""Coletor: recebe resultados dos workers e imprime estatísticas (nova funcionalidade)."""
import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import zmq
from config import *

ctx = zmq.Context()
s = ctx.socket(zmq.PULL)
s.bind(f"tcp://{BIND}:{SINK_PORT}")
per_worker = collections.Counter()
total = 0
print("sink em", SINK_PORT)
while True:
    r = s.recv_json()
    per_worker[r["worker"]] += 1
    total += 1
    print(f"#{total} resultado {r['result']} (fonte {r['src']}, worker {r['worker']}) | por worker: {dict(per_worker)}")
