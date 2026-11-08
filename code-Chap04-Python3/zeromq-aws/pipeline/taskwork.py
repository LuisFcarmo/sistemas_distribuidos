"""Uso: python taskwork.py NOME  (worker: PULL das fontes, PUSH dos resultados ao sink)"""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import zmq
from config import *

me = sys.argv[1] if len(sys.argv) > 1 else "w"
ctx = zmq.Context()
r = ctx.socket(zmq.PULL)
r.connect(f"tcp://{SRC1}:{SRC1_PORT}")
r.connect(f"tcp://{SRC2}:{SRC2_PORT}")
out = ctx.socket(zmq.PUSH)
out.connect(f"tcp://{SINK_HOST}:{SINK_PORT}")
print(me, "started")
while True:
    t = r.recv_json()
    print(me, "received", t["workload"], "from", t["src"])
    time.sleep(t["workload"] * 0.01)   # simula trabalho
    out.send_json({"worker": me, "src": t["src"], "id": t["id"], "result": t["workload"] ** 2})
