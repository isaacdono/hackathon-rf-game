import os
import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path_prefix):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img_path = os.path.join(image_path_prefix, f"bird{num}.png")
            self.images.append(pygame.image.load(img_path))
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = 0
        self.is_thrusting = False  # Novo: True se o botão/sensor estiver pressionado

    def update(self, is_game_active, is_game_over, ground_y_position):
        if is_game_active:
            if self.is_thrusting and not is_game_over:
                # Aplicar impulso para cima enquanto o botão estiver pressionado
                self.vel = -5  # Velocidade ascendente constante durante o impulso
            else:
                # Gravidade normal quando não há impulso ou o jogo acabou
                self.vel += 0.5
                if self.vel > 8:
                    self.vel = 8

            if (
                self.rect.bottom < ground_y_position or self.vel < 0
            ):  # Permitir subir acima do chão
                self.rect.y += int(self.vel)

            # Impede que o pássaro vá para cima do limite superior da tela
            if self.rect.top < 0:
                self.rect.top = 0
                self.vel = 0  # Para a subida se bater no teto

        if not is_game_over:
            # A lógica de pulo por clique direto do mouse é removida daqui
            # pois será gerenciada em Game com MOUSEBUTTONDOWN e MOUSEBUTTONUP

            # handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate the bird
            if self.is_thrusting:
                # Rotação para cima quando está subindo
                self.image = pygame.transform.rotate(self.images[self.index], 20)
            else:
                # Rotação para baixo baseada na velocidade de queda
                self.image = pygame.transform.rotate(
                    self.images[self.index], max(self.vel * -3, -90)
                )
        else:  # is_game_over == True
            self.image = pygame.transform.rotate(self.images[self.index], -90)
            self.is_thrusting = False  # Garante que o impulso pare no game over
