from game.flappy import Game
from sensor.serial_reader import SerialReader

if __name__ == "__main__":
    game = Game()
    serial = SerialReader(game.handle_sensor)

    serial.start_listening()
    game.run()

    serial.stop_listening()
