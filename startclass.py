import pygame

pygame.mixer.init()
pygame.mixer.music.load("Sound\\title.ogg")

class start(object):
    def thing(screen):
        pygame.mixer.music.load("Sound\\title.ogg")
        screenW = screen.get_width()
        screenH = screen.get_height()
        pback = pygame.image.load("imgs\\jail.jpg").convert()
        booms = pygame.image.load("imgs\\boom.png").convert()
        pback = pygame.transform.scale(pback,(int(screenW/2),int(screenH/2)))
        boom = pygame.transform.scale(booms,((int(screenW/2),int(screenH/2))))
        start = pygame.image.load("imgs\\start.png").convert()
        background = pygame.image.load("imgs\\castle.jpg")
        background = pygame.transform.scale(background,(screenW,screenH))
        start = pygame.transform.scale(start,(350,100))
        start.set_colorkey((0,0,0))
        start.set_alpha(200)


        done = False
        musicStart = False
        startText = pygame.font.SysFont("Courier New", 24)
        startText1 = pygame.font.SysFont("Comic Sans", 36)
        startText2 = pygame.font.SysFont("Comic Sans", 42)
        credits = False
        controls = False
        joys = []
        for i in range(pygame.joystick.get_count()):
            joys.append(pygame.joystick.Joystick(i))
            joys[-1].init()

        playerMappings = []
        mode = "start"
        p1 = False
        p2 = False
        p3 = False
        p4 = False

        while not done:
            eList = pygame.event.get()
            keys = pygame.key.get_pressed()
            for e in eList:
                if e.type == pygame.KEYDOWN and len(joys) < 4:
                    if keys[pygame.K_a]:
                        if mode == "start":
                            mode = "select"
                        elif mode == "select":
                            p4 = True
                    elif keys[pygame.K_BACKSPACE]:
                        if mode == "start":
                            done = True
                        elif mode == "select" and not (p1 or p2 or p3 or p4):
                            mode = "start"
                        elif mode == "select":
                            p4 = False
                    elif keys[pygame.K_RETURN] and mode == "select":
                        mode = "game"
                if e.type == pygame.JOYBUTTONDOWN:
                    if e.button == 3:
                        credits = True
                    elif e.button == 2:
                        controls = True
                    elif e.button == 0:
                        if mode == "start":
                            mode = "select"
                        elif mode == "select":
                            if e.joy not in playerMappings:
                                playerMappings.append(e.joy)
                            if e.joy == 0:
                                p1 = True

                            if e.joy == 1:
                                p2 = True

                            if e.joy == 2:
                                p3 = True

                            if e.joy == 3:
                                p4 = True
                    elif e.button == 1:
                        if mode == "start":
                            done = True

                        elif mode == "select" and not (p1 or p2 or p3 or p4):
                            mode = "start"

                        elif mode == "select":
                            if e.joy == 0:
                                p1 = False


                            if e.joy == 1:
                                p2 = False


                            if e.joy == 2:
                                p3 = False


                            if e.joy == 3:
                                p4 = False

                    elif e.button == 7 and mode == "select" and len(playerMappings) > 0:
                        mode = "game"
                else:
                    credits = False
                if e.type == pygame.QUIT or  pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    done = True
            # Draw screen
            if mode == "start":
                if musicStart == False:
                    pygame.mixer.music.play(-1)
                    musicStart = True
                screen.fill((0, 0, 255))
                screen.blit(background, (0,0))
                tempS = startText.render("Press A to start", 1, (0,0,0))
                tempB = startText.render("Press Y for Credits", 1, (0,0,0))
                tempX = startText.render("Press X for controls", 1, (0,0,0))

                screen.blit(start, ((screenW - start.get_width()) / 2, (screenH - start.get_height()) / 2))
                screen.blit(tempS, ((screenW - tempX.get_width()) / 2, ((screenH - tempB.get_height()) / 2) - 20))
                screen.blit(tempB, ((screenW - tempX.get_width()) / 2, (screenH - tempB.get_height()) / 2))
                screen.blit(tempX, ((screenW - tempX.get_width()) / 2, ((screenH - tempB.get_height()) / 2) + 20))



                if pygame.key.get_pressed()[pygame.K_y] or credits:
                    temp0 = startText2.render("Credits", 1, (0,0,0))
                    temp1 = startText1.render("Duke Mike Barlage", 1, (0,0,0))
                    temp2 = startText1.render("Barron Logan Boggs", 1, (0,0,0))
                    temp3 = startText1.render("Chickenator Kory Byrne", 1, (0,0,0))
                    temp4 = startText1.render("The Best Marshall Fuentes", 1, (0,0,0))
                    temp5 = startText1.render("Overlord Brian Gallagher", 1, (0,0,0))
                    temp6 = startText1.render("Tsar Chris Gallagher (Composer)", 1, (0,0,0))
                    temp7 = startText1.render("Dictator Adam Schroeder", 1, (0,0,0))
                    temp8 = startText1.render("Knyaz Sarrency Seymour", 1, (0,0,0))
                    temp9 = startText1.render("Odd Christopher Charles Taylor III", 1, (0,0,0))
                    screen.fill((0, 150, 255))
                    screen.blit(temp0, ((screenW - temp0.get_width()) / 2, 30))
                    screen.blit(temp1, ((screenW - temp1.get_width()) / 2, 100))
                    screen.blit(temp2, ((screenW - temp2.get_width()) / 2, 140))
                    screen.blit(temp3, ((screenW - temp3.get_width()) / 2, 180))
                    screen.blit(temp4, ((screenW - temp4.get_width()) / 2, 220))
                    screen.blit(temp5, ((screenW - temp5.get_width()) / 2, 260))
                    screen.blit(temp6, ((screenW - temp6.get_width()) / 2, 300))
                    screen.blit(temp9, ((screenW - temp9.get_width()) / 2, 340))
                    screen.blit(temp7, ((screenW - temp7.get_width()) / 2, 380))
                    screen.blit(temp8, ((screenW - temp8.get_width()) / 2, 420))


                elif pygame.key.get_pressed()[pygame.K_x] or controls:
                    joystick = startText2.render("Joystick", 1, (0,0,0))
                    joy1 = startText1.render("Movement: Left analog", 1, (0,0,0))
                    joy2 = startText1.render("Attack: A/button0", 1, (0,0,0))
                    joy3 = startText1.render("Pickup item/weapon: B/button1", 1, (0,0,0))
                    joy4 = startText1.render("Use item: X/button2", 1, (0,0,0))
                    joy5 = startText1.render("Switch weapon: Y/button3", 1, (0,0,0))
                    keyboard = startText2.render("Keyboard", 1, (0,0,0))
                    key1 = startText1.render("Movement: WASD", 1, (0,0,0))
                    key2 = startText1.render("Attack: H", 1, (0,0,0))
                    key3 = startText1.render("Pickup item/weapon: J", 1, (0,0,0))
                    key4 = startText1.render("Use item: K", 1, (0,0,0))
                    key5 = startText1.render("Switch weapon: L", 1, (0,0,0))
                    screen.fill((0, 150, 255))
                    screen.blit(joystick, ((screenW - joystick.get_width()) / 2, 10))
                    screen.blit(joy1, ((screenW - joy3.get_width()) / 2, 60))
                    screen.blit(joy2, ((screenW - joy3.get_width()) / 2, 100))
                    screen.blit(joy3, ((screenW - joy3.get_width()) / 2, 140))
                    screen.blit(joy4, ((screenW - joy3.get_width()) / 2, 180))
                    screen.blit(joy5, ((screenW - joy3.get_width()) / 2, 220))
                    screen.blit(keyboard, ((screenW - keyboard.get_width()) / 2, 300))
                    screen.blit(key1, ((screenW - joy3.get_width()) / 2, 350))
                    screen.blit(key2, ((screenW - joy3.get_width()) / 2, 390))
                    screen.blit(key3, ((screenW - joy3.get_width()) / 2, 430))
                    screen.blit(key4, ((screenW - joy3.get_width()) / 2, 470))
                    screen.blit(key5, ((screenW - joy3.get_width()) / 2, 510))



            elif mode == "select":
                screen.fill((255, 0, 0))
                if p1:
                    pygame.draw.rect(screen,(0,20,45), (0, 0, screenW/2, screenH/2))
                    screen.blit(boom,(0,0))
                    p1Ready = startText.render(("PLAYER 1 READY!"), 1, (0,0,0))
                    screen.blit(start, (screenW/4 - start.get_width()/2,
                                          screenH/4 - start.get_height()/2))
                    screen.blit(p1Ready, (screenW/4 - p1Ready.get_width()/2,
                                          screenH/4 - p1Ready.get_height()/2))
                else:
                    screen.blit(pback,(0,0))
                    p1Start = startText.render(("Press A to join!"),1 , (0,0,0))
                    screen.blit(start, (screenW/4 - start.get_width()/2,
                                          screenH/4 - start.get_height()/2))
                    screen.blit(p1Start, (screenW/4 - p1Start.get_width()/2,
                                          screenH/4 - p1Start.get_height()/2))

                if p2:
                    pygame.draw.rect(screen,(0,90,45), (screenW/2, 0, screenW, screenH/2))
                    screen.blit(boom,(screenW/2,0))
                    p2Ready = startText.render(("PLAYER 2 READY!"), 1, (0,0,0))
                    screen.blit(start, (screenW - screenW/4 - start.get_width()/2,
                                          screenH/4 - start.get_height()/2))
                    screen.blit(p2Ready, (screenW - screenW/4 - p2Ready.get_width()/2,
                                          screenH/4 - p2Ready.get_height()/2))
                else:
                    screen.blit(pback,(screenW/2,0))
                    p2Start = startText.render(("Press A to join!"),1 , (0,0,0))
                    screen.blit(start, (screenW - screenW/4 - start.get_width()/2,
                                          screenH/4 - start.get_height()/2))
                    screen.blit(p2Start, (screenW - screenW/4 - p2Start.get_width()/2,
                                          screenH/4 - p2Start.get_height()/2))

                if p3:
                    screen.blit(boom,(0,screenH/2))
                    p3Ready = startText.render(("PLAYER 3 READY!"), 1, (0,0,0))
                    screen.blit(start, (screenW/4 - start.get_width()/2,
                                          screenH - screenH/4 - start.get_height()/2))
                    screen.blit(p3Ready, (screenW/4 - p3Ready.get_width()/2,
                                          screenH - screenH/4 - p3Ready.get_height()/2))
                else:
                    screen.blit(pback,(0,screenH/2))
                    p3Start = startText.render(("Press A to join!"),1 , (0,0,0))
                    screen.blit(start, (screenW/4 - start.get_width()/2,
                                          screenH - screenH/4 - start.get_height()/2))
                    screen.blit(p3Start, (screenW/4 - p3Start.get_width()/2,
                                          screenH - screenH/4 - p3Start.get_height()/2))

                if p4:
                    screen.blit(boom,(screenW/2,screenH/2))
                    p4Ready = startText.render(("PLAYER 4 READY!"), 1, (0,0,0))
                    screen.blit(start, (screenW - screenW/4 - start.get_width()/2,
                                          screenH - screenH/4 - start.get_height()/2))
                    screen.blit(p4Ready, (screenW - screenW/4 - p4Ready.get_width()/2,
                                          screenH - screenH/4 - p4Ready.get_height()/2))
                else:
                    screen.blit(pback,(screenW/2,screenH/2))
                    p4Start = startText.render(("Press A to join!"),1 , (0,0,0))
                    screen.blit(start, (screenW - screenW/4 - start.get_width()/2,
                                          screenH - screenH/4 - start.get_height()/2))
                    screen.blit(p4Start, (screenW - screenW/4 - p4Start.get_width()/2,
                                          screenH - screenH/4 - p4Start.get_height()/2))
            else:
                screen.fill((0, 0, 0))
                playerlist = [p1, p2, p3, p4]
                pygame.mixer.music.stop()
                return playerlist

            pygame.display.flip()
