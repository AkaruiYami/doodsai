'''
    testtank/tank.py
'''

import time
import random
import os
import pygame
from pygame.locals import *
from food import Food
from dood import Dood
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

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
DEBUG_DRAW_ORIGIN_POINT = True
DEBUG_DRAW_DOOD_DETECTION_CIRCLE = True
DEBUG_DRAW_ORIGIN_POINT = False

### GROUPS
doods = pygame.sprite.Group()
foods = pygame.sprite.Group()

### RENDERING
def renderEntity(entity) -> None:
    main_screen.blit(entity.image, entity.center)

    if DEBUG_DRAW_COLLISION_MASKS:
        main_screen.blit(entity.drawMask(), entity.center)

    if DEBUG_DRAW_RECTS:
        w, h = entity.image.get_width()+1, entity.image.get_height()+1
        rect_surf = pygame.Surface(size=(w, h))
        rect_surf.set_colorkey((0, 0, 0))
        pygame.draw.rect(rect_surf, (0, 255, 255), entity._rect, 1)
        main_screen.blit(rect_surf, entity.center)

    if DEBUG_DRAW_ORIGIN_POINT:
        rect_surf = pygame.Surface(size=(3, 3))
        rect_surf.set_colorkey((0, 0, 0))

        pygame.draw.circle(rect_surf, (0, 255, 0), (0, 0), 1, 1)
        main_screen.blit(rect_surf, entity.pos)
        
    if DEBUG_DRAW_DOOD_DETECTION_CIRCLE and isinstance(entity, Dood):
        r = entity.area_detection.radius
        rect_surf = pygame.surface.Surface(size=(2*r, 2*r))
        rect_surf.set_colorkey((0, 0, 0))
        center = (entity.pos[0] - r, entity.pos[1] - r)
        pygame.draw.circle(rect_surf, (255, 50, 0), (r, r), r, 1)
        main_screen.blit(rect_surf, center)  

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

# check if an entity enter Dood area
# this suppose to check if there is food enter dood area
# but I somehow hate this
# but I kinda like it at the same time
def doodsDetection(dood: Dood, food):
    enter = dood.area_detection.enterArea(food)
    leave = dood.area_detection.leaveArea(food)
    if enter:
        pass
        #dood.sayHello(food)
    if leave:
        pass
        #dood.sayBye(food)
    return enter

### COLLISION HANDLING
def collisionHandler() -> None:
    nearest_food = pygame.sprite.groupcollide(doods, foods, False, False, doodsDetection) # this is to check if there is any food around doods
    close_food = pygame.sprite.groupcollide(foods, doods, True, False, pygame.sprite.collide_mask)

    if close_food:
        for food, dood in close_food.items():
            dood[0].collision(food)
            print(f"Get eaten boiiii! {food}")
            food.alive = False

### STARTUP POPULATION
def populate(num_foods:int=0, num_doods:int=0):
    for i in range(num_foods):
        new_food = Food(
            grow_rate=0.1,
            max_energy=50,
        )
        new_food.pos = (random.randint(0, main_width - new_food.size[0]),
                        random.randint(0, main_height - new_food.size[1]))
        foods.add(new_food)
        
    for i in range(num_doods):
        new_dood = Dood(speed_mult=7.5)
        new_dood.pos  = (random.randint(0, main_width - new_food.size[0]),
                         random.randint(0, main_height - new_food.size[1]))
        new_dood.angle = random.randint(0, 359)
        doods.add(new_dood)

def testPopulate():
    for i in range(0, main_height, 15):
        new_food = Food(
            grow_rate=1.0,
            max_energy=50
        )
        new_food.pos = (main_width/2 - new_food.size[0], i)
        foods.add(new_food)
    
    testDood = Dood(speed_mult=30.0)
    testDood.pos = (main_width/2, main_height/2 - 3)
    testDood.movingForward = True
    testDood.movingLeft = True
    doods.add(testDood)

### MAIN LOOP
if __name__ == "__main__":
    populate(num_foods=30, num_doods=20)
    #testPopulate()
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
                if event.key == K_3:
                    DEBUG_DRAW_ORIGIN_POINT = not DEBUG_DRAW_ORIGIN_POINT
                if event.key == K_4:
                    DEBUG_DRAW_DOOD_DETECTION_CIRCLE = not DEBUG_DRAW_DOOD_DETECTION_CIRCLE
        
        update(perf_timer)
        render()
        collisionHandler()
        
        # Display screen
        pygame.display.flip()
        fps_clock.tick(fps_lock)
        
    # Exit App
    pygame.quit()
