from ..tools import geometry as geo
from .gameobject import GameObject
from .gameobject import Collidable
from enum import Enum


class Tile(GameObject):
    tiles = []
    def __init__(self, pos, sprite):
        super().__init__(pos, sprite)
        Tile.tiles.append(self)

class CollidableTile(Collidable):
    def __init__(self, pos, sprite, hitbox):
        super().__init__(pos, sprite, hitbox)

class BackgroundTile(Tile):
    def __init__(self, pos, sprite):
        super().__init__(pos, sprite)

class Border(CollidableTile):
    border = []
    def __init__(self, pos, sprite, hitbox):
        super().__init__(pos, sprite, hitbox)

        # is this really needed?
        # we already have a reference in both collidable and tile
        Border.border.append(self)
    #do not move
    def onCollision(self, other):
        pass
    


    
    