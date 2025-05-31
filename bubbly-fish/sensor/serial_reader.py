import serial
import threading
import time

from typing import Optional, Callable


class SerialReader:
    def __init__(
        self,
        callback: Callable[[str], None] = lambda _: None,
        port: str = "COM3",
        baudrate: int = 115200,
        timeout: Optional[float] = 1,
    ):
        self.port: str = port
        self.baudrate: int = baudrate
        self.timeout: Optional[float] = timeout
        self.serial: Optional[serial.Serial] = None
        self.is_listening: bool = False
        self.thread: Optional[threading.Thread] = None
        self.latest_data: Optional[str] = None  # Para armazenar o último dado lido
        self.callback: Callable[[str], None] = callback

    def connect(self) -> bool:
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Conectado à porta serial {self.port} com baudrate {self.baudrate}")
            return True
        except serial.SerialException as e:
            print(f"Erro ao conectar à porta serial {self.port}: {e}")
            self.serial = None
            return False

    def _listen(self) -> None:
        print("Iniciando escuta da serial...")
        while self.is_listening and self.serial:
            try:
                if self.serial.in_waiting > 0:
                    line: str = self.serial.readline().decode("utf-8").strip()
                    if line:
                        self.latest_data = line
                        self.callback(self.latest_data)  # Chama o callback com o dado
                else:
                    time.sleep(0.01)  # Pequena pausa para não sobrecarregar a CPU

            except serial.SerialException as e:
                print(f"Erro durante a leitura da serial: {e}")
                self.is_listening = False  # Parar de escutar em caso de erro grave
                break

            except Exception as e:
                print(f"Erro inesperado: {e}")
                time.sleep(0.1)

        print("Escuta da serial encerrada.")

    def start_listening(self) -> bool:
        if not self.serial:
            if not self.connect():
                return False

        if self.is_listening:
            print("A escuta já está ativa.")
            return True

        self.is_listening = True
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()
        print("Thread de escuta iniciada.")
        return True

    def stop_listening(self) -> None:
        if self.is_listening:
            self.is_listening = False
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=2)  # Esperar a thread terminar
            print("Solicitação para parar a escuta enviada.")

        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Porta serial fechada.")

        self.serial = None

    def get_latest_data(self) -> Optional[str]:
        """Retorna o último dado lido e o limpa para evitar releitura."""
        data = self.latest_data
        self.latest_data = None
        return data
