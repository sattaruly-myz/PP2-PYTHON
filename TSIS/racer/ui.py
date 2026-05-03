import pygame

WHITE = (255, 255, 255)
GRAY  = (130, 130, 130)
BLUE  = (60, 120, 200)
HOVER = (90, 155, 235)


def draw_text(surface, text, pos, font, color=WHITE, center=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=pos) if center else surf.get_rect(topleft=pos)
    surface.blit(surf, rect)


class Button:
    def __init__(self, rect, text, font, color=BLUE, hover=HOVER, text_color=WHITE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.hover = hover
        self.text_color = text_color

    def draw(self, surface):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surface, self.hover if hovered else self.color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        s = self.font.render(self.text, True, self.text_color)
        surface.blit(s, s.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class TextInput:
    def __init__(self, rect, font, placeholder='', max_len=20):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.placeholder = placeholder
        self.max_len = max_len
        self.text = ''

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return False
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return True
            if event.unicode and event.unicode.isprintable() and len(self.text) < self.max_len:
                self.text += event.unicode
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, (25, 25, 35), self.rect, border_radius=6)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=6)
        display = self.text + '|' if self.text else self.placeholder
        color = WHITE if self.text else GRAY
        s = self.font.render(display, True, color)
        surface.blit(s, (self.rect.x + 10, self.rect.y + (self.rect.h - s.get_height()) // 2))