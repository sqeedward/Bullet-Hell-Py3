import pygame



class Camera:
    #pygame.vector2 args
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.center = pos - size/2
        self.rect = pygame.rect.Rect(pos.x, pos.y, size.x, size.y)
    
    def setCenter(self, center):
        self.center = center
        self.pos = center + self.size/2
    
    # Absolute center 
    def getRealCenter(self):
        return self.center

    # Relative to view center
    def getCenter(self):
        return self.size/2

    def setPos(self, pos):
        self.pos = pos
        self.center = pos - self.size/2
        self.rect.update(self.center.x, self.center.y, self.size.x, self.size.y)
    
    def getPos(self):
        return self.pos

    #obj must be GameObject descendant
    def draw(self, screen, obj):
        pos = obj.getPos()
        # Optimization, if the object is not in the camera view, dont draw it
        if not self.rect.colliderect((pos.x, pos.y, obj.sprite.image.get_width(), obj.sprite.image.get_height())):
            return
        
        # Call any subroutine that has to be done before blitting
        obj.onBlit()

        # blit the sprite
        screen.blit(obj.sprite.image, (pos.x - self.center.x, pos.y - self.center.y))

    
    # draw a surface to the screen
    def draw_raw(self, screen, img, pos):
        screen.blit(img, (pos.x - self.center.x, pos.y - self.center.y))
        
