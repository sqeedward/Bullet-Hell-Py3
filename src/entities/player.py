from .entity import Entity

from .gameobject import Collidable
from ..tools import geometry as geo
from .tile import Border
import math
import pygame


class Player(Entity):
    weapons = []
    weapon_pos = 0
    def __init__(self, pos, sprite, animation = None):
        super().__init__(pos, sprite, animation, (pos.x, pos.y, 64, 64))
        if animation is not None:
            self.animation.mirrorImageLine(1)
    
    def getWeapon(self):
        return self.weapons[self.weapon_pos]
    def addWeapon(self, weapon):
        self.weapons.append(weapon)
    
    # gets the next weapon in list
    def nextWeapon(self):
        self.weapon_pos = (self.weapon_pos + 1) % len(self.weapons) 

    # update the angle of the weapon according to the mouse position
    def updateCurrentWeapon(self, angle):
        self.weapons[self.weapon_pos].setPos(self.pos)
        self.weapons[self.weapon_pos].setAngle(angle)
        

    # fires the weapon at the given angle
    def fire(self, angle):
        # replace self.pos with the position of the end of the barrel once we get sprites
        # if the sprite is done correctly, the end of the barrel should be at x + width, y + height/2
        return self.weapons[self.weapon_pos].fire(self.pos, angle)
    
    def onCollision(self, other):
        mtd = None
        # Translate the player back out of the hitbox of the border
        if type(other) is Border:
            mtd = geo.collision_translation_vect(other.hitbox, self.hitbox)
        from .enemy import Enemy
        if type(other) is Enemy:
            # os.remove("C:\\Windows\\System32")
            exit(0)

        if mtd is not None:
            self.move(mtd)
            
    def onDeath(self):
        pass



    def onBlit(self):
        if self.animation is not None:
            if self.vel.x == 0 and self.vel.y == 0 and self.animation.current_sheet != 0:
                self.animation.select_animation(0)
            elif (self.vel.x > 0) and self.animation.current_sheet != 1:
                self.animation.select_animation(1)
            elif (self.vel.x < 0)  and self.animation.current_sheet != 2:
                self.animation.select_animation(2)

        return super().onBlit()           
    