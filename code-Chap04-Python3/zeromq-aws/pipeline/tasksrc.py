"""Uso: python tasksrc.py 1|2  (fonte de tarefas, PUSH)"""
import sys, os, time, json, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import zmq
from config import *

me = sys.argv[1] if len(sys.argv) > 1 else "1"
port = SRC1_PORT if me == "1" else SRC2_PORT
ctx = zmq.Context()
s = ctx.socket(zmq.PUSH)
s.bind(f"tcp://{BIND}:{port}")
time.sleep(2)   # dá tempo aos workers de conectarem
for i in range(int(os.environ.get("N_TASKS", 100))):
    time.sleep(0.2)
    s.send_json({"src": me, "id": i, "workload": random.randint(1, 100)})  # JSON no lugar de pickle
