import pygame
from math3d import VectorN

class SpriteSheet(object):
    def __init__(self, grid, sheet, finishPos=None, maxTime = 1 / 20, repeat = False):
        """
        This is a utility class to help with animations.
        :return: N/A
        """


        self.mGridSize = grid
        self.mCurGridPos = VectorN(2)
        if not finishPos:
            self.mFinishPos = VectorN(self.mGridSize) - VectorN((1, 1))
        else:
            self.mFinishPos = finishPos

        self.mSheet = sheet
        self.mSheetSize = sheet.get_size()
        self.mSquareSize = (int(self.mSheetSize[0] / grid[0]),
                             int(self.mSheetSize[1] / grid[1]))

        self.MAX_TIME = maxTime
        self.mFrameTime = self.MAX_TIME / (self.mGridSize[0] * self.mGridSize[1] - (self.mGridSize[0] - self.mFinishPos[0]))

        self.mCurTime = 0

        self.mIsDone = False
        self.mDoRepeat = repeat

        self.mIsRunning = False


    def setMaxTime(self, newMax, reset=True):
        """
        This just sets self.MAX_TIME to a new value
        :param newMax: any float
        :param reset: a flag, if true reset's curtime and CurGridPos to 0
        :return: None
        """

        self.MAX_TIME = newMax
        self.mFrameTime = self.MAX_TIME / (self.mGridSize[0] * self.mGridSize[1])

        if reset:
            self.reset()


    def reset(self):
        """
        This just resets the needed values to set up for the next round of animation
        :return: None
        """

        self.mCurTime = 0
        self.mCurGridPos = VectorN(2)
        self.mIsDone = False


    def start(self):
        """
        This just sets self.mIsRunning to True
        :return: None
        """

        self.mIsRunning = True
        self.mIsDone = False

    def stop(self):
        """
        THis just sets self.mIsRunning to False
        :return: None
        """

        self.mIsRunning = False
        self.mIsDone = True


    def update(self, dtime):
        """
        Updates the animation of the sprite.
        :param dtime: change in time since last update
        """
        if not self.mIsDone and self.mIsRunning:
            self.mCurTime += dtime

            if self.mCurTime >= self.mFrameTime:

                self.mCurTime = 0

                self.mCurGridPos[0] += 1

                if self.mCurGridPos[0] >= self.mGridSize[0]:

                    self.mCurGridPos[0] = 0
                    self.mCurGridPos[1] += 1

                    if self.mCurGridPos[1] >= self.mGridSize[1]:
                        self.mIsDone = True

            if self.mCurGridPos == self.mFinishPos:
                self.mIsDone = True


            if self.mIsDone:
                if self.mDoRepeat:
                    self.mIsDone = False
                    self.mCurGridPos = VectorN(2)


    def getSprPos(self):
        """

        :return: a tuple representing the X and Y position of the sprite on the sprite sheet. Basically which frame of animation it's on.
        """
        x = self.mSquareSize[0] * self.mCurGridPos[0]
        y = self.mSquareSize[1] * self.mCurGridPos[1]

        return x, y


    def getCurImg(self):
        # returns a surface that contains the current sprite sheet square.
        # this is used for more accurate rotation of whatever is using the sprite sheet.

        # reference here:
        # http://stackoverflow.com/questions/6239769/crop-an-image-in-pygame-get-a-new-surface

        croppedSurface = pygame.Surface(self.mSquareSize).convert_alpha()
        croppedSurface.fill((0, 0, 0, 0))
        croppedSurface.blit(self.mSheet, (0, 0), (self.getSprPos(), self.mSquareSize))

        return croppedSurface
