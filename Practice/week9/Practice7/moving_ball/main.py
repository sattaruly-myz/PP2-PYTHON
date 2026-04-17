import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BALL_RADIUS = 25
MOVE_STEP = 20
FPS = 60

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Ball Game")

# Начальная позиция шарика (центр экрана)
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2

# Часы для контроля FPS
clock = pygame.time.Clock()

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Обработка нажатий клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Двигаем вверх, если не выходит за границу
                if ball_y - MOVE_STEP >= BALL_RADIUS:
                    ball_y -= MOVE_STEP
            
            elif event.key == pygame.K_DOWN:
                # Двигаем вниз, если не выходит за границу
                if ball_y + MOVE_STEP <= SCREEN_HEIGHT - BALL_RADIUS:
                    ball_y += MOVE_STEP
            
            elif event.key == pygame.K_LEFT:
                # Двигаем влево, если не выходит за границу
                if ball_x - MOVE_STEP >= BALL_RADIUS:
                    ball_x -= MOVE_STEP
            
            elif event.key == pygame.K_RIGHT:
                # Двигаем вправо, если не выходит за границу
                if ball_x + MOVE_STEP <= SCREEN_WIDTH - BALL_RADIUS:
                    ball_x += MOVE_STEP
    
    # Очистка экрана (белый фон)
    screen.fill(WHITE)
    
    # Рисование красного шарика
    pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)
    
    # Обновление экрана
    pygame.display.flip()
    
    # Контроль FPS
    clock.tick(FPS)

# Выход из игры
pygame.quit()
sys.exit()