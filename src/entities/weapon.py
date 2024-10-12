import pygame
import numpy
from .projectile import *
from .gameobject import GameObject
from ..tools import geometry as geo
import math


class Weapon(GameObject):
    def __init__(self, pos, sprite):
        super().__init__(pos, sprite)
        self.original_image = sprite.image
        self.angle = 0

    


# When adding new weapons, they should inherit the weapon class!

# About general arguments of the functions:
        # proj_speed: the speed of the projectile
        # proj_count: the number of projectiles fired
        # spread: the spread of the projectiles, in radians
        # the middle being the angle of the weapon
        # thus, the spread will range from (angle - spread/2) to (angle + spread/2)        


class Shotgun(Weapon):
    def __init__(self, proj_speed=30, proj_count=3, spread=math.pi/6):
        super().__init__(geo.v2(0, 0), al.getSprite("shotgun", (0, 0, 100, 32), -1))
        self.proj_speed = proj_speed
        self.proj_count = proj_count
        self.spread = spread
        self.offset = geo.v2(30, 0)
    
    # Fire from pos, with center of spread at angle
    def fire(self, pos, angle):
        pos = self.pos + geo.v2(43, 12).rotate(geo.rad_to_deg(-self.angle)) 
        print(self.pos)
        print(pos)
        # add code here to return in case of no ammo
        # or in case there haven't passed enough ticks since last shot

        # compute the angle between each projectile
        step = self.spread / self.proj_count
        # start angle is the angle of the first projectile
        start = angle - (self.spread/2)
        for i in range(self.proj_count):
            # compute velocity vector
            velx = self.proj_speed * math.cos(start)
            vely = self.proj_speed * math.sin(start)
            
            # create actual proj
            pellet = Pellet(geo.v2(pos.x, pos.y))
            pellet.setVel(pygame.Vector2(velx, vely))

            # iterate to next angle
            start += step
    
    def setAngle(self, angle):
        self.angle = angle
        self.sprite.image, self.sprite.rect = geo.rotate(self.original_image, geo.rad_to_deg(angle), geo.v2(0, 0), geo.v2(0, 0))
#de test, ca sa ma obisnuiesc cu notatiile lui rotaru / functiile create
#acceleratie doar ca sa verific daca functioneaza functia de viteza

class Sniper(Weapon):
    def __init__ (self, proj_speed = 800, proj_count = 1):
        super().__init__(geo.v2(0, 0), al.getSprite("sniper", (0, 0, 120, 46), -1))
        self.proj_speed = proj_speed
        self.proj_count = proj_count

    def fire (self, pos, angle):
        pos = self.pos + geo.v2(40, 12).rotate(geo.rad_to_deg(-self.angle)) 
        start = angle
        velx = self.proj_speed * math.cos(start)
        vely = self.proj_speed * math.sin(start)

        pellet = Bullet(geo.v2(pos.x, pos.y))
        pellet.setVel(pygame.Vector2(velx, vely))

        return [pellet]
    
    def setAngle(self, angle):
        self.angle = angle
        self.sprite.image, self.sprite.rect = geo.rotatePivoted(self.original_image, geo.rad_to_deg(-angle), geo.v2(40, 12))

# Arrow is a projectile, maybe make this a Bow class?
class Arrow:
    def __init__ (self, proj_speed = 30):
        self.proj_speed = proj_speed

    def fire (self, pos, angle):
        start = angle
        velx = self.proj_speed * math.cos(start)
        vely = self.proj_speed * math.sin(start)

        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface([10, 2])
        sprite.image.fill(pygame.Color(0, 0, 0))
        pellet = Pellet(sprite)
        pellet.setPos(pygame.Vector2(pos.x, pos.y))
        pellet.setVel(pygame.Vector2(velx, vely))

        return [pellet]

class Gun:
    def __init__ (self, proj_speed=30, accuracy = 1, max_angle = math.pi/3):
        self.proj_speed = proj_speed
        self.accuracy = accuracy
        self.max_angle = max_angle

    def fire(self, posx, posy, angle):
        rand_angle = 2 * np.random.rand() * self.max_angle - self.max_angle
        start = angle + (1 - self.accuracy) * rand_angle
        velx = self.proj_speed * math.cos(start)
        vely = self.proj_speed * math.sin(start)

        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface([5, 5])
        sprite.image.fill(pygame.Color(0, 0, 0))
        pellet = Pellet(geo.v2(posx, posy), sprite)
        pellet.setPos(pygame.Vector2(posx, posy))
        pellet.setVel(pygame.Vector2(velx, vely))

        return [pellet]