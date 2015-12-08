import pygame
from math3d import VectorN
from entity import Entity
from Projectile import Projectile
from player import Player
import MapReader

class Map(object):
    
    def __init__(self, tiles):
        """
        This class will be the interface between the pane and the map. It was becomming a huge hassle to try and have 
        a list of tiles. This class should solve that.
        :param tiles: The tile list
        :return: N/A
        """
        
        self.mTiles = tiles
        self.mGridSize = [len(tiles[0]), len(tiles)]
        self.mTileWidth = self.mTiles[0][0].mSprWidth
        
        self.mTileSurface = self.preRenderTiles()

        self.mPlayerSpawnPoint = self.getSpawn()
        self.mEnemyList = []
        self.mItemList = []
        self.mProjectileList = []


    def addProjectile(self, projectile):
        """
        I wasn't sure if a function for this would be useful. Just decided to add it
        :param projectile: a Projectile object
        :return: None
        """

        self.mProjectileList.append(projectile)


    def preRenderTiles(self):
        """
        This function pre-renders self.mTiles into a big surface, a rectangle of this surface will be blitted
        After testing, we found this to be faster than blitting the individual tiles
        :return: a pygame.Surface object containing the rendered tiles.
        """

        tSurf = pygame.Surface((len(self.mTiles[0]) * self.mTiles[0][0].mSprWidth, len(self.mTiles) * self.mTiles[0][0].mSprWidth))

        for row in self.mTiles:
            for tile in row:
                tile.render(tSurf, tile.mPos)

        return tSurf


    def getSpawn(self):
        """
        :return: The center of the Entrence tile from the tile list.
        """
        spawnPoint = VectorN(2)
        for row in self.mTiles:
            for tile in row:
                if tile.mType == MapReader.ENTRENCE_CODE:
                    spawnPoint = VectorN(tile.mBoundingRect.center)
                    return spawnPoint


        return spawnPoint

    def getNewSpawn(self):
        spawnPoint = []
        for row in self.mTiles:
            for tile in row:
                if tile.mType == MapReader.ENTRENCE_CODE:
                    spawnPoint.append(tile.mBoundingRect.center[0])
                    spawnPoint.append(tile.mBoundingRect.center[1])
                if tile.mType == MapReader.ENTRENCE2_CODE:
                    spawnPoint.append(tile.mBoundingRect.center[0])
                    spawnPoint.append(tile.mBoundingRect.center[1])
                if tile.mType == MapReader.ENTRENCE3_CODE:
                    spawnPoint.append(tile.mBoundingRect.center[0])
                    spawnPoint.append(tile.mBoundingRect.center[1])
                if tile.mType == MapReader.ENTRENCE4_CODE:
                    spawnPoint.append(tile.mBoundingRect.center[0])
                    spawnPoint.append(tile.mBoundingRect.center[1])
        return spawnPoint


    def blitTiles(self, surface, rect, pos=VectorN(2)):
        surface.blit(self.mTileSurface, pos, rect)


    def collideWalls(self, list_or_entity):
        """
        this function detects and handles the collisions of either a list of entities or a single entity

        basically it just detects if there is a collision between the entity and all wall tiles near it
            then pushes the entity out of the wall, independently in the X and Y. This will produce the sliding affect
        :param list_or_entity: a list of entity objects or a single entity
        :return: None
        """

        if isinstance(list_or_entity, Entity):
            if isinstance(list_or_entity, Player) or list_or_entity.mType != 0:
                entityGridPos = self.worldToGrid(list_or_entity.mHitBox.center)

                #construct a list of the 9 tiles surrounding the entity. This will be used for efficient collision detection of all nine of them with pygame.

                # added a try statement to quickfix a nasty bug I don't understand. Not great, but good for now.
                try:
                    nineTileList = \
                        [
                            self.mTiles[entityGridPos[1]-1][entityGridPos[0]-1], self.mTiles[entityGridPos[1]-1][entityGridPos[0]], self.mTiles[entityGridPos[1]-1][entityGridPos[0]+1],
                            self.mTiles[entityGridPos[1]][entityGridPos[0]-1]  , self.mTiles[entityGridPos[1]][entityGridPos[0]]  , self.mTiles[entityGridPos[1]][entityGridPos[0]+1]  ,
                            self.mTiles[entityGridPos[1]+1][entityGridPos[0]-1], self.mTiles[entityGridPos[1]+1][entityGridPos[0]], self.mTiles[entityGridPos[1]+1][entityGridPos[0]+1]
                        ]
                except:
                    return


                collideTiles = []
                for idx, tile in enumerate(nineTileList):
                    if tile.mType == MapReader.WALL_CODE and list_or_entity.mHitBox.colliderect(tile.mBoundingRect):
                        collideTiles.append(idx)


                offset = [0, 0]
                for index in collideTiles:      # collidelistall returns the indices of the rectangles in the list.
                    # the offset will be determined based on the side of the nineTileList the index is at.
                    # left and right will only push left or right, top and bottom only up or down.

                    if index == 1:                # top middle
                        offset[1] = list_or_entity.mHitBox.top - nineTileList[index].mBoundingRect.bottom

                    if index == 3:
                        offset[0] = list_or_entity.mHitBox.left - nineTileList[index].mBoundingRect.right

                    if index == 5:
                        offset[0] = list_or_entity.mHitBox.right - nineTileList[index].mBoundingRect.left

                    if index == 7:
                        offset[1] = list_or_entity.mHitBox.bottom - nineTileList[index].mBoundingRect.top

                list_or_entity.mX -= offset[0]
                list_or_entity.mY -= offset[1]

                list_or_entity.mHitBox = pygame.Rect(list_or_entity.mX - 16, list_or_entity.mY - 16, 32, 32)

    def collideWallsP(self, list_or_entity):
        if isinstance(list_or_entity, Projectile):
            entityGridPos = self.worldToGrid(list_or_entity.getWorldPos())
            tile = self.mTiles[entityGridPos[1]][entityGridPos[0]]
            if tile.mType == MapReader.WALL_CODE:
                return True
            else:
                return False

    def worldToGrid(self, pos):
        """
        This function takes a world-space position and converts it to a grid position.
        :param pos: Position, in world space. A sequence type (list, tuple, VectorN, etc.)
        :return: VectorN corresponding to the grid position of pos
        """

        gridPosList = [pos[0] // self.mTileWidth, pos[1] // self.mTileWidth]

        gridPosList[0] = int(min(self.mGridSize[0], max(gridPosList[0], 0)))
        gridPosList[1] = int(min(self.mGridSize[1], max(gridPosList[1], 0)))

        return gridPosList