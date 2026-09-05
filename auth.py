import os, json, urllib.request
from fastapi import Header, HTTPException
JANUS=os.getenv('JANUS_BASE_URL',os.getenv('IAM_BASE_URL',''))
def principal(authorization:str|None=Header(None)):
 if not authorization or not authorization.startswith('Bearer '): raise HTTPException(401,'Bearer token required')
 if not JANUS: raise HTTPException(503,'UNG-JANUS not configured')
 req=urllib.request.Request(JANUS.rstrip('/')+'/v1/principal',headers={'Authorization':authorization})
 try:
  with urllib.request.urlopen(req,timeout=3) as r:return json.loads(r.read())
 except Exception: raise HTTPException(401,'Invalid UNG-JANUS session')
def require(permission):
 def dep(p=principal):
  perms=set(p.get('permissions',[]));
  if permission not in perms and 'ung.core.admin' not in perms: raise HTTPException(403,'Permission denied')
  return p
 return dep
