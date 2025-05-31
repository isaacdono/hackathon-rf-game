from machine import Pin, ADC
import time

sensor = ADC(0)  # ADC0 → GP26
led = Pin(25, Pin.OUT)  # Onboard LED for debug

limiar = 750  # Ajuste conforme o comportamento do sensor

while True:
    valor_adc = sensor.read_u16() % 1024
    # print(valor_adc)
    valor = 1 if valor_adc > limiar else 0

    print(valor)  # Envia '1' ou '0' via serial

    led.toggle()
    time.sleep(0.2)  # Ajuste o tempo conforme necessário
