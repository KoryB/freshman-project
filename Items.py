import pygame
from math3d import VectorN
from Weapon import Weapon
from TempEffect import TempEffect

class Item(object):
    def __init__(self, hudimg, pos, player, mapimg):
        self.mPlayer = player
        self.mHudImg = hudimg
        self.mMapImg = mapimg
        self.mUseOnPickup = False
        self.mIsWeapon = False

        self.mName = "item"
        self.mPos = pos
        self.mHalfMapSize = VectorN((16, 16))
        self.mMapRadius = 20
        self.mMapRadius2 = self.mMapRadius*self.mMapRadius

    def setPlayer(self, player):
        self.mPlayer = player

    def getCenter(self):
        return self.mPos + self.mHalfMapSize

    def render(self, surf, cam):
        # This method renders the item to the screen, meant to be for on the map rendering
        surf.blit(self.mMapImg, (self.mPos - cam.position).iTuple())

class healthPotion(Item):
    def __init__(self, player):
        self.instantUse = False
        img = pygame.image.load("imgs\\Items\\Potion06.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mName = "health potion"

    def effect(self):
        self.mPlayer.mCurHealth += 80
        if self.mPlayer.mCurHealth > self.mPlayer.mMaxHealth:
            self.mPlayer.mCurHealth = self.mPlayer.mMaxHealth

class manaPotion(Item):
    def __init__(self, player):
        self.instantUse = False
        img = pygame.image.load("imgs\\Items\\Potion04.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mName = "mana potion"

    def effect(self):
        self.mPlayer.mCurMana += 80
        if self.mPlayer.mCurMana > self.mPlayer.mMaxMana:
            self.mPlayer.mCurMana = self.mPlayer.mMaxMana

class speedBoost(Item):
    def __init__(self, player):
        self.instantUse = True
        img = pygame.image.load("imgs\\Items\\Etc04.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mName = "speed boost"

    def effect(self):
        self.mPlayer.mSpeedMult += 0.03

class strengthBoost(Item):
    def __init__(self, player):
        self.instantUse = True
        img = pygame.image.load("imgs\\Items\\Etc02.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mName = "strength boost"

    def effect(self):
        self.mPlayer.mAttack += 1.5

class defenseBoost(Item):
    def __init__(self, player):
        self.instantUse = True
        img = pygame.image.load("imgs\\Items\\Etc03.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mName = "defense boost"

    def effect(self):
        self.mPlayer.mDefense += 1.5

class speedBoots(Item):
    def __init__(self, player):
        self.instantUse = False
        img = pygame.image.load("imgs\\Armor\\Foot02.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mName = "speed boots"

    def effect(self):
        tEffect = TempEffect(self.mPlayer, 'mSpeedMult', 1, 1.5)
        self.mPlayer.addEffect(tEffect)

class shield(Item):
    def __init__(self, player):
        self.instantUse = False
        img = pygame.image.load("imgs\\Armor\\Shield02.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mName = "shield"

    def effect(self):
        tEffect = TempEffect(self.mPlayer, 'mDefense', 10, 1.5)
        self.mPlayer.addEffect(tEffect)

class cocaine(Item):
    def __init__(self, player):
        self.instantUse = False
        img = pygame.image.load("imgs\\Items\\Etc19.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mName = "cocaine"

    def effect(self):
        tEffect = TempEffect(self.mPlayer, 'mAttack', 10, 1.5)
        self.mPlayer.addEffect(tEffect)

class sword(Item):
    def __init__(self, player):
        self.instantUse = False
        self.mIsWeapon = True
        img = pygame.image.load("imgs\\Weapon\\Weapon03.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mUseOnPickup = True
        self.mIsWeapon = True
        self.mName = "sword"
        self.mMyWeapon = Weapon(self.mPlayer, fileName="Generic Sword")

    def effect(self):
        self.mMyWeapon.setPlayer(self.mPlayer)
        self.mPlayer.mInventory.addWeapon(self.mMyWeapon)

class mace(Item):
    def __init__(self, player):
        self.instantUse = False
        img = pygame.image.load("imgs\\Weapon\\Weapon08.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mUseOnPickup = True
        self.mIsWeapon = True
        self.mName = "mace"
        self.mMyWeapon = Weapon(self.mPlayer, fileName="Generic Axe")

    def effect(self):
        self.mMyWeapon.setPlayer(self.mPlayer)
        self.mPlayer.mInventory.addWeapon(self.mMyWeapon)

class bow(Item):
    def __init__(self, player):
        self.instantUse = False
        img = pygame.image.load("imgs\\Weapon\\Weapon14.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mUseOnPickup = True
        self.mIsWeapon = True
        self.mName = "bow"
        self.mMyWeapon = Weapon(self.mPlayer, fileName="Generic Bow")

    def effect(self):
        self.mMyWeapon.setPlayer(self.mPlayer)
        self.mPlayer.mInventory.addWeapon(self.mMyWeapon)

class fire(Item):
    def __init__(self, player):
        self.instantUse = False
        img = pygame.image.load("imgs\\Weapon\\Weapon16.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mUseOnPickup = True
        self.mIsWeapon = True
        self.mName = "fire"
        self.mMyWeapon = Weapon(self.mPlayer, fileName="Fire Magic")

    def effect(self):
        self.mMyWeapon.setPlayer(self.mPlayer)
        self.mPlayer.mInventory.addWeapon(self.mMyWeapon)

class wind(Item):
    def __init__(self, player):
        self.instantUse = False
        img = pygame.image.load("imgs\\Weapon\\Weapon18.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mUseOnPickup = True
        self.mIsWeapon = True
        self.mName = "wind"
        self.mMyWeapon = Weapon(self.mPlayer, fileName="Wind Magic")

    def effect(self):
        self.mMyWeapon.setPlayer(self.mPlayer)
        self.mPlayer.mInventory.addWeapon(self.mMyWeapon)

class ice(Item):
    def __init__(self, player):
        self.instantUse = False
        img = pygame.image.load("imgs\\Weapon\\Weapon17.png")
        pos = VectorN(2)
        scaledImg = pygame.transform.scale(img, (45, 45))
        scaledMapImg = pygame.transform.scale(img, (32, 32))
        Item.__init__(self, scaledImg, pos, player, scaledMapImg)
        self.mUseOnPickup = True
        self.mIsWeapon = True
        self.mName = "sword"
        self.mMyWeapon = Weapon(self.mPlayer, fileName="Ice Magic")

    def effect(self):
        self.mMyWeapon.setPlayer(self.mPlayer)
        self.mPlayer.mInventory.addWeapon(self.mMyWeapon)



itemTypeDict = {
                0: healthPotion,
                1: manaPotion,
                2: speedBoost,
                3: strengthBoost,
                4: defenseBoost,
                5: speedBoots,
                6: shield,
                7: cocaine,
                8: speedBoost,
                9: strengthBoost,
                10: defenseBoost,
                11: healthPotion,
                12: manaPotion,
                13: speedBoost,
                14: strengthBoost,
                15: defenseBoost,
                16: speedBoots,
                17: shield,
                18: cocaine,
                19: speedBoost,
                20: strengthBoost,
                21: defenseBoost,
                22: sword,
                23: mace,
                24: bow,
                25: fire,
                26: wind,
                27: ice,
                28: sword,
                29: mace,
                30: bow,
                31: fire,
                32: wind,
                33: ice
}

filenameToWeapon = {
                "Generic Bow": bow,
                "Generic Sword": sword,
                "Generic Axe": mace,
                "Fire Magic": fire,
                "Wind Magic": wind,
                "Ice Magic": ice
}

def getItemFromType(typeOfItem, player=None):
    # This returns an Item based itemTypeDict (at the bottom)

    itemClass = itemTypeDict[typeOfItem]

    return itemClass(player)

def getWeaponFromName(name, weapon=None, player=None):

    itemClass = filenameToWeapon.get(name)

    if itemClass:
        tItem  = itemClass(player)

        if weapon:
            tItem.mMyWeapon = weapon

        return tItem

    else:
        return sword(None)
