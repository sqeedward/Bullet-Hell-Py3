import math
import pygame

# angle of two vectors
def angle_pos(pos1, pos2):
    pos = pos2 - pos1
    return math.atan2(pos.y, pos.x)

def rad_to_deg(rad):
    return rad * 180 / math.pi

def deg_to_rad(deg):
    return deg / 180 * math.pi

def v2(x, y):
    return pygame.Vector2(x, y)

# returns the vector from center of rect1 to center of rect2
def translation_vector(rect1, rect2):
    vect = v2(rect2.centerx - rect1.centerx, rect2.centery - rect1.centery)
    # vect.normalize_ip()
    return vect

# vect to move rect2 out of rect1
def collision_translation_vect(rect1, rect2):
    overlap_x = 0

    # check if rects overlap on x axis
    if rect2.right > rect1.right:
        overlap_x = rect1.right - rect2.left
    elif rect2.left < rect1.left:
        overlap_x = rect1.left - rect2.right
    elif rect1.left <= rect2.left and rect1.right >= rect2.right:
        overlap_x = 0 
    
    # check if rects overlap on y axis
    overlap_y = 0
    if rect2.top < rect1.top:
        overlap_y = rect1.top - rect2.bottom
    elif rect2.bottom > rect1.bottom:
        overlap_y = rect1.bottom - rect2.top
    elif rect1.top <= rect2.top and rect1.bottom >= rect2.bottom:
        overlap_y = 0
    
    # if hitbox is smaller move it out of the other rect
    if rect1.left <= rect2.left and rect1.right >= rect2.right:
        return v2(0, overlap_y)
    
    if rect1.top <= rect2.top and rect1.bottom >= rect2.bottom:
        return v2(overlap_x, 0)
    
    # find the correct side to translate to
    if abs(overlap_x) < abs(overlap_y):
        return v2(overlap_x, 0)
    else:    
        return v2(0, overlap_y)
        
def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotate(surface, -angle)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

def rotatePivoted(im, angle, pivot):
    # rotate the leg image around the pivot
    image = pygame.transform.rotate(im, angle)
    rect = image.get_rect()
    rect.center = pivot
    return image, rect
