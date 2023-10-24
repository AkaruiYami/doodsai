###
#   src/main.py
#       - twitch.tv/CodeNameTribbs

### IMPORTS
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time
import pygame
from pygame.locals import *
from dood import Dood
from food import Food

### PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((600, 600), DOUBLEBUF)
clock = pygame.time.Clock()
lock_fps = 30
running  = True

### DEBUG FLAGS
DEBUG_DRAWRECTS = False
DEBUG_DRAWCOLLISON_MASKS = False

### ENTITY LISTS
group_doods = pygame.sprite.Group()
group_foods = pygame.sprite.Group()
doods = []
foods = []
doods.append(Dood(pos=(300, 300), speed_mult=5.0))
foods.append(Food(pos=(30, 30), speed_mult=5.0))

### RENDER
def renderFrame():
    # Clear the frame
    screen.fill((60, 60, 60))

    # Render Foods
    for food in foods:
        render_food = food.render()
        screen.blit(render_food[0], render_food[1])
        if DEBUG_DRAWRECTS:
            pygame.draw.rect(screen, (255, 255, 0), food.getRect(), 1)
        if DEBUG_DRAWCOLLISON_MASKS:
            screen.blit(food.drawMask(), render_food[1])

    #Render Foods
    for dood in doods:
        render_dood = dood.render()
        screen.blit(render_dood[0], render_dood[1])
        if DEBUG_DRAWRECTS:
            pygame.draw.rect(screen, (255, 255, 0), dood.getRect(), 1)
        if DEBUG_DRAWCOLLISON_MASKS:
            screen.blit(dood.drawMask(), render_dood[1])

### UPDATES
def update(deltatime):
    # Update Food
    for food in foods:
        food.update(deltatime)
    # Update Doods
    for dood in doods:
        dood.update(deltatime)

# MAIN LOOP
while running:
    # Check for Events
    for event in pygame.event.get():
        # Window Events
        if event.type == pygame.QUIT:
            running = False
        # Key Events
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_1:
                DEBUG_DRAWRECTS = not DEBUG_DRAWRECTS
            if event.key == K_2:
                DEBUG_DRAWCOLLISON_MASKS = not DEBUG_DRAWCOLLISON_MASKS

    # Call renders
    renderFrame()
    
    # Call updates
    update(time.perf_counter())
    
    # display to screen
    pygame.display.flip()
    clock.tick(lock_fps)

### Exit App
pygame.quit()
