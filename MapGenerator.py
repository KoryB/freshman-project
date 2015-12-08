import random, math, copy, MapReader, enemy
from os import listdir
from Items import *

"""
TODO:
    create some sort of map creation constant module, full of all the codes we'll need
"""

# types of hermites
OFFPATH_CODE = 0
ONPATH_CODE = 1

ENTRANCE_CODE = 2
EXIT_CODE = 3




class Hermite(object):
    """
    class that contains basic hermite data
    a hermite is a subsection of the level
    """

    def __init__(self, value, type):
        """
        :param value: Value of the harmite, represents pathways. similar to neighbor sensitive tiles
        :param type: Type of hermite. see above for types.
        """

        self.mValue = value
        self.mType = type

        self.mSpecialChar = MapReader.FLOOR_CODE	# default value for a special char will just be a floor code

        self.mIsSpecial = True						# defaults to true, will be made false if not special

        if self.mType == ENTRANCE_CODE:
            self.mSpecialChar = 'e'
        elif self.mType == EXIT_CODE:
            self.mSpecialChar = 'x'
        else:
            self.mIsSpecial = False

        self.mTextList = self.getText()


    def getText(self):
        """
        just a simple function to retrieve and return a text document containing the layout of the hermite.
        also adds an entrance/exit if the hermite is that kind of hermite
        """
        filepath = "hermite files/" + str(self.mValue) + "/" + str(random.randint(0, len(listdir("hermite files/" + str(self.mValue))) - 1)) + ".txt"

        hermiteFile = open(filepath)
        hermiteText = []

        for line in hermiteFile:
            hermiteText.append(list(line.strip("\n\r")))

        hermiteFile.close()

        if self.mIsSpecial:
            hermiteText = self.addSpecialCharacters(hermiteText)


        return hermiteText


    def addSpecialCharacters(self, textList):
        """
        based on the type of hermite that calls this function is, will add a special character that is needed for that hermite
        """

        # while looping through the list, special attention will be payed to the last available tile.
        # If upon completion there hasn't been a special character placed yet, the special character will be placed there

        lastPos = VectorN((0, 0))
        placed = False
        for r in range(len(textList)):
            for c in range(len(textList[r])):
                if textList[r][c] != MapReader.WALL_CODE:
                    lastPos = VectorN((r, c))
                    if random.random() < .1:
                        # the conditions are like this:
                        # if it's not a wall code do a check, 10% of the time it will insert the special char and break

                        textList[r][c] = self.mSpecialChar
                        placed = True
                        break
            if placed:
                break

        if not placed:
            textList[lastPos.iTuple()[0]][lastPos.iTuple()[1]] = self.mSpecialChar

        return textList

