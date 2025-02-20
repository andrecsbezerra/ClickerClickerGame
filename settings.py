import pygame

class Settings:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.bg_color = (50, 50, 50)  # Cor de fundo da tela de configurações
        self.font = pygame.font.Font(None, 50)

    def draw(self, screen):
        # Desenha a tela de configurações
        screen.fill(self.bg_color)
        title = self.font.render("Settings", True, (255, 255, 255))
        screen.blit(title, (320, 15))  # Título da tela de configurações
        pygame.display.update()
