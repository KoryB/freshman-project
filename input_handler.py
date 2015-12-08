import pygame

class InputHandler(object):
    def __init__(self):
        self.mJoyList = []
        for i in range(pygame.joystick.get_count()):
            self.mJoyList.append(Joystick(i))
            self.mJoyList[i].mJoy.init()

class Joystick(object):
    def __init__(self, joyNum):
        if joyNum >= 0:
            self.mJoy = pygame.joystick.Joystick(joyNum)
        else:
            self.mJoy = -1
        self.mButtons = [(False,)*10]
        self.mAxis = [0.0, 0.0]
    def update(self, eList):
        a,b,x,y,lb,rb,select,start,l3,r3 = (False,)*10
        if self.mJoy != -1:
            self.mAxis = [self.mJoy.get_axis(0), self.mJoy.get_axis(1)]
            for e in eList:
                if e.type == pygame.JOYBUTTONDOWN and e.joy == self.mJoy.get_id():
                    if e.button == 0:
                        a = True
                    elif e.button == 1:
                        b = True
                    elif e.button == 2:
                        x = True
                    elif e.button == 3:
                        y = True
                    elif e.button == 7:
                        start = True
                    elif e.button == 6:
                        select = True
                    """elif e.button == 4:
                        lb = True
                    elif e.button == 5:
                        rb = True
                    elif e.button == 8:
                        l3 = True
                    elif e.button == 9:
                        r3 = True"""
        else:
            self.mAxis = [0.0, 0.0]
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:         self.mAxis[0] -= 1.0
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:        self.mAxis[0] += 1.0
            if keys[pygame.K_UP] or keys[pygame.K_w]:           self.mAxis[1] -= 1.0
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:         self.mAxis[1] += 1.0
            if self.mAxis[0] != 0 and self.mAxis[1] != 0:
                d = 1.41421356237 #square root of 2
                self.mAxis[0] *= d
                self.mAxis[1] *= d
            for e in eList:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_h:
                        a = True
                    elif e.key == pygame.K_j:
                        b = True
                    elif e.key == pygame.K_k:
                        x = True
                    elif e.key == pygame.K_l:
                        y = True
                    elif e.key == pygame.K_p:
                        start = True
                    elif e.key == pygame.K_BACKSPACE:
                        select = True
                    """elif e.key == pygame.K_ESCAPE:
                        lb = True
                    elif e.key == pygame.K_ESCAPE:
                        rb = True
                    elif e.key == pygame.K_ESCAPE:
                        l3 = True
                    elif e.key == pygame.K_ESCAPE:
                        r3 = True"""
        self.mButtons = [a,b,x,y,lb,rb,select,start,l3,r3]