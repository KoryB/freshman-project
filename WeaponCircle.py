from math3d import VectorN
import pygame
import math

class WeaponCircle(object):

    SQRT_2_OVER_2 = math.sqrt(2) / 2

    def __init__(self, weapon, offset=VectorN(2), radius=5, knockBackForce=300, debugColor=(255,255,255), debugColorHit=(255,0,0), freezeOrigin=False):
        """
        This is just a nice utility class to be able to have hit data contained in objects.
        These can be loaded with things like radius, offset from origin of the weapon, knockback power, knockback angle, damage, etc.
        :return: N/A
        """

        self.mCurOffsetLength = offset.magnitude()

        if self.mCurOffsetLength != 0:
            self.mCurOffsetDir = offset / self.mCurOffsetLength
        else:
            self.mCurOffsetDir = VectorN(2)

        self.mORIGINAL_OFFSET = offset.copy()
        self.mORIGINAL_RADIUS = radius

        self.mRadius = radius
        self.mRadius2 = radius * radius

        self.mWeapon = weapon

        self.mIsColliding = False
        self.mDebugColorNoHit = debugColor
        self.mDebugColorHit = debugColorHit

        self.mKnockBackForce = knockBackForce

        self.mIsFreeze = freezeOrigin
        self.mFreezeOrigin = None


    def resetHit(self):
        """
        For now this just sets self.mIsColliding to False. But it might do some other things down the line
        :return: None
        """

        self.mIsColliding = False


    def resetOffset(self):
        """
        This just resets self.mCurOffset to the original
        :return: None
        """

        self.mCurOffsetLength = self.mORIGINAL_OFFSET.magnitude()
        if self.mCurOffsetLength != 0:
            self.mCurOffsetDir = self.mORIGINAL_OFFSET / self.mCurOffsetLength
        else:
            self.mCurOffsetDir = VectorN(2)


    def resetRadii(self):
        """
        This just resets self.mRadius and self.mRadius2 to the original
        :return: None
        """

        self.mRadius = self.mORIGINAL_RADIUS
        self.mRadius2 = self.mORIGINAL_RADIUS


    def resetOriginal(self):
        """
        This just resets self.mORIGINAL_OFFSET vector to the current offset
        :return: None
        """

        self.mORIGINAL_OFFSET = self.mCurOffsetLength*self.mCurOffsetDir
        self.mORIGINAL_RADIUS = self.mRadius


    def reset(self):
        """
        Resets everything back to original state.
        :return: None
        """

        self.resetHit()
        self.resetOffset()
        self.resetRadii()

        if self.mIsFreeze:
            self.mFreezeOrigin = self.mWeapon.getPos()


    def rotateAboutOrigin(self, angle, optimize=False, radians=True):
        """
        This will rotate self around the origin, which changes self.mCurOffset

        if optimize == True, it only works at 45 degree angles, but uses the unit circle to avoid using sine and cosine.

        if radians == False, the function will convert the angle into radians
        source: book for 1803
        :param angle:
        :return:
        """

        if not radians:
            angle = math.radians(angle)

        newOffset = VectorN(2)

        if optimize:
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

        else:
            sinAngle = math.sin(angle)
            cosAngle = math.cos(angle)

        newOffset[0] = self.mCurOffsetDir[0] * cosAngle - self.mCurOffsetDir[1] * sinAngle
        newOffset[1] = self.mCurOffsetDir[0] * sinAngle + self.mCurOffsetDir[1] * cosAngle

        self.mCurOffsetDir = newOffset.copy()


    def scaleRadius(self, multiplier_or_offset, multiply=True):
        """
        Just scales the radius by the factor of multiplier if multiply=True
        Otherwise adds multiplier_or_offset to the radius
        :param multiplier_or_offset: any float, if multiply=True, must be non-negative
        :param multiply: if True, multiplies self.mRadius by multiplier, otherwise adds multiplier_or_offset to self.mRadius
        :return: None
        """

        if multiply:
            if multiplier_or_offset < 0:
                return

            self.mRadius *= multiplier_or_offset
            self.mRadius2 = self.mRadius*self.mRadius

        else:
            self.mRadius += multiplier_or_offset
            self.mRadius2 = self.mRadius*self.mRadius


    def getWorldPos(self):
        """
        This returns the world space position of the circle, instead of the weapon-space position.
        If it is 'frozen' takes the freezePos instead of the weaponPos
        :return: world space position of self
        """

        if self.mIsFreeze:
            return self.mFreezeOrigin + self.getCurOffsetVector()
        else:
            return self.mWeapon.getPos() + self.getCurOffsetVector()


    def getCurOffsetVector(self):
        """
        This multiplies the length by the direction to create the true offset vector
        :return: a 2D VectorN representing the WeaponCircle's true offset
        """

        return self.mCurOffsetDir*self.mCurOffsetLength


    def getDict(self):
        """
        returns a dictionary of the CurrentOffset and the radius
        :return: a dict type object
        """

        curOffsetVector = self.getCurOffsetVector()

        return {"pos": [curOffsetVector[0], curOffsetVector[1]],
                "radius": self.mRadius
               }

    def collideEntity(self, entity):
        """
        For now this will simply detect if a collision occured, and change the debug color accordingly.
        This is done with simple circle-rect hit detection
        :param entity: An Entity object.
        :return: a 1D vector if no collision, the Point of Collision otherwise.
        """

        inside = True
        closestPoint = VectorN(2)

        curPos = self.getWorldPos()

        #check if circle is above/below/right/left/in circle
        if curPos[0] > entity.mHitBox.right + self.mRadius:
            inside = False

            closestPoint[0] = entity.mHitBox.right
            closestPoint[1] = curPos[1]

            closestPoint[1] = max(closestPoint[1], entity.mHitBox.top) # Cap closestPointY at the top of the box.
            closestPoint[1] = min(closestPoint[1], entity.mHitBox.bottom) # Cap closestPointY at the bottom of the box as well

        elif curPos[0] < entity.mHitBox.left - self.mRadius:
            inside = False

            closestPoint[0] = entity.mHitBox.left
            closestPoint[1] = curPos[1]

            closestPoint[1] = max(closestPoint[1], entity.mHitBox.top) # Cap closestPointY at the top of the box.
            closestPoint[1] = min(closestPoint[1], entity.mHitBox.bottom) # Cap closestPointY at the bottom of the box as well

        if curPos[1] > entity.mHitBox.bottom + self.mRadius:
            inside = False

            closestPoint[0] = curPos[0]
            closestPoint[1] = entity.mHitBox.bottom

            closestPoint[0] = max(closestPoint[0], entity.mHitBox.right) # Cap closestPoint.x at the right of the box.
            closestPoint[0] = min(closestPoint[0], entity.mHitBox.left) # Cap closestPoint.x at the left of the box as well

        elif curPos[1] < entity.mHitBox.top - self.mRadius:
            inside = False

            closestPoint[0] = curPos[0]
            closestPoint[1] = entity.mHitBox.top

            closestPoint[0] = max(closestPoint[0], entity.mHitBox.right) # Cap closestPoint.x at the right of the box.
            closestPoint[0] = min(closestPoint[0], entity.mHitBox.left) # Cap closestPoint.x at the left of the box as well

        if inside:
            closestPoint = curPos.copy()

        # calculate distance squared between the closest point and the current position of the circle
        offsetVector = closestPoint - curPos

        if offsetVector.dot(offsetVector) <= self.mRadius2:
            self.mIsColliding = True
            return closestPoint
        else:
            self.mIsColliding = False
            return VectorN(1)


    def render(self, surface, camera):
        """
        Renders the circle to the screen, used for debugging purposes
        :param surface: surface to render to
        :return: None
        """

        worldPos = self.getWorldPos()
        renderPos = worldPos - camera.position

        if self.mIsColliding:
            pygame.draw.circle(surface, self.mDebugColorHit, renderPos.iTuple(), int(self.mRadius))
        else:
            pygame.draw.circle(surface, self.mDebugColorNoHit, renderPos.iTuple(), int(self.mRadius))