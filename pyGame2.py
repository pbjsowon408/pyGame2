import pygame
import os
##############################################################

# Basic initiallize part (Must)
pygame.init()  # initiation

# Setting Screen size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Screen Title Setting
pygame.display.set_caption("Shoot the Ball")  # Game title

# FPS
clock = pygame.time.Clock()
##############################################################

# 1. Initaillize User Game (Background, Image, Coordinates, Speed, Font, etc.)
current_path = os.path.dirname(__file__)  # return current file Location
# return image folder Location
image_path = os.path.join(current_path, "")

# Create background
background = pygame.image.load(os.path.join(image_path, "background.png"))

# Create Stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # To put character beyond the stage

# Create character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# character moving side
character_to_x = 0

# character speed
character_speed = 5

# Create Weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# Available to shoot weapon connectively
weapons = []

# weapon speed
weapon_speed = 10

# Create ball (Create each 4 balls)
ball_images = [
    pygame.image.load(os.path.join(image_path, "ballon1.png")),
    pygame.image.load(os.path.join(image_path, "ballon2.png")),
    pygame.image.load(os.path.join(image_path, "ballon3.png")),
    pygame.image.load(os.path.join(image_path, "ballon4.png"))
]

# initial speed due to the ball size
ball_speed_y = [-18, -15, -12, -9]  # Value of index 0,1,2,3,

# Ball info
balls = []
# add initial ball
balls.append({
    "pos_x": 50,
    "pos_y": 50,
    "img_idx": 0,  # img index of ball
    "to_x": 3,  # moving to x side, if -3 left, if 3 right
    "to_y": -6,  # moving to y side
    "init_spd_y": ball_speed_y[0]  # initial speed y
})

running = True
while running:
    dt = clock.tick(60)
    # 2. Deal with Event (Keyboard, Mouse, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # character to the left
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:  # Shoot weapon
                weapon_x_pos = character_x_pos + \
                    (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

# 3. Define Game Character location
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

# change weapon location
    weapons = [[w[0], w[1] - weapon_speed]
               for w in weapons]  # Locate weapon up
# 4. Deal with Collision
# disable Weapon over the ceil
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

# Define ball location
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
# change the way of ball when touch the stage
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

# height
# dealing with bump up the stage
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:  # decrease the speed of the other cases
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
        # 5. Draw on a Screen
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

##############################################################
    pygame.display.update()

pygame.quit()
