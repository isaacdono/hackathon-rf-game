import pygame
import os
from game.config import IMG_DIR  
from game.bubbly import Game as BubblyFishGame


class Hub:
    def __init__(self):
        pygame.init()
        self.screen_width = 1080
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game Hub")
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.font = pygame.font.SysFont("Bauhaus 93", 60)
        self.button_font = pygame.font.SysFont("Bauhaus 93", 40)
        self.white_color = (255, 255, 255)
        self.button_color = (20, 150, 200)
        self.button_text_color = (255, 255, 255)
        self.disabled_button_color = (100, 100, 100)
        self.disabled_text_color = (200, 200, 200)

        # Load background image (can be the same as Bubbly Fish or a new one)
        try:
            self.bg_img = pygame.transform.scale(
                pygame.image.load(os.path.join(IMG_DIR, "bg.png")),
                (self.screen_width, self.screen_height),
            )
        except pygame.error as e:
            print(f"Error loading background image for hub: {e}")
            self.bg_img = pygame.Surface((self.screen_width, self.screen_height))
            self.bg_img.fill((0, 0, 50))  # Fallback background

        # Hub button definitions
        self.bubbly_fish_button_rect = pygame.Rect(
            self.screen_width // 2 - 150, self.screen_height // 2 - 100, 300, 80
        )
        self.other_game_button_rect = pygame.Rect(
            self.screen_width // 2 - 150, self.screen_height // 2 + 20, 300, 80
        )

    def _draw_text(self, text, font, text_col, x, y, center_x=False):
        img = font.render(text, True, text_col)
        rect = img.get_rect()
        if center_x:
            rect.centerx = x
        else:
            rect.x = x
        rect.y = y
        self.screen.blit(img, rect)

    def _draw_button(self, rect, text, button_color, text_color):
        pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
        text_img = self.button_font.render(text, True, text_color)
        text_rect = text_img.get_rect(center=rect.center)
        self.screen.blit(text_img, text_rect)

    def _draw_elements(self):
        self.screen.blit(self.bg_img, (0, 0))
        self._draw_text(
            "Hub de Jogos",
            self.font,
            self.white_color,
            self.screen_width // 2,
            150,
            center_x=True,
        )

        self._draw_button(
            self.bubbly_fish_button_rect,
            "Iniciar Bubbly Fish",
            self.button_color,
            self.button_text_color,
        )
        self._draw_button(
            self.other_game_button_rect,
            "Outro Jogo (Breve)",
            self.disabled_button_color,
            self.disabled_text_color,
        )

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Signal to stop the hub

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.bubbly_fish_button_rect.collidepoint(event.pos):
                        print("Starting Bubbly Fish...")
                        bubbly_game = BubblyFishGame()
                        bubbly_game.run()
                        # After Bubbly Fish finishes, we might want to re-initialize hub display
                        # or simply let the hub loop continue, which will redraw.
                        # For now, it will return to the hub screen.
                        pygame.display.set_caption("Game Hub")  # Reset caption

                    elif self.other_game_button_rect.collidepoint(event.pos):
                        print("Other game button clicked (not implemented).")
        return True

    def run(self):
        running = True
        while running:
            running = self._handle_events()
            if not running:
                break

            self._draw_elements()
            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()


if __name__ == "__main__":
    hub = Hub()
    hub.run()
