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
jump_strength = -20
is_jumping = False
speed = 5

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
    global velocity_y, is_jumping
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_pos.x -= speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_pos.x += speed
    if keys[pygame.K_SPACE] and not is_jumping:
        velocity_y = jump_strength
        is_jumping = True

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