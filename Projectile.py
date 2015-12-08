import pygame
from math3d import VectorN
from WeaponCircle import WeaponCircle

class Projectile(object):

    ICE_IMAGE = pygame.image.load("imgs/Projectiles/Ice.png").convert_alpha()
    ARROW_IMAGE = pygame.image.load("imgs/Projectiles/Arrow.png").convert_alpha()

    def __init__(self, owner, direction, radius=5, originalOffsetLength=0, speed=30, originalAngle=0, maxRange=100, damage=35, imageType=None, knockBackForce=300):

        self.mOwner = owner
        self.mOffsetLength = originalOffsetLength
        self.mRadius = radius
        self.mAngle = originalAngle
        self.mSpeed = speed
        self.mRange = maxRange
        self.mRange2 = maxRange*maxRange
        self.mDirection = direction.normalized_copy()

        self.mDamage = damage

        self.mRemove = False

        self.mOrigin = self.mOwner.getPos()

        self.mWeaponCircle = WeaponCircle(self.mOwner, radius=radius, freezeOrigin=True, knockBackForce=knockBackForce)
        self.mWeaponCircle.reset()

        self.mImage = None
        if imageType:
            self.mImage = getattr(Projectile, imageType)


    def update(self, dtime):
        self.mOffsetLength += self.mSpeed * dtime

        if self.mOffsetLength*self.mOffsetLength >= self.mRange2:
            self.mRemove = True

        self.mWeaponCircle.mCurOffsetLength = self.mOffsetLength
        self.mWeaponCircle.mCurOffsetDir = self.mDirection


    def getWorldPos(self):
        """
        This function returns the world position of the Projectile
        :return: a 2D VectorN
        """

        return self.mOrigin + self.mOffsetLength*self.mDirection


    def collideEntity(self, entity):
        """
        This will run through all of the sword's WeaponCircles and check collision with the entity with all of them
        :param entity: an entity object
        :param dt: time passed since last update, probably a better place to apply force
        :return: a 1D vector if no collision, the point of collision otherwise.
        """

        if (not entity.mIsInvincible) and id(entity)!= id(self.mOwner.mOwner):
            pointOfCollision = self.mWeaponCircle.collideEntity(entity)


            if len(pointOfCollision) != 1:

                # Apply a force on the entity from the point of collision
                pointToEntityVector = (VectorN((entity.mX, entity.mY)) - pointOfCollision)
                forcedir = pointToEntityVector.normalized_copy()

                force = forcedir * self.mWeaponCircle.mKnockBackForce
                damage = self.mDamage+(((self.mDamage*self.mOwner.mOwner.mAttack)/100)) - entity.mDefense

                entity.getHit(force, damage)

                return pointOfCollision

        else:
            return VectorN(1)


    def render(self, surf, cam):

        if self.mImage:
            blitPos = self.getWorldPos() - cam.position - VectorN(self.mImage.get_size())/2

            surf.blit(self.mImage, blitPos)