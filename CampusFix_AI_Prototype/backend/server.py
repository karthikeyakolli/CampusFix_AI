from http.server import BaseHTTPRequestHandler,HTTPServer
import json,uuid
def category(t):
 t=t.lower()
 for k,words in {'wifi':['wifi','wi-fi'],'login':['login','sign in'],'password':['password'],'printer':['printer'],'software':['software','install'],'network':['network','internet']}.items():
  if any(w in t for w in words): return k
 return 'system_configuration'
class H(BaseHTTPRequestHandler):
 def out(self,o,c=200):
  b=json.dumps(o).encode();self.send_response(c);self.send_header('Content-Type','application/json');self.send_header('Access-Control-Allow-Origin','*');self.end_headers();self.wfile.write(b)
 def do_GET(self):
  if self.path=='/api/health': self.out({'ok':True,'service':'CampusFix mock backend'})
  else:self.out({'error':'not found'},404)
 def do_POST(self):
  n=int(self.headers.get('Content-Length','0'));body=json.loads(self.rfile.read(n) or b'{}')
  if self.path=='/api/diagnose':self.out({'category':category(body.get('message','')),'confidence':.82,'next_question':'Are other users/devices affected?','simulated':True})
  elif self.path=='/api/tickets':self.out({'ticket_id':'CF-'+uuid.uuid4().hex[:8].upper(),'status':'NEW','simulated':True})
  else:self.out({'error':'not found'},404)
if __name__=='__main__': HTTPServer(('0.0.0.0',8080),H).serve_forever()
