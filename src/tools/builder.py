import pygame
from .animations import Animation
from .assetsloader import AssetLoader as al
from ..entities.enemy import Enemy
from . import geometry as geo
from ..entities import *

class Builder:
    tile_size = 64
    tiles_set = set()
    tile_img_set = set()
    build_mode = 0
    block_list = []
    tiles = ["iarba", "iarba1", "iarba3", "iarba4", "iarba5", "iarba6"]
    tiles_indx = 0

    def __init__(self, camera):
        self.camera = camera

    def initSpawnPos(self, posx, posy, block = 0):
        setVal = (posx, posy)
        self.tiles_set.add(setVal)
        setVal2 = (posx, posy, block)
        self.tile_img_set.add(setVal2)
        tile.BackgroundTile(geo.v2(posx, posy), al.getSprite(self.tiles[block],
                                        (0, 0, self.tile_size, self.tile_size)))

    def spawnAtPos(self, posx, posy):
        setVal = (posx, posy)
        if setVal not in self.tiles_set:
            setVal2 = (posx, posy, self.tiles_indx)
            self.tile_img_set.add(setVal2)
            # print(self.imgs)
            tile.BackgroundTile(geo.v2(posx, posy), al.getSprite(self.tiles[self.tiles_indx],
                                        (0, 0, self.tile_size, self.tile_size)))
            self.tiles_set.add(setVal)

    def spawnBlocks(self, pos):
        if self.build_mode == 0:
            posx = pos.x
            posy = pos.y
            self.spawnAtPos(posx, posy)

        if self.build_mode != 0:
             for i in range(-self.build_mode, self.build_mode+1):
                  for j in range(-self.build_mode, self.build_mode+1):
                        posx = pos.x + self.tile_size * i
                        posy = pos.y + self.tile_size * j
                        self.spawnAtPos(posx, posy)
    
    def change_tile(self):
        self.tiles_indx += 1
        self.tiles_indx = self.tiles_indx % len(self.tiles)

             
    
    def eventHandler(self, event):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos() + self.camera.getCenter()
            pos.x -= pos.x % self.tile_size;
            pos.y -= pos.y % self.tile_size;
            self.spawnBlocks(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.build_mode = 0
            elif event.key == pygame.K_e:
                self.build_mode += 1
            elif event.key == pygame.K_ESCAPE:
                self.save_map()
            elif event.key == pygame.K_1:
                self.change_tile()
            
    
    def save_map(self):
        with open("map.txt", "w") as map:
            for pos_img in self.tile_img_set:
                map.write(str(int(pos_img[0])) + " " + str(int(pos_img[1]))+ " " +str(int(pos_img[2])) +"\n")
        print(len(self.tiles_set))
    
    def load_map(self, mapPath):
        with open(mapPath, 'r') as map:
            for line in map:
                [posx,posy,bloc] = line.strip().split(" ")
                self.initSpawnPos(int(posx), int(posy), int(bloc))
                