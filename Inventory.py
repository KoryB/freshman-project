from math3d import VectorN

class Inventory(object):
    def __init__(self):
        self.inventory = []
        self.weaponInventory = []
        self.currentWeapon = 0
        self.weaponPos = VectorN((5, 3))
        self.itemPos = VectorN((63, 3))

    def switchItem(self, item):
        self.removeItem()
        self.addItem(item)

    def addItem(self, item):
        if len(self.inventory) < 1:
            self.inventory.append(item)

    def removeItem(self):
        if len(self.inventory) > 0:
            del(self.inventory[0])

    def useItem(self):
        if len(self.inventory) > 0:
            self.inventory[0].effect()
            self.removeItem()

    def addWeapon(self, weapon):
        if len(self.weaponInventory) < 2:
            self.weaponInventory.append(weapon)

        else:
            self.weaponInventory[self.currentWeapon] = weapon

    def removeCurrentWeapon(self):

        if len(self.weaponInventory) > self.currentWeapon:
            del(self.weaponInventory[self.currentWeapon])
            self.currentWeapon = 0

    def clearWeaponInventory(self):

        del self.weaponInventory
        self.weaponInventory = []

    def switchCurrentWeapon(self):

        if len(self.weaponInventory) == 2:
            if self.currentWeapon:
                self.currentWeapon = 0
            else:
                self.currentWeapon = 1

    def isWeaponInInventory(self, name):

        for weapon in self.weaponInventory:
            if weapon.mFileName == name:
                return True

        return False

    def getCurrentWeapon(self):
        return self.weaponInventory[self.currentWeapon]

    def hasWeapon(self):
        return len(self.weaponInventory) > 0

    def render(self, surf):
        if len(self.inventory) > 0:
            surf.blit(self.inventory[0].mHudImg, self.itemPos.iTuple())

        if len(self.weaponInventory) > 0:
            if self.weaponInventory[self.currentWeapon].mHudImg:
                surf.blit(self.weaponInventory[self.currentWeapon].mHudImg, self.weaponPos.iTuple())


