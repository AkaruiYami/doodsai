###
#   testtank/tank.py
#

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time
import pygame
from pygame.locals import *
from testfood import TestFood
import random

### Display Setting
main_width = 800
main_height = 800
main_flags = DOUBLEBUF
main_running = True
speed_multiplier = 10.0
pygame.init()
main_screen = pygame.display.set_mode((main_width, main_height), main_flags)
fps_clock = pygame.time.Clock()
fps_lock = 60

### DEBUG FLAGS
DEBUG_DRAW_RECTS = False
DEBUG_DRAW_COLLISION_MASKS = False

### GROUPS
doods = pygame.sprite.Group()
foods = pygame.sprite.Group()

def renderEntity(entity) -> None:
    main_screen.blit(entity.image, entity.pos)
    if DEBUG_DRAW_COLLISION_MASKS:
        main_screen.blit(entity.drawMask(), entity.pos)
    if DEBUG_DRAW_RECTS:
        w, h = entity.image.get_width(), entity.image.get_height()
        rect_surf = pygame.surface.Surface(size=(w, h))
        rect_surf.set_colorkey((0, 0, 0))
        pygame.draw.rect(rect_surf, (0, 255, 255), entity.rect, 1, 1)
        main_screen.blit(rect_surf, entity.pos)
    
### RENDERING    
def render():
    main_screen.fill((45, 45, 45))
    for food in foods:
        renderEntity(food)
    for dood in doods:
        renderEntity(dood)

### UPDATING
def update(timer):
    for food in foods:
        if food.alive: food.update(timer)
        else: foods.remove(food)
    for dood in doods:
        if dood.alive: dood.update(timer)
        else: doods.remove(dood)

### STARTUP POPULATION
def populate(num_foods:int=20):
    for i in range(num_foods):
        new_food = TestFood(
            grow_rate=1.0,
            max_energy=50,
        )
        foods.add(new_food)

### MAIN LOOP
if __name__ == "__main__":
    populate(num_foods=20)
    while main_running:
        perf_timer = time.perf_counter()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    main_running = False
                if event.key == K_1:
                    DEBUG_DRAW_RECTS = not DEBUG_DRAW_RECTS
                if event.key == K_2:
                    DEBUG_DRAW_COLLISION_MASKS = not DEBUG_DRAW_COLLISION_MASKS
        
        update(perf_timer)
        render()
        
        # Display screen
        pygame.display.flip()
        fps_clock.tick(fps_lock)
        
    # Exit App
    pygame.quit()