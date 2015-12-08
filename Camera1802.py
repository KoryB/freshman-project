import pygame
from math3d import VectorN


class Camera(object):
    def __init__(self, x, y, w, h, mapsize, map):
        self.position = VectorN([x, y])
        self.width = w
        self.height = h
        self.mBoundingRect = pygame.Rect(x, y, w, h)
        self.mapSize = mapsize
        self.mMap = map

    def setTileMap(self, newtilemap):
        self.tilemap = newtilemap

    def setMap(self, newMap, mapsize):
        """
        This sets the camera map to a new Map object
        :param newMap: a Map object
        :return: None
        """

        self.mMap = newMap
        self.mapSize = mapsize

    def getOnscreenEnemies(self):
        """
        I wasn't really sure where to put this function, I figured the camera over the map.
        The map didn't have a reference to the pane it was in, and I didn't want to limit it to only being in one pane.

        :return: a list of Enemies, in self.mMap.mEnemyList that are on screen
        """

        onScreenEnemies = []
        for i in range(len(self.mMap.mEnemyList)):
            if self.mBoundingRect.colliderect(self.mMap.mEnemyList[i].mHitBox):
                onScreenEnemies.append(self.mMap.mEnemyList[i])

        return onScreenEnemies

    def update(self, playerX, playerY, surf):
        x = playerX - surf.get_width()/2
        y = playerY - surf.get_height()/2
        if 0 < x < self.mapSize[0] - surf.get_width():
            self.position[0] = x
        elif x < 0:
            self.position[0] = 0
        else:
            self.position[0] = self.mapSize[0] - surf.get_width()
        if 0 < y < self.mapSize[1] - surf.get_height():
            self.position[1] = y
        elif y < 0:
            self.position[1] = 0
        else:
            self.position[1] = self.mapSize[1] - surf.get_height()

        self.mBoundingRect.topleft = self.position.iTuple()

    def render(self, surface):
        surface.blit(self.mMap.mTileSurface, (0,0), self.mBoundingRect)