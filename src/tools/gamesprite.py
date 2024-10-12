import pygame
from .spritesheet import Spritesheet

class Gamesprite():
    def __init__(self, path=None, state_count=1, sprite_counts=[1]):
        self.path = path
        self.spritesheet = Spritesheet(path)
        self.sprite_count = sprite_count
