import pygame

#Primitive for all things that may appear in game

# Additional tips:
# GameObject subclasses will usually have a static variable "members", which will allow for easy access to all instances of that class
# For example, if you want to access all instances of the Collidable class, you can do so by using Collidable.members
# This is useful for collision detection, as you can check for collision between all instances of a class

# Try to limit how many classes have access to all instances since this could cause problems with memory management
# For example, if you have a class TreeTile inheriting Tile, and you just need to draw it, use the Tile.members to get the instances, and check there
# if it is an instance of TreeTile, and then do additional code, or use onBlit for it

# Dont use the del keyword, as it will only delete the reference to the object, instead
# call __del__() and let gc handle it, as there may be other references to the object


class GameObject:
    def __init__(self, pos, sprite):
        self.pos = pos
        self.sprite = sprite

    def move(self, vect):
        self.pos += vect

    def getPos(self):
        return self.pos

    def setPos(self, posv):
        self.pos = posv

    def onBlit(self):
        pass



class Collidable(GameObject):
    #static member
    members = []

    # maybe add a relative offset to the hitbox
    def __init__(self, pos, sprite, hitbox: pygame.rect.Rect):
        super().__init__(pos, sprite)
        self.hitbox = pygame.rect.Rect(hitbox)
        Collidable.members.append(self)
    
    def setPos(self, posv):
        self.pos = posv
        self.updateHitboxPos(self.pos)

    def updateHitboxPos(self, newPos):
        self.hitbox.update(newPos.x, newPos.y, self.hitbox.width, self.hitbox.height)

    # Override this
    # Argument: object that is collided with
    def onCollision(self, other):
        pass

    # dont override this unless there is a good reason, use onCollision to execute code
    def checkCollision(self):
        for obj in Collidable.members:
            if obj is not self:
                if self.hitbox.colliderect(obj.hitbox):
                    self.onCollision(obj)
                    obj.onCollision(self)

    def __del__(self):
        if self in Collidable.members:
            Collidable.members.remove(self)
