import pygame
import sys
import time
import os
from menu import Menu

def resource_path(relative_path):
    """Obtem o caminho absoluto para um recurso, funciona tanto no ambiente de desenvolvimento quanto no executável."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.width = 800
        self.height = 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Clicker Clicker Game")

        # Carregar e tocar música de fundo
        self.music_volume = 0.05  # Volume inicial da música
        
        pygame.mixer.music.load(resource_path("assets/music/soundtrack.mp3"))
        pygame.mixer.music.play(-1)  # -1 para tocar em loop
        pygame.mixer.music.set_volume(0.05)  # Ajusta o volume da música

        self.click_sound = pygame.mixer.Sound("assets/music/Click.mp3")
        self.upgrade_sound = pygame.mixer.Sound("assets/music/upgrade.mp3")
        self.click_sound.set_volume(0.2)  # Volume máximo
        self.upgrade_sound.set_volume(0.1)  # Volume máximo
        # Carregar e tocar música de fundo
        

        self.clicks = 0
        self.click_per_click = 1

        # Variáveis do clique automático
        self.auto_clicks = 1
        self.last_auto_click_time = time.time()

        # Carregar imagens
        self.mouse_img = pygame.image.load("./assets/mouse.png")
        self.mouse_img = pygame.transform.scale(self.mouse_img, (200, 200))

        self.settings_img = pygame.image.load("./assets/settings.png")
        self.settings_img = pygame.transform.scale(self.settings_img, (50, 50))
        self.settings_rect = self.settings_img.get_rect(topleft=(10, 10))

        self.back_img = pygame.image.load("./assets/back.png")
        self.back_img = pygame.transform.scale(self.back_img, (40, 40))

        self.upgrades_img = pygame.image.load("./assets/upgrades.png")
        self.upgrades_img = pygame.transform.scale(self.upgrades_img, (50, 50))
        self.upgrades_rect = self.upgrades_img.get_rect(topleft=(self.width - 60, 10))

        self.mouse_rect = self.mouse_img.get_rect(center=(self.width // 2, 500))

        self.font = pygame.font.Font(None, 50)
        self.title = self.font.render("Clicker Clicker Game", True, "#ffffff")
        self.clock = pygame.time.Clock()

        self.in_settings = False
        self.in_upgrades = False

        # Configuração dos upgrades
        self.upgrades = [
            {"name": "Dedo", "base_price": 10, "increment": 1, "level": 0},
            {"name": "Clique Duplo", "base_price": 100, "increment": 2, "level": 0},
            {"name": "Clique Triplo", "base_price": 1000, "increment": 5, "level": 0},
            {"name": "Clique Automático", "base_price": 5000, "increment": 10, "level": 0},
            {"name": "Super Dedo", "base_price": 25000, "increment": 20, "level": 0},
        ]

        # Inicializa o preço de cada upgrade
        for upgrade in self.upgrades:
            upgrade['price'] = upgrade['base_price']

        # Configurar um timer para o clique automático a cada 0.2 segundos
        pygame.time.set_timer(pygame.USEREVENT, 200)

        # Variáveis de controle do botão de voltar
        self.back_cooldown = False  # Variável para rastrear o cooldown do botão de voltar
        self.cooldown_time = 0.8 # Tempo de cooldown em segundos
        self.last_back_click_time = 0  # Tempo do último clique no botão de voltar

    def auto_click(self):
        self.clicks += self.auto_clicks

    def click_button(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.mouse_rect.collidepoint(event.pos):
                self.clicks += self.click_per_click
            elif self.settings_rect.collidepoint(event.pos) and not self.in_upgrades:
                self.in_settings = True  
            elif self.upgrades_rect.collidepoint(event.pos) and not self.in_settings:
                self.in_upgrades = True  
            elif self.in_upgrades:
                self.handle_upgrade_click(event.pos)  
            elif self.in_settings:
                # Aqui você pode adicionar a lógica para lidar com cliques na tela de configurações, se necessário
                pass
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.mouse_rect.collidepoint(event.pos):
                    self.clicks += self.click_per_click
                    self.click_sound.play()  # Som do clique

    def handle_upgrade_click(self, mouse_pos):
        for index, upgrade in enumerate(self.upgrades):
            dedo_box_rect = pygame.Rect(20, 100 + index * 120, 280, 100)
            back_rect = self.back_img.get_rect(topleft=(self.width - 50, 10))

            if dedo_box_rect.collidepoint(mouse_pos):
                if self.clicks >= upgrade['price']:
                    self.upgrade_sound.play()
                    self.clicks -= upgrade['price']
                    self.click_per_click += upgrade['increment']
                    self.auto_clicks += upgrade['increment']

                    # Aumenta o nível do upgrade
                    upgrade['level'] += 1

                    # Verifica se o nível do upgrade é 25
                    if upgrade['level'] % 25 == 0:
                        self.click_per_click *= 5
                        self.auto_clicks *= 5

                    # Atualiza o preço do upgrade
                    upgrade['price'] = int(upgrade['base_price'] * (1.1 ** upgrade['level']))
            elif back_rect.collidepoint(mouse_pos):
                if not self.back_cooldown:  # Verifica se o cooldown não está ativo
                    self.in_upgrades = False  # Fecha a tela de upgrades
                    self.back_cooldown = True  # Ativa o cooldown
                    self.last_back_click_time = time.time()  # Atualiza o tempo do último clique


    def render(self):
        """ Renderiza os elementos na tela. """
        if self.in_settings:
            self.show_settings_page()
        elif self.in_upgrades:
            self.show_upgrades_page()
        else:
            self.screen.fill("#000000")

            self.screen.blit(self.title, (220, 15))

            click_per_click_text = self.font.render(f"Clicks per Click: {self.format_number(self.click_per_click)}", True, "#ffffff")
            self.screen.blit(click_per_click_text, (self.width // 1.8 - 200, 75))
            auto_click_text = self.font.render(f"Auto Clicks: {self.format_number(self.auto_clicks)}/s", True, "#ffffff")
            self.screen.blit(auto_click_text, (self.width // 1.75 - 200, 135))

            self.screen.blit(self.mouse_img, self.mouse_rect)
            self.screen.blit(self.settings_img, self.settings_rect)
            self.screen.blit(self.upgrades_img, self.upgrades_rect)

            click_text = self.font.render(f"Clicks: {self.format_number(self.clicks)}", True, "#ffffff")
            self.screen.blit(click_text, (self.width // 2 - 100, 750))

            pygame.display.update()
            self.clock.tick(60)

        # Atualiza o cooldown
        if self.back_cooldown:
            if time.time() - self.last_back_click_time >= self.cooldown_time:
                self.back_cooldown = False  # Reseta o cooldown

    def show_upgrades_page(self):
        self.screen.fill("#222222")  # Cor de fundo da tela de upgrades
        title = self.font.render("Upgrades", True, "#ffffff")
        self.screen.blit(title, (320, 15))  # Título da tela

        # Desenhar caixas de upgrades
        for index, upgrade in enumerate(self.upgrades):
            box_rect = pygame.Rect(20, 100 + index * 120, 280, 100)  # Posição e tamanho da caixa
            
            # Muda a cor da caixa com base na possibilidade de compra
            if self.clicks >= upgrade['price']:
                box_color = "#00ff00"  # Verde se puder comprar
            else:
                box_color = "#ff0000"  # Vermelho se não puder comprar
            
            pygame.draw.rect(self.screen, box_color, box_rect)  # Fundo da caixa
            pygame.draw.rect(self.screen, "#ffffff", box_rect, 2)  # Borda da caixa

            # Texto do upgrade
            upgrade_text = self.font.render(f"{upgrade['name']} (lvl {self.format_number(upgrade['level'])})", True, "#ffffff")
            self.screen.blit(upgrade_text, (30, 110 + index * 120))

            # Texto do preço
            price_text = self.font.render(f"Preço: {self.format_number(upgrade['price'])}", True, "#ffffff")
            self.screen.blit(price_text, (30, 150 + index * 120))

        # Botão de voltar
        back_rect = self.back_img.get_rect(topleft=(self.width - 50, 10))
        self.screen.blit(self.back_img, back_rect)

        # Verifica se o botão de "Voltar" foi clicado
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and back_rect.collidepoint(mouse_pos):
            if not self.back_cooldown:  # Verifica se o cooldown não está ativo
                self.in_upgrades = False  # Fecha a tela de upgrades
                self.back_cooldown = True  # Ativa o cooldown
                self.last_back_click_time = time.time()  # Atualiza o tempo do último clique

        pygame.display.update()

    def show_settings_page(self):
        """ Exibe a página de configurações """
        self.screen.fill("#333333")

        title = self.font.render("Configurações", True, "#ffffff")
        self.screen.blit(title, (320, 15))  

        # Botão de voltar (Exit)
        back_rect = self.back_img.get_rect(topleft=(self.width - 50, 10))
        self.screen.blit(self.back_img, back_rect)

        # Desenhar barra de volume
        pygame.draw.rect(self.screen, "#ffffff", (100, 200, 300, 10))  # Linha da barra
        pygame.draw.circle(self.screen, "#ff0000", (int(100 + self.music_volume * 300), 205), 10)  # Botão do slider

        # Texto do volume
        volume_text = self.font.render(f"Music Sound: {int(self.music_volume * 100)}%", True, "#ffffff")
        self.screen.blit(volume_text, (420, 190))

        pygame.display.update()

        # Verifica se o botão de "Voltar" foi clicado
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Clique do mouse
            if back_rect.collidepoint(mouse_pos):
                if not self.back_cooldown:
                    self.in_settings = False
                    self.back_cooldown = True
                    self.last_back_click_time = time.time()
            elif 100 <= mouse_pos[0] <= 400 and 195 <= mouse_pos[1] <= 215:  # Se clicar no slider
                self.music_volume = (mouse_pos[0] - 100) / 300  # Atualiza o volume com base na posição do mouse
                pygame.mixer.music.set_volume(self.music_volume)  # Ajusta o volume da música


    @staticmethod
    def format_number(num):
        num = float(num)
        if num >= 10**63:
            return f"{num / 10**63:.2f}Vg"
        elif num >= 10**60:
            return f"{num / 10**60:.2f}Nn"
        elif num >= 10**57:
            return f"{num / 10**57:.2f}Od"
        elif num >= 10**54:
            return f"{num / 10**54:.2f}Sp"
        elif num >= 10**51:
            return f"{num / 10**51:.2f}SS"
        elif num >= 10**48:
            return f"{num / 10**48:.2f}QD"
        elif num >= 10**45:
            return f"{num / 10**45:.2f}Qd"
        elif num >= 10**42:
            return f"{num / 10**42:.2f}td"
        elif num >= 10**39:
            return f"{num / 10**39:.2f}dd"
        elif num >= 10**36:
            return f"{num / 10**36:.2f}un"
        elif num >= 10**33:
            return f"{num / 10**33:.2f}D"
        elif num >= 10**30:
            return f"{num / 10**30:.2f}N"
        elif num >= 10**27:
            return f"{num / 10**27:.2f}O"
        elif num >= 10**24:
            return f"{num / 10**24:.2f}ss"
        elif num >= 10**21:
            return f"{num / 10**21:.2f}s"
        elif num >= 10**18:
            return f"{num / 10**18:.2f}qq"
        elif num >= 10**15:
            return f"{num / 10**15:.2f}q"
        elif num >= 10**12:
            return f"{num / 10**12:.2f}t"
        elif num >= 10**9:
            return f"{num / 10**9:.2f}b"
        elif num >= 10**6:
            return f"{num / 10**6:.2f}m"
        elif num >= 10**3:
            return f"{num / 10**3:.2f}k"
        else:
            return str(int(num))  # Garante que valores pequenos sejam exibidos como inteiros

menu = Menu()
if menu.run() == "start":
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                game.auto_click()
            game.click_button(event)
        game.render()