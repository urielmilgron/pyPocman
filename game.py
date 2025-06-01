import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Carga imagen
peron_image = pygame.image.load('assets\\pacman.png')
player_img = pygame.transform.scale(peron_image, (100, 100))

# Jugador
player_pos = pygame.Rect(100, 100, 100, 100)
velocity_y = 0
gravity = 1
jump_strength = -20
is_jumping = False

# Piso
FLOOR_Y = 500

def handle_input(keys):
    global velocity_y, is_jumping
    if keys[pygame.K_LEFT]:
        player_pos.x -= 5
    if keys[pygame.K_RIGHT]:
        player_pos.x += 5
    # Saltar con espacio, solo si está en el piso
    if keys[pygame.K_SPACE] and not is_jumping:
        velocity_y = jump_strength
        is_jumping = True

def apply_gravity():
    global velocity_y, is_jumping
    velocity_y += gravity
    player_pos.y += velocity_y

    # Si toca el piso, frena
    if player_pos.y + player_pos.height >= FLOOR_Y:
        player_pos.y = FLOOR_Y - player_pos.height
        velocity_y = 0
        is_jumping = False

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        handle_input(keys)
        apply_gravity()

        screen.fill((30, 30, 30))
        pygame.draw.line(screen, (0, 255, 0), (0, FLOOR_Y), (WIDTH, FLOOR_Y), 4)
        screen.blit(player_img, player_pos)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()