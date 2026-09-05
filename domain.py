from dataclasses import dataclass, asdict
from uuid import uuid4

@dataclass
class Asset:
    id: str
    name: str
    asset_class: str
    status: str = "active"

_assets: dict[str, Asset] = {}

def create_asset(name: str, asset_class: str):
    asset = Asset(str(uuid4()), name, asset_class)
    _assets[asset.id] = asset
    return asdict(asset)

def list_assets(): return [asdict(x) for x in _assets.values()]
