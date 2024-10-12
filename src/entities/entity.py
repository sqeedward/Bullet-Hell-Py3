import pygame
from .gameobject import GameObject
from .gameobject import Collidable
from ..tools import geometry as geo
from ..tools import animations

class Entity(Collidable):
    members = []

    def __init__(self, pos, sprite, animation = None, hitbox=None):
        if hitbox is None:
            hitbox = (pos.x, pos.y, 10, 10)
        super().__init__(pos, sprite, hitbox)
        self.vel = geo.v2(0, 0)
        self.acc = geo.v2(0, 0)
        self.animation = animation
        if animation is not None:
            self.updateAnimation()
        Entity.members.append(self)
    
    def setVel(self, velv):
        self.vel = velv

    def addVel(self, velv):
        self.vel += velv
    
    def setAcc(self, accv):
        self.acc = accv

    def getSprite(self):
        return self.sprite

    def setHp(self, hp):
        self.hp = hp

    # code to be executed on tick
    def onTick(self, tickrate):
        self.updatePos(1/tickrate)
    
    # move along a vector
    def move(self, vect):
        self.pos += vect
        self.updateHitboxPos(self.pos)

    # move_to, simillar to setPos, but updates the hitbox, use this instead of setPos
    def move_to(self, pos):
        self.pos = pos
        self.updateHitboxPos(self.pos)

    def updatePos(self, dt):
        vect = dt * self.vel + dt*dt/2 * self.acc
        self.pos = self.pos + vect
        self.updateHitboxPos(self.pos)
    
    def updateAnimation(self):
        if self.animation is not None:
            self.sprite.image = self.animation.surface

    # code to be executed on blit
    def onBlit(self):
        if self.animation is not None:
            self.animation.update(self.sprite, 60, 0.3)

    def __del__(self):
        if self in Entity.members:
            Entity.members.remove(self)
        super().__del__()




        
