import pygame
import random
import os

from .entities import Fish
from .entities import Button
from .entities import Pipe
from .config import *


class Game:
    def __init__(self):
        pygame.init()

        self.screen_width = 864
        self.screen_height = 936
        self.fps = 60
        self.scroll_speed = 4
        self.pipe_frequency = 1500  # milliseconds
        self.ground_y_position = 768  # Y position of the ground

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Bubbly Fish")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Bauhaus 93", 60)
        self.white_color = (255, 255, 255)

        self._load_images()
        self._create_objects()
        self._reset_game_state()  # Initialize game state variables

    def _load_images(self):
        self.bg_img = pygame.transform.scale(
            pygame.image.load(os.path.join(IMG_DIR, "bg.png")),
            (self.screen_width, self.screen_height),
        )

        midground_original_img = pygame.image.load(
            os.path.join(IMG_DIR, "midground.png")
        )
        original_width = midground_original_img.get_width()
        original_height = midground_original_img.get_height()

        self.midground_img = pygame.transform.scale(
            midground_original_img,
            (
                int(self.screen_height * original_width / original_height),
                self.screen_height,
            ),
        )

        original_ground_img = pygame.image.load(os.path.join(IMG_DIR, "ground.png"))
        original_ground_width = original_ground_img.get_width()
        original_ground_height = original_ground_img.get_height()

        new_ground_height = self.screen_height - self.ground_y_position

        if original_ground_height > 0:
            new_ground_width = int(
                new_ground_height * original_ground_width / original_ground_height
            )

        else:  # Default to original width if height is 0
            new_ground_width = original_ground_width
            new_ground_height = original_ground_height

        # Scale the ground image
        self.ground_img = pygame.transform.scale(
            original_ground_img, (new_ground_width, new_ground_height)
        )

        self.button_img = pygame.image.load(os.path.join(IMG_DIR, "restart.png"))
        self.pipe_img_path = os.path.join(IMG_DIR, "pipe.png")

    def _create_objects(self):
        self.bubbly = Fish(100, int(self.screen_height / 2), IMG_DIR)
        self.fish_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.fish_group.add(self.bubbly)
        self.restart_button = Button(
            self.screen_width // 2 - 50,
            self.screen_height // 2 - 100,
            self.button_img,
        )

    def _reset_game_state(self):
        self.pipe_group.empty()
        self.bubbly.rect.x = 100
        self.bubbly.rect.y = int(self.screen_height / 2)
        self.bubbly.vel = 0
        # self.flappy.clicked = False # Removido
        # self.flappy.jump_requested = False # Removido
        self.bubbly.is_thrusting = False  # Resetar estado de impulso
        self.bubbly.index = 0  # Reset bird animation
        self.bubbly.image = self.bubbly.images[self.bubbly.index]  # Reset bird image

        self.score = 0
        self.flying = False
        self.game_over = False
        self.ground_scroll = 0
        self.midground_scroll = 0  # Initialize midground scroll
        self.last_pipe = pygame.time.get_ticks() - self.pipe_frequency
        self.pass_pipe = False

    def _draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def handle_sensor(self, msg: str):
        # O sensor agora controla diretamente o estado de is_thrusting do pássaro
        # Assumindo que msg '1' significa impulso e '0' (ou ausência) significa sem impulso.
        # Esta lógica pode precisar de ajuste dependendo de como o SerialReader envia os dados.
        if not self.game_over:
            if msg == "1":  # Ou qualquer que seja o sinal de "ativo" do sensor
                if not self.flying:  # Inicia o jogo no primeiro impulso
                    self.flying = True
                self.bubbly.is_thrusting = True
            else:  # Sensor não está ativo (ou enviou '0')
                self.bubbly.is_thrusting = False

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Signal to stop the game

            # Lógica para o mouse controlar o impulso contínuo
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.game_over:  # Botão esquerdo do mouse
                    if not self.flying:
                        self.flying = True
                    self.bubbly.is_thrusting = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Botão esquerdo do mouse
                    self.bubbly.is_thrusting = False
        return True  # Signal to continue

    def _update_game_state(self):
        if self.game_over:
            if self.restart_button.draw(self.screen):
                self._reset_game_state()
        else:
            self.fish_group.update(self.flying, self.game_over, self.ground_y_position)

            # A lógica de reset de clicked/jump_requested é removida daqui,
            # pois o impulso é contínuo e gerenciado por is_thrusting.

            if self.flying:
                # Generate new pipes
                time_now = pygame.time.get_ticks()
                if time_now - self.last_pipe > self.pipe_frequency:
                    pipe_height = random.randint(-100, 100)
                    btm_pipe = Pipe(
                        self.screen_width,
                        int(self.screen_height / 2) + pipe_height,
                        -1,
                        self.scroll_speed,
                        self.pipe_img_path,
                    )
                    top_pipe = Pipe(
                        self.screen_width,
                        int(self.screen_height / 2) + pipe_height,
                        1,
                        self.scroll_speed,
                        self.pipe_img_path,
                    )
                    self.pipe_group.add(btm_pipe)
                    self.pipe_group.add(top_pipe)
                    self.last_pipe = time_now

                # Scroll the ground
                self.ground_scroll -= self.scroll_speed
                if (
                    abs(self.ground_scroll)
                    > self.ground_img.get_width()  # Use a largura da imagem do chão
                ):
                    self.ground_scroll = 0

                # Scroll the midground
                self.midground_scroll -= (
                    self.scroll_speed * 0.5
                )  # Slower speed for parallax
                if abs(self.midground_scroll) > self.midground_img.get_width():
                    self.midground_scroll = 0

            self.pipe_group.update()

            # Check score
            if (
                not self.game_over and self.flying
            ):  # Only check score if game is active and bird is flying
                if len(self.pipe_group) > 0:
                    bird_sprite = self.fish_group.sprites()[0]
                    # The pipe relevant for scoring is the first one in the group (most to the left)
                    pipe_to_score = self.pipe_group.sprites()[0]

                    # Stage 1: Bird is entering the pipe's scoring zone
                    # Set self.pass_pipe to True if the bird's front (left edge) has passed
                    # the pipe's front (left edge), but not yet its back (right edge).
                    if not self.pass_pipe:
                        if (
                            bird_sprite.rect.left > pipe_to_score.rect.left
                            and bird_sprite.rect.left < pipe_to_score.rect.right
                        ):
                            self.pass_pipe = True

                    # Stage 2: Bird has completely passed the pipe
                    # Increment score and reset self.pass_pipe if the bird's front (left edge)
                    # has passed the pipe's back (right edge), and we were in "pass_pipe" state.
                    if self.pass_pipe:
                        if bird_sprite.rect.left > pipe_to_score.rect.right:
                            self.score += 1
                            self.pass_pipe = False

            if (
                pygame.sprite.groupcollide(
                    self.fish_group, self.pipe_group, False, False, pygame.sprite.collide_mask
                )
                or self.bubbly.rect.top < 0
            ):
                self.game_over = True

            # Check if bird has hit the ground
            if self.bubbly.rect.bottom >= self.ground_y_position:
                self.game_over = True
                self.flying = False  # Stop flying if hit ground
                self.bubbly.is_thrusting = False  # Para o impulso se bater no chão

    def _draw_elements(self):
        self.screen.blit(self.bg_img, (0, 0))

        # Draw midground (scrolling)
        # Position it, for example, aligned with the ground or slightly above
        # Adjust midground_y_position as needed based on your image and desired placement
        midground_y_position = (
            self.ground_y_position - self.midground_img.get_height() + 50
        )  # Example: 50px above ground bottom

        self.screen.blit(
            self.midground_img, (self.midground_scroll, midground_y_position)
        )
        self.screen.blit(
            self.midground_img,
            (
                self.midground_scroll + self.midground_img.get_width(),
                midground_y_position,
            ),
        )

        self.pipe_group.draw(self.screen)
        self.fish_group.draw(self.screen)

        # Draw scrolling ground (optimized)
        ground_width = self.ground_img.get_width()
        self.screen.blit(self.ground_img, (self.ground_scroll, self.ground_y_position))
        self.screen.blit(
            self.ground_img,
            (self.ground_scroll + ground_width, self.ground_y_position),
        )
        self.screen.blit(
            self.ground_img,
            (self.ground_scroll + 2 * ground_width, self.ground_y_position),
        )

        self._draw_text(
            str(self.score), self.font, self.white_color, int(self.screen_width / 2), 20
        )

        if self.game_over:
            self.restart_button.draw(self.screen)

    def run(self):
        running = True
        while running:
            running = self._handle_events()
            if not running:
                break

            self._update_game_state()
            self._draw_elements()

            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
