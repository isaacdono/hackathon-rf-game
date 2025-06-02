from machine import Pin, ADC
import time

sensor = ADC(0)  # GP26
led = Pin(25, Pin.OUT)

LIMIAR = 500
estado_anterior = 0

led.off()
while True:
    valor_adc = sensor.read_u16() % 1024
    valor = 1 if valor_adc > LIMIAR else 0

    if valor == 1 and estado_anterior == 0:
        print(1)
        led.on()
        # Após detectar, espera breve tempo para permitir novo sopro
        time.sleep(0.2)  # Reduz para permitir "double tap"
        estado_anterior = 0  # Força rearmar rápido
    else:
        print(0)
        led.off()
        estado_anterior = valor

    time.sleep(0.15)
