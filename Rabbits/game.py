''' description about this game'''
'''
Win: if you can reach 60% accuracy in the given time, then, you wil the game
Lose: if your health value is zero, or your accuracy is below 60% in the given time,
      then, you will lose the game
'''
import pygame
from pygame.locals import *
import math
import random

# init the game
pygame.init()
width = 640
height = 480
# define the screen
screen = pygame.display.set_mode((width, height))

# record the status of keys: w a s d
keys = [False, False, False, False]
# initial position of the player
playerPos = [200, 200]
# record the information of accuracy, first element presents the number of projectile arrows
# second element presents the number of killed wild pigs
acc = [0, 0]
accuracy = 0
# record the status of arrows
arrows = []


# load all the images
player = pygame.image.load("resources/images/dude.png")
player1 = pygame.image.load("resources/images/dude2.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badGuy = pygame.image.load("resources/images/badguy.png")
healthBar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameOver = pygame.image.load("resources/images/gameover.png")
youWin = pygame.image.load("resources/images/youwin.png")

# load all the audios
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# determine whether to change player
flag = 0

badTimer = 100
badTimerTemp = 0
badGuys = [[640, 100]]
healthValue = 194

running = 1
# exitCode mean which way to exit the game, 0 presents health value is 0; 1 presents time is up
exitCode = 0
while running:
    badTimer -= 1
    # clear the screen for every start
    screen.fill(0)

    # draw the background, including grass and castles
    for x in range(int(width/grass.get_width()) + 1):
        for y in range(int(height/grass.get_height()) + 1):
            screen.blit(grass, (x * 100, y * 100))
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    # get the mouse position
    position = pygame.mouse.get_pos()
    # get the angle according to player position and mouse position
    angle = math.atan2(position[1] - (playerPos[1] + 32), position[0] - (playerPos[0] + 26))
    # get the rotated player
    if flag == 0:
        playerRot = pygame.transform.rotate(player, 360 - angle * 57.29)
    else:
        playerRot = pygame.transform.rotate(player1, 360 - angle * 57.29)
    playerPosTemp = (playerPos[0] - playerRot.get_rect().width / 2, playerPos[1] - playerRot.get_rect().height / 2)
    screen.blit(playerRot, playerPosTemp)

    index = 0
    # draw the arrows
    for bullet in arrows:
        # distance it moves
        velX = math.cos(bullet[0]) * 10
        velY = math.sin(bullet[0]) * 10
        bullet[1] += velX
        bullet[2] += velY
        # check whether the arrow is outside of the screen, if it is, then pop from the original list
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            arrows.pop(index)
        # keep recording which bullet is outside of the screen
        index += 1
        # draw all the arrows in the screen
        for projectile in arrows:
            # get the rotated arrow and then draw to the screen
            arrowRotTemp = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrowRotTemp, (projectile[1], projectile[2]))

    # print(len(arrows))

    # set the interval time slot of enemies
    if badTimer == 0:
        badGuys.append([640, random.randint(50, 450)])
        badTimer = 100 - badTimerTemp * 2
        if badTimerTemp >= 35:
            badTimerTemp = 35
        else:
            badTimerTemp += 5

    index1 = 0
    # draw the enemies
    for badGuyPos in badGuys:
        # the value of player will decrease randomly when the wild pig's x coordinate is less than 64
        badGuyRect = pygame.Rect(badGuy.get_rect())
        badGuyRect.top = badGuyPos[1]
        badGuyRect.left = badGuyPos[0]
        if badGuyPos[0] < 64:
            enemy.play()
            badGuys.pop(index1)
            healthValue -= random.randint(5, 25)
        # check whether the wild pig is outside of the screen
        if badGuyPos[0] < -64:
            badGuys.pop(index1)
        # the speed of the wild pig is 7
        badGuyPos[0] -= 5
        # check collision
        index2 = 0
        for bullet in arrows:
            bulletRect = pygame.Rect(arrow.get_rect())
            bulletRect.top = bullet[2]
            bulletRect.left = bullet[1]
            if badGuyRect.colliderect(bulletRect):
                hit.play()
                acc[1] += 1
                badGuys.pop(index1)
                arrows.pop(index2)
            index2 += 1
        index1 += 1
        for badGuyPosTemp in badGuys:
            screen.blit(badGuy, (badGuyPosTemp[0], badGuyPosTemp[1]))

    # draw the health bar
    screen.blit(healthBar, (5, 5))
    for healthTemp in range(healthValue):
        screen.blit(health, (healthTemp + 8, 8))

    # draw the clock
    font = pygame.font.Font(None, 24)
    survivedTime = font.render(str(int((60000 - pygame.time.get_ticks()) / 60000)) + ':' +
                               str(int((60000 - pygame.time.get_ticks()) % 60000 / 1000)).zfill(2), True, (0, 0, 0))
    textRect = survivedTime.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survivedTime, textRect)

    # time is up
    print(pygame.time.get_ticks())
    if pygame.time.get_ticks() >= 60000:
        running = 0
        exitCode = 1

    # win or lose check
    if healthValue <= 0:
        running = 0
        exitCode = 0

    # calculate the accuracy
    if acc[0] == 0:
        pass
    else:
        accuracy = acc[1] / acc[0] * 100

    pygame.display.flip()

    # deal with the events
    for event in pygame.event.get():
        # check if the event is quit
        if event.type == pygame.QUIT:
            # if it is, quit the game
            pygame.quit()
            exit(0)
        # event if key has been pushed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys[0] = True
            elif event.key == pygame.K_a:
                keys[1] = True
            elif event.key == pygame.K_s:
                keys[2] = True
            elif event.key == pygame.K_d:
                keys[3] = True
        # event after key has been released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
        # event after mouse button has been pushed
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            flag = 1
            position = pygame.mouse.get_pos()
            acc[0] += 1
            # the first elem presents the angle, the second and the third present x coordinate and y coordinate
            arrows.append([math.atan2(position[1]-(playerPosTemp[1]+32), position[0]-(playerPosTemp[0]+26)),
                           playerPosTemp[0] + 32, playerPosTemp[1] + 32])
        if event.type == pygame.MOUSEBUTTONUP:
            flag = 0

    # move the player by keys: w a s d
    if keys[0]:
        playerPos[1] -= 5
    elif keys[1]:
        playerPos[0] -= 5
    if keys[2]:
        playerPos[1] += 5
    elif keys[3]:
        playerPos[0] += 5

# display win or lose
if exitCode == 0:
    pygame.font.init()
    fontNew = pygame.font.Font(None, 24)
    text = fontNew.render('Accuracy: ' + str(int(accuracy)) + '%', True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(gameOver, (0, 0))
    screen.blit(text, textRect)
elif exitCode == 1 and int(accuracy) < 60:
    pygame.font.init()
    fontNew = pygame.font.Font(None, 24)
    text = fontNew.render('Accuracy: ' + str(int(accuracy)) + '%', True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(gameOver, (0, 0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    fontNew = pygame.font.Font(None, 24)
    text = fontNew.render('Accuracy: ' + str(accuracy) + '%', True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(youWin, (0, 0))
    screen.blit(text, textRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()