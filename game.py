import pygame
import sys
import random

pygame.init()

# Pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego con bloques flotantes")
clock = pygame.time.Clock()

# Cargar imágenes
peron_image = pygame.image.load('assets/pacman.png').convert_alpha()
player_img = pygame.transform.scale(peron_image, (100, 100))

bg_img = pygame.image.load('assets/background.png').convert()
bg_img = pygame.transform.scale(bg_img, (800, 600))

block_img = pygame.image.load('assets/dice.png').convert_alpha()
block_img = pygame.transform.scale(block_img, (80, 80))

# Jugador
player_pos = pygame.Rect(100, 100, 100, 100)
velocity_y = 0
gravity = 1
jump_strength = -18
is_jumping = False
speed = 5
previous_key = None
jump_strength_count = 0
# Piso virtual
FLOOR_Y = 520

# Cámara
camera_x = 0

# Bloques flotantes
blocks = []
for i in range(20):  # generar 20 bloques
    x = random.randint(500, 5000)
    y = random.choice([300, 350, 400])
    blocks.append(pygame.Rect(x, y, 80, 80))

def handle_input(keys):
    global velocity_y, is_jumping,jump_strength_count, previous_key
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        previous_key = pygame.K_LEFT
        player_pos.x -= speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        previous_key = pygame.K_RIGHT
        player_pos.x += speed
    if keys[pygame.K_SPACE] and not is_jumping:
        if previous_key == pygame.K_SPACE or jump_strength_count == 0:
            # User keeps holding the key - spacebar then accumulates jump strength
            previous_key = pygame.K_SPACE
            jump_strength_count += 1
            print(jump_strength_count)

    elif jump_strength_count != 0 :
        print("Aca deberia saltar")
        if jump_strength_count <= 5:
            jump_strength_count = 0
            print("Entro en menor que 5")
        elif jump_strength_count > 5 and jump_strength_count <= 10:
            jump_strength_count = 20
            print("Entro en mayor que 5 y menor a 10")
        else:
            jump_strength_count = 30
            print("Entro en mayor que 20")
        # User release the holding key - spacebar
        velocity_y = jump_strength - (jump_strength_count*0.2)
        is_jumping = True   
        previous_key = None
        jump_strength_count = 0

def apply_gravity():
    global velocity_y, is_jumping
    velocity_y += gravity
    player_pos.y += velocity_y

    # Colisión con bloques
    for block in blocks:
        if player_pos.colliderect(block):
            if velocity_y > 0 and player_pos.bottom <= block.top + 20:
                player_pos.bottom = block.top
                velocity_y = 0
                is_jumping = False

    # Colisión con piso
    if player_pos.y + player_pos.height >= FLOOR_Y:
        player_pos.y = FLOOR_Y - player_pos.height
        velocity_y = 0
        is_jumping = False

def main():
    global camera_x
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        handle_input(keys)
        apply_gravity()

        camera_x = player_pos.centerx - WIDTH // 2

        # Fondo loopeado
        for i in range(-1, 1000):
            screen.blit(bg_img, ((i * bg_img.get_width()) - camera_x, 0))

        # Dibujar bloques
        for block in blocks:
            screen.blit(block_img, (block.x - camera_x, block.y))

        # Dibujar jugador
        screen.blit(player_img, (player_pos.x - camera_x, player_pos.y))

        pygame.display.flip()
        clock.tick(60)
        screen.fill((0, 0, 0))

if __name__ == "__main__":
    main()