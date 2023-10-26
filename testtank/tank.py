###
#   testtank/tank.py
#

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time
import pygame
from pygame.locals import *

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

def renderEntiry(entity) -> None:
    main_screen.blit(entity.getImage(), entity.getPos())
    if DEBUG_DRAW_COLLISION_MASKS:
        main_screen.blit(entity.drawMask(), entity.getPos())
    if DEBUG_DRAW_RECTS:
        w, h = entity.getImage().get_width(), entity.getImage().get_height()
        rect_surf = pygame.surface.Surface(size=(w, h))
        rect_surf.set_colorkey((0, 0, 0))
        pygame.draw.rect(rect_surf, (0, 255, 255), (0, 0, w, h))
        main_screen.blit(rect_surf, entity.getPos())
    
### RENDERING    
def render():
    main_screen.fill((45, 45, 45))
    for food in foods:
        renderEntiry(food)
    for dood in doods:
        renderEntiry(dood)

### UPDATING
def update(timer):
    for food in foods:
        if food.alive: food.update(timer)
        else: foods.remove(food)
    for dood in doods:
        if dood.alive: dood.update(timer)
        else: doods.remove(dood)

### STARTUP POPULATION
def populate():
    pass

if __name__ == "__main__":
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