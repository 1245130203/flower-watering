import time
import machine


led_onBoard = machine.Pin("LED",machine.Pin.OUT)
led_onBoard.value(0)


led_external = machine.Pin(15, machine.Pin.OUT)
led_external.value(0)

def wifi_error():
    while True:
        led_onBoard.value(0)
        time.sleep(2)
        led_onBoard.value(1)
        time.sleep(0.2)
        led_onBoard.value(0)
        time.sleep(0.2)
        led_onBoard.value(1)
        time.sleep(0.2)
        led_onBoard.value(0)
        time.sleep(0.2)
        led_onBoard.value(1)
        time.sleep(1)
        led_onBoard.value(0)
        time.sleep(0.2)
        led_onBoard.value(1)
        time.sleep(1)
        led_onBoard.value(0)
        time.sleep(0.2)

def water_on():
    led_onBoard.value(1)
    led_external.value(1)

def water_off():
    led_onBoard.value(0)
    led_external.value(0)
    
def getSensorInfo():
    ADC2= machine.ADC(machine.Pin(28))
    reading = round(ADC2.read_u16()*3.3/65535, 4)
    percent = 0.000
    if reading > 2.25:
        percent = 0.000
    elif reading < 1.000:
        percent = 100.000
    else:
        percent = round((2.25 - reading) * 80, 3)
    return { "percent": percent, "value": reading }

def getSwitchState():
    return led_onBoard.value()


# water_on()
# print(led_external.value())
# time.sleep(3)
# water_off()
# print(led_external.value())    
#     
