import pygame

font = pygame.font.SysFont("Times New Roman", 15)
class HUD(object):
    def __init__(self, player, playerNumber, face):
        self.playerNumber = playerNumber
        self.mPlayer = player
        self.weapon = font.render(str("Weapon"), True, (243, 243, 21))
        self.item = font.render(str("Item"), True, (243, 243, 21))
        self.face = face
        self.mWalkoverOverlay = None

    def render(self, surf):
        w = surf.get_width()
        h = surf.get_height()
        bottomStatBar = h - 55
        #weapon inventory
        pygame.draw.rect(surf, (255, 255, 255), [3, 3, 50, 50], 1)
        surf.blit(self.weapon, (0, 50))
        #item inventory
        pygame.draw.rect(surf, (255, 255, 255), [63, 3, 50, 50], 1)
        surf.blit(self.item, (73, 50))
        #stats
        stats = font.render(str("Strength:  " + "{:.1f}".format(self.mPlayer.mAttack) + "    Speed:  " + "{:.2f}".format(self.mPlayer.mSpeedMult) + "    Defense:  " + "{:.1f}".format(self.mPlayer.mDefense)), True, (243, 243, 21))
        surf.blit(stats, (120, 0))
        #ring
        pygame.draw.ellipse(surf, (255, 255, 255), [0, bottomStatBar, 200, 50], 5)
        #face rect padding
        pygame.draw.rect(surf, (0, 0, 255), [5, bottomStatBar, 50, 50])
        #player face
        surf.blit(self.face, (6, bottomStatBar + 1), [((self.playerNumber - 1) * 48), 0, 48, 48])
        #health and special bar padding
        if self.mPlayer.mMaxHealth >= self.mPlayer.mMaxMana:
            padding = self.mPlayer.mMaxHealth
        else:
            padding = self.mPlayer.mMaxMana
        pygame.draw.rect(surf, (0, 0, 255), [55, bottomStatBar + 12, padding, 26])
        #empty health bar
        pygame.draw.rect(surf, (30, 30, 30), [55, bottomStatBar + 17, self.mPlayer.mMaxHealth, 5])
        #health bar
        if self.mPlayer.mCurHealth > 0:
            pygame.draw.rect(surf, (255, 0, 0), [55, bottomStatBar + 17, self.mPlayer.mCurHealth, 5])
        #empty special bar
        pygame.draw.rect(surf, (30, 30, 30), [55, bottomStatBar + 28, self.mPlayer.mMaxMana, 5])
        #special bar
        if self.mPlayer.mCurMana > 0:
            pygame.draw.rect(surf, (0, 255, 0), [55, bottomStatBar + 28, self.mPlayer.mCurMana, 5])


        #Blit the overlays
        curFarRight = surf.get_width() - 5
        curFarBottom = surf.get_height() - 5

        # player's weapon
        if self.mPlayer.mInventory.hasWeapon():
            overlay = self.mPlayer.mInventory.getCurrentWeapon().drawOverlay(title="Equipped Weapon: ")

            surf.blit(overlay, (curFarRight - overlay.get_width(), curFarBottom - overlay.get_height()))
            curFarRight -= overlay.get_width() + 5

        if self.mWalkoverOverlay:
            surf.blit(self.mWalkoverOverlay, (curFarRight - self.mWalkoverOverlay.get_width(), curFarBottom - self.mWalkoverOverlay.get_height()))

