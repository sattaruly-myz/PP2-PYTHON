import pygame
from pygame.locals import *
import sys

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint Application")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)

CANVAS_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 100)

TOOL_BRUSH = 'brush'
TOOL_RECTANGLE = 'rectangle'
TOOL_CIRCLE = 'circle'
TOOL_ERASER = 'eraser'

current_tool = TOOL_BRUSH
current_color = BLACK
brush_size = 5

drawing_shape = False
shape_start_pos = None

color_palette = [
    (BLACK, pygame.Rect(10, SCREEN_HEIGHT - 90, 60, 60)),
    (RED, pygame.Rect(80, SCREEN_HEIGHT - 90, 60, 60)),
    (GREEN, pygame.Rect(150, SCREEN_HEIGHT - 90, 60, 60)),
    (BLUE, pygame.Rect(220, SCREEN_HEIGHT - 90, 60, 60)),
    (YELLOW, pygame.Rect(290, SCREEN_HEIGHT - 90, 60, 60)),
    (ORANGE, pygame.Rect(360, SCREEN_HEIGHT - 90, 60, 60)),
    (PURPLE, pygame.Rect(430, SCREEN_HEIGHT - 90, 60, 60)),
    (PINK, pygame.Rect(500, SCREEN_HEIGHT - 90, 60, 60)),
]

tool_buttons = {
    TOOL_BRUSH: pygame.Rect(600, SCREEN_HEIGHT - 90, 80, 60),
    TOOL_RECTANGLE: pygame.Rect(690, SCREEN_HEIGHT - 90, 80, 60),
    TOOL_CIRCLE: pygame.Rect(780, SCREEN_HEIGHT - 90, 80, 60),
    TOOL_ERASER: pygame.Rect(870, SCREEN_HEIGHT - 90, 80, 60),
}

clear_button = pygame.Rect(SCREEN_WIDTH - 110, SCREEN_HEIGHT - 90, 100, 60)

canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - 100))
canvas.fill(WHITE)

font = pygame.font.Font(None, 24)

last_pos = None


def draw_interface():
    """Draw the bottom panel with color palette and tools"""
    pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
    
    for color, rect in color_palette:
        pygame.draw.rect(screen, color, rect)
        if color == current_color:
            pygame.draw.rect(screen, WHITE, rect, 3)
    
    for tool, rect in tool_buttons.items():
        btn_color = WHITE if tool == current_tool else (200, 200, 200)
        pygame.draw.rect(screen, btn_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        
        # Button labels
        if tool == TOOL_BRUSH:
            label = font.render("Brush", True, BLACK)
        elif tool == TOOL_RECTANGLE:
            label = font.render("Rect", True, BLACK)
        elif tool == TOOL_CIRCLE:
            label = font.render("Circle", True, BLACK)
        elif tool == TOOL_ERASER:
            label = font.render("Eraser", True, BLACK)
        
        screen.blit(label, (rect.x + 10, rect.y + 20))
    
    pygame.draw.rect(screen, (255, 100, 100), clear_button)
    pygame.draw.rect(screen, BLACK, clear_button, 2)
    clear_label = font.render("Clear", True, BLACK)
    screen.blit(clear_label, (clear_button.x + 20, clear_button.y + 20))


def draw_line(surface, color, start, end, width):
    """Draw a line between two points"""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    
    if distance > 0:
        for i in range(int(distance)):
            x = int(start[0] + float(i) / distance * dx)
            y = int(start[1] + float(i) / distance * dy)
            pygame.draw.circle(surface, color, (x, y), width)


def handle_color_selection(pos):
    """Check if a color was clicked and update current color"""
    global current_color
    for color, rect in color_palette:
        if rect.collidepoint(pos):
            current_color = color
            return True
    return False


def handle_tool_selection(pos):
    """Check if a tool button was clicked and update current tool"""
    global current_tool
    for tool, rect in tool_buttons.items():
        if rect.collidepoint(pos):
            current_tool = tool
            return True
    return False


def handle_clear_button(pos):
    """Check if clear button was clicked and clear canvas"""
    global canvas
    if clear_button.collidepoint(pos):
        canvas.fill(WHITE)
        return True
    return False


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            if pos[1] > SCREEN_HEIGHT - 100:
                handle_color_selection(pos)
                handle_tool_selection(pos)
                handle_clear_button(pos)
            else:
                if current_tool == TOOL_BRUSH:
                    last_pos = pos
                elif current_tool == TOOL_ERASER:
                    last_pos = pos
                elif current_tool in [TOOL_RECTANGLE, TOOL_CIRCLE]:
                    drawing_shape = True
                    shape_start_pos = pos
        
        elif event.type == MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            if drawing_shape and shape_start_pos:
                if current_tool == TOOL_RECTANGLE:
                    x1, y1 = shape_start_pos
                    x2, y2 = pos
                    rect_x = min(x1, x2)
                    rect_y = min(y1, y2)
                    rect_width = abs(x2 - x1)
                    rect_height = abs(y2 - y1)
                    
                    pygame.draw.rect(canvas, current_color, 
                                   (rect_x, rect_y, rect_width, rect_height), 
                                   0)
                
                elif current_tool == TOOL_CIRCLE:
                    x1, y1 = shape_start_pos
                    x2, y2 = pos
                    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                    
                    if radius > 0:
                        pygame.draw.circle(canvas, current_color, 
                                         (x1, y1), radius, brush_size)
                
                drawing_shape = False
                shape_start_pos = None
            
            last_pos = None
        
        elif event.type == MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            
            if pygame.mouse.get_pressed()[0] and pos[1] < SCREEN_HEIGHT - 100:
                if current_tool == TOOL_BRUSH and last_pos:
                    draw_line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos
                
                elif current_tool == TOOL_ERASER and last_pos:
                    draw_line(canvas, WHITE, last_pos, pos, brush_size * 2)
                    last_pos = pos
    
    screen.fill(WHITE)
    
    screen.blit(canvas, (0, 0))
    
    if drawing_shape and shape_start_pos:
        current_pos = pygame.mouse.get_pos()
        
        if current_tool == TOOL_RECTANGLE:
            x1, y1 = shape_start_pos
            x2, y2 = current_pos
            rect_x = min(x1, x2)
            rect_y = min(y1, y2)
            rect_width = abs(x2 - x1)
            rect_height = abs(y2 - y1)
            pygame.draw.rect(screen, current_color, 
                           (rect_x, rect_y, rect_width, rect_height), 
                           0)
        
        elif current_tool == TOOL_CIRCLE:
            x1, y1 = shape_start_pos
            x2, y2 = current_pos
            radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
            if radius > 0:
                pygame.draw.circle(screen, current_color, 
                                 (x1, y1), radius, brush_size)
    
    draw_interface()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()