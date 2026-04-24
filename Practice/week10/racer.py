import pygame
import random
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")
# Цвета
WHITE = (255, 255, 255)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)
# FPS
clock = pygame.time.Clock()
FPS = 60
# Создаём машину игрока
player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 80, 40, 60)
player_speed = 6
#COINS
coins = []                # список монет
coin_size = 20
coin_speed = 5
coin_spawn_delay = 40     # через сколько кадров появляется монета
coin_timer = 0
#SCORE
score = 0
font = pygame.font.SysFont(None, 30)
#GAME LOOP
running = True
while running:
    # Очистка экрана
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #PLAYER CONTROL
    keys = pygame.key.get_pressed()
    # Движение влево
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    # Движение вправо
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    # Ограничение движения по экрану
    if player.x < 0:
        player.x = 0
    if player.x > WIDTH - player.width:
        player.x = WIDTH - player.width
    # SPAWN COINS
    coin_timer += 1
    # Каждые N кадров создаём новую монету
    if coin_timer >= coin_spawn_delay:
        coin_timer = 0
        x = random.randint(0, WIDTH - coin_size)
        new_coin = pygame.Rect(x, 0, coin_size, coin_size)
        coins.append(new_coin)
    # UPDATE COINS
    for coin in coins[:]:  # копия списка
        # Движение вниз
        coin.y += coin_speed
        # Проверка столкновения с игроком
        if player.colliderect(coin):
            coins.remove(coin)
            score += 1  # увеличиваем счёт
        # Если монета ушла за экран — удаляем
        elif coin.y > HEIGHT:
            coins.remove(coin)
    #DRAW
    # Игрок
    pygame.draw.rect(screen, RED, player)
    # Монеты
    for coin in coins:
        pygame.draw.rect(screen, YELLOW, coin)
    #SCORE DISPLAY (правый верх)
    score_text = font.render(f"Coins: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 120, 10))
    # Обновление экрана
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()