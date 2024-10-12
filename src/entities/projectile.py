from .entity import Entity
from .player import Player
import numpy as np
from ..tools.animations import Animation
from ..tools.assetsloader import AssetLoader as al

class Projectile(Entity):
    def __init__(self, pos, sprite, dmg=0):
        super().__init__(pos, sprite, animation = None, hitbox = (pos.x, pos.y, 10, 10))
        self.dmg = dmg # damage
        self.cnt = 0 # tick counter, used to delete the projectile after a certain amount of ticks
        self.seconds_alive = 2 # seconds that we want the projectile to be alive, seconds * tickrate > cnt

    def getDamgage(self):
        return self.dmg
    
    def onCollision(self, other):
        # Do not delete the projectile if it collides with another projectile or the player
        if issubclass(type(other), Projectile):
            return
        if type(other) is Player:
            return
        # Note: dont call "del self" since we need the object for the other
        # onCollision call, the gc will take care of it
        else: 
            self.__del__()

    def onTick(self, tickrate):
        # maybe add here subticks for more precise collision detection

        self.cnt += 1
        if self.cnt > self.seconds_alive * tickrate:
            self.__del__()
        super().onTick(tickrate)
    

class Pellet(Projectile):
    def __init__(self, pos):
        super().__init__(pos, al.getSprite("bullet", (0, 0, 12, 12), -1), 20)

class Bullet(Projectile):
    def __init__(self, pos):
        super().__init__(pos, al.getSprite("bullet", (0, 0, 12, 12), -1), 100)