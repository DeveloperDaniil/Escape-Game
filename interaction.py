import os
import threading

import pygame
import pyglet
from numba import njit

from map import world_map
from ray_casting import mapping
from settings import *


@njit(fastmath=True, cache=True)
def ray_casting_npc_player(npc_x, npc_y, blocked_doors, world_map, player_pos):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    # verticals
    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map or tile_v in blocked_doors:
            return False
        x += dx * TILE

    # horizontals
    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map or tile_h in blocked_doors:
            return False
        y += dy * TILE
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.cong = True

    def interaction_objects(self):

        for obj in sorted(self.sprites.list_of_objects, key=lambda obj: obj.distance_to_sprite):
            x, y = self.player.pos
            if self.player.card and obj.flag == 'door_v':
                obj.door_open_trigger = True
                obj.blocked = None
            if (2751.4117991496555 < x < 2794.3185249468675) and \
                    (1305.4698377235816 < y < 1385.5701163093422) and \
                    self.player.card and \
                    obj.flag == 'door_h':
                obj.door_open_trigger = True
                obj.blocked = None
            if (126.56118126540473 < x < 327.03186469940954) and \
                    (621.2959097142761 < y < 676.6902760766659) and self.cong:
                b = threading.Thread(target=self.viet_cong, name='B', daemon=True)
                b.start()
                self.cong = False
            if (124.42980694077735 < x < 175.55093524554078) and \
                    (460.362434219678 < y < 602.603500169018):
                self.Viet_Death()

    def viet_cong(self):
        song = pyglet.media.load('sound/Viet Cong.mp3')
        song.play()

    def npc_action(self):
        for obj in self.sprites.list_of_objects:
            if obj.flag == 'npc' and not obj.is_dead:
                if ray_casting_npc_player(obj.x, obj.y,
                                          self.sprites.blocked_doors,
                                          world_map, self.player.pos):
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                else:
                    obj.npc_action_trigger = False

    def npc_move(self, obj):
        if abs(obj.distance_to_sprite) > TILE:
            dx = obj.x - self.player.pos[0]
            dy = obj.y - self.player.pos[1]
            obj.x = obj.x + 1 if dx < 0 else obj.x - 1
            obj.y = obj.y + 1 if dy < 0 else obj.y - 1

    def clear_world(self):
        deleted_objects = self.sprites.list_of_objects[:]
        [self.sprites.list_of_objects.remove(obj) for obj in deleted_objects if obj.delete]

    def play_music(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('sound/theme.mp3')
        pygame.mixer.music.play(10)

    def Viet_Death(self):
        file = os.path.abspath("movies/hallway_movie.mp4")
        pygame.quit()
        os.startfile(file)

    def check_win(self):
        x, y = self.player.pos
        if (2124.2502488849636 < x < 2476.1029519530352) and \
                (1024.862939374329 < y < 1775.4744483801185):
            file = os.path.abspath("movies/end_movie.mp4")
            pygame.quit()
            os.startfile(file)
            # pygame.mixer.music.stop()
            # pygame.mixer.music.load('sound/win.mp3')
            # pygame.mixer.music.play()
            # while True:
            #    for event in pygame.event.get():
            #        if event.type == pygame.QUIT:
            #            exit()
            #    self.drawing.win()
