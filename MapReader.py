import pygame
from math3d import VectorN
from TileClass import Tile
from Map import Map


# Define some constants here. Used for file reading things, instead of having to memorize the key codes
WALL_CODE = '1'
FLOOR_CODE = '0'

ENTRENCE_CODE = 'e'
ENTRENCE2_CODE = 'f'
ENTRENCE3_CODE = 'g'
ENTRENCE4_CODE = 'h'
EXIT_CODE = 'x'
INTERACTABLE_CODE = 'i'
OBSTACLE_CODE = 'b'
EMPTY_CODE = ' '
ENEMY_CODE = 'n'

PASSABLE = True
NOT_PASSABLE = False

class MapReader(object):
    """
    Class for reading map files and creating the map from the file.
    Creating maps includes:
        Creating the tiles
        Giving tiles their images/image references
        Using the contextual tiles algorithm to auto tile the walls
    """


    def __init__(self, tileSet, colorkey):
        """
        Won't pass in the map file info in the constructor.
        Eventually will need multiple for the creating of a whole dungeon, so I won't set it up that way now
        This class assumes the tilewidth to be 32
        :param tileSet: a loaded image, is the tile set
        :return: N/A
        """

        self.mTileWidth = 32

        self.mTileSet = tileSet
        self.mColorKey = colorkey

        self.mTileSet.set_colorkey(colorkey)

        self.mTileList = []

    def setTileSet(self, filepath, colorkey):
        """
        Set the current tileset of the map. Changes what the tile images become
        :param filepath: string containing the filepath of the new tileset
        :return:
        """

        self.mTileSet = pygame.image.load(filepath).convert()
        self.mColorKey = colorkey

    def loadMap(self, filepath):
        """
        loads a map to be set into tiles. map list contains lists with the contents of each line from the filepath
        Probably will only be called internally
        :param filepath: filepath of the map, a string.
        :return: a list containing the map data
        """

        mapFile = open(filepath)
        map = []

        for line in mapFile:

            map.append(line.strip("\n\r"))

        return map

    def autoTile(self, map):
        """
        creates the values for mapValues from map, which is eventually used to create spatially relevant tiles for walls
        this function is also probably internal
        :param map:
        :return: mapValues, a list of data to be used for spatially relevant tiles
        """

        mapValues = []

        #this loop creates and defines mapValues
        for r, row in enumerate(map):
            mapValues.append([]) # create a new row (one empty list for each list in map)
            for c, element in enumerate(row): # c is an index location, element is value at that location
                mapValues[-1].append(0)     # in the newest row, add a zero to the last element. going to be modified in the next if statement
                if map[r][c] == WALL_CODE:
                    if r > 0 and map[r-1][c] == WALL_CODE:               mapValues[r][c] += 1
                    if c < len(row)-1 and map[r][c+1] == WALL_CODE:      mapValues[r][c] += 2
                    if r < len(map)-1 and map[r+1][c] == WALL_CODE:      mapValues[r][c] += 4
                    if c > 0 and map[r][c-1] == WALL_CODE:               mapValues[r][c] += 8

        return mapValues

    def createTiles(self, map, mapValues):
        """
        this function will take data from map and mapValues and assign tiles their position and image.
        probably mostly an internal function
        :param map: a map list, made from loadMap
        :param mapValues: the mapValues list, mad from autoTile
        :return: a list of lists of tiles
        """

        tileList = []
        """
        this loop will create and fill tileList with tiles. Works similarly to the loop in autoTile
        in second for loop, the VectorN section determines the x and y location of the tile on the world map. vapValues
        [r] [c] * self.mTileWidth indicate where on the tile sheet the tile being used is, then the tile width is passed
        and tile set is passed
        """
        for r in range(len(map)):
            tileList.append([])
            for c in range(len(map[r])):
                if map[r][c] == WALL_CODE:
                    newTile = Tile(VectorN((c * self.mTileWidth, r * self.mTileWidth)), mapValues[r][c] * self.mTileWidth, 0, self.mTileWidth, WALL_CODE, self.mTileSet)
                    tileList[-1].append(newTile)
                elif map[r][c] == FLOOR_CODE or map[r][c] == ENEMY_CODE:
                    newTile = Tile(VectorN((c * self.mTileWidth, r * self.mTileWidth)), 0, self.mTileWidth, self.mTileWidth, FLOOR_CODE, self.mTileSet)
                    tileList[-1].append(newTile)
                elif map[r][c] == OBSTACLE_CODE:
                    newTile = Tile(VectorN((c * self.mTileWidth, r * self.mTileWidth)), 0, 0, self.mTileWidth, OBSTACLE_CODE, self.mTileSet)
                    tileList[-1].append(newTile)
                elif map[r][c] == ENTRENCE_CODE:
                    newTile = Tile(VectorN((c * self.mTileWidth, r * self.mTileWidth)), self.mTileWidth, self.mTileWidth, self.mTileWidth, ENTRENCE_CODE, self.mTileSet)
                    tileList[-1].append(newTile)
                elif map[r][c] == ENTRENCE2_CODE:
                    newTile = Tile(VectorN((c * self.mTileWidth, r * self.mTileWidth)), self.mTileWidth, self.mTileWidth, self.mTileWidth, ENTRENCE2_CODE, self.mTileSet)
                    tileList[-1].append(newTile)
                elif map[r][c] == ENTRENCE3_CODE:
                    newTile = Tile(VectorN((c * self.mTileWidth, r * self.mTileWidth)), self.mTileWidth, self.mTileWidth, self.mTileWidth, ENTRENCE3_CODE, self.mTileSet)
                    tileList[-1].append(newTile)
                elif map[r][c] == ENTRENCE4_CODE:
                    newTile = Tile(VectorN((c * self.mTileWidth, r * self.mTileWidth)), self.mTileWidth, self.mTileWidth, self.mTileWidth, ENTRENCE4_CODE, self.mTileSet)
                    tileList[-1].append(newTile)
                elif map[r][c] == EXIT_CODE:
                    newTile = Tile(VectorN((c * self.mTileWidth, r * self.mTileWidth)), self.mTileWidth, self.mTileWidth, self.mTileWidth, EXIT_CODE, self.mTileSet)
                    tileList[-1].append(newTile)
                elif map[r][c] == EMPTY_CODE:
                    newTile = Tile(VectorN((c * self.mTileWidth, r * self.mTileWidth)), 2 * self.mTileWidth, 0, self.mTileWidth, EMPTY_CODE, None)
                    tileList[-1].append(newTile)
        return tileList


    def getSpawn(self, tileList):
        spawnPoint = VectorN(2)
        for row in tileList:
            for tile in row:
                if tile.mType == ENTRENCE_CODE:
                    spawnPoint = VectorN(tile.mBoundingRect.center)

        return spawnPoint


    def createSurface(self, tileList):
        tSurf = pygame.Surface((len(tileList[0]) * tileList[0][0].mSprWidth, len(tileList[0]) * tileList[0][0].mSprWidth))

        for row in tileList:
            for tile in row:
                tile.render(tSurf, tile.mPos)

        return tSurf



    def makeMap(self, param):
        """
        This is the function called externally, returns a list of tiles.

        :param param: can either be a filepath, or an already built map text <<come up with a better name for this>>
        :return: a list of tiles
        """

        if isinstance(param, str):      # assuming any string passed in is a filepath
            map = self.loadMap(param)
        else:
            map = param

        mapValues = self.autoTile(map)
        tileList = self.createTiles(map, mapValues)

        return Map(tileList)

