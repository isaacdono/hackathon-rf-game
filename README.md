# Hackathon da Receita Federal

O 1º Hackathon da Receita Federal, teve como objetivo reaproveitar de forma sustentável cigarros eletrônicos apreendidos. Nossa equipe, Fresh Air, criou uma solução focada em educação: um kit com peças plug and play para criar projetos de eletrônica e programação. Como exemplo, desenvolvemos o Bubbly Fish, um jogo no estilo Flappy Bird controlado por sopro usando o sensor de pressão do e-cig. 

## Visão Geral

O jogador interage soprando no sensor, enviando dados para o jogo via comunicação serial.

### Componentes do Projeto

#### 1. Raspberry Pi Pico

- Lê sinais do sensor usando um analog-to-digital-converter
- Scripts principais:
  - `pico/main.py`: Lê o valor do sensor e acende o LED onboard, além de enviar o valor via serial.
  - `pico/button.py`: Faz a leitura do botão e envia mudanças pelo serial.

#### 2. Comunicação Serial

- Utiliza o módulo `bubbly-fish/sensor/serial_reader.py` para receber os dados da Pico no PC.  
- O `SerialReader` escuta a porta serial usando threads, repassando eventos para o jogo.

#### 3. Jogo Bubbly Fish

- Arquivos principais em `bubbly-fish/game/`.
- O jogo é feito em Python com Pygame, simulando um peixe que deve "nadar" evitando obstáculos.
- A interação principal ocorre quando o sensor detecta um sopro ou clique, fazendo o peixe subir.
- O hub de jogos (`bubbly-fish/hub.py`) permite iniciar o Bubbly Fish e, futuramente, outros minigames.

#### 4. Lógica do Sensor

- O valor lido do sensor é comparado a um limiar para detectar um sopro.
- A cada detecção, um pulso é enviado via serial para ser interpretado pelo jogo.

## Como Usar

1. Grave o script `pico/main.py` ou `pico/button.py` na Raspberry Pi Pico.
2. Conecte a Pico ao PC e anote a porta serial.
3. No PC, rode `bubbly-fish/main.py`, ajustando a porta serial no código (`port='COM12'` ou similar).
4. Use o hub de jogos (`bubbly-fish/hub.py`) para iniciar.

## Requisitos

- Raspberry Pi Pico
- Sensor analógico (ex: sensor de sopro) ou botão
- Python 3.x + Pygame no PC
- Bibliotecas: `pyserial`, `pygame`

## Créditos
Nossa equipe trabalhou em diversas frentes: hardware, software e na elaboração do pitch em vídeo.  
Mais informações sobre a equipe neste [post no LinkedIn](https://www.linkedin.com/posts/isaacdonoliv_pitch-receitafederal-campinas-activity-7335482164198699008-wHod?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEfWl70BYX_WwddYEyEeQUxNJJpHjce6NLU).
