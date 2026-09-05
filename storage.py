import os, json
from sqlalchemy import create_engine, text
DB=os.getenv('DATABASE_URL','').replace('postgres://','postgresql+psycopg://',1).replace('postgresql://','postgresql+psycopg://',1)
_engine=create_engine(DB,pool_pre_ping=True) if DB else None
def init_db():
 if not _engine:return
 with _engine.begin() as c:
  c.execute(text('CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, payload JSONB NOT NULL)'))
  c.execute(text('CREATE TABLE IF NOT EXISTS outbox (id BIGSERIAL PRIMARY KEY, payload JSONB NOT NULL, delivered BOOLEAN NOT NULL DEFAULT FALSE)'))
def put(record):
 if not _engine:return record
 with _engine.begin() as c:c.execute(text('INSERT INTO records(id,payload) VALUES (:id,CAST(:p AS JSONB)) ON CONFLICT(id) DO UPDATE SET payload=EXCLUDED.payload'),{'id':record['id'],'p':json.dumps(record)})
 return record
def all_records():
 if not _engine:return []
 with _engine.begin() as c:return [r[0] for r in c.execute(text('SELECT payload FROM records ORDER BY id'))]
def enqueue(event):
 if _engine:
  with _engine.begin() as c:c.execute(text('INSERT INTO outbox(payload) VALUES (CAST(:p AS JSONB))'),{'p':json.dumps(event)})
