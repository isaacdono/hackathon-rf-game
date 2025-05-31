from game.flappy import Game
from serial.serial_reader import SerialReader

if __name__ == "__main__":
    game = Game()
    serial = SerialReader()

    game.run()
