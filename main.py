import pygame
# Pygame setup
pygame.joystick.init()
pygame.font.init()
pygame.display.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800,600))


import input_handler
from MapReader import MapReader
import startclass
import pane
from Items import *



musicStart = False
finalMusicStart = False
gameOver = False
showFPS = True
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(),20)

battleTime = 150

timeleft = battleTime
modeChanged = False
paused = False

pausefade = pygame.Surface([screen.get_width(),screen.get_height()])
pausefade.fill([0,0,0])
pausefade.set_alpha(225)
pausetext = font.render(("Paused"), 1, [255,255,255])

# Load assets
joySticks = input_handler.InputHandler().mJoyList
while len(joySticks) < 4:
    joySticks.append(None)
    if len(joySticks) == 4:
        joySticks[3] = input_handler.Joystick(-1)

playerthing = startclass.start.thing(screen)

all_panes = []

if playerthing[0] == True:
    pane1 = pane.pane(screen, "imgs/playersprite0.png", "imgs/enemysprite.png",
                      "imgs/tileset.png",1, (0,0))
    all_panes.append(pane1)
if playerthing[1] == True:
    pane2 = pane.pane(screen, "imgs/playersprite1.png", "imgs/enemysprite.png",
                      "imgs/tileset.png",2, (screen.get_width()/2,0))
    all_panes.append(pane2)
if playerthing[2] == True:
    pane3 = pane.pane(screen, "imgs/playersprite2.png", "imgs/enemysprite.png",
                        "imgs/tileset.png",3, (0,screen.get_height()/2))
    all_panes.append(pane3)
if playerthing[3] == True:
  
    pane4 = pane.pane(screen, "imgs/playersprite3.png", "imgs/enemysprite.png",
                      "imgs/tileset.png",4, (screen.get_width() / 2, screen.get_height() / 2))
    all_panes.append(pane4)

playerList = []

clock.tick()

tileset = pygame.image.load("imgs/tileset.png").convert()
MapRead = MapReader(tileset, (152,142,133))
finalmap = MapRead.makeMap("maps/emptymap.txt")

