import random
from typing import List, Optional, Tuple
from simulation.entities import Entity, EntityType

class GridWorld:
    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height
        self.entities: List[Entity] = []
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        
    def place_entity(self, entity: Entity):
        """Put an entity on the board if the spot is free."""
        if 0 <= entity.x < self.width and 0 <= entity.y < self.height:
            self.entities.append(entity)
            self.grid[entity.y][entity.x] = entity
            return True
        return False

    def move_entity(self, entity_id: int, dx: int, dy: int) -> str:
        """
        Attempts to move an entity. 
        Now handles EATING apples! 🍎
        """
        entity = next((e for e in self.entities if e.id == entity_id), None)
        if not entity: return "Entity not found"

        new_x = entity.x + dx
        new_y = entity.y + dy

        # 1. Check Boundaries
        if not (0 <= new_x < self.width and 0 <= new_y < self.height):
            return "Blocked: Out of bounds"

        # 2. Check Collisions
        target = self.grid[new_y][new_x]
        
        if target:
            # --- NEW LOGIC: EATING ---
            if target.type == EntityType.APPLE:
                # Remove the apple from the game
                if target in self.entities:
                    self.entities.remove(target)
                
                # Heal the player (Optional)
                entity.health = min(100, entity.health + 20)
                status_msg = "Crunch! Ate an Apple 🍎"
                
            # If it's NOT an apple (like a Tree or Wolf), stop.
            else:
                return f"Blocked: Collided with {target.type.name}"
        else:
            status_msg = "Moved successfully"

        # 3. Commit the Move
        self.grid[entity.y][entity.x] = None  # Clear old spot
        entity.x = new_x
        entity.y = new_y
        self.grid[new_y][new_x] = entity      # Set new spot
        
        return status_msg
    
    def move_wolves(self):
        """
        Simple AI: All wolves move 1 step towards the Player.
        """
        # 1. Find the Player
        player = next((e for e in self.entities if e.type == EntityType.PLAYER), None)
        if not player: return # Player is dead/gone

        # 2. Find all Wolves
        wolves = [e for e in self.entities if e.type == EntityType.WOLF]

        for wolf in wolves:
            # Calculate distance (dx, dy)
            dx = player.x - wolf.x
            dy = player.y - wolf.y
            
            # Decide move: Move in the direction of the largest gap
            # (If player is far right, move right. If far down, move down)
            step_x, step_y = 0, 0
            
            if abs(dx) > abs(dy):
                step_x = 1 if dx > 0 else -1 # Move Horizontal
            else:
                step_y = 1 if dy > 0 else -1 # Move Vertical
                
            # Try to move
            # Note: We use our existing move_entity function!
            # But we ignore the text result because wolves don't speak.
            
            # CHECK COLLISION: Did the wolf catch the player?
            if wolf.x + step_x == player.x and wolf.y + step_y == player.y:
                print("💀 CHOMP! The Wolf attacked Alex!")
                player.health -= 30 # Ouch!
                # We don't move the wolf INTO the player (that would delete the player),
                # we just stand next to them and bite.
            else:
                self.move_entity(wolf.id, step_x, step_y)

    def get_surroundings(self, entity_id: int) -> str:
        """
        The 'Eyes' of the AI. Returns text description of what is nearby.
        This is what we will feed to the LLM later!
        """
        entity = next((e for e in self.entities if e.id == entity_id), None)
        if not entity: return "Dead"
        
        view = []
        # Check 4 directions (North, South, East, West)
        # North is (0, -1) because Y gets smaller as you go UP in computer graphics.
        directions = [("North", 0, -1), ("South", 0, 1), ("East", 1, 0), ("West", -1, 0)]
        
        for name, dx, dy in directions:
            nx, ny = entity.x + dx, entity.y + dy
            # Check boundaries again (Can't see past the wall)
            if 0 <= nx < self.width and 0 <= ny < self.height:
                obj = self.grid[ny][nx]
                if obj:
                    view.append(f"{name}: {obj.type.name}") #i see apple

                else:
                    view.append(f"{name}: Empty") #i see grass
            else:
                view.append(f"{name}: Wall")
                
        return ", ".join(view)