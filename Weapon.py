from math3d import VectorN
from WeaponCircle import WeaponCircle
from SimpleTimer import SimpleTimer
from Projectile import Projectile
from SpriteSheet import SpriteSheet
import math
import json, pygame, random

class Weapon(object):

    GENERIC_SWORD_ANIMATION = pygame.transform.smoothscale(pygame.image.load("imgs/Animations/Attack7.png").convert_alpha(), (320, 128))
    GENERIC_SWORD_ANIMATION_LENGTH = 20

    GENERIC_WIND_ANIMATION = pygame.transform.smoothscale(pygame.image.load("imgs/Animations/Special6.png").convert_alpha(), (550, 220))
    GENERIC_WIND_ANIMATION_LENGTH = 0

    GENERIC_FIRE_ANIMATION = pygame.transform.smoothscale(pygame.image.load("imgs/Animations/Special12.png").convert_alpha(), (550, 400))
    GENERIC_FIRE_ANIMATION_LENGTH = 50

    GENERIC_ICE_ANIMATION = pygame.transform.smoothscale(pygame.image.load("imgs/Animations/Heal5.png").convert_alpha(), (300, 180))
    GENERIC_ICE_ANIMATION_LENGTH = 0

    GENERIC_BOW_ANIMATION = pygame.transform.smoothscale(pygame.image.load("imgs/Animations/Sword4.png").convert_alpha(), (300, 180))
    GENERIC_BOW_ANIMATION_LENGTH = 35

    OVERLAY_FONT = pygame.font.SysFont("Times New Roman", 14)

    def __init__(self, owner, fileName="testWeapon", damage=50, damageRange=(.8, 1.2), reloadRange=(.8, 1.2)):
        """
        eventually this class will inherit from weapon (and probably melee or something)
        but I don't exactly know what it will need yet :S
        :param owner: owner of the weapon, used to get the origin point of the weapon.
        :return: N/A
        """

        self.mWeaponCircleList = []
        self.mWeaponCircleTravelData = []
        self.mProjectileArgs = {}
        self.mNumFrames = 0
        self.mNumCircles = 0
        self.mReloadTime = 0
        self.mIsRotateWeapon = True
        self.mFreezeCircles = True
        self.mHudImg = None
        self.mManaCost = 0
        self.mFileName = fileName
        self.mSwingTime = 1
        
        self.mDamageRange = damageRange
        self.mReloadRange = reloadRange

        self.mIsMelee = False
        self.mIsRanged = False

        self.mBaseMeleeDamage = 0
        self.mBaseRangedDamage = 0

        self.mAnimationType = ""
        self.mAnimationGrid = []
        self.mAnimationGridEndPos = 0
        self.mAnimationOriginalAngle = 0

        self.mSwingingAngle = 0

        self.mFrameTime = 0

        self.mOwner = owner

        self.loadWeaponData("weapons/" + fileName + ".json")

        self.mCurHitDataTime = 0
        self.mCurFrame = 0

        self.mSwingTimer = SimpleTimer(self.mSwingTime, stopOnReach=True)
        self.mIsSwinging = False

        self.mShootTimer = SimpleTimer(self.mSwingTime, stopOnReach=True)
        self.mIsShooting = False

        self.mReloadTimer = SimpleTimer(self.mReloadTime, stopOnReach=True)
        self.mIsReloading = False

        self.mSpriteSheet = SpriteSheet(self.mAnimationGrid, getattr(Weapon, self.mAnimationType), self.mAnimationGridEndPos, maxTime=self.mSwingTime)
        self.mSpriteSheet.start()
        self.mAnimationLength = getattr(Weapon, self.mAnimationType + "_LENGTH")

        self.mDamage = damage

        if self.mNumFrames != 0:
            self.mFrameTime = self.mSwingTime / self.mNumFrames
        else:
            self.mFrameTime = 0

        self.updateHitData(0, init=True)

        for i in range(self.mNumCircles):
            self.mWeaponCircleList[i].resetOriginal()


        if owner:
            self.setPlayer(owner)


    def getMap(self):

        return self.mOwner.mMap


    def loadWeaponData(self, filepath):
        """
        This function loads the json file for the weapon and sets all of the attributes the make everything work
        :param filepath: a string representing the filepath
        :return: None
        """

        file = open(filepath)
        jsonFile = json.load(file)

        jsonHitData = jsonFile['weapon']['hit data']
        jsonRangedData = jsonFile['weapon']['ranged data']
        jsonAnimation = jsonFile['weapon']['animation']
        jsonFrames = jsonHitData['frames']
        self.mNumFrames = jsonHitData['num frames']
        self.mNumCircles = jsonHitData['num circles']
        self.mIsRotateWeapon = jsonHitData['rotate']
        self.mFreezeCircles = jsonHitData['freeze']
        self.mIsMelee = jsonHitData['isMelee']
        self.mIsRanged = jsonRangedData['isRanged']
        self.mProjectileArgs = jsonRangedData['projectile args']

        meleeKnockBack = jsonHitData['knockback']

        self.mReloadTime = jsonRangedData['reload time']
        self.mManaCost = jsonFile['weapon']['mana cost']

        self.mBaseMeleeDamage = jsonHitData['base damage']
        self.mSwingTime = jsonAnimation['time']

        self.mAnimationType = jsonAnimation['type']
        self.mAnimationGrid = jsonAnimation['grid']
        self.mAnimationGridEndPos = VectorN(jsonAnimation['end'])
        self.mAnimationOriginalAngle = jsonAnimation['original angle']

        if self.mIsRanged:
            self.mProjectileArgs['damage'] *= random.uniform(self.mDamageRange[0], self.mDamageRange[1])
            self.mReloadTime *= random.uniform(self.mReloadRange[0], self.mReloadRange[1])

        self.mBaseMeleeDamage *= random.uniform(self.mDamageRange[0], self.mDamageRange[1])

        for i in range(self.mNumCircles):
            self.mWeaponCircleList.append(WeaponCircle(self, freezeOrigin=self.mFreezeCircles, knockBackForce=meleeKnockBack))

        tmpFrames = []

        for i in range(self.mNumFrames):
            tmpFrames.append([])

            for j in range(self.mNumCircles):
                tmpFrames[-1].append((VectorN(jsonFrames[i][j]['pos']), jsonFrames[i][j]['radius']))

        self.mWeaponCircleTravelData = tmpFrames


    def setPlayer(self, player):
        hudImgFP = json.load(open("weapons/" + self.mFileName + ".json"))['weapon'].get('hud image')
        self.mHudImg = pygame.transform.scale(pygame.image.load(hudImgFP), (45, 45))

        self.mOwner = player


    def getPos(self):
        """
        returns the current world position of the weapon origin.
        For now is just the player position.

        :return: world space position of the weapon origin.
        """

        return VectorN((self.mOwner.mX, self.mOwner.mY))


    def stopSwinging(self):
        """
        This terminates the swing of the weapon/shooting/reloading etc. Useful for when the owner dies
        """

        self.mIsSwinging = False
        self.mIsShooting = False
        self.mIsReloading = False


    def swing(self, angle):
        """
        Starts swinging the sword
        Starts the swing timer, and signals to check collision with the world.

        :param angle: angle to rotate the sword for the original swing, in radians
        :return: None
        """

        if self.mOwner.mCurMana > self.mManaCost or self.mManaCost == 0:
            self.mOwner.mCurMana -= self.mManaCost
            self.mOwner.mCurMana = max(0, self.mOwner.mCurMana)

            if self.mIsMelee and not self.mIsSwinging:
                self.mSwingTimer.reset()
                self.mSwingTimer.start()
                self.mIsSwinging = True

                self.mSpriteSheet.reset()

                self.mCurFrame = 0
                self.mSwingingAngle = angle

                for i in range(len(self.mWeaponCircleList)):
                    self.mWeaponCircleList[i].reset()

            if self.mIsRanged:
                if not self.mIsReloading:
                    self.mReloadTimer.reset()
                    self.mReloadTimer.start()
                    self.mIsReloading = True

                    self.mSwingingAngle = angle

                    direction = self.getVectorFromAngle(angle)
                    self.getMap().addProjectile(Projectile(self, direction, **self.mProjectileArgs))

                if not self.mIsShooting:
                    self.mShootTimer.reset()
                    self.mShootTimer.start()
                    self.mIsShooting = True

                    self.mSpriteSheet.reset()


    @staticmethod
    def getVectorFromAngle(angle):
        """
        THis function is modeled off of the rotate about origin function in the weaponCircles.
        It uses the optimized version.
        :param angle: angle, in Radians
        :return: a unit length Vector2
        """

        if angle == math.pi * 0.25:
            sinAngle = WeaponCircle.SQRT_2_OVER_2
            cosAngle = WeaponCircle.SQRT_2_OVER_2
        elif angle == math.pi * 0.50:
            sinAngle = 1
            cosAngle = 0
        elif angle == math.pi * 0.75:
            sinAngle = WeaponCircle.SQRT_2_OVER_2
            cosAngle = -WeaponCircle.SQRT_2_OVER_2
        elif angle == math.pi:
            sinAngle = 0
            cosAngle = -1
        elif angle == math.pi * 1.25:
            sinAngle = -WeaponCircle.SQRT_2_OVER_2
            cosAngle = -WeaponCircle.SQRT_2_OVER_2
        elif angle == math.pi * 1.50:
            sinAngle = -1
            cosAngle = 0
        elif angle == math.pi * 1.75:
            sinAngle = -WeaponCircle.SQRT_2_OVER_2
            cosAngle = WeaponCircle.SQRT_2_OVER_2
        else:
            sinAngle = 0
            cosAngle = 1

        return VectorN((cosAngle, sinAngle))


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


    def updateHitData(self, dtime, init=False):
        """
        This function updates the hitData timer and if the timer overflows updates the hitData to the next frame

        :param dtime: time passed since the last update
        :return: None
        """

        if self.mIsMelee:
            self.mCurHitDataTime += dtime

            while self.mCurHitDataTime >= self.mFrameTime:
                self.mCurHitDataTime -= self.mFrameTime
                self.mCurFrame += 1

            if self.mCurFrame >= self.mNumFrames:
                self.mCurFrame = self.mNumFrames - 1

            for i in range(len(self.mWeaponCircleList)):
                length = self.mWeaponCircleTravelData[self.mCurFrame][i][0].magnitude()

                if length != 0:
                    dir = self.mWeaponCircleTravelData[self.mCurFrame][i][0] / length
                else:
                    dir = VectorN(2)

                self.setWeaponCircleOffset(i, length, dir, radius=self.mWeaponCircleTravelData[self.mCurFrame][i][1])

                if not init:
                    if self.mIsRotateWeapon:
                        self.mWeaponCircleList[i].rotateAboutOrigin(self.getSwingingAngle(), optimize=True)


    def getSwingingAngle(self):
        """
        This will return the angle the attack should face at any given time

        :return: either self.mSwingingAngle or self.mOwner.mAngle, depending if it is a freeze weapon or not
        """

        if self.mFreezeCircles:
            return self.mSwingingAngle

        else:
            return self.mOwner.mAngle


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
        self.mShootTimer.update(dtime)

        if self.mIsSwinging or self.mIsShooting:
            self.updateHitData(dtime)

            # Update Animation
            self.mSpriteSheet.update(dtime)

        if self.mSwingTimer.mReached:
            self.mSwingTimer.reset()
            self.mIsSwinging = False

        if self.mReloadTimer.mReached:
            self.mReloadTimer.reset()
            self.mIsReloading = False

        if self.mShootTimer.mReached:
            self.mShootTimer.reset()
            self.mIsShooting = False


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

                    # Apply a force on the entity from the point of collision
                    pointToEntityVector = (VectorN((entity.mX, entity.mY)) - pointOfCollision)
                    forcedir = pointToEntityVector.normalized_copy()

                    force = forcedir * self.mWeaponCircleList[i].mKnockBackForce

                    damage = (self.mBaseMeleeDamage / 2) + (math.sqrt(self.mOwner.mAttack) - math.sqrt(entity.mDefense)) * 5
                    if damage < 1:
                        damage = 1

                    entity.getHit(force, damage)

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

        if self.mIsSwinging or self.mIsShooting:
            # Render the animation

            blitImg = self.mSpriteSheet.getCurImg()

            if self.mAnimationOriginalAngle:
                rotImg = pygame.transform.rotate(blitImg, math.degrees(self.mAnimationOriginalAngle - self.getSwingingAngle()))

                size = VectorN(rotImg.get_size())

                if self.mFreezeCircles:
                    blitPos = self.mWeaponCircleList[0].mFreezeOrigin - size/2
                else:
                    pos = self.getPos()
                    blitPos = VectorN((pos[0] - size[0]/2, pos[1] - size[1]/2))


                surface.blit(rotImg, (blitPos + self.getVectorFromAngle(self.getSwingingAngle())*self.mAnimationLength - camera.position).iTuple())

            else:       # No Rotation, assumes around center of player
                size = VectorN(blitImg.get_size())

                if self.mFreezeCircles:
                    blitPos = self.mWeaponCircleList[0].mFreezeOrigin - size/2
                else:
                    blitPos = self.getPos() - size/2

                surface.blit(blitImg, (blitPos - camera.position).iTuple())


    def drawOverlay(self, title=None):
        """
        This draws a nice weapon overlay telling the stats of the weapon
        And returns the surface it makes

        :return: a pygame.Surface
        """

        if title:
            blitList = [Weapon.OVERLAY_FONT.render(title, True, (0, 255, 255))]
            heightList = [blitList[-1].get_height()]
            widthList = [blitList[-1].get_width()]

        else:
            blitList = []
            heightList = []
            widthList = []

        blitList.append(Weapon.OVERLAY_FONT.render(self.mFileName, True, (0, 255, 0)))
        heightList.append(blitList[-1].get_height())
        widthList.append(blitList[-1].get_width())

        if self.mIsMelee:
            blitList.append(Weapon.OVERLAY_FONT.render("Damage: " +      str(int(self.mBaseMeleeDamage)), True, (255, 255, 255)))
            heightList.append(blitList[-1].get_height())
            widthList.append(blitList[-1].get_width())

        if self.mIsRanged:
            blitList.append(Weapon.OVERLAY_FONT.render("Shot Damage: " + str(int(self.mProjectileArgs['damage'])), True, (255, 255, 255)))
            heightList.append(blitList[-1].get_height())
            widthList.append(blitList[-1].get_width())
            blitList.append(Weapon.OVERLAY_FONT.render("Reload Speed: " +str(round(self.mReloadTime, 2)), True, (255, 255, 255)))
            heightList.append(blitList[-1].get_height())
            widthList.append(blitList[-1].get_width())

        if self.mManaCost != 0:
            blitList.append(Weapon.OVERLAY_FONT.render("Mana Cost: " +   str(int(self.mManaCost)), True, (255, 255, 255)))
            heightList.append(blitList[-1].get_height())
            widthList.append(blitList[-1].get_width())


        tSurf = pygame.Surface((max(widthList) + 6, max(heightList)*len(heightList) + 6)).convert_alpha()
        tSurf.fill((0, 0, 0, 128))

        curY = 3
        for text in blitList:
            tSurf.blit(text, (3, curY))
            curY += Weapon.OVERLAY_FONT.get_linesize()

        return tSurf