class MapGenerator(object):
    """
    Class to generate a map text file. Read by MapReader to create the tiles for the map
    """

    def __init__(self):
        self.mHermiteList = []
        self.mEnemyImg = pygame.image.load("imgs/enemysprite.png").convert_alpha()


    def __str__(self):
        """
        returns numbers of the hermite types. in a grid form
        """

        returnStr = ""

        for row in self.mHermiteList:
            for hermite in row:
                returnStr += str(hermite.mType) + " "

            returnStr += "\n"

        return returnStr


    def makePath(self, param):
        """
        internal function to create a single path on the path list. returns a series of VectorN's corresponding
        to the position of the rooms in that path.

        can either pass in a start/end pos, or a dim;
        if dim, then the start/end poses will be random

        the type checking is not very rigorous, it assumes param[0]=param[1]

        :param param: either a tuple of start/end pos, or a dim of the level.
        :return: a list of VectorN's corresponding to the points on the path
        """

        startPos, endPos = VectorN(2), VectorN(2)

        if isinstance(param[0], int):
            # a dim was passed. create random start/end points
            startPos = VectorN((random.randint(0, param[0] - 1), random.randint(0, param[1] - 1)))
            endPos = VectorN((random.randint(0, param[0] - 1), random.randint(0, param[1] - 1)))

            while endPos == startPos:		# we don't want entrance and exit in same hermite
                endPos = VectorN((random.randint(0, param[0] - 1), random.randint(0, param[1] - 1)))

        elif isinstance(param[0], VectorN):
            # start/end pos were passed in

            startPos, endPos = param[0], param[1]

        else:
            # neither were passed, return an empty list
            return list()

        pathList = []


        pathPos = startPos.copy()		# current path position

        # start making the path
        # the plan is to find the change in rows/columns from start to end (subtract vectors)
        # then from these values, go in that direction (depending on sign of drow/dcol)
        # subtracting from drow/dcol until one gets to zero, then finish it off

        deltaVector = endPos - startPos

        deltaSignList = [math.copysign(1, deltaVector[0]), math.copysign(1, deltaVector[1])]	# sign of the elements in deltaVector

        while deltaVector.magnitude() != 1 and not deltaVector.isZero():
            # decide on changing row/column
            dir = random.randint(0, 1)		# 0 == row, 1 == column

            if dir == 0:	# if changing row
                if deltaVector[0] != 0:
                    deltaVector[0] -= deltaSignList[0]

                    pathPos[0] += deltaSignList[0]	   # current pos of the path

                    pathList.append(pathPos.copy())

            else:		# if changing col
                if deltaVector[1] != 0:
                    deltaVector[1] -= deltaSignList[1]

                    pathPos[1] += deltaSignList[1]	   # current pos of the path

                    pathList.append(pathPos.copy())

        return pathList


    def makePaths(self, dim, numPaths=4):
        """
        Changes self.mHermite list to the values of the types of hermite it is.
        Values are similar to Neighbor Sensitive Tiling

        :param dim: dimension of the level
        :param numPaths: number of paths, including the main path. defaults to 4 (just the main box). MUST BE AT LEAST FOUR
        :return: list of types of hermites, and a list of the values of those hermites.
        """

        # if numPaths is less than four, just return two empty lists
        if numPaths < 4:
            return [], []

        # setup some variables

        valueList = copy.deepcopy(self.mHermiteList)
        typeList = copy.deepcopy(valueList)

        # The first step in making paths is to set up the box corners
        boxPosList = []
        newPos = VectorN(2)
        for i in range(4):
            canPlace = False
            while not canPlace:
                newPos = VectorN((random.randint(0, dim[0] - 1), random.randint(0, dim[1] - 1)))

                for pos in boxPosList:
                    if newPos == pos:
                        break
                else:
                    canPlace = True

            boxPosList.append(newPos.copy())

        # Set the startPos and endPos to some of the boxPoints
        possibleStartEndPos = list(range(4))
        random.shuffle(possibleStartEndPos)
        startPos = boxPosList[possibleStartEndPos.pop()]
        endPos = boxPosList[possibleStartEndPos.pop()]

        # make the paths
        paths = []

        for i in range(numPaths):
            if i < 3:
                # first make the box path
                paths.extend(self.makePath((boxPosList[i], boxPosList[i+1])))

            elif i == 3:
                # connect the first and final boxPoint
                paths.extend(self.makePath((boxPosList[0], boxPosList[-1])))
            else:
                # all others are random
                paths.extend(self.makePath(dim))

        # set the types based on paths
        for pathPos in paths:
            typeList[pathPos.iTuple()[0]][pathPos.iTuple()[1]] = 1

        # create values and types for entrance and exit. doing this last so that they aren't overwritten
        typeList[startPos.iTuple()[0]][startPos.iTuple()[1]], typeList[endPos.iTuple()[0]][endPos.iTuple()[1]] = ENTRANCE_CODE, EXIT_CODE




        # make value list from type list
        neighborList = (ONPATH_CODE, ENTRANCE_CODE, EXIT_CODE)
        for r in range(len(typeList)):
            for c in range(len(typeList[r])):
                curHermite = typeList[r][c]
                if curHermite in neighborList:		# if curHermite is one of onpath/entrance/exit
                    if r > 0 and typeList[r-1][c] in neighborList:	        			 valueList[r][c] += 1
                    if c < len(typeList[r])-1 and typeList[r][c+1] in neighborList:		 valueList[r][c] += 2
                    if r < len(typeList)-1 and typeList[r+1][c] in neighborList:    	 valueList[r][c] += 4
                    if c > 0 and typeList[r][c-1] in neighborList:				         valueList[r][c] += 8


        return typeList, valueList


    def makeHermites(self, typeList, valueList):
        """
        creates hermites from typelist and valuelist
        internal function
        :param typeList: matrix of types
        :param valueList: matrix of values
        :return:
        """

        for r in range(len(typeList)):
            for c in range(len(typeList[r])):
                self.mHermiteList[r][c] = Hermite(valueList[r][c], typeList[r][c])


    def createTextFile(self):
        """
        this function creates the final map file from the hermites.
        :return:
        """

        # first get all the text files into one place
        hermiteTextFiles = []

        for row in self.mHermiteList:
            hermiteTextFiles.append([])
            for hermite in row:
                hermiteTextFiles[-1].append(hermite.mTextList)

        # then combine them, stitching them together by row
        finalTextList = []

        for rowOfHermitesIndex in range(len(hermiteTextFiles)):
            for hermiteLineIndex in range(len(hermiteTextFiles[rowOfHermitesIndex][0])):		#number of lines in a hermite
                finalTextList.append([])
                for hermiteIndex in range(len(hermiteTextFiles[rowOfHermitesIndex])):			#number of hermites in a row
                    finalTextList[-1].extend(hermiteTextFiles[rowOfHermitesIndex][hermiteIndex][hermiteLineIndex])


        return finalTextList


    def spawnEnemies(self, numEnemies, mapObject):

        enemyList = []

        curEnemies = 0

        while curEnemies < numEnemies:
            # get a position to test
            #TODO:
            #   do the ecgc strat to eliminate any mega-hordes spawning. Context sensitive enemy spawns :D (kinda)

            tX, tY = random.randint(1, mapObject.mGridSize[0]-1), random.randint(1, mapObject.mGridSize[1]-1)

            if mapObject.mTiles[tX][tY].mType != MapReader.FLOOR_CODE:
                continue    # picked a bad spot, try again

            enemyPos = mapObject.mTiles[tX][tY].mBoundingRect.topleft
            enemyType = random.randint(0, 3)

            enemyList.append(enemy.Enemy(self.mEnemyImg, enemyPos[0], enemyPos[1], enemyType, mapObject))

            curEnemies += 1

        mapObject.mEnemyList.extend(enemyList)


    def spawnItems(self, numItems, mapObject):

        itemList = []

        curItems = 0

        while curItems < numItems:
            # get a position to test
            # TODO:
            #   do the ecgc strat to eliminate any mega-hordes spawning. Context sensitive item spawns :D (kinda)

            tX, tY = random.randint(1, mapObject.mGridSize[0]-1), random.randint(1, mapObject.mGridSize[1]-1)

            if mapObject.mTiles[tX][tY].mType != MapReader.FLOOR_CODE:
                continue    # picked a bad spot, try again

            itemPos = VectorN(mapObject.mTiles[tX][tY].mBoundingRect.topleft)
            itemType = random.randint(0, 33)
            newItem = getItemFromType(itemType)
            newItem.mPos = itemPos

            itemList.append(newItem)

            curItems += 1

        mapObject.mItemList.extend(itemList)


    def generateMap(self, dim, tileset, colorkey=(0,0,0)):
        """
        generate the Map text file.
        :param dim: dimension of the map (in hermites). Num rows x num Columns
        :return: map text file
        """

        # fill the hermite list with zeros according to dim.

        zeroList = [0] * dim[1]
        for i in range(dim[0]):
            self.mHermiteList.append(copy.deepcopy(zeroList))

        t, v = self.makePaths(dim, 9)

        self.makeHermites(t, v)

        mapTextList = self.createTextFile()

        mr = MapReader.MapReader(tileset, colorkey)
        map = mr.makeMap(mapTextList)

        #POPULATE THE MAP
        self.spawnEnemies(30, map)
        self.spawnItems(30, map)

        return map
