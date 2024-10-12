from .entity import Entity
from .projectile import Projectile
import pygame

from ..tools import geometry as geo
import math
import random

SPAWN_DISTANCE = 20

class Enemy(Entity):

    def __init__(self, sprite, player, speed, health, pos = geo.v2(0,0), randomPos = False, animation = None):
        super().__init__(pos, sprite, animation, (pos.x, pos.y, 50, 50))
        self.player = player
        self.setEnemyStats(speed, health)
        if randomPos:
            self.randomSpawnRelativeToScren()
        if animation is not None:
            self.animation.mirrorImageLine(0)

    
    def setEnemyStats(self, speed, health):
        self.health = health
        self.speed = speed

    def damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.__del__()

    #Pur si simplu , inamicul se misca direct spre o pozitie, fara sa tina cont de obstacole
    def moveToPosSimplified(self):
        angle = geo.angle_pos(self.pos, self.player.getPos())
        xVel = self.speed * math.cos(angle)
        yVel = self.speed * math.sin(angle)
        enemyVel = geo.v2(xVel, yVel)

        self.setVel(enemyVel)

    def moveToPosition(self, posv, map):
        #Viitor A*
        pass


    #o sa facem ca caracterul sa poata lua o pozitie random in afara ecranului, la o distanta de x%, astfel sa nu apara
    #direct in ecran. TBH , nu e cel mai frumos cod dar functioneaza. also, victor e gae
    def randomSpawnRelativeToScren(self):
        screen = list(pygame.display.get_surface().get_size())
        
        zones = [[0, 1], [1, 0] , [-1, 0], [0, -1]]

        cZone = random.randint(0,len(zones)-1)
        randomPos = random.random()*2 - 1

        xPos = zones[cZone][0] * screen[0] // 2
        yPos = zones[cZone][1] * screen[1] // 2

        xPos += int(screen[0] * (SPAWN_DISTANCE / 100) * 0.5) * zones[cZone][0]
        yPos += int(screen[1] * (SPAWN_DISTANCE / 100) * 0.5) * zones[cZone][1]

        if zones[cZone][0] != 0:
            xPos += int(screen[0] * (SPAWN_DISTANCE / 100) * 0.5 * random.random()) * zones[cZone][0]
            yPos += int(screen[1] * ((SPAWN_DISTANCE / 100) + 1) * 0.5 * randomPos)
        else:
            xPos += int(screen[0] * ((SPAWN_DISTANCE / 100) + 1) * 0.5 * randomPos)
            yPos += int(screen[1] * (SPAWN_DISTANCE / 100) * 0.5 * random.random()) * zones[cZone][1]

        posV = geo.v2(xPos, yPos)
        posV += self.player.getPos()

        self.setPos(posV)

    def onTick(self, tickrate):
        self.moveToPosSimplified()
        super().onTick(tickrate)

    def onCollision(self, other):
        mtd = None
        
        if issubclass(type(other), Projectile):
            self.damage(other.getDamgage())
            return
        mtd = geo.collision_translation_vect(other.hitbox, self.hitbox)
        if mtd is not None:
            self.move(mtd)


#CONVENTIE, MOVEMENT RIGHT = 0 SAU 1 (DACA avem idle), LEFT = Right+1
    def onBlit(self):
        if self.vel.x >= 0 and self.animation.current_sheet != 0:
            self.animation.select_animation(0)
        elif self.vel.x < 0 and self.animation.current_sheet != 1:
            self.animation.select_animation(1)
        return super().onBlit()
    