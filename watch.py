import util
import time
import machine

def autoWater(mqttClient):
    data = util.getSensorInfo()
    if data['value'] > 1.85:
        util.water_on()
        changeSwitchState(mqttClient, 'ON')
        print('开始浇水')
        tim0 = machine.Timer()
        def stopWater(t):
            state = util.getSwitchState()
            util.water_off()
            changeSwitchState(mqttClient, 'OFF')
            print('结束浇水')
        tim0.init(period = 39000,mode = machine.Timer.ONE_SHOT,callback=stopWater)
#         time.sleep(30)
#         util.water_off()
#         changeSwitchState(mqttClient, 'OFF')
#         print('结束浇水')
    

def changeSwitchState(mqttClient, msg):
    try:
        mqttClient.publish('homeassistant/switch/irrigation_1999/state', msg)
    except:
        print('watch net err ', msg)


