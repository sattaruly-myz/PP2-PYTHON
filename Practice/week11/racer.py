import pygame
import random

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

# Цвета
WHITE  = (255, 255, 255)
RED    = (200,   0,   0)   # цвет игрока
BLUE   = (30,  100, 200)   # цвет врага
BLACK  = (  0,   0,   0)
GRAY   = (150, 150, 150)   # дорожная разметка

# Цвета монет по весу
COIN_COLORS = {
    1: (200, 200, 200),   # серебро  — 1 очко
    3: (255, 215,   0),   # золото   — 3 очка
    5: (138,  43, 226),   # фиолет.  — 5 очков (редкий)
}

# FPS и таймер
clock = pygame.time.Clock()
FPS = 60

# Игрок
player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 80, 40, 60)
player_speed = 6

# Враг
enemy = pygame.Rect(random.randint(0, WIDTH - 40), -80, 40, 60)
enemy_base_speed   = 4    # начальная скорость врага
enemy_speed        = enemy_base_speed
ENEMY_SPEED_UP_AT  = 5    # каждые N монет враг ускоряется
ENEMY_SPEED_STEP   = 1    # на сколько единиц растёт скорость

# Монеты
# Каждая монета хранится как словарь: {rect, weight}
# weight - ценность монеты
coins = []
coin_spawn_delay = 40   # кадров между появлениями монет
coin_timer = 0

# Таблица весов: (вес, вероятность)
COIN_WEIGHTS      = [1,   3,   5]
COIN_PROBABILITIES = [70, 25,   5]   # в процентах; сумма = 100

def spawn_coin():
    """Создаёт новую монету со случайным весом и позицией."""
    weight = random.choices(COIN_WEIGHTS, weights=COIN_PROBABILITIES, k=1)[0]
    # Размер монеты зависит от её ценности: чем ценнее — тем больше
    size = 14 + weight * 2          # 1→16 px, 3→20 px, 5→24 px
    x    = random.randint(0, WIDTH - size)
    rect = pygame.Rect(x, -size, size, size)
    return {"rect": rect, "weight": weight, "size": size}

def coin_speed_for(weight):
    """Скорость падения монеты: лёгкие падают быстрее, тяжёлые — медленнее."""
    return max(3, 7 - weight)       # 1→6, 3→4, 5→2

# Счёт
score = 0
font       = pygame.font.SysFont(None, 30)
font_big   = pygame.font.SysFont(None, 48)

# Дорожная разметка
road_marks = [pygame.Rect(WIDTH // 2 - 5, y, 10, 40)
              for y in range(0, HEIGHT, 80)]
road_speed = 5   # скорость прокрутки разметки

# Переменная состояния игры
game_over = False

# Главный игровой цикл
running = True
while running:

    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Перезапуск после гибели
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                # Сбрасываем всё в начальное состояние
                score        = 0
                enemy_speed  = enemy_base_speed
                player.x     = WIDTH // 2 - 20
                player.y     = HEIGHT - 80
                enemy.x      = random.randint(0, WIDTH - 40)
                enemy.y      = -80
                coins.clear()
                coin_timer   = 0
                game_over    = False

    if game_over:
        # Экран окончания игры
        over_text  = font_big.render("GAME OVER", True, RED)
        score_text = font.render(f"Score: {score}   (R — restart)", True, BLACK)
        screen.blit(over_text,  (WIDTH // 2 - over_text.get_width()  // 2, HEIGHT // 2 - 40))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.update()
        clock.tick(FPS)
        continue   # пропускаем остальную логику

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # Ограничение движения по границам экрана
    player.x = max(0, min(player.x, WIDTH - player.width))

    # Прокрутка дорожной разметки
    for mark in road_marks:
        mark.y += road_speed
        if mark.y > HEIGHT:
            mark.y = -40   # зацикливаем вверх

    # Движение и логика врага
    enemy.y += enemy_speed

    # Если враг вышел за нижний край — появляется сверху в новой позиции
    if enemy.y > HEIGHT:
        enemy.x = random.randint(0, WIDTH - enemy.width)
        enemy.y = -80

    # Столкновение игрока с врагом
    if player.colliderect(enemy):
        game_over = True

    # Спавн монет
    coin_timer += 1
    if coin_timer >= coin_spawn_delay:
        coin_timer = 0
        coins.append(spawn_coin())

    #  Обновление монет
    for coin in coins[:]:   # итерируемся по копии списка
        speed = coin_speed_for(coin["weight"])
        coin["rect"].y += speed

        # Игрок подбирает монету
        if player.colliderect(coin["rect"]):
            coins.remove(coin)
            score += coin["weight"]   # прибавляем вес монеты к счёту

            # Ускорение врага каждые ENEMY_SPEED_UP_AT монет
            # (считаем «пороги»: 5, 10, 15, … очков)
            new_level = score // ENEMY_SPEED_UP_AT
            old_level = (score - coin["weight"]) // ENEMY_SPEED_UP_AT
            if new_level > old_level:
                enemy_speed = enemy_base_speed + new_level * ENEMY_SPEED_STEP

        # Монета ушла за нижний край — удаляем
        elif coin["rect"].y > HEIGHT:
            coins.remove(coin)

    #  Отрисовка

    # Дорожная разметка
    for mark in road_marks:
        pygame.draw.rect(screen, GRAY, mark)

    # Игрок (красный прямоугольник)
    pygame.draw.rect(screen, RED, player)

    # Враг (синий прямоугольник)
    pygame.draw.rect(screen, BLUE, enemy)

    # Монеты: цвет и размер зависят от веса
    for coin in coins:
        color = COIN_COLORS[coin["weight"]]
        pygame.draw.ellipse(screen, color, coin["rect"])   # монета — кружок

        # Подпись веса монеты внутри кружка
        lbl = pygame.font.SysFont(None, coin["size"] + 4).render(
            str(coin["weight"]), True, BLACK)
        screen.blit(lbl, (coin["rect"].centerx - lbl.get_width()  // 2,
                          coin["rect"].centery - lbl.get_height() // 2))

    # Счёт (правый верхний угол)
    score_text = font.render(f"Coins: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 120, 10))

    # Текущая скорость врага (левый верхний угол)
    spd_text = font.render(f"Enemy spd: {enemy_speed}", True, BLUE)
    screen.blit(spd_text, (10, 10))

    #  Обновление экрана
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()