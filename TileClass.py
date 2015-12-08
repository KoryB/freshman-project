import pygame

class Tile:

    WALL_CODE = "1"
    FLOOR_CODE = "0"
    ENTRANCE_CODE = "e"
    EXIT_CODE = "x"


    def __init__(self, posvector, x, y, width, type, spritesheet):
        """
        :param posvector: the position vector of the tile
        :param x: the x pos on the spritesheet that the tile will blit from
        :param y: the y pos on the spritesheet that the tile will blit from
        :param width: the width of the tiles
        :param passable: A boolean, Whether or not the tile can be walked over
        :param spritesheet: the image with all the sprites
        """
        self.mPos = posvector
        self.mSpr = spritesheet
        self.mSprX = x
        self.mSprY = y
        self.mSprWidth = width
        self.mType = type
        self.mBoundingRect = pygame.Rect(self.mPos.iTuple(), (self.mSprWidth, self.mSprWidth))

    def render(self, surface, pos):
        """ Renders on the given surface at the given position
        """
        if self.mSpr is not None:
            surface.blit(self.mSpr, pos.iTuple(), (self.mSprX, self.mSprY, self.mSprWidth, self.mSprWidth))
