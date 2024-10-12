import pygame
import math
from .entities import *
from .entities import gameobject
import sys
from enum import Enum
from .tools import camera
from .tools import geometry as geo
from .tools.animations import Animation
from .tools.assetsloader import AssetLoader as al
from .tools.builder import Builder

class GameStates(Enum):
    PAUSED = 0
    RUNNING = 1
    QUIT = 2

playerAnimation = None

class GameEngine:
    def __init__(self, width, height):
        global playerAnimation
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Petru Griffon x Ghiu Simulator")
        self.clock = pygame.time.Clock()
        self.state = GameStates.PAUSED
        self.entities = []
        self.drawables = []
        self.camera = camera.Camera(geo.v2(0, 0), geo.v2(width, height))
        self.tickrate = 60
        self.framerate = 60
        self.ticks = 0
        self.enemy_spawn_tick_cnt = 100

        self.map_width = 60
        self.map_height = 60
        self.tile_size = 32
        self.builder = Builder(self.camera)
        self.init_background()

        playerAnimation = Animation(al.getImage("player"),32,32,[13,8],2)

        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface([64, 64])
        sprite.image.fill(pygame.Color(255, 0, 0))
        self.player = player.Player(geo.v2(200,200), sprite , playerAnimation)
        self.player.addWeapon(weapon.Shotgun(proj_speed=1000, proj_count=7))
        self.player.addWeapon(weapon.Sniper(proj_speed=2000, proj_count=1))
        self.entities.append(self.player)

        # self.barrier_ex = tile.Border(geo.v2(0, 0), (0, 0, 10 , 10))


        # self.barrier_ex = tile.Border(geo.v2(-50, -50), al.getSprite("test_tile", (0, 0, 100, 100)), (-50, -50, 100, 100))
        
        batAnimation = Animation(al.getImage("petru"),64,64)
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface([10, 10])
        sprite.image.fill(pygame.Color(255, 0, 0))
        self.enemy = enemy.Enemy(sprite, self.player, 100, 0, animation= batAnimation, randomPos=True)

    def handle_events(self):
        velocity = 500

        for event in pygame.event.get():
            self.builder.eventHandler(event)
            # ar merge un keyhandler aici
            if event.type == pygame.QUIT:
                self.state = GameStates.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.addVel(geo.v2(0, -velocity))
                if event.key == pygame.K_a:
                    self.player.addVel(geo.v2(-velocity, 0))
                if event.key == pygame.K_s:
                    self.player.addVel(geo.v2(0, velocity))
                if event.key == pygame.K_d:
                    self.player.addVel(geo.v2(velocity, 0))
                if event.key == pygame.K_q:
                    self.player.nextWeapon()
                if event.key == pygame.K_p:
                    self.state = GameStates.PAUSED
                    self.pause() 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.addVel(geo.v2(0, velocity))
                if event.key == pygame.K_a:
                    self.player.addVel(geo.v2(velocity, 0))
                if event.key == pygame.K_s:
                    self.player.addVel(geo.v2(0, -velocity))
                if event.key == pygame.K_d:
                    self.player.addVel(geo.v2(-velocity, 0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    self.player.fire(geo.angle_pos(self.camera.getCenter(), mouse_pos))
                    pos2 = mouse_pos + self.camera.getRealCenter()
    




    def render(self):
        mouse_pos = pygame.mouse.get_pos()

        # Render game graphics here
        self.camera.setPos(self.player.getPos())
        self.screen.fill((0 ,128,0))  # Fill screen with white for simplicity

        # sprite = pygame.sprite.Sprite()
        # sprite.image = pygame.Surface([64, 64])
        # sprite.image.fill(pygame.Color(255, 0, 0))
        # self.camera.draw_raw(self.screen, sprite.image, self.player.getPos())
        #for img in self.drawables:
        #    self.camera.draw(img)
        self.draw_background()
        # self.camera.draw(self.screen, self.barrier_ex)
        
        
        for ent in entity.Entity.members:
            self.camera.draw(self.screen, ent)

        self.player.updateCurrentWeapon(geo.angle_pos(self.camera.getCenter(), mouse_pos))

        self.camera.draw(self.screen, self.player.getWeapon())
        pygame.display.flip()       #Comentariu

    def tick(self):
        #tick logic here
        self.player.checkCollision()
        # print(len(gameobject.Collidable.members))
        
        self.camera.setPos(self.player.getPos())

        #TREBUIE STERS --------------------------------

        if self.ticks % self.enemy_spawn_tick_cnt == 0:
            batAnimation = Animation(al.getImage("petru"),64,64)
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.Surface([10, 10])
            sprite.image.fill(pygame.Color(255, 0, 0))
            self.enemy = enemy.Enemy(sprite, self.player, 100, 100, animation= batAnimation, randomPos=True)
        # #TREBUIE STERS --------------------------------
        # batAnimation = Animation(al.getImage("petru"),64,64)
        # sprite = pygame.sprite.Sprite()
        # sprite.image = pygame.Surface([10, 10])
        # sprite.image.fill(pygame.Color(255, 0, 0))
        # self.enemy = enemy.Enemy(sprite, self.player, 100, 0, animation= batAnimation, randomPos=True)
        # self.entities.append(self.enemy)
        # # #TREBUIE STERS --------------------------------
        
        for ent in entity.Entity.members:
            ent.onTick(self.tickrate)
            ent.checkCollision()
        return None

    def run(self):
        while self.state != GameStates.QUIT:
            self.handle_events()
            self.render()
            self.ticks += 1
            
            if self.ticks % (self.framerate // self.tickrate) == 0:
                self.tick()


            self.clock.tick(self.framerate)  # Cap the frame rate to 60 FPS

        pygame.quit()
        sys.exit()

    def pause(self):
        while(self.state == GameStates.PAUSED):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = GameStates.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = GameStates.RUNNING
            self.render()

    def init_background(self):
        self.builder.load_map("map.txt")

    def draw_background(self):
        for i in tile.Tile.tiles:
            self.camera.draw(self.screen, i)
        # redundant
        for i in tile.Border.border:
            self.camera.draw(self.screen, i)


