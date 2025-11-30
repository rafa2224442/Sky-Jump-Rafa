import pygame
import random

pygame.init()
#mixer.init()

#mixer.music.load('musicccc.ogg')
#mixer.music.play()
#mixer.music.play()

# Ukuran layar
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sky Jump")



# Warna
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
GREEN = (0, 200, 0)
RED = (255, 100, 100)

# Player
player_size = 40
player_img = pygame.image.load("gambaruntuksprite.png")
player_img = pygame.transform.scale(player_img, (player_size, player_size))
player_velocity_y = 0
gravity = 0.5
jump_power = -10
speed_x = 5

player = pygame.Rect(WIDTH//2 - player_size//2, HEIGHT - 150, player_size, player_size)

#background
background = pygame.image.load("langit.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Platform
platforms = []
platform_width = 80
platform_height = 15
platform_count = 20 # lebih banyak platform
platform_gap = 100   # jarak vertikal antar platform 

# Buat platform awal
for i in range(platform_count):
    x = random.randint(0, WIDTH - platform_width)
    y = i * platform_gap
    platforms.append(pygame.Rect(x, y, platform_width, platform_height)) #memposisikan platform secara acak

# Skor
score = 0
font = pygame.font.SysFont("Arial", 24)

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    screen.blit(background, (0, 0))

    # Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= speed_x
    if keys[pygame.K_d]:
        player.x += speed_x

    # Loop kiri-kanan
    if player.x < -player_size:
        player.x = WIDTH
    if player.x > WIDTH:
        player.x = -player_size #Jika player keluar dari layar sebelah kiri, dia akan muncul kembali dari sebelah kanan Jika player keluar dari layar sebelah kanan, dia akan muncul kembali dari sebelah kiri.

    # Fisika
    player_velocity_y += gravity
    player.y += player_velocity_y #Menambah gravitasi ke pemain agar jatuh ke bawah

    # Collision dengan platform
    for plat in platforms:
        if player.colliderect(plat) and player_velocity_y > 0:
            player_velocity_y = jump_power #ika pemain menyentuh platform saat turun  melompat ke atas

    # Scroll layar
    if player.y < HEIGHT // 3:
        offset = HEIGHT // 3 - player.y
        player.y = HEIGHT // 3
        for plat in platforms:
            plat.y += offset
        score += 1 #Saat player naik ke atas layar, platform dan background bergerak ke bawah  Skor bertambah

    # Platform baru
    while len(platforms) < platform_count:
        x = random.randint(0, WIDTH - platform_width)
        y = platforms[-1].y - platform_gap
        platforms.append(pygame.Rect(x, y, platform_width, platform_height)) #Jika platform lebih sedikit (karena ada yang dihapus dari bawah), maka program akan membuat platform baru

    # Hapus platform yang jatuh di bawah layar
    platforms = [p for p in platforms if p.y < HEIGHT]

    # Game Over
    if player.y > HEIGHT:
        text = font.render("Game Over! Score: " + str(score), True, RED)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Gambar
    screen.blit(player_img, (player.x, player.y))
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
