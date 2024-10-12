import pygame
import os


class AssetLoader:
    paths = {
        "player" : os.path.normpath("src/assets/sprites/entities/player.png"),
        "grass" : os.path.normpath("src/assets/sprites/tiles/grass.png"),
        "goblin": os.path.normpath("src/assets/sprites/entities/goblin.png"),
        "fireball": os.path.normpath("src/assets/sprites/entities/fireball.png"),
        "snoppy": os.path.normpath("src/assets/sprites/entities/snoop_dogg.png"),
        "petru": os.path.normpath("src/assets/sprites/entities/petru_griffon_alearga.png"),
        "iarba": os.path.normpath("src/assets/sprites/tiles/iarba.png"),
        "test_tile": os.path.normpath("src/assets/sprites/tiles/test.png"),
        "iarba1": os.path.normpath("src/assets/sprites/tiles/iarba1.png"),
        "iarba2": os.path.normpath("src/assets/sprites/tiles/iarba2.png"),
        "iarba3": os.path.normpath("src/assets/sprites/tiles/iarba3.png"),
        "iarba4": os.path.normpath("src/assets/sprites/tiles/iarba4.png"),
        "iarba5": os.path.normpath("src/assets/sprites/tiles/iarba5.png"),
        "iarba6": os.path.normpath("src/assets/sprites/tiles/iarba6.png"),
        "shotgun": os.path.normpath("src/assets/sprites/weapons/shotgun.png"),
        "sniper": os.path.normpath("src/assets/sprites/weapons/sniper.png"),
        "bullet": os.path.normpath("src/assets/sprites/weapons/bullet.png")
    }
    loaded = {
        
    }
    @staticmethod
    # Returns the image from the given path and caches it
    def getImage(name):
        if name in AssetLoader.loaded:
            sprite = AssetLoader.loaded[name]
        else:
            sprite = pygame.image.load(AssetLoader.paths[name]).convert()
            AssetLoader.loaded[name] = sprite
        return sprite

    @staticmethod
    # gets a sprite/surface from an image
    def getSprite(name, rectangle, colorkey=None):
        sprite = AssetLoader.getImage(name)

        # "Loads image from x,y,x+offset,y+offset"
        
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert()
        image.blit(sprite, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        out = pygame.sprite.Sprite()
        out.image = image
        return out