import serial

porta = 'COM3'  # Substitua pelo nome correto, ex.: COM4
baudrate = 9600

ser = serial.Serial(porta, baudrate, timeout=1)

print("Lendo da serial...")

while True:
    linha = ser.readline().decode('utf-8').strip()
    if linha:
        print(f"Recebido: {linha}")
