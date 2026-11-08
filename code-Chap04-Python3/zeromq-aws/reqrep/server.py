import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import zmq
from config import *

def handle(req):
    cmd, args = req.get("cmd", "").upper(), req.get("args", [])
    if cmd == "ECHO":    return " ".join(map(str, args)) + "*"   # comportamento original
    if cmd == "UPPER":   return " ".join(args).upper()
    if cmd == "REVERSE": return " ".join(args)[::-1]
    if cmd == "ADD":     return sum(float(a) for a in args)
    if cmd == "TIME":    return time.asctime()
    if cmd == "STATS":   return dict(stats)
    raise ValueError("comando desconhecido: " + cmd)

ctx = zmq.Context()
s = ctx.socket(zmq.REP)
s.bind(f"tcp://{BIND}:{REP_PORT}")
stats = {}
print("servidor REP em", REP_PORT)
while True:
    try:
        req = json.loads(s.recv())
    except ValueError:
        s.send_json({"ok": False, "error": "JSON inválido"}); continue
    cmd = str(req.get("cmd", "")).upper()
    if cmd == "STOP":
        s.send_json({"ok": True, "result": "encerrando"}); break
    try:
        stats[cmd] = stats.get(cmd, 0) + 1
        s.send_json({"ok": True, "result": handle(req)})
    except Exception as e:
        s.send_json({"ok": False, "error": str(e)})
