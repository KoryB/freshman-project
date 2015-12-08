import pygame
import math
import random
import entity
from Weapon import Weapon

"""
States:
    0 = stay
    1 = walk
    2 = follow
    3 = aggro
"""

class Enemy(entity.Entity):
    """
    Creates a enemy class
    """
    def __init__(self, img, x, y, type, map):
        """
        Initializes enemy
        :param img: spritesheet
        :param x: horizontal position
        :param y: vertical position
        :param type: type of enemy
        :param map: a reference to the map the Enemy resides in
        :return: N/A
        """
        super().__init__(img, x, y, 100, map)
        self.mInventory.clearWeaponInventory()
        self.mRange = 64
        self.mAtkDelay = 1.0
        if type == 0:
            self.mDetectRadius = 100
            self.mSpeed = 90
            self.mAttack = 4
            self.mDefense = 2
            self.mRange = 100
            self.mAtkDelay = 2.0
            self.mInventory.addWeapon(Weapon(self, fileName="Fire Magic"))
        elif type == 1:
            self.mDetectRadius = 80
            self.mSpeed = 75
            self.mAttack = 2
            self.mDefense = 1
            self.mInventory.addWeapon(Weapon(self, fileName="Generic Sword"))
        elif type == 2:
            self.mDetectRadius = 50
            self.mSpeed = 45
            self.mAttack = 3
            self.mDefense = 2
            self.mInventory.addWeapon(Weapon(self, fileName="Generic Axe"))
        elif type == 3:
            self.mDetectRadius = 120
            self.mSpeed = 120
            self.mAttack = 2
            self.mDefense = 1
            self.mRange = 100
            self.mAtkDelay = 1.5
            self.mInventory.addWeapon(Weapon(self, fileName="Generic Bow"))
        self.mType = type
        self.mState = 0
        self.mMoveAngle = math.pi * 0.5
        self.mWalkTimer = 0.0
        self.mWalkLength = random.uniform(1.0, 2.0)
        self.mAtkTimer = self.mAtkDelay / 2
        self.mSpawnPos = [self.mX, self.mY]
        self.mRespawnTimer = 0.0
        self.mRespawnLength = 30.0


    def update(self, player, cam, entityList, dt):
        """
        Updates enemy
        :param player: player
        :param dt: deltatime
        :return: N/A
        """
        if not self.mIsDead:
            if self.mCurHealth <= 0:
                self.mIsDead = True

            super().physUpdate(entityList, dt)
            self.mCurMana = 100
            x = player.mX - self.mX
            y = player.mY - self.mY
            dist = x*x + y*y
            camArea = cam.width/2 + cam.height/2

            if dist < camArea * camArea:
                if dist < (self.mDetectRadius + 16)**2 and self.mState != 3:
                    self.mState = 2
                    self.mMoveAngle = math.atan2(player.mY - self.mY, player.mX - self.mX)
                    if self.mWalkTimer > 0.0:
                        self.mWalkTimer = 0.0
                else:
                    if self.mState == 2:
                        self.mState = 0
                    self.mWalkTimer += dt
                    if self.mState == 3:
                        self.mMoveAngle = math.atan2(player.mY - self.mY, player.mX - self.mX)
                        if self.mWalkTimer > self.mWalkLength:
                            self.mWalkTimer = 0.0
                            self.mState = 1
                            self.mWalkLength = random.uniform(1.0, 2.0)
                            self.mMoveAngle = random.uniform(0,math.pi*2)
                    if self.mWalkTimer > self.mWalkLength:
                        if random.randint(0,1) == 1:
                            self.mState = 1
                            self.mMoveAngle = random.uniform(0,math.pi*2)
                        else:
                            self.mState = 0
                        self.mWalkLength = random.uniform(1.0, 2.0)
                        self.mWalkTimer = 0.0
                if self.mState != 0:
                    velocity = [ math.cos(self.mMoveAngle)*self.mSpeed, math.sin(self.mMoveAngle)*self.mSpeed ]
                    self.move(velocity[0], velocity[1], [player]+entityList, dt)
                    self.checkDirection(math.degrees(self.mMoveAngle) % 360)

                if self.mInventory.hasWeapon() and dist < (self.mRange * self.mRange)\
                        and (self.mState == 2 or self.mState == 3):
                    self.mAtkTimer += dt
                    if self.mAtkTimer >= self.mAtkDelay:
                        self.mInventory.getCurrentWeapon().swing(self.mAngle)
                        self.mIsSwinging = True
                        self.mAtkTimer = 0.0
                else:
                    self.mAtkTimer = self.mAtkDelay / 2

            if self.mInventory.hasWeapon():
                self.mInventory.getCurrentWeapon().update(dt)
        else:
            self.mRespawnTimer += dt
            if self.mRespawnTimer >= self.mRespawnLength:
                self.__init__(self.mSheet, self.mSpawnPos[0], self.mSpawnPos[1], self.mType, self.mMap)

            if self.mInventory.hasWeapon():
                self.mInventory.getCurrentWeapon().stopSwinging()
        self.mHitBox.topleft = (self.mX - 16, self.mY - 16)

    def getHit(self, force, damage):
        self.mState = 3
        self.mWalkTimer = 0.0
        self.mWalkLength = 5.0
        super().getHit(force, damage)

    def checkDirection(self, angle):
        """
        Checks enemy direction
        :param angle: angle of movement
        :return: N/A
        """
        super().checkDirection(angle)
        if angle >= 315 or angle <= 45:
            self.mDirection = 2
        elif 45 <= angle <= 135:
            self.mDirection = 0
        elif 135 <= angle <= 225:
            self.mDirection = 1
        elif 225 <= angle <= 315:
            self.mDirection = 3

    def render(self, surf, cam):
        if not self.mIsDead:
            pygame.draw.rect(surf, (255, 0, 0), (int(self.mX - cam.position[0]) - 16, int(self.mY - cam.position[1] - 20), (self.mCurHealth / self.mMaxHealth) * 32, 3))
            if cam.position[0] - 16 < self.mX < cam.position[0] + cam.width + 16 and cam.position[1] - 16 < self.mY < cam.position[1] + cam.height + 16:
                surf.blit(self.mSheet, (self.mX - 16 - cam.position[0], self.mY - 16 - cam.position[1]),
                          (96 * self.mType + self.mFrame * 32, (self.mDirection % 4) * 32, 32, 32))

            if self.mInventory.hasWeapon():
                self.mInventory.getCurrentWeapon().render(surf, cam)
