from math3d import VectorN
from SimpleTimer import SimpleTimer
from Projectile import Projectile
import json, math

class WriteWeapon(object):

    def __init__(self, owner, map, fileName="Hector Berlioz"):
        """
        This is the class used to write the data of a weapon's swing into a JSON file.

        I'm going to be editing the values in this class in order to create the JSON files manually for now.

        :param owner: the owner of the weapon.
        :return: N/A
        """

        self.mMap = map

        self.mWeaponCircleList = [

        ]
        self.mIsMelee = False

        self.mWriteFrameData = []
        self.mCurrentWrittenFrame = 0
        self.mFrameTime = 0

        self.mNewFileName = fileName

        self.mNumCircles = len(self.mWeaponCircleList)
        self.mNumFrames = 30
        self.mIsRotatable = True

        self.mWeaponCircleTravelData = []

        self.mCurHitDataTime = 0
        self.mCurFrame = 0
        self.mSwingTime = 4

        self.mOwner = owner

        self.mSwingTimer = SimpleTimer(self.mSwingTime, stopOnReach=True)

        self.mIsSwinging = False

        self.mReloadTime = .5
        self.mIsRanged = True
        self.mIsReloading = False
        self.mProjectileArgs = {
            "radius": 5,
            "originalOffsetLength": 0,
            "speed": 300,
            "originalAngle": 0,
            "maxRange": 100
        }
        self.mReloadTimer = SimpleTimer(self.mReloadTime, stopOnReach=True)

        self.mDamage = 50

        self.calculateSwingValues()

    def updateHitData(self, dtime):
        """
        This is an extension of Sword's function.

        All that's changed is I update the writeFrameData to include the new frame
        Also if the last frame is called I write the JSON file.

        :param dtime: timePassed since last update
        :return: None
        """

        self.mCurHitDataTime += dtime

        while self.mCurHitDataTime >= self.mFrameTime:
            self.mCurHitDataTime -= self.mFrameTime
            self.mCurFrame += 1

        if self.mCurFrame >= self.mNumFrames:
            self.mCurFrame = self.mNumFrames - 1

        if dtime > 0:
            if self.mCurFrame > self.mCurrentWrittenFrame:
                self.mCurrentWrittenFrame = self.mCurFrame
                self.writeFrame()

                if self.mCurFrame == self.mNumFrames - 1:
                    self.saveJSONFile()


    def writeFrame(self):
        """
        This function appends on to the writeFrameList the data of the current frame the WriteWeapon is on.
        :return: None
        """

        frame = []

        for i in range(self.mNumCircles):
            frame.append(self.mWeaponCircleList[i].getDict())


        self.mWriteFrameData.append(frame)


    def swing(self, angle):
        """
        This swings the sword. It will do any pre-swing rotation if needed as well.
        :param angle: angle of the player, not needed really.
        :return: None
        """

        if not self.mIsSwinging:
            self.mSwingTimer.start()
            self.mIsSwinging = True

            self.mCurFrame = 0

            for i in range(len(self.mWeaponCircleList)):
                self.mWeaponCircleList[i].reset()

        if not self.mIsReloading:
            self.mReloadTimer.start()
            self.mIsReloading = True

            direction = VectorN((math.cos(angle), math.sin(angle)))
            self.mMap.addProjectile(Projectile(self, direction, **self.mProjectileArgs))


    def saveJSONFile(self):
        """
        This converts the current data of the weapon into a JSON file.
        :return: None
        """
        if not self.mIsMelee:
            self.mWriteFrameData = None

        if self.mWriteFrameData:
            numFramesActual = len(self.mWriteFrameData)
        else:
            numFramesActual = 0

        if not self.mIsRanged:
            self.mProjectileArgs = None


        dataDict = {
            "weapon": {
                "hit data": {
                    "isMelee": self.mIsMelee,
                    "type": "prerendered",
                    "rotate": self.mIsRotatable,
                    "num circles": self.mNumCircles,
                    "num frames": numFramesActual,

                    "frames": self.mWriteFrameData,

                    },

                "ranged data": {
                    "isRanged": self.mIsRanged,
                    "reload time": self.mReloadTime,
                    "projectile args": self.mProjectileArgs
                }
            }
        }

        fp = open('weapons/'+self.mNewFileName+'.json', 'w')

        json.dump(dataDict, fp=fp, indent="\t", sort_keys=True)


    def calculateSwingValues(self):
        """
        This function calculates values such as SwingAngle and SwingDelta based on numFrames and timerLength etc.
        :return:
        """

        self.mFrameTime = self.mSwingTime / self.mNumFrames


    def getPos(self):
        """
        returns the current world position of the weapon origin.
        For now is just the player position.

        :return: world space position of the weapon origin.
        """


        return VectorN((self.mOwner.mX, self.mOwner.mY)).copy()


    def rotateSword(self, angle):
        """
        This basically just rotates every WeaponCircle in the sword
        :param angle: angle to rotate the sword for the original swing, in radians
        :return: None
        """

        for i in range(len(self.mWeaponCircleList)):
            self.mWeaponCircleList[i].rotateAboutOrigin(angle)


    def extendSword(self, lengthOffset, doFirst=False, doScale=True):
        """
        This function extends the length of all offsets of weaponCircles, except by default the first.
        This also defaults so that the further away a point is, the more it extends
        That way it functions almost like a hookshot.

        Without this is could function as a cone increase. IE: Fire blast

        :param lengthOffset: the amount to add to the length.
        :param doFirst: Whether to affect the first weaponCircle
        :param doScale: Whether to have it scale the further ones more, creating a scaling affect.
        :return: None
        """

        if doScale:
            if doFirst:
                for i in range(1, len(self.mWeaponCircleList)+1):
                    self.mWeaponCircleList[i-1].mCurOffsetLength += lengthOffset*i
            else:
                for i in range(len(self.mWeaponCircleList)):
                    self.mWeaponCircleList[i].mCurOffsetLength += lengthOffset*i

        else:
            if doFirst:
                for i in range(1, len(self.mWeaponCircleList)+1):
                    self.mWeaponCircleList[i-1].mCurOffsetLength += lengthOffset
            else:
                for i in range(len(self.mWeaponCircleList)):
                    self.mWeaponCircleList[i].mCurOffsetLength += lengthOffset


    def setWeaponCircleOffset(self, index, length, direction, radius=None):
        """
        This function is probably going to be used with the 'pre-rendered' hit data files, seperating the length and direction because speed
        :param index: which weaponCircle to modify
        :param length: new distance from origin
        :param direction: new direction, an assumed unitLength 2D VectorN
        :return: None
        """

        self.mWeaponCircleList[index].mCurOffsetLength = length
        self.mWeaponCircleList[index].mCurOffsetDir = direction

        if radius:
            self.mWeaponCircleList[index].mRadius = radius
            self.mWeaponCircleList[index].mRadius2 = radius*radius


    def update(self, dtime):
        """
        right now this will just update the swing timer

        but I have plans to update things like current swing angle, etc.
        Further down the line something like a path for the weapon to take, in an external file to be loaded in.
        :param dtime: time passed since the last update
        :return: None
        """

        self.mSwingTimer.update(dtime)
        self.mReloadTimer.update(dtime)

        if self.mIsSwinging:
            self.updateHitData(dtime)

        if self.mSwingTimer.mReached:
            self.mSwingTimer.reset()
            self.mIsSwinging = False

        if self.mReloadTimer.mReached:
            self.mReloadTimer.reset()
            self.mIsReloading = False


    def collideEntity(self, entity, dt):
        """
        This will run through all of the sword's WeaponCircles and check collision with the entity with all of them
        :param entity: an entity object
        :param dt: time passed since last update, probably a better place to apply force
        :return: a 1D vector if no collision, the point of collision otherwise.
        """

        for i in range(len(self.mWeaponCircleList)):
            if (not entity.mIsInvincible) and self.mIsSwinging:
                pointOfCollision = self.mWeaponCircleList[i].collideEntity(entity)


                if len(pointOfCollision) != 1:

                    entity.setInvincible()

                    # Apply a force on the entity from the point of collision
                    pointToEntityVector = (VectorN((entity.mX, entity.mY)) - pointOfCollision)
                    forcedir = pointToEntityVector.normalized_copy()

                    force = forcedir * self.mWeaponCircleList[i].mKnockBackForce

                    entity.setVelocity(forcedir * self.mWeaponCircleList[i].mKnockBackForce)

                    entity.mCurHealth -= self.mDamage
                    entity.getHit(force, self.mDamage)

                    return pointOfCollision

        else:
            return VectorN(1)


    def render(self, surface, camera):
        """
        For now all this does is render the weaponCircles

        :param surface: pygame.Surface object to render onto
        :param camera: a camera object, used for camera space conversion
        :return: None
        """

        if self.mIsSwinging:
            for i in range(len(self.mWeaponCircleList)):
                self.mWeaponCircleList[i].render(surface, camera)
