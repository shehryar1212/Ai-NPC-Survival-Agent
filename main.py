import pygame
import sys
from simulation.world import GridWorld
from simulation.entities import Entity, EntityType
from simulation.brain import NPCBrain
from dotenv import load_dotenv

load_dotenv()

# Configuration
TILE_SIZE = 60 
GRID_W, GRID_H = 10, 10
SCREEN_W = GRID_W * TILE_SIZE
SCREEN_H = GRID_H * TILE_SIZE + 60 # Bottom UI Bar

# Colors
COLORS = {
    "BG": (245, 245, 245),             # Off-White
    "GRID": (220, 220, 220),           # Light Grey
    "UI_BG": (30, 30, 30),             # Dark UI
    "TEXT": (255, 255, 255),           # White Text
    "HEALTH_BG": (100, 0, 0),          # Dark Red
    "HEALTH_FG": (0, 200, 0)           # Bright Green
}

def draw_ui(screen, font, player):
    """Draws a professional bottom UI panel."""
    # Draw Dark Panel
    ui_rect = (0, SCREEN_H - 60, SCREEN_W, 60)
    pygame.draw.rect(screen, COLORS["UI_BG"], ui_rect)
    
    if player:
        # 1. Name & Status
        name_text = font.render(f"🤖 {player.name} | Status: Active", True, COLORS["TEXT"])
        screen.blit(name_text, (20, SCREEN_H - 45))
        
        # 2. Health Bar
        bar_width = 200
        fill_width = int((player.health / 100) * bar_width)
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (300, SCREEN_H - 40, bar_width + 4, 24), 2)
        # Background
        pygame.draw.rect(screen, COLORS["HEALTH_BG"], (302, SCREEN_H - 38, bar_width, 20))
        # Fill
        pygame.draw.rect(screen, COLORS["HEALTH_FG"], (302, SCREEN_H - 38, fill_width, 20))
        
        # Health Text Overlay
        hp_text = font.render(f"{player.health}%", True, (255, 255, 255))
        screen.blit(hp_text, (300 + bar_width + 15, SCREEN_H - 45))
        
    else:
        dead_text = font.render("💀 STATUS: DECEASED", True, (255, 50, 50))
        screen.blit(dead_text, (20, SCREEN_H - 45))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Generative NPC Simulation (DeepSeek)")
    clock = pygame.time.Clock()
    
    # Fonts
    ui_font = pygame.font.SysFont("Segoe UI", 20, bold=True)
    # Emoji Font: Segoe UI Emoji works best on Windows for icons
    emoji_font = pygame.font.SysFont("Segoe UI Emoji", int(TILE_SIZE * 0.6)) 

    # 1. Initialize World
    world = GridWorld(GRID_W, GRID_H)
    
    # 2. Add Entities
    player = Entity(id=1, type=EntityType.PLAYER, x=5, y=5, name="Alex")
    world.place_entity(player)

    # Initialize Brain
    try:
        brain = NPCBrain(player_name="Alex")
        print("🧠 Brain initialized successfully.")
    except:
        brain = None
        print("⚠️ Brain connection failed.")

    # Setup Scenario
    world.place_entity(Entity(2, EntityType.TREE, 2, 2))
    world.place_entity(Entity(3, EntityType.TREE, 8, 1))
    world.place_entity(Entity(4, EntityType.TREE, 3, 7))
    world.place_entity(Entity(5, EntityType.APPLE, 6, 5))
    world.place_entity(Entity(6, EntityType.APPLE, 1, 8))
    world.place_entity(Entity(7, EntityType.WOLF, 5, 2))

    running = True
    game_over = False

    while running:
        # A. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and not game_over:
                # SPACE: AI Turn
                if event.key == pygame.K_SPACE:
                    if brain:
                        vision = world.get_surroundings(player.id)
                        move = brain.decide(vision, player.health)
                        
                        if move:
                            print(f"💡 Thought: {move.get('thought')}")
                            world.move_entity(player.id, move.get('dx',0), move.get('dy',0))
                            world.move_wolves()
                            if player.health <= 0: game_over = True

                # ENTER: Wait
                elif event.key == pygame.K_RETURN:
                    print("⏳ Waiting...")
                    world.move_wolves()
                    if player.health <= 0: game_over = True

        # B. Drawing
        screen.fill(COLORS["BG"])
        
        # Draw Grid
        for x in range(0, SCREEN_W, TILE_SIZE):
            pygame.draw.line(screen, COLORS["GRID"], (x, 0), (x, SCREEN_H - 60))
        for y in range(0, SCREEN_H - 60, TILE_SIZE):
            pygame.draw.line(screen, COLORS["GRID"], (0, y), (SCREEN_W, y))

        # Draw Entities (As Emojis!)
        for entity in world.entities:
            # 1. Calculate Position
            x_pos = entity.x * TILE_SIZE
            y_pos = entity.y * TILE_SIZE
            
            # 2. Render Emoji
            # We access the .value of the Enum (e.g., "🐺")
            emoji_surf = emoji_font.render(entity.type.value, True, (0, 0, 0))
            
            # 3. Center the Emoji in the Tile
            rect = emoji_surf.get_rect(center=(x_pos + TILE_SIZE//2, y_pos + TILE_SIZE//2))
            screen.blit(emoji_surf, rect)

        # Game Over Overlay
        if game_over:
            s = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            screen.blit(s, (0,0))
            msg = ui_font.render("💀 SIMULATION ENDED: AGENT ELIMINATED", True, (255, 50, 50))
            text_rect = msg.get_rect(center=(SCREEN_W//2, SCREEN_H//2))
            screen.blit(msg, text_rect)

        # UI Panel
        draw_ui(screen, ui_font, player)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()