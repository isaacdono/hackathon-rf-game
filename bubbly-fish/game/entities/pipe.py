import pygame

from ..config import PIPE_GAP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, scroll_speed, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.scroll_speed = scroll_speed
        if position == 1:  # Top pipe
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - int(PIPE_GAP / 2))
        if position == -1:  # Bottom pipe
            self.rect.topleft = (x, y + int(PIPE_GAP / 2))
        
        self.mask = pygame.mask.from_surface(self.image) # Cria a máscara para o cano

    def update(self):
        self.rect.x -= self.scroll_speed
        if self.rect.right < 0:
            self.kill()
