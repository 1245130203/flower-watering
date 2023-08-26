# Filename: pico_w_mqtt.py
# 本文件主要与网络相关
import network
from umqtt.simple import MQTTClient
import time
import util

ssid = 'Floor2EN' # wifi 名称
password = '19990116' # wifi 密码
BrokerAddr = '192.168.0.27'   # 指定的MQTT服务器
mqttPort = 1883  # 1883为指定的MQTT服务器端口号
ClientID = "Pico_W_01"  # 设定PICO_W为Pico W开发板设备ID
#Topic = "coolcall"  # 设定MQTT主题为LED
mqttClient = {}

# 订阅回调函数
def sub_callback(topic, msg):
    print('sub')
    topic = str(topic,'utf-8')
    msg = str(msg,'utf-8')
    command= msg.strip()
    print(topic, command)
    # 显示主题和命令消息
    if topic == 'homeassistant/switch/irrigation_1999/set' and command == "ON":  # "开水阀"命令消息
        util.water_on()
    if topic == 'homeassistant/switch/irrigation_1999/set' and command == "OFF":  # "关水阀"命令消息
        util.water_off()
    # 是否需要检查pin口状态，再返回 todo
    mqttClient.publish('homeassistant/switch/irrigation_1999/state', msg)
    
def initDeviceSensor():
    mqttClient.publish("homeassistant/sensor/office_temp_adc2_source/config", '{ "unique_id": "office_temp_adc2_source", "device_class": "humidity", "name": "office_temp_adc2_source", "state_topic": "homeassistant/sensor/office_temp_adc2_source/state", "unit_of_measurement": "", "value_template": "{{ value_json.text }}" }')
    mqttClient.publish("homeassistant/sensor/office_temp_adc2/config", '{ "unique_id": "office_temp_adc2", "device_class": "humidity", "name": "office_temp_adc2", "state_topic": "homeassistant/sensor/office_temp_adc2/state", "unit_of_measurement": "%", "value_template": "{{ value_json.text }}" }')

def initDeviceSwitch():
    mqttClient.publish("homeassistant/switch/irrigation_1999/config",'{"unique_id": "irrigation_1999", "name": "irrigation_1999", "command_topic": "homeassistant/switch/irrigation_1999/set", "state_topic": "homeassistant/switch/irrigation_1999/state"}')

def uploadDeviceInfo():
    data = util.getSensorInfo()
    #print(data)
	#读取ADC通道0的数值
	#并根据ADC电压计算公式得到GPIO26引脚上的电压
    mqttClient.publish("homeassistant/sensor/office_temp_adc2/state", '{ "text": ' + str(data['percent']) + ' }')
    mqttClient.publish("homeassistant/sensor/office_temp_adc2_source/state", '{ "text": ' + str(data['value']) + ' }')

def subscribeSwitch():
    mqttClient.subscribe("homeassistant/switch/irrigation_1999/set")
    state = util.getSwitchState()
    mqttClient.publish('homeassistant/switch/irrigation_1999/state', "OFF" if state == 0 else "ON")
    
def initNet(wdt):
    global mqttClient
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    wdt.feed()
    time.sleep(4)
    wdt.feed()
    time.sleep(4)
    wdt.feed()

    # wifi 状态检查
    if station.status() != 3:
        #util.wifi_error()
        raise RuntimeError('network connection failed')
    else:
      print('connected')
      status = station.ifconfig()
      print( 'ip = ' + status[0] )
      #led_onBoard.value(1)


    # 将Pico W开发板连接到指定的MQTT服务器
    mqttClient = MQTTClient(ClientID, BrokerAddr, mqttPort, 'shensiming', '19990116', keepalive = 300)
    wdt.feed()   
    mqttClient.set_callback(sub_callback)
    mqttClient.connect()


    initDeviceSensor()
    time.sleep(1)
    wdt.feed()
    initDeviceSwitch()
    time.sleep(1)
    wdt.feed()
    return mqttClient

    #mqttClient.publish("coolcall", "234", qos = 0)
    # mqttClient.wait_msg()




