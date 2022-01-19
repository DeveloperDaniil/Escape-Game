import os
import time

from drawing import Drawing
from interaction import Interaction
from player import Player
from ray_casting import ray_casting_walls
from sprite_objects import *

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface(MINIMAP_RES)

sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map, player, clock)
interaction = Interaction(player, sprites, drawing)
drawing.menu()
pygame.mouse.set_visible(False)
file = os.path.abspath("movies/start_movie.mp4")
pygame.quit()
os.startfile(file)
time.sleep(62)

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface(MINIMAP_RES)

sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map, player, clock)
pygame.mouse.set_visible(False)
interaction = Interaction(player, sprites, drawing)

interaction.play_music()

while True:
    player.movement()
    player.d_card()
    drawing.background(player.angle)
    walls, wall_shot = ray_casting_walls(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    # drawing.fps(clock)
    # drawing.mini_map(player)
    drawing.player_weapon([wall_shot, sprites.sprite_shot])

    interaction.interaction_objects()
    interaction.npc_action()
    interaction.clear_world()
    interaction.check_win()

    pygame.display.flip()
    clock.tick()
