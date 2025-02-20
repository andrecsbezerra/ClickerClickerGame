import pygame
import sys

class Menu:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Clicker Clicker Game")

        self.font = pygame.font.Font(None, 50)
        self.title = self.font.render("Clicker Clicker Game", True, "#ffffff")

        # Criar botões "Iniciar" e "Sair"
        self.start_button = pygame.Rect(300, 400, 200, 60)
        self.exit_button = pygame.Rect(300, 500, 200, 60)

        self.clock = pygame.time.Clock()

    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, "#444444", rect, border_radius=10)
        text_surface = self.font.render(text, True, "#ffffff")
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def run(self):
        while True:
            self.screen.fill("#000000")
            self.screen.blit(self.title, (220, 100))

            # Desenhar botões
            self.draw_button(self.start_button, "Iniciar")
            self.draw_button(self.exit_button, "Sair")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.start_button.collidepoint(event.pos):
                        return "start"  # Sai do menu e inicia o jogo
                    if self.exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            self.clock.tick(60)
