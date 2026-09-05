from fastapi.testclient import TestClient
from app import app
c=TestClient(app)
def test_health_ready_and_rbac():
 assert c.get('/health').status_code==200
 assert c.get('/ready').status_code==200
 assert c.get('/v1/assets').status_code==403
 assert c.get('/v1/assets',headers={'x-ung-permissions':'titan.assets.read'}).status_code==200
