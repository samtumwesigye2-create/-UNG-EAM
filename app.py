from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from domain import create_asset, list_assets
from integration import dependencies
SYSTEM_ID="UNG-TITAN"; LEGACY_ID="UNG-EAM"; VERSION="0.2.0"
app=FastAPI(title=SYSTEM_ID,version=VERSION,description="UNG Enterprise Asset Management and Heavy Assets System")
class AssetIn(BaseModel): name:str; asset_class:str
def authorize(permission:str, x_ung_permissions:str|None):
    perms={p.strip() for p in (x_ung_permissions or "").split(",") if p.strip()}
    if permission not in perms and "ung.admin" not in perms: raise HTTPException(403,"UNG-JANUS permission required")
@app.get("/")
def root(): return {"system":SYSTEM_ID,"legacy_id":LEGACY_ID,"status":"online","version":VERSION}
@app.get("/health")
def health(): return {"status":"ok","service":SYSTEM_ID,"version":VERSION}
@app.get("/ready")
def ready(): return {"status":"ready","service":SYSTEM_ID,"dependencies":dependencies()}
@app.get("/v1/system")
def system(): return {"system_id":SYSTEM_ID,"legacy_id":LEGACY_ID,"domain":"enterprise-asset-management","dependencies":dependencies()}
@app.get("/v1/assets")
def assets(x_ung_permissions:str|None=Header(None)): authorize("titan.assets.read",x_ung_permissions); return list_assets()
@app.post("/v1/assets",status_code=201)
def add_asset(body:AssetIn,x_ung_permissions:str|None=Header(None)): authorize("titan.assets.write",x_ung_permissions); return create_asset(body.name,body.asset_class)
