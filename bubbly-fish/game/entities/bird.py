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
        self.clicked = False  # Usado para debounce do pulo
        self.jump_requested = False  # Novo: para sinalizar um pedido de pulo

    def jump(self):
        # Só pula se não estiver já em um estado de "clique" (debounce)
        # e o jogo não estiver em game over (verificação adicional no Game)
        if not self.clicked:
            self.vel = -10
            self.clicked = (
                True  # Impede pulos múltiplos imediatos com um sinal contínuo
            )
            self.jump_requested = (
                True  # Sinaliza que um pulo foi efetivamente solicitado/processado
            )

    def update(
        self, is_game_active, is_game_over, ground_y_position
    ):  # Renomeado is_flying para is_game_active
        if is_game_active:  # O jogo está rodando (pássaro está sujeito à física)
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < ground_y_position:
                self.rect.y += int(self.vel)
            # else: # Colisão com o chão é tratada no Game para definir game_over

        if not is_game_over:
            # Lógica de pulo por mouse (mantida para debug ou como alternativa)
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.jump()  # Chama o novo método jump

            # Reset do clicked para permitir novo pulo após soltar o mouse
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                # Não resetamos jump_requested aqui, pois ele é resetado no Game
                # após o pulo ser "consumido" (pássaro começa a cair)

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
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:  # is_game_over == True
            self.image = pygame.transform.rotate(self.images[self.index], -90)
            # Quando o jogo acaba, resetamos 'clicked' e 'jump_requested'
            # para que, se o jogo for reiniciado, um novo clique/sinal possa funcionar.
            self.clicked = False
            self.jump_requested = False
