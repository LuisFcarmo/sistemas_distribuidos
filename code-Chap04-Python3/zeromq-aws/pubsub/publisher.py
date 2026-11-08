import sys, os, time, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import zmq
from config import *

ctx = zmq.Context()
s = ctx.socket(zmq.PUB)
s.bind(f"tcp://{BIND}:{PUB_PORT}")
print("publisher em", PUB_PORT)
while True:
    time.sleep(2)
    s.send_string("TIME " + time.asctime())
    s.send_string("TEMP %.1f" % random.uniform(18, 35))
    s.send_string("LOAD %.2f" % os.getloadavg()[0])