# Game Loop
while not gameOver:
    # UPDATES:
    dt = clock.tick() / 1000.0

    if dt > .2:
        dt = 0

    if musicStart == False:
        pygame.mixer.music.load("Sound/main.ogg")
        pygame.mixer.music.play(-1)
        musicStart = True

    eList = pygame.event.get()
    keys = pygame.key.get_pressed()

    if not paused:
        timeleft -= dt
        if timeleft <= 3:
            pygame.mixer.music.fadeout(3000)
        if timeleft <= 0 and modeChanged == False:
            if playerthing[0] == True:
                pane1.setmap(finalmap)
            if playerthing[1] == True:
                pane2.setmap(finalmap)
            if playerthing[2] == True:
                pane3.setmap(finalmap)
            if playerthing[3] == True:
                pane4.setmap(finalmap)
            timeleft = 60 * 1
            modeChanged = True

        for i in joySticks:
            if i is not None:
                i.update(eList)
                if i.mButtons[7]:
                    paused = not paused

        for p in all_panes:
            p.update(joySticks, playerList, dt)

        # INPUT
        # ... do event-handling
        for e in eList:
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                gameOver = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_o:
                showFPS = not showFPS

        if modeChanged:
            if finalMusicStart == False:
                pygame.mixer.music.load("Sound/battle.ogg")
                pygame.mixer.music.play(-1)
                finalMusicStart = True
            for i in range(len(playerList)):
                for j in range(len(finalmap.mProjectileList)):
                    finalmap.mProjectileList[j].collideEntity(playerList[i])

            removeList = []
            for i in range(len(finalmap.mProjectileList)):
                # Update Projectiles
                finalmap.mProjectileList[i].update(dt)
                if finalmap.mProjectileList[i].mRemove:
                    removeList.append(finalmap.mProjectileList[i])

                elif finalmap.collideWallsP(finalmap.mProjectileList[i]):
                    removeList.append(finalmap.mProjectileList[i])

            for projectile in removeList:
                finalmap.mProjectileList.remove(projectile)
        playersLeft = 0
        if modeChanged and len(playerList) < 1:
            for q in all_panes:
                playerList.append(q.player)
    else:
        for e in eList:
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                gameOver = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_o:
                showFPS = not showFPS
        for i in joySticks:
            if i is not None:
                i.update(eList)
                if i.mButtons[7]:
                    paused = not paused

    screen.fill((0,0,0))

    for p in all_panes:
        otherPlayers = []
        # This next section of code does what the generator (on the line below the following section) did
        if modeChanged and len(otherPlayers) < 1:
            for q in all_panes:
                if q.me != p.me and q.player.mIsDead == False:
                    otherPlayers.append(q.player)
        if p.player.mIsDead == False:
            p.render(otherPlayers, modeChanged)
            screen.blit(p.surf, p.screen_offset)
            #Throwing this in here because we are already iterating though the panes here
            playersLeft += 1
    pygame.draw.line(screen, (255,255,255), (screen.get_width()/2, 0), (screen.get_width()/2, screen.get_height()), 2)
    pygame.draw.line(screen, (255,255,255), (0, screen.get_height()/2), (screen.get_width(), screen.get_height()/2), 2)
    if playersLeft <= 1:
        for p in all_panes:
            if p.player.mLives >= 1:
                if modeChanged:
                    winner = font.render("Player " + str(p.me) + " Is The Winner!!!", 1, [242,255,0])
                    restarttxt = font.render("Press back to restart", 1, [242,255,0])
                    pygame.draw.rect(screen, [0,0,0], [(screen.get_width() - winner.get_width()) / 2 - 5,
                                                       (screen.get_height() - winner.get_height()) / 2 - 5,
                                                       winner.get_width()+10, winner.get_height()+25])
                    screen.blit(winner, ((screen.get_width() - winner.get_width()) / 2, (screen.get_height() - winner.get_height()) / 2))
                    screen.blit(restarttxt, ((screen.get_width() - winner.get_width()) / 2 + 20, (screen.get_height() - winner.get_height()) / 2 + 20))
                    for i in joySticks:
                        if i is not None:
                            i.update(eList)
                            if i.mButtons[6]:

                                timeleft = battleTime
                                modeChanged = False
                                musicStart = False
                                finalMusicStart = False

                                playerthing = startclass.start.thing(screen)
                                all_panes = []

                                if playerthing[0] == True:
                                    pane1 = pane.pane(screen, "imgs/playersprite0.png", "imgs/enemysprite.png",
                                                      "imgs/tileset.png",1, (0,0))
                                    all_panes.append(pane1)
                                if playerthing[1] == True:
                                    pane2 = pane.pane(screen, "imgs/playersprite1.png", "imgs/enemysprite.png",
                                                      "imgs/tileset.png",2, (screen.get_width()/2,0))
                                    all_panes.append(pane2)
                                if playerthing[2] == True:
                                    pane3 = pane.pane(screen, "imgs/playersprite2.png", "imgs/enemysprite.png",
                                                        "imgs/tileset.png",3, (0,screen.get_height()/2))
                                    all_panes.append(pane3)
                                if playerthing[3] == True:
                                    pane4 = pane.pane(screen, "imgs/playersprite3.png", "imgs/enemysprite.png",
                                                      "imgs/tileset.png",4, (screen.get_width() / 2, screen.get_height() / 2))
                                    all_panes.append(pane4)

                                playerList = []
                                clock.tick()

                                tileset = pygame.image.load("imgs/tileset.png").convert()
                                MapRead = MapReader(tileset, (152,142,133))

    if not modeChanged:
        if timeleft > 10:
            timer = font.render( str(round(timeleft)), 1, [255,255,255])
        else:
            timer = font.render( str(round(timeleft)), 1, [255,0,0])
        pygame.draw.rect(screen, [0,0,0], [(screen.get_width() - timer.get_width()) / 2 - 5,
                                           (screen.get_height() - timer.get_height()) / 2 - 5,
                                           timer.get_width()+10, timer.get_height()+10])
        screen.blit(timer, ((screen.get_width() - timer.get_width()) / 2, (screen.get_height() - timer.get_height()) / 2))

    if paused:
        screen.blit(pausefade, (0,0))
        screen.blit(pausetext, ((screen.get_width() - pausetext.get_width()) / 2, (screen.get_height() - pausetext.get_height()) / 2))

    if showFPS:
        fpstext = font.render("FPS: " + str(round(clock.get_fps())), 1, [255,255,255])
        screen.blit(fpstext, (0,0))

    pygame.display.flip()
# Pygame shutdown
pygame.mixer.quit()
pygame.font.quit()
pygame.joystick.quit()
pygame.display.quit()
