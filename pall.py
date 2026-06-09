'''Jonatan Soomets'''

import pygame, sys

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Something")

# Värvid
TAEVAS = (173, 216, 230)

# Taustapilt
bg_img = pygame.image.load("ball.jpg").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# Klahvid – muuda siin kui soovid teisi klahve
KEY_LEFT  = pygame.K_LEFT   # vasakule
KEY_RIGHT = pygame.K_RIGHT  # paremale

# Palli andmed
BALL_SIZE = 20
ball_x = WIDTH - BALL_SIZE
ball_y = 0
ball_sx = -4
ball_sy = 4

# Aluse andmed
PAD_W = 120
PAD_H = 20
pad_x = WIDTH // 2 - PAD_W // 2
pad_y = int(HEIGHT / 1.5)
pad_speed = 6

# Taustamuusika
pygame.mixer.music.load("song.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

ball_img = pygame.image.load("ball.jpg").convert_alpha()
ball_img = pygame.transform.scale(ball_img, (BALL_SIZE, BALL_SIZE))

pad_img = pygame.image.load("ball.jpg").convert_alpha()
pad_img = pygame.transform.scale(pad_img, (PAD_W, PAD_H))

font = pygame.font.SysFont("Georgia", 24, bold=True)

skoor = 0
game_over = False

clock = pygame.time.Clock()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    if not game_over:

        # Aluse juhtimine
        keys = pygame.key.get_pressed()
        if keys[KEY_LEFT]:
            pad_x -= pad_speed
        if keys[KEY_RIGHT]:
            pad_x += pad_speed

        # Alus ei lähe ekraanilt välja
        if pad_x < 0:
            pad_x = 0
        if pad_x + PAD_W > WIDTH:
            pad_x = WIDTH - PAD_W

        # Pall liigub
        ball_x += ball_sx
        ball_y += ball_sy

        # Seinad
        if ball_x <= 0:
            ball_x = 0
            ball_sx = -ball_sx

        if ball_x + BALL_SIZE >= WIDTH:
            ball_x = WIDTH - BALL_SIZE
            ball_sx = -ball_sx

        if ball_y <= 0:
            ball_y = 0
            ball_sy = -ball_sy

        # Põrge alusega
        ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
        pad_rect = pygame.Rect(pad_x, pad_y, PAD_W, PAD_H)

        if ball_sy > 0 and ball_rect.colliderect(pad_rect):
            ball_sy = -ball_sy
            ball_y = pad_y - BALL_SIZE

            hit = (ball_x + BALL_SIZE / 2 - pad_x) / PAD_W
            ball_sx = (hit - 0.5) * 9
            
            pygame.mixer.Sound("hit.mp3").play()
            skoor += 1

        # Alumine serv
        if ball_y + BALL_SIZE >= HEIGHT:
            ball_y = HEIGHT - BALL_SIZE
            ball_sy = -ball_sy
            skoor -= 1

        if skoor < 0:
            game_over = True

    # Taust
    screen.blit(bg_img, (0, 0))

    if game_over:

        pygame.mixer.music.stop()
        big_font = pygame.font.SysFont("Georgia", 64, bold=True)
        tekst = big_font.render("GAME OVER", True, (180, 30, 30))
        screen.blit(tekst, (140, 170))

        small_font = pygame.font.SysFont("Georgia", 32)
        skoor_tekst = small_font.render("Skoor: " + str(skoor), True, (0, 60, 120))
        screen.blit(skoor_tekst, (250, 260))

    else:

        screen.blit(pad_img, (pad_x, pad_y))
        screen.blit(ball_img, (ball_x, ball_y))

        skoor_tekst = font.render("Skoor: " + str(skoor), True, (0, 60, 120))
        screen.blit(skoor_tekst, (10, 10))

    pygame.display.flip()