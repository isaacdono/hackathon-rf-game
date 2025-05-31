from machine import Pin, ADC
import time

botao = Pin(3, Pin.IN, Pin.PULL_DOWN)  # GPIO3, ajuste se necessário
led = Pin(25, Pin.OUT)  # Onboard LED on GPIO 25

valor_last = '0'

def trata_botao(pin):
    global valor_last
    valor = pin.value()
    if valor_last != valor:
        print(valor)  # Envia '1' ou '0' via serial
    valor_last = valor

botao.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=trata_botao)

while True:
    led.toggle()
    time.sleep(0.4)  # Delay de 400 ms
