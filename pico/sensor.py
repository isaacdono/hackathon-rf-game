from machine import Pin, ADC
import time

# === CONFIGURAÇÃO ===

# Para teste com botão:
botao = Pin(3, Pin.IN, Pin.PULL_DOWN)  # GPIO2, ajuste se necessário

# # Para teste com sensor ADC:
# sensor = ADC(0)  # ADC0 → GP26

# # === MODO DE TESTE ===
# usar_botao = True  # True = usar botão, False = usar sensor

while True:
    # if usar_botao:
    valor = botao.value()  # 1 (pressionado) ou 0 (não)
    # else:
    #     valor_adc = sensor.read_u16()  # 0 a 65535
    #     # Simples binarização: se muito acima do fundo de escala, considera "ativo"
    #     valor = 1 if valor_adc > 50000 else 0

    print(valor)  # Envia '1' ou '0' via serial
    time.sleep(0.2)  # Delay de 200 ms
