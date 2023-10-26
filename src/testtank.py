###
#   src/main.py
#       - twitch.tv/CodeNameTribbs

### IMPORTS
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time
import random
import pygame
from pygame.locals import *
from dood import Dood
from food import Food

### PYGAME SETUP
pygame.init()
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF)
clock = pygame.time.Clock()
lock_fps = 30
running  = True
startup_cooldown = 1.0

### DEBUG FLAGS
DEBUG_DRAWRECTS = False
DEBUG_DRAWCOLLISON_MASKS = False
DEBUG_DRAW_OBJECTS = True

debug_objects = []
def addDebugObj(pos:tuple[float, float]=(0, 0), color:tuple[int, int, int]=(0, 0, 0)):
    col_pos = {
        "color": (75, 75, 255),
        "radius": 4,
        "width": 0,
        "pos": pos
    }
    debug_objects.append(col_pos)

### ENTITY LISTS
doods = pygame.sprite.Group()
foods = pygame.sprite.Group()
garbage_insts = []

def renderEntity(inst):
    entity = inst.render()
    screen.blit(entity[0], entity[1])
    if DEBUG_DRAWRECTS:
        pygame.draw.rect(screen, (255, 255, 0), inst.getRect(), 1)
    if DEBUG_DRAWCOLLISON_MASKS:
        screen.blit(inst.drawMask(), entity[1])

### RENDER
def renderFrame():
    # Clear the frame
    screen.fill((60, 60, 60))

    # Render Foods
    for food in foods:
        renderEntity(food)
        
    #Render Doods
    for dood in doods:
        renderEntity(dood)

    if DEBUG_DRAW_OBJECTS:
        for obj in debug_objects:
            pygame.draw.circle(screen, obj['color'], obj['pos'], obj['radius'], obj['width'])
        

## COLLISIONS
def maskCollision(entityA:pygame.sprite.Sprite, entityB:pygame.sprite.Sprite):
    offset_x = entityA.rect.x - entityB.rect.x
    offset_y = entityA.rect.y - entityB.rect.y
    collision = entityA.getMask().overlap(entityB.getMask(), (offset_x, offset_y))
    
    off_x = entityA.getPos()[0] - entityB.getPos()[0]
    off_y = entityA.getPos()[1] - entityB.getPos()[1]
    
    pygame.draw.rect(screen, (0, 250, 0), entityA.rect, 1, 1)
    pygame.draw.rect(screen, (0, 250, 250), entityB.rect, 1, 1)
    new_surf = pygame.surface.Surface((50, 50))
    new_surf.set_colorkey((0,0,0))
    pygame.draw.rect(new_surf, (255, 255, 255), Rect(0, 0, 50, 50), 2, 1)
    screen.blit(new_surf, (off_x, off_y))
    
    if collision:
        print(f"{entityA} collided with {entityB}")
    return collision if collision else None

def collisionHandler():
    for dood in doods:
        close_food = pygame.sprite.spritecollideany(dood, foods)
        if close_food:
            if maskCollision(dood, close_food):
                foods.remove(close_food)
                
                
### UPDATES
def update(deltatime):
    # Update Food
    for food in foods:
        if food.alive:
            food.update(deltatime)
            food.rect = food.getRect()
        else:
            foods.remove(food)
    # Update Doods
    for dood in doods:
        if dood.alive:
            dood.update(deltatime)
            dood.rect = dood.getRect()
            
        else:
            doods.remove(dood)
            
### STARTUP
def populate(num_foods:int, num_doods:int, speed_mult:float=1.0) -> None:
    #create foods
    for i in range(num_foods):
        new_food = Food(
            pos=(screen_width/2, i * 10),
            speed_mult=speed_mult,
            scale=(16, 16))
        foods.add(new_food)
        new_food.rect= new_food.getRect()
        addDebugObj(new_food.getPos(), (200, 200, 50))
    #create doods
    for i in range(num_doods):
       new_dood = Dood(
           pos=(0, screen_height/2),
           speed_mult=speed_mult,
           scale=(40, 40))
       new_dood.rect = new_dood.getRect()
       doods.add(new_dood)

# MAIN LOOP
populate(50, 1, 10.0)
while running:
    perf = time.perf_counter()
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
            if event.key == K_3:
                DEBUG_DRAW_OBJECTS = not DEBUG_DRAW_OBJECTS

    # Call renders
    renderFrame()
    # Call updates
    update(time.perf_counter())
    # Handle Collisions
    collisionHandler()

    # display to screen
    pygame.display.flip()
    clock.tick(lock_fps)

### Exit App
pygame.quit()
