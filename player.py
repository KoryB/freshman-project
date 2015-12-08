import math
import entity
from Items import *

class Player(entity.Entity):
    """
    Creates a player class
    """
    def __init__(self, img, x, y, map):
        """
        Initializes player
        :param img: spritesheet
        :param x: horizontal position
        :param y: vertical position
        :param map: a reference to the current map
        :return: N/A
        """
        super().__init__(img, x, y, 150, map)
        self.mAnimAtk = 0.0
        self.mAttacking = False

        self.mIsPlayer = True
        self.mIsOverWeapon = False

        self.mInventory.clearWeaponInventory()
        self.mInventory.addWeapon(Weapon(self, fileName="Generic Sword"))

        self.mLives = 3

    def update(self, x, y, entityList, dt):
        """
        Updates player
        :param x: horizontal movement
        :param y: vertical movement
        :param tiles: tiles
        :param dt: deltatime
        :return: N/A
        """
        super().physUpdate(entityList, dt)
        self.mCurMana += 7 * dt
        if self.mCurMana > self.mMaxMana:
            self.mCurMana = self.mMaxMana

        if x*x + y*y < 0.04:
            x = 0.0
            y = 0.0
        if x == 0.0 and y == 0.0:
            self.mAnimationTimer = 0.0
            self.mFrame = 1
        else:
            self.mAnimationTimer += dt
            if self.mAnimationTimer >= 0.15:
                self.mAnimationTimer = 0.0
                self.mFrame += 1
                if self.mFrame > 2:
                    self.mFrame = 0
            angle = math.degrees(math.atan2(y, x)) % 360
            self.checkDirection(angle)
            x += math.cos(math.radians(angle)) * self.mSpeed * self.mSpeedMult
            y += math.sin(math.radians(angle)) * self.mSpeed * self.mSpeedMult
            self.move(x, y, [self]+entityList, dt)
        if self.mAttacking:
            self.mAnimAtk += dt
            if self.mAnimAtk == 1.0:
                self.mAttacking = False

        if self.mInventory.hasWeapon():
            self.mInventory.getCurrentWeapon().update(dt)


        # Loop through effects
        for effect in self.mEffectList:
            effect.update(dt)

            if effect.mIsReached:
                effect.onExit()
                self.mEffectList.remove(effect)
        self.mHitBox.topleft = (self.mX - 16, self.mY - 16)


    def pickUpItem(self, item):
        """
        This will attempt to add the item to the player's inventory
        If there is already something in the inventory, it will be removed

        Do we want the old item to fall back to the ground?
            Currently just gets deleted
        :param item: an Item object
        :return: None
        """

        item.setPlayer(self)
        self.mInventory.switchItem(item)


    def switchWeapon(self):
        """
        This just switches the weapon. Not exactly sure all it needs
        :return: None
        """

        self.mInventory.switchCurrentWeapon()


    def render(self, surf, cam, isSelf=True):
        if cam.position[0] - 16 < self.mX < cam.position[0] + cam.width + 16 and cam.position[1] - 16 < self.mY < cam.position[1] + cam.height + 16:
            if self.mDirection >= 4:
                surf.blit(self.mSheet, (self.mX - 16 - cam.position[0], self.mY - 16 - cam.position[1]),
                          (32 * 3 + self.mFrame * 32, (self.mDirection % 4) * 32, 32, 32)) # If direction is diagonal then use second set
            else:
                surf.blit(self.mSheet, (self.mX - 16 - cam.position[0], self.mY - 16 - cam.position[1]),
                          (self.mFrame * 32, self.mDirection * 32, 32, 32))

        if self.mInventory.hasWeapon():
            self.mInventory.getCurrentWeapon().render(surf, cam)
        if isSelf:
            self.mInventory.render(surf)

    def getDeath(self, mC, spawn):
        if mC:
            self.mLives -= 1
            if self.mLives == 0:
                self.mIsDead = True
        if not mC:
            self.deathpenalty()
        self.mX = spawn[0]
        self.mY = spawn[1]
        self.mCurHealth = self.mMaxHealth
        self.mCurMana = self.mMaxMana



