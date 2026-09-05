from uuid import uuid4
from datetime import datetime, timezone
from storage import init_db, put, all_records, enqueue

init_db()

def _now(): return datetime.now(timezone.utc).isoformat()

def create_asset(name: str, asset_class: str):
    record={"id":str(uuid4()),"record_type":"asset","name":name,"asset_class":asset_class,"status":"active","created_at":_now()}
    put(record); enqueue({"type":"titan.asset.created","record":record}); return record

def list_assets(): return [x for x in all_records() if x.get("record_type")=="asset"]

def create_work_order(asset_id: str, title: str, priority: str="normal"):
    record={"id":str(uuid4()),"record_type":"work_order","asset_id":asset_id,"title":title,"priority":priority,"status":"open","created_at":_now()}
    put(record); enqueue({"type":"titan.work_order.created","record":record}); return record

def list_work_orders(): return [x for x in all_records() if x.get("record_type")=="work_order"]
