# Execução: sobe rest/EmployeeService.py (porta 5678) e grpc/python/EmployeeService.py (50051) com IP 127.0.0.1 em const.py;
# gera os stubs (grpc_tools.protoc) e roda este script da pasta que contém rest/ e grpc/.
import sys, time, statistics, requests, grpc
sys.path.insert(0,'grpc/python')
import EmployeeService_pb2 as pb, EmployeeService_pb2_grpc as rpc
N=2000
def t(f):
    f(); xs=[]
    for _ in range(N):
        a=time.perf_counter(); f(); xs.append((time.perf_counter()-a)*1000)
    xs.sort(); return statistics.mean(xs), xs[int(.99*N)]
ses=requests.Session(); base='http://127.0.0.1:5678/empdb/employee'
ch=grpc.insecure_channel('127.0.0.1:50051'); st=rpc.EmployeeServiceStub(ch)
print("== latência (ms, média / p99), %d chamadas sequenciais"%N)
print("REST GET 1 :  %.2f / %.2f"%t(lambda: ses.get(base+'/201').json()))
print("gRPC Get 1 :  %.2f / %.2f"%t(lambda: st.GetEmployeeDataFromID(pb.EmployeeID(id=201))))
print("REST GET all: %.2f / %.2f"%t(lambda: ses.get(base).json()))
print("gRPC List  :  %.2f / %.2f"%t(lambda: st.ListAllEmployees(pb.EmptyMessage())))
print("REST sem keep-alive GET 1: %.2f / %.2f"%t(lambda: requests.get(base+'/201').json()))
print("== tamanho das mensagens (bytes)")
r=ses.get(base+'/201'); m=st.GetEmployeeDataFromID(pb.EmployeeID(id=201))
print("GET 1  REST corpo=%d, cabeçalhos resp=%d | gRPC mensagem=%d (+5 de framing)"%(len(r.content),sum(len(k)+len(v)+4 for k,v in r.headers.items()),m.ByteSize()))
r=ses.get(base); m=st.ListAllEmployees(pb.EmptyMessage())
print("GET all REST corpo=%d | gRPC mensagem=%d"%(len(r.content),m.ByteSize()))
# lista maior
for i in range(1000,1200): st.CreateEmployee(pb.EmployeeData(id=i,name='Fulano de Tal %d'%i,title='Software Engineer'))
for i in range(1000,1200): ses.post(base,json={'id':str(i),'name':'Fulano de Tal %d'%i,'title':'Software Engineer'})
r=ses.get(base); m=st.ListAllEmployees(pb.EmptyMessage())
print("202 registros: REST corpo=%d | gRPC mensagem=%d  (razão %.1fx)"%(len(r.content),m.ByteSize(),len(r.content)/m.ByteSize()))
print("202 registros latência: REST %.2f/%.2f | gRPC %.2f/%.2f"%(*t(lambda: ses.get(base).json()),*t(lambda: st.ListAllEmployees(pb.EmptyMessage()))))
print("== comportamento em erro")
r=ses.get(base+'/999'); print("REST GET id inexistente -> HTTP",r.status_code,r.text.strip())
r=ses.put(base+'/999/100'); print("REST PUT salário id inexistente -> HTTP",r.status_code)
try: st.GetEmployeeDataFromID(pb.EmployeeID(id=999))
except grpc.RpcError as e: print("gRPC Get id inexistente ->",e.code().name)
print("gRPC Delete inexistente -> status =",st.DeleteEmployee(pb.EmployeeID(id=999)).status)
r=ses.post(base,json={'id':'301','name':'X','title':'Y','salary':'3000'}); print("REST POST ignora salary? ->",r.json())
