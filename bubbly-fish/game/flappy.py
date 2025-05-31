import pygame
import random
import os

from .entities import Bird
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
        pygame.display.set_caption("Flappy Bird OOP")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Bauhaus 93", 60)
        self.white_color = (255, 255, 255)

        self._load_images()
        self._create_objects()
        self._reset_game_state()  # Initialize game state variables

    def _load_images(self):
        self.bg_img = pygame.image.load(os.path.join(IMG_DIR, "bg.png"))
        self.ground_img = pygame.image.load(os.path.join(IMG_DIR, "ground.png"))
        self.button_img = pygame.image.load(os.path.join(IMG_DIR, "restart.png"))
        self.pipe_img_path = os.path.join(IMG_DIR, "pipe.png")

    def _create_objects(self):
        self.flappy = Bird(100, int(self.screen_height / 2), IMG_DIR)
        self.bird_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.bird_group.add(self.flappy)
        self.restart_button = Button(
            self.screen_width // 2 - 50,
            self.screen_height // 2 - 100,
            self.button_img,
        )

    def _reset_game_state(self):
        self.pipe_group.empty()
        self.flappy.rect.x = 100
        self.flappy.rect.y = int(self.screen_height / 2)
        self.flappy.vel = 0
        self.flappy.clicked = False  # Reset clicked state for the bird
        self.flappy.index = 0  # Reset bird animation
        self.flappy.image = self.flappy.images[self.flappy.index]  # Reset bird image

        self.score = 0
        self.flying = False
        self.game_over = False
        self.ground_scroll = 0
        self.last_pipe = pygame.time.get_ticks() - self.pipe_frequency
        self.pass_pipe = False

    def _draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Signal to stop the game
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and not self.flying
                and not self.game_over
            ):
                self.flying = True
        return True  # Signal to continue

    def _update_game_state(self):
        if self.game_over:
            if self.restart_button.draw(self.screen):
                self._reset_game_state()
        else:
            self.bird_group.update(self.flying, self.game_over, self.ground_y_position)

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
                if abs(self.ground_scroll) > 35:
                    self.ground_scroll = 0

            self.pipe_group.update()

            # Check score
            if (
                not self.game_over and self.flying
            ):  # Only check score if game is active and bird is flying
                if len(self.pipe_group) > 0:
                    bird_sprite = self.bird_group.sprites()[0]
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
                    self.bird_group, self.pipe_group, False, False
                )
                or self.flappy.rect.top < 0
            ):
                self.game_over = True

            # Check if bird has hit the ground
            if self.flappy.rect.bottom >= self.ground_y_position:
                self.game_over = True
                self.flying = False  # Stop flying if hit ground

    def _draw_elements(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.pipe_group.draw(self.screen)
        self.bird_group.draw(self.screen)
        self.screen.blit(self.ground_img, (self.ground_scroll, self.ground_y_position))
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
