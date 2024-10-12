import pygame
import numpy as np
from .spritesheet import Spritesheet

"""
This class returns a surface from an array image. It takes the size of each picture, the pictures per
animation sheet. An animation sheet is a vector of pictures that are concatenated into an image.
Specify the amount of pictures to take and the current animation index we want.
"""
class AnimationSheet:
    surface = None
    anim_row = 0
    current_sheet = 0
    


    """
    Constructorul pentru animation sheet, in animations intra o matrice de animatii, sub format imagine, lsita sau np.array.
    width - height se refera la dimensiunea fiecarei imagini, ex: o animatie poate avea width = 64, heigth = 64,
    pictures per line spune cate imagini avem pe fiecare linie, ex prima animatie poate avea 8, a doua doar 4, o sa avem
    pictures_per_line = [8,4], count = nr_imagini, current = animatia curenta, scales pt dimensiuni
    """
    def __init__(self, width, height, animations=[], pictures_per_line=[], count=0, current=0, xscale = 100, yscale = 100):
        self.width = width
        self.height = height
        self.animations = animations
        self.xscale = xscale
        self.yscale = yscale

        if count == 0:
            self.anim_count = len(animations) // height
        else:
            self.anim_count = count

        if pictures_per_line == [] :
            self.rows = [len(animations[0]) // width] * self.anim_count
        else:
            self.rows = pictures_per_line

        self.animations = [[] for _ in range(self.anim_count)]
        for i in range(self.anim_count):
            sheet = animations[height * i: height * (i + 1)]
            images = [self.cutImageFromSheet(sheet, j) for j in range(self.rows[i])]
            self.animations[i] = images

        self.current_sheet = current
        self.surface = self.animations[current][0]


    """
    Concatenam un set de animatii, bun daca vrem sa avem mai multi inamici pe o imagine
    """
    def add_animation_sheet(self, sheet, amount):
        self.anim_count += 1
        self.rows.append(sheet)
        images = [self.cutImageFromSheet(sheet, i) for i in range(amount)]
        self.animations.append(images)


    """
    Selectam animatie exact pe care o vrem, de exemplu putem de pe linia 5 sa luam imaginea3.
    """
    def select_animation(self, animation_line, pic_num=0):
        self.current_sheet = animation_line % self.anim_count
        self.anim_row = pic_num % self.rows[pic_num]
        self.surface = self.animations[self.current_sheet][self.anim_row]


    """
    Dintr-un sheet de imagini luam fiecare imagine in parte si o bagam intr-o lista.
    Vom avea o lista de imagini.
    """
    def cutImageFromSheet(self, sheet, image_num):
        current_image = np.array(sheet)
        img = current_image[:, image_num * self.width: (image_num + 1) * self.width]
        img = np.transpose(img, (1, 0, 2))  # Because x and y are swapped

        surface = pygame.surfarray.make_surface(img)
        surface = pygame.transform.scale(surface, (self.xscale, self.yscale))
        surface.set_colorkey((0, 0, 0))

        return surface

    """
    Functia care aduce efectul de animatie, da shift prin linia curenta sa arate fiecare animatie
    """

    def next(self):
        self.anim_row += 1
        if self.anim_row == self.rows[self.current_sheet]:
            self.anim_row = 0
        self.surface = self.animations[self.current_sheet][self.anim_row]



    """
    Dam mirror la un animation sheet, bun daca vrem animatii pt fiecare directie
    """    
    def mirrorImageLine(self, line):
        sheetLine = self.animations[line]
        newLine = []

        for i in range(len(sheetLine)):
            newLine.append(pygame.surfarray.array3d(sheetLine[i]))
            newLine[i] = pygame.surfarray.make_surface(newLine[i][::-1])
            newLine[i] = pygame.transform.scale(newLine[i], (self.xscale, self.yscale))
            newLine[i].set_colorkey((0, 0, 0))



        new_animation_set = [self.animations[i] for i in range(line+1)]
        new_animation_set.append(newLine)

        newRows = [self.rows[i] for i in range(line+1)]
        newRows.append(self.rows[line])

        for i in range(line+1, len(self.animations)):
            new_animation_set.append(self.animations[i])
            newRows.append(self.rows[i])
        
        self.animations = new_animation_set
        self.rows = newRows

        self.anim_count += 1


        


"""
This is the same class as AnimationSheet, but it takes the input as a path.
"""
class Animation(AnimationSheet):
    ticks = 0
    def __init__(self, path, width, height, pictures_per_line=[], count=0, current=0, xscale=100, yscale=100):
        animations = Spritesheet(path)
        array = pygame.surfarray.pixels3d(animations.sheet)
        normal_array = np.transpose(array, (1, 0, 2))  # Swap x and y
        super().__init__(width, height, normal_array, pictures_per_line, count, current, xscale , yscale)

    def update(self, sprite, tickrate, seconds):
        self.ticks += 1
        if self.ticks % int(seconds * tickrate) == 0: #we update every second we give, can be float
            self.ticks = 0
            self.next()
            sprite.image = self.surface

    def tickUpdate(self, sprite, ticks): #if we want to calculate the update time directly with ticks
        self.ticks += 1
        if self.ticks % ticks == 0:
            self.ticks = 0
            self.next()
            sprite.image = self.surface

    def nextAnimation(self):
        if self.animation is not None:
            self.animation.next()
            self.updateAnimation()
    

