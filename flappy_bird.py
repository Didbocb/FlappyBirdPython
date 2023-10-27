import pygame
from pygame.locals import *

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

#load images
background_img = pygame.image.load('sprites/background-day.png')
ground_img = pygame.image.load('sprites/base.png')

pygame_icon = pygame.image.load('favicon.ico')
pygame.display.set_icon(pygame_icon)

run = True
while run:

    clock.tick(fps)

    screen.blit(background_img, (0, 0))
    screen.blit(background_img, (288, 0))

    screen.blit(ground_img, (ground_scroll, 512))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 48:
        ground_scroll = 0

    screen.blit(ground_img, (ground_scroll2, 512))
    ground_scroll2 -= scroll_speed
    if ground_scroll2 < 288:
        ground_scroll2 = 336

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()