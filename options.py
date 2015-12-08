import pygame
pause = False
# Volume
# Screen res
# full screen


class options(object):

    def __init__(self, volume, screen_Resolution):
        """use thsi class to change the volume and the screen resolution
            self.opt should be used in the main program to check if the options menu should be up
            """
        self.v = volume
        self.mainscreenWid = screen_Resolution[0]
        self.mainscreenHig = screen_Resolution[1]
        self.opt = True
        self.curSelect = 0

        pygame.font.init()


    def update(self, down, up,left,right, enter, back ,dt,opt):
        """intergrate controller and swap out the keyboard
            use the left and right keys to change volume and resolution
            use up and down to select the option
            press b to go back"""

        self.mFont = pygame.font.SysFont("Courier New", int(self.mainscreenHig * .10, ))


        self.opt = opt
        if   back ==True:
            self.opt = False
        if  down == True:

            if self.curSelect == 0:
                self.curSelect = 1
            else:
                self.curSelect -= 1
        elif up == True:
            if self.curSelect == 1:
                self.curSelect = 0
            else:
                self.curSelect += 1
        if self.curSelect == 0:
            if   left == True and self.v !=0:
                self.v -= 5
            if  right == True and self.v !=100:
                self.v += 5
        if self.curSelect == 1:
            if  right == True and self.mainscreenHig <= 800:
                self.mainscreenWid += 20
                self.mainscreenHig += 20


            if  left ==True and self.mainscreenHig >= 100:
                self.mainscreenWid -= 20
                self.mainscreenHig -= 20
        if down == False and up == False and right == False and left == False and back ==False and enter == False:

            self.opt = True
        return  self.opt,self.v, (self.mainscreenWid,self.mainscreenHig)




    def render(self, surf):
        """renders the squares to be a certain percent of the screen"""
        rez = self.mFont.render("Resolution", False, (0, 0, 0))
        vol = self.mFont.render("Volume", False, (0, 0, 0))
        surf.fill((0,0,0))
        vbar =((self.mainscreenWid*.45) * self.v) /100

        if self.curSelect == 0:
                pygame.draw.rect(surf, (255, 255, 0), (self.mainscreenWid * .25 - 5, self.mainscreenHig * .20 - 5, self.mainscreenWid * .50 + 10, self.mainscreenHig * .15 + 10))


        if self.curSelect == 1:
                pygame.draw.rect(surf, (255, 255, 0), (self.mainscreenWid * .25 - 5, self.mainscreenHig * .4-0 - 5, self.mainscreenWid * .50 + 10, self.mainscreenHig * .15 + 10))
        pygame.draw.rect(surf, (132, 112, 255), (self.mainscreenWid * .25, self.mainscreenHig * .20, self.mainscreenWid * .50, self.mainscreenHig * .15))



        pygame.draw.rect(surf, (132, 0, 255), (self.mainscreenWid * .25, self.mainscreenHig * .40, self.mainscreenWid * .50, self.mainscreenHig * .15))
        pygame.draw.rect(surf,(90,255,255),(self.mainscreenWid *.275, self.mainscreenHig *.225, vbar,self.mainscreenHig *.10 ))
        surf.blit(rez, (self.mainscreenWid * .275, self.mainscreenHig * .425))
        surf.blit(vol, (self.mainscreenWid *.275, self.mainscreenHig *.225))