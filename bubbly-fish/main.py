from game.bubbly import Game
from sensor.serial_reader import SerialReader

if __name__ == "__main__":
    game = Game()
    serial = SerialReader(game.handle_sensor, port='COM12', baudrate=115200)

    serial.start_listening()
    game.run()

    serial.stop_listening()
