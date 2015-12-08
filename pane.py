import player
import enemy
import Camera1802
from hud import HUD
import MapGenerator
from Inventory import Inventory
import random
from Items import *

class pane(object):
    def __init__(self, screensurf, playersprite, enemysprite, tilesetimage, playerNumber, screen_offset):
        """
        This is called once at the beginning of the main, before the game loop
        Called once per pane wanted
        screensurf = the surface that represents the screen
        playersprite is the image used to draw the player
        enemysprite is the same but with enemies
        tilesetimage is the same but with the tiles used to make the map
        """
        self.me = playerNumber
        screenWidth = screensurf.get_width()
        screenHeight = screensurf.get_height()
        self.surfWidth = screenWidth/2
        self.surfHeight = screenHeight/2

        self.screen_offset = screen_offset

        self.surf = pygame.Surface((self.surfWidth, self.surfHeight))

        self.tileset = pygame.image.load(tilesetimage).convert()
        self.mapgen = MapGenerator.MapGenerator()
        self.map = self.mapgen.generateMap((7, 7), self.tileset, colorkey=(152,142,133))
        self.mMapSurf = self.map.mTileSurface
        self.spawn = self.map.getSpawn()
        self.mMapsize = (self.map.mTileSurface.get_width(), self.map.mTileSurface.get_height())


        self.playerSprite = pygame.image.load(playersprite).convert_alpha()
        self.enemySprite = pygame.image.load(enemysprite).convert_alpha()
        self.player = player.Player(self.playerSprite,self.spawn[0], self.spawn[1], self.map)
        self.enemy = enemy.Enemy(self.enemySprite,self.player.mX, self.player.mY, 0, self.map)
        self.projectile = []


        #hud
        self.hud = HUD(self.player, self.me, pygame.image.load("imgs\\pic.png").convert_alpha())
        self.inventory = Inventory()
        self.camera = Camera1802.Camera(self.spawn[0], self.spawn[1] ,self.surfWidth,self.surfHeight, self.mMapsize, self.map)


    def update(self, joysticklist, playerList, deltaTime):
        """
        This draws all the player, enemy, world stuff to the subsurface
        THIS DOES NOT DRAW THE SUBSURFACE TO THE SCREEN
        IH is the input handler but it is not used right now
        deltaTime is passed to the camera update
        """
        self.deltaTime = deltaTime
        joyStick = joysticklist[self.me-1]
        if len(playerList) == 0:
            self.player.update(joyStick.mAxis[0], joyStick.mAxis[1], self.map.mEnemyList, deltaTime)
        else:
            self.player.update(joyStick.mAxis[0], joyStick.mAxis[1], playerList, deltaTime)

        if joyStick.mButtons[0]: #A/h
            self.player.swingSword()
        if joyStick.mButtons[1]: #B/j
            for i in range(len(self.map.mItemList)):
                dist2 = (self.map.mItemList[i].getCenter()[0] - self.player.mX)**2 + (self.map.mItemList[i].getCenter()[1] - self.player.mY)**2
                if dist2 <= self.map.mItemList[i].mMapRadius2:
                    if self.map.mItemList[i].mUseOnPickup:
                        if (not self.player.mInventory.isWeaponInInventory(self.map.mItemList[i].mMyWeapon.mFileName)) or self.player.mInventory.getCurrentWeapon().mFileName == self.map.mItemList[i].mMyWeapon.mFileName:
                            self.map.mItemList[i].mPlayer = self.player

                            if self.map.mItemList[i].mIsWeapon and len(self.player.mInventory.weaponInventory) > 1:
                                # Respawn weapon in the old pickup place

                                tItem = getWeaponFromName(self.player.mInventory.getCurrentWeapon().mFileName)
                                tItem.mMyWeapon = self.player.mInventory.getCurrentWeapon()
                                tItem.mPos = self.map.mItemList[i].mPos
                                self.map.mItemList.append(tItem)

                            self.map.mItemList[i].effect()

                            del self.map.mItemList[i]
                            break

                    else:
                        self.player.pickUpItem(self.map.mItemList[i])

                        del self.map.mItemList[i]
                        break
        if joyStick.mButtons[2]: #X/k
            self.player.mInventory.useItem()
        if joyStick.mButtons[3]: #Y/l
            self.player.switchWeapon()

        # TO-DO: Draw all the other_players (a tuple of player objects)
        #   using *our* camera.

        onScreenEnemies = self.camera.getOnscreenEnemies()


        self.map.collideWalls(self.player)
        removeDead = []
        for i in range(len(self.map.mEnemyList)):
            self.map.mEnemyList[i].update(self.player, self.camera, self.map.mEnemyList, deltaTime)
            if self.map.mEnemyList[i].mIsDead and self.map.mEnemyList[i].mRespawnTimer == 0.0:
                removeDead.append(self.map.mEnemyList[i])
                continue
            self.map.collideWalls(self.map.mEnemyList[i])

        for i in range(len(removeDead)):
            onScreenEnemies.remove(removeDead[i])
            #spawn loot drop
            itemPos = VectorN(removeDead[i].mHitBox.center)
            itemType = random.randint(2, 4)
            newItem = getItemFromType(itemType)
            newItem.mPos = itemPos
            self.map.mItemList.append(newItem)

        # Do collision detections.
        for i in range(len(onScreenEnemies)):
            self.player.checkSwordCollision(onScreenEnemies[i], deltaTime)
            onScreenEnemies[i].checkSwordCollision(self.player, deltaTime)

        if len(playerList) == 0:
            # Check collisions with projectiles
            for i in range(len(onScreenEnemies)):
                for j in range(len(self.map.mProjectileList)):
                    self.map.mProjectileList[j].collideEntity(onScreenEnemies[i])

            for i in range(len(self.map.mProjectileList)):
                self.map.mProjectileList[i].collideEntity(self.player)

            removeList = []
            for i in range(len(self.map.mProjectileList)):
                # Update Projectiles
                self.map.mProjectileList[i].update(deltaTime)

                if self.map.mProjectileList[i].mRemove:
                    removeList.append(self.map.mProjectileList[i])

                elif self.map.collideWallsP(self.map.mProjectileList[i]):
                    removeList.append(self.map.mProjectileList[i])

            for projectile in removeList:
                self.map.mProjectileList.remove(projectile)

        self.hud.mWalkoverOverlay = None
        for i in range(len(self.map.mItemList)):
            dist2 = (self.map.mItemList[i].getCenter()[0] - self.player.mX)**2 + (self.map.mItemList[i].getCenter()[1] - self.player.mY)**2
            if dist2 <= self.map.mItemList[i].mMapRadius2:
                if self.map.mItemList[i].instantUse == True:
                    self.map.mItemList[i].mPlayer = self.player
                    self.map.mItemList[i].effect()
                    del self.map.mItemList[i]
                    break

                elif self.map.mItemList[i].mIsWeapon:
                    self.hud.mWalkoverOverlay = self.map.mItemList[i].mMyWeapon.drawOverlay(title="Ground Weapon: ")
                    break

        self.camera.update(self.player.mX, self.player.mY, self.surf)

    def render(self, other_players, modeChanged):
        self.surf.fill((0,0,0))

        self.camera.render(self.surf)
        for i in range(len(self.map.mItemList)):
            self.map.mItemList[i].render(self.surf, self.camera)
        for i in range(len(self.map.mEnemyList)):
            self.map.mEnemyList[i].render(self.surf, self.camera)
        for p in self.map.mProjectileList:
            p.render(self.surf, self.camera)
        self.player.render(self.surf, self.camera)
        if modeChanged:
            for op in other_players:
                op.render(self.surf, self.camera, False)
                for i in range(len(other_players)):
                    self.player.checkSwordCollision(other_players[i], self.deltaTime)

        self.hud.render(self.surf)
        self.inventory.render(self.surf)

        #Not technically render stuff but already passing modeChanged here and don't want to add new attributes to update
        if self.player.mCurHealth <= 0:
            self.player.getDeath(modeChanged, self.spawn)

    def setmap(self, mapobj):
        self.map = mapobj
        self.mMapsize = (self.map.mTileSurface.get_width(), self.map.mTileSurface.get_height())
        self.player.mMap = mapobj
        self.mMapSurf = self.map.mTileSurface
        newSpawn = self.map.getNewSpawn()
        if self.me == 1:
            self.player.mX = newSpawn[0]
            self.player.mY = newSpawn[1]
            self.spawn = [newSpawn[0], newSpawn[1]]
        if self.me == 2:
            self.player.mX = newSpawn[2]
            self.player.mY = newSpawn[3]
            self.spawn = [newSpawn[2], newSpawn[3]]
        if self.me == 3:
            self.player.mX = newSpawn[4]
            self.player.mY = newSpawn[5]
            self.spawn = [newSpawn[4], newSpawn[5]]
        if self.me == 4:
            self.player.mX = newSpawn[6]
            self.player.mY = newSpawn[7]
            self.spawn = [newSpawn[6], newSpawn[7]]
        self.camera.setTileMap(self.map)
        self.camera.setMap(self.map, self.mMapsize)
        self.player.mCurMana = self.player.mMaxMana
        self.player.mCurHealth = self.player.mMaxHealth





