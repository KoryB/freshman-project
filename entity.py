import math
from Inventory import Inventory
from Items import *
from Weapon import Weapon
from math3d import VectorN
import random

class Entity(object):
    def __init__(self, img, x, y, speed, map):
        """
        Initializes entity object
        :param img: spritesheet
        :param x: x position
        :param y: y position
        :param speed: entity speed
        :param map: a reference to the map the Entity belongs to, used for firing projectiles.
        :return: N/A
        """
        self.mX = x
        self.mY = y
        self.mSpeed = speed
        self.mSpeedMult = 1.0
        self.mSheet = img
        self.mDirection = 0
        self.mAngle = math.pi * 0.5
        self.mFrame = 1
        self.mAnimationTimer = 0.0
        self.mHitBox = pygame.Rect(self.mX, self.mY, 32, 32)

        # Invincibility frames related things
        self.mMaxInvincibilityTime = 0.3
        self.mInvincibilityTimer = 0.0

        self.mMap = map

        self.mIsInvincible = False
        self.mWasHit = False

        self.mIsPlayer = False

        self.mInventory = Inventory()
        self.mInventory.addItem(healthPotion(self))
        self.mInventory.addWeapon(Weapon(self, fileName="Generic Sword"))

        self.mIsSwinging = False


        self.mMaxHealth = 100
        self.mCurHealth = 100
        self.mMaxMana = 100
        self.mCurMana = 100
        self.mAttack = 1
        self.mDefense = 1

        self.mIsDead = False
        self.mEffectList = []

        # These are variables used in the knockback of weapons, I figure mass is important for that.
        # Modeling a lot of this off of our physics object from 1803. Except setting velocity instead of applying a force for knockback
        # For now I figure seperating out the PhysVelocity and movement is a good idea.

        self.mMass = 10
        self.mPhysVelocity = VectorN(2)
        self.mFriction = 1000


    def addEffect(self, newEffect):
        self.mEffectList.append(newEffect)

        newEffect.onEnter()


    def applyForce(self, force, dt):
        """
        apply a force to the object, where dtime is the amount of time the force is applied

        :param force: A VectorN object, representing the force to be applied
        :param dt: amount of time to apply the force
        :return: None
        """
        a = force / self.mMass
        self.mPhysVelocity += a * dt

    def setVelocity(self, newVel):
        """
        This simply sets self.mPhysVelocity to newVel
        :param newVel: a 2D VectorN object
        :return: None
        """

        self.mPhysVelocity = newVel.copy()

    def applyFriction(self, dt):
        """
        This applies a frictional force opposite to velocity

        :param dt: amount of time passed since last update
        :return: None
        """

        frictionForce = self.mFriction * self.mMass * -self.mPhysVelocity.normalized_copy()
        self.applyForce(frictionForce, dt)

    def physUpdate(self, entityList, dt):
        """
        Function used to update physics components of an object. To be called during a child object's update loop
        :param dt:  amount of time that has passed since last call, in seconds
        :return: N/A
        """
        if self.mPhysVelocity != VectorN(2):
            oldVelocity = self.mPhysVelocity.copy()

            self.applyFriction(dt)

            if oldVelocity.dot(self.mPhysVelocity) < 0:
                # If the direction changed due to friction, make the velocity zero.
                self.mPhysVelocity = VectorN(2)

            self.mX = self.mX + self.mPhysVelocity[0] * dt
            self.mY = self.mY + self.mPhysVelocity[1] * dt
            self.checkEntityCollision(entityList)
            self.mHitBox.topleft = (self.mX - 16, self.mY - 16)

        # Update invincibility frames
        if self.mInvincibilityTimer > 0:
            self.mIsInvincible = True

            self.mInvincibilityTimer -= dt

        else:
            self.mIsInvincible = False

    def getHit(self, knockBack, damage):
        """
        This handles the entity getting hit. Will be inherited and modified by enemy.
        :param knockBack: a 2D VectorN, this changes the physVelocity of the entity.
        :param damage: how much damage the hit did.
        :return: None
        """

        self.setInvincible()

        self.setVelocity(knockBack)
        self.mCurHealth -= damage

        if self.mCurHealth <= 0:
            self.mCurHealth = 0

    def deathpenalty(self):
        self.mPhysVelocity = VectorN(2)
        randompenalty = random.randint(0, 2)

        if randompenalty == 0:
            self.mDefense -= self.mDefense * 0.30
        elif randompenalty == 1:
            self.mAttack -= self.mAttack * 0.30
        elif randompenalty == 2:
            self.mSpeedMult -= 0.03

        if self.mDefense < 1:
            self.mDefense = 1
        if self.mAttack < 1:
            self.mAttack = 1
        if self.mSpeedMult < 1.0:
            self.mSpeedMult = 1.0

    def setInvincible(self):
        """
        This function just starts the Invincibility timer to its max time.

        :return: None
        """

        self.mInvincibilityTimer = self.mMaxInvincibilityTime
        self.mIsInvincible = True

    def swingSword(self):
        """
        This function will just activate the sword swinging.
        Also sets the rotation angle for the swing.

        Might need more stuff to it, so I'm making a function for it for now.
        :return: None
        """

        if self.mInventory.hasWeapon():
            self.mInventory.getCurrentWeapon().swing(self.mAngle)
            self.mIsSwinging = True


    def checkSwordCollision(self, entity, dt):
        """
        Contains the logic for sword collisions.
        For now just tests whether a collision occurs.

        :param entity: an entity object
        :return: a 1d vector if no collision, the point of collision otherwise
        """
        if self.mInventory.hasWeapon() and self.mInventory.getCurrentWeapon().mIsSwinging and id(entity) != id(self):
            pointOfCollision = self.mInventory.getCurrentWeapon().collideEntity(entity, dt)
            return pointOfCollision
        else:
            return VectorN(1)

    def move(self, x, y, entityList, dt):
        """
        Update entity (placeholder)
        :param x: horizontal movement
        :param y: vertical movement
        :param dt: deltatime
        :return: N/A
        """
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
            self.mX = self.mX + x * dt
            self.mY = self.mY + y * dt
            self.checkEntityCollision(entityList)

    def checkDirection(self, angle):
        """
        Checks player direction
        :param angle: angle of movement
        :return: N/A
        """
        if angle >= 338.5 or angle <= 23.5:
            self.mDirection = 2
            self.mAngle = 0
        elif 23.5 <= angle <= 68.5:
            self.mDirection = 6
            self.mAngle = math.pi * 0.25
        elif 68.5 <= angle <= 113.5:
            self.mDirection = 0
            self.mAngle = math.pi * 0.5
        elif 113.5 <= angle <= 158.5:
            self.mDirection = 4
            self.mAngle = math.pi * 0.75
        elif 158.5 <= angle <= 203.5:
            self.mDirection = 1
            self.mAngle = math.pi
        elif 203.5 <= angle <= 248.5:
            self.mDirection = 5
            self.mAngle = math.pi * 1.25
        elif 248.5 <= angle <= 293.5:
            self.mDirection = 3
            self.mAngle = math.pi * 1.5
        elif 293.5 <= angle <= 338.5:
            self.mDirection = 7
            self.mAngle = math.pi * 1.75

    def checkEntityCollision(self, entityList):
        for i in entityList:
            if self != i and not i.mIsDead and self.mHitBox.colliderect(i.mHitBox):
                delta = [0, 0]

                if self.mHitBox.right - i.mHitBox.left <= self.mHitBox.width/2:
                        delta[0] = self.mHitBox.right - i.mHitBox.left

                elif self.mHitBox.left - i.mHitBox.right <= self.mHitBox.width/2:
                        delta[0] = self.mHitBox.left - i.mHitBox.right

                if self.mHitBox.bottom - i.mHitBox.top <= self.mHitBox.height/2:
                        delta[1] = self.mHitBox.bottom - i.mHitBox.top

                elif self.mHitBox.top - i.mHitBox.bottom <= self.mHitBox.height/2:
                        delta[1] = self.mHitBox.top - i.mHitBox.bottom


                if abs(delta[0]) < abs(delta[1]):
                        self.mX -= delta[0]
                        self.mPhysVelocity[0] = 0

                else:
                        self.mY -= delta[1]
                        self.mPhysVelocity[1] = 0

                self.mHitBox.topleft = (self.mX - 16, self.mY - 16)