import pygame
from pygame.locals import *
from pygame.sprite import Group
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 576
screen_height = 624

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define game variables
ground_scroll = 0
ground_scroll2 = 336
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 800 #milliseconds
last_pipe = pygame.time.get_ticks()
pass_pipe = False
score = 0

#load images
background_img = pygame.image.load('sprites/background-day.png')
ground_img = pygame.image.load('sprites/base.png')

pygame_icon = pygame.image.load('favicon.ico')
pygame.display.set_icon(pygame_icon)

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        img = pygame.image.load('sprites/yellowbird-downflap.png')
        self.images.append(img)
        img = pygame.image.load('sprites/yellowbird-midflap.png')
        self.images.append(img)
        img = pygame.image.load('sprites/yellowbird-upflap.png')
        self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True:
            #gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 512:
                self.rect.y += int(self.vel)
        
        if game_over == False:
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/pipe-green.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Score(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.indexOnes = 0
        self.indexTens = 0
        self.indexHundreds = 0
        self.indexThousands = 0
        self.counter = 0
        for num in range(0, 10):
            img = pygame.image.load(f'sprites/{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
    def update(self):
        #handle the animation
        list_of_score_nums = [int(i) for i in str(score)]
        
        #updates the number of score sprites depending on digit number of places
        #I know this part of the code looks bad to look at but idc I just brute forced it
        if len(list_of_score_nums) == 1:
            self.indexOnes = list_of_score_nums[0]
            if self.indexOnes >= len(self.images):
                self.indexOnes = 0
            scoreCounterOnes.image = self.images[self.indexOnes]
        if len(list_of_score_nums) == 2:
            self.indexTens = list_of_score_nums[0]
            self.indexOnes = list_of_score_nums[1]
            if self.indexOnes >= len(self.images):
                self.indexOnes = 0
            if self.indexTens >= len(self.images):
                self.indexTens = 0
            scoreCounterOnes.image = self.images[self.indexOnes]
            scoreCounterTens.image = self.images[self.indexTens]
        if len(list_of_score_nums) == 3:
            self.indexHundreds = list_of_score_nums[0]
            self.indexTens = list_of_score_nums[1]
            self.indexOnes = list_of_score_nums[2]
            if self.indexOnes >= len(self.images):
                self.indexOnes = 0
            if self.indexTens >= len(self.images):
                self.indexTens = 0
            if self.indexHundreds >= len(self.images):
                self.indexHundreds = 0
            scoreCounterOnes.image = self.images[self.indexOnes]
            scoreCounterTens.image = self.images[self.indexTens]
            scoreCounterHundreds.image = self.images[self.indexHundreds]
        if len(list_of_score_nums) == 4:
            self.indexThousands = list_of_score_nums[0]
            self.indexHundreds = list_of_score_nums[1]
            self.indexTens = list_of_score_nums[2]
            self.indexOnes = list_of_score_nums[3]
            if self.indexOnes >= len(self.images):
                self.indexOnes = 0
            if self.indexTens >= len(self.images):
                self.indexTens = 0
            if self.indexHundreds >= len(self.images):
                self.indexHundreds = 0
            if self.indexThousands >= len(self.images):
                self.indexThousands = 0
            scoreCounterOnes.image = self.images[self.indexOnes]
            scoreCounterTens.image = self.images[self.indexTens]
            scoreCounterHundreds.image = self.images[self.indexHundreds]
            scoreCounterThousands.image = self.images[self.indexThousands]

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
score_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

scoreCounterOnes = Score(int(screen_width / 2), 40)
scoreCounterTens = Score(int(screen_width / 2), 40)
scoreCounterHundreds = Score(int(screen_width / 2), 40)
scoreCounterThousands = Score(int(screen_width / 2), 40)

run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(background_img, (0, 0))
    screen.blit(background_img, (288, 0))

    #draw bird
    bird_group.draw(screen)
    bird_group.update()

    #draw pipe
    pipe_group.draw(screen)

    #draw the ground
    screen.blit(ground_img, (ground_scroll, 512))
    screen.blit(ground_img, (ground_scroll2, 512))

    #update the score the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    
    #draw the score positioning and new digits based on score number
    list_of_score_nums = [int(i) for i in str(score)]

    if len(list_of_score_nums) == 1:
        score_group.add(scoreCounterOnes)
    elif len(list_of_score_nums) == 2:
        scoreCounterOnes.rect.center = [int(screen_width / 2 + 13), 40]
        score_group.add(scoreCounterTens)
        scoreCounterTens.rect.center = [int(screen_width / 2 - 13), 40]
    elif len(list_of_score_nums) == 3:
        scoreCounterOnes.rect.center = [int(screen_width / 2 + 26), 40]
        scoreCounterTens.rect.center = [int(screen_width / 2), 40]
        score_group.add(scoreCounterHundreds)
        scoreCounterHundreds.rect.center = [int(screen_width / 2 - 26), 40]
    elif len(list_of_score_nums) == 4:
        scoreCounterOnes.rect.center = [int(screen_width / 2 + 52), 40]
        scoreCounterTens.rect.center = [int(screen_width / 2 + 26), 40]
        scoreCounterHundreds.rect.center = [int(screen_width / 2), 40]
        score_group.add(scoreCounterThousands)
        scoreCounterThousands.rect.center = [int(screen_width / 2 - 26), 40]

    score_group.draw(screen)

    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over =  True

    #check if bird hits ground
    if flappy.rect.bottom >= 512:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-90, 90)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        pipe_group.update()

        #scroll the ground
        screen.blit(ground_img, (ground_scroll, 512))
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 48:
            ground_scroll = 0
        screen.blit(ground_img, (ground_scroll2, 512))
        ground_scroll2 -= scroll_speed
        if ground_scroll2 < 288:
            ground_scroll2 = 336
        
        #update score
        score_group.update()

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
        
    pygame.display.update()

pygame.quit()