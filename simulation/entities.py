from dataclasses import dataclass
from enum import Enum

class EntityType(Enum):
    PLAYER = "🤖"
    TREE = "🌲"
    APPLE = "🍎"
    WOLF = "🐺"
    EMPTY = "⬜"

@dataclass
class Entity:
    id: int
    type: EntityType
    x: int
    y: int
    name: str = "Unknown"
    
    # We can add stats here later (Health, Energy, etc.)
    health: int = 100
    energy: int = 100