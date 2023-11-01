'''
    testtank/main.py
'''
import time
import random
import os
# Needs to be before pygame import to hide welcome msg
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" 
import pygame
from pygame.locals import *
from entity import Entity
from food import Food
from dood import Dood
from tank import Tank

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
    rect_surf = pygame.Surface(main_screen.get_size())
    rect_surf.set_colorkey((0,0,0))

    if DEBUG_DRAW_COLLISION_MASKS:
        main_screen.blit(entity.drawMask(), entity.center)

    if DEBUG_DRAW_RECTS:
        rect = entity.rect
        rect = (rect.x + rect.w / 2, rect.y + rect.h / 2, rect.w, rect.h)
        pygame.draw.rect(rect_surf, (0, 255, 255), rect, 1)

    if DEBUG_DRAW_ORIGIN_POINT:
        pygame.draw.circle(rect_surf, (0, 255, 0), entity.pos, 1, 1)

    if DEBUG_DRAW_DOOD_DETECTION_CIRCLE and isinstance(entity, Dood):
        r = entity.area_detection.radius
        pygame.draw.circle(rect_surf, (255, 50, 0), entity.pos, r, 1)

    main_screen.blit(rect_surf, (0, 0))
    
def render():
    main_screen.fill((45, 45, 45))
    for food in foods:
        renderEntity(food)
    for dood in doods:
        renderEntity(dood)

### UPDATING
def update(timer:float, tank:Tank):
    tank.update(timer)
    if tank.spawnFood() and len(foods) < tank.foodLimit:
        spawnFood()

    # Sprite group can call update method to all sprite inside it
    # Easier to keep track of them since if we remove them from sprite groupa,
    # it mean we vaporize them from existence
    foods.update(timer)
    doods.update(timer)

    for dood in doods: borderCheck(tank, dood)

def borderCheck(tank:Tank, dood:Dood):
    '''check dood border'''
    x, y = dood.pos

    # Set the border limits
    border_left = 0 - dood.width
    border_right = tank.width + dood.width
    border_top = 0 - dood.height
    border_bottom = tank.height + dood.height

    # if borderWalled = True, dont let doods pass
    if tank.borderWalled:
        # Check left border
        if x < border_left:
            dood.pos = (border_left, y)
        # Check right border
        if x > border_right:
            dood.pos = (border_right, y)
        # Check top border
        if y < border_top:
            dood.pos = (x, border_top)
        # Check bottom border
        if y > border_bottom:
            dood.pos = border_bottom
    # if borderWalled = False, donut world the doods
    if not tank.borderWalled:
        # Check left border
        if x < border_left:
            dood.pos = (border_right - 1, y)
        # Check right border
        if x > border_right:
            dood.pos = (border_left + 1, y)
        # Check top border
        if y < border_top:
            dood.pos = (x, border_bottom - 1)
        if y > border_bottom:
            dood.pos = (x, border_bottom + 1)

# check if an entity enter Dood area
# this suppose to check if there is food enter dood area
# but I somehow hate this
# but I kinda like it at the same time
def doodsDetection(dood: Dood, other: Entity):
    enter = dood.area_detection.enterArea(other)
    leave = dood.area_detection.leaveArea(other)
    if enter:
        pass
        # dood.sayHello(other)
    if leave:
        pass
        # dood.sayBye(other)
    return enter

### COLLISION HANDLING
def collisionHandler() -> None:
    # this is to check if there is any food around doods
    nearest_foods = pygame.sprite.groupcollide(doods, foods, False, False, doodsDetection)
    # this is to check if there is any other doods around
    nearest_doods = pygame.sprite.groupcollide(doods, doods, False, False, doodsDetection)
    # I suck at naming variables. 
    # also, I change the argument position so that it return Dood:list[Food] instead of Food:list[Dood]
    foods_collide = pygame.sprite.groupcollide(doods, foods, False, True, pygame.sprite.collide_mask) 

    for dood in foods_collide:
        print(f"{dood} ate {foods_collide[dood]}")
        # since it return a list of foods, i think getting the total amount of energy should do the job
        # this might happen if dood spawn on multiple food resulting it ate them simultaneously
        total_energy = sum(food.energy for food in foods_collide[dood]) 
        # I use eatFood method here instead collision because it much easier
        # and I dont have to check if the entity is a Food since it comfirm to be
        # Food unless we put something else in food sprite group.
        dood.eatFood(total_energy) 

### GAME FUNCTIONS
def spawnFood():
    new_food = Food(
        grow_rate=0.1,
        max_energy=50,
    )
    new_food.pos = (random.randint(0, main_width - new_food.size[0]),
                    random.randint(0, main_height - new_food.size[1]))
    foods.add(new_food)

def spawnDood():
    new_dood = Dood(speed_mult=7.5, neurons=5)
    new_dood.pos = (random.randint(0, main_width - new_dood.scale[0]),
                        random.randint(0, main_height - new_dood.scale[1]))
    new_dood.angle = random.randint(0, 359)
    doods.add(new_dood)

### STARTUP
def populate(num_foods:int=0, num_doods:int=0):
    for i in range(num_foods):
        spawnFood()
    for i in range(num_doods):
        spawnDood()

### MAIN LOOP
if __name__ == "__main__":
    ### Tank Specifications
    test_tank = Tank(
        size=(main_width, main_height),
        border_wall=False,
        food_spawn_rate=3.5,
        food_limit=50,
        dood_limit=50)

    populate(num_foods=20, num_doods=20)
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

        update(perf_timer, test_tank)
        render()
        collisionHandler()

        # Display screen
        pygame.display.flip()
        fps_clock.tick(fps_lock)
        #print(f"{time.perf_counter() - perf_timer}")
        
    # Exit App
    pygame.quit()
