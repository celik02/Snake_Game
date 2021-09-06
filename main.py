import pygame
import sys
import os
import time
import random
import sqlite3
from database import HighScores


database = HighScores()


pygame.init()
if not pygame.font: print("[WARNING] Font disabled...")
if not pygame.mixer: print("[WARNING] Sound disabled...")

random.seed(time.time())


SIZE = WIDTH,HEIGHT = 1200,800

BLACK = [0,0,0]
WHITE = [255,255,255]
COLOR1 = [128,128,128]
COLOR2 = [192,192,192]
RED = [255, 0 , 0]
BLUE = [0, 0, 200]
FPS = 60
VEL = 20  # this should be 1, 2, 4, 5, 10, 20 so series devisible by 40


WIN = pygame.display.set_mode(SIZE)

SCORE_FONT = pygame.font.SysFont("comic sans", 30)

GAME_OVER = pygame.font.SysFont("comic sans", 100)


def food_catch(background, food_rect, SNAKE_OBJ, SNAKE_lEN, score, snake_body):
    WIN.blit(background, (0,0))
    
    pose = list((SNAKE_OBJ.x, SNAKE_OBJ.y))
    snake_body.insert(0, pose)

    if abs(SNAKE_OBJ.x-food_rect.x*40) <=VEL and abs(SNAKE_OBJ.y - food_rect.y*40) <= VEL:

        # print("collision", SNAKE_OBJ.x, food_rect.x*40, SNAKE_OBJ.y, food_rect.y*40)
        food_rect.x = random.randint(0,29)
        food_rect.y = random.randint(0,19)
        score +=1
        SNAKE_lEN += 1
    else:
        if len(snake_body) > 1:
            snake_body.pop()
            # print(snake_body)
    

    score_font = SCORE_FONT.render("Score:" + str(score),1, RED)
    WIN.blit(score_font, (1200-score_font.get_width(),10))
    
    pygame.draw.circle(WIN, RED, (20 + food_rect.x*40, 20 + food_rect.y*40), 13)

    for body in snake_body:
        pygame.draw.rect(WIN, BLUE, pygame.Rect(body[0], body[1], 40, 40))

    pygame.display.update()

    return score, SNAKE_lEN, snake_body

    


def snake_move(keys_pressed, food_rect, SNAKE_OBJ, DIR):
    # DIR:0 UP, 1:LEFT, 2:DOWN, 3:RIGHT
    pressed = False
    gameOver = False
    if (keys_pressed[pygame.K_LEFT] and DIR !=3) or (keys_pressed[pygame.K_RIGHT] and DIR !=1) or (keys_pressed[pygame.K_DOWN] and DIR !=0) or (keys_pressed[pygame.K_UP] and DIR !=2):
        pressed = True

    if keys_pressed[pygame.K_LEFT] and DIR != 3 and SNAKE_OBJ.y%40 == 0 :
        DIR = 1
        pressed = False
    if keys_pressed[pygame.K_RIGHT] and DIR != 1 and SNAKE_OBJ.y%40 == 0:
        DIR = 3
        pressed = False
    if  keys_pressed[pygame.K_DOWN] and DIR!=0 and SNAKE_OBJ.x %40 ==0 :
        DIR = 2
        pressed = False
    if  keys_pressed[pygame.K_UP] and DIR != 2 and SNAKE_OBJ.x %40 ==0:
        DIR = 0
        pressed = False

    if DIR == 1:
        if SNAKE_OBJ.x- VEL>=0:
            SNAKE_OBJ.x -=VEL
        elif SNAKE_OBJ.x - VEL <0:
            print("game is over")
            gameOver = True
    elif DIR ==2:
        if SNAKE_OBJ.y + VEL <=800-40:
            SNAKE_OBJ.y += VEL
        elif SNAKE_OBJ.y + VEL > 800-40:
            print("game is over")
            gameOver = True
    elif  DIR == 3:
        if SNAKE_OBJ.x + VEL <=1200-40:
            SNAKE_OBJ.x += VEL
        elif SNAKE_OBJ.x + VEL > 1200-40:
            gameOver = True
            print("game is over")
    elif DIR == 0:
        if SNAKE_OBJ.y - VEL >= 0:
            SNAKE_OBJ.y -= VEL
        elif SNAKE_OBJ.y - VEL <0:
            gameOver = True
            print("game is over")
 
    
    return DIR, pressed, gameOver

def draw_game_over():
    game_over_font = GAME_OVER.render("GAME IS OVER", 1, RED)
    WIN.blit(game_over_font, ((1200-game_over_font.get_width())//2,400 ))
    pygame.display.update()

def main():
    DIR = random.randint(0,3)
    SNAKE_lEN = 1
    snake_body = []
    score = 0
    run = True
    # checkerboard background
    color = COLOR1
    username = "Player1"
    background = pygame.surface.Surface(WIN.get_size())
    for x in range(0, WIDTH, 40):
        if color == COLOR1:
            color = COLOR2
        else:
            color = COLOR1
        for y in range(0, HEIGHT, 40):
            pygame.draw.rect(background, color, [x,y, 40,40])
            if color == COLOR1:
                color = COLOR2
            else:
                color = COLOR1

    food_rect = pygame.Rect(0, 0, 40, 40)
    SNAKE_OBJ = pygame.Rect(random.randint(3,26)*40, random.randint(3, 16)*40, 40, 40)
    
    #main game loop
    while run:
        pygame.time.Clock().tick(FPS)  # set the desired FPS
        pressed = True
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        key_pressed = pygame.key.get_pressed()
        count = 40
        while pressed and count >= 0:
            pygame.time.Clock().tick(60)
            DIR, pressed, gameOver = snake_move(key_pressed, food_rect, SNAKE_OBJ, DIR)
            score, SNAKE_lEN, snake_body = food_catch(background, food_rect, SNAKE_OBJ, SNAKE_lEN, score, snake_body)
            count -= VEL

        for block in snake_body[1:]:
            if block[0] == SNAKE_OBJ.x and block[1] == SNAKE_OBJ.y:
                gameOver = True
        

        if gameOver:
            draw_game_over()
            pygame.time.delay(1000)
            run = False
            database.update(username, score)
            


    main()

if __name__ == '__main__':
    main()


        

    

