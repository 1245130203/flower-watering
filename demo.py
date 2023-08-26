# Filename: pico_w_mqtt.py
import network
from umqtt.simple import MQTTClient
import time
from machine import Pin, ADC
import util

ssid = 'Floor2EN'
password = '19990116'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

time.sleep(8)

led_onBoard = Pin("LED",Pin.OUT)
led_onBoard.value(0)
led_external = Pin(15, Pin.OUT)
led_external.value(0)

# Handle connection error
if station.status() != 3:
    util.wifi_error()
    raise RuntimeError('network connection failed')
else:
  print('connected')
  status = station.ifconfig()
  print( 'ip = ' + status[0] )
  led_onBoard.value(1)


BrokerAddr = '192.168.0.27'   # 指定的MQTT服务器: test.mosquitto.org
mqttPort = 1883  # 1883为指定的MQTT服务器端口号
ClientID = "Pico_W"  # 设定PICO_W为Pico W开发板设备ID
Topic = "coolcall"  # 设定MQTT主题为LED

mqttClient = MQTTClient(ClientID, BrokerAddr, mqttPort, 'shensiming', '19990116', keepalive = 300)

def sub_callback(topic, msg):
    print('sub')
    topic = str(topic,'utf-8')
    msg = str(msg,'utf-8')
    print(topic, msg)
    command= msg.strip()
    print(topic, command)  # 显示主题和命令消息
    if topic == 'homeassistant/switch/irrigation_1999/set' and command == "ON":  # "开灯"命令消息
        led_onBoard.value(1)
        led_external.value(1)
    if topic == 'homeassistant/switch/irrigation_1999/set' and command == "OFF":  # "关灯"命令消息
        led_onBoard.value(0)
        led_external.value(0)
    mqttClient.publish('homeassistant/switch/irrigation_1999/state', msg)
    
mqttClient.set_callback(sub_callback)

def on_message_callback(client, userdata, message):
    print(message.topic+" " + ":" + str(message.payload))
    client.publish('homeassistant/switch/irrigation_1999/state', message.payload)

  
# 将Pico W开发板连接到指定的MQTT服务器
#mqttClient = MQTTClient(ClientID, BrokerAddr, mqttPort, 'shensiming', '19990116', keepalive = 300)
#mqttClient.set_callback(sub_callback)
#mqttClient.on_message = on_message_callback
#mqttClient.on_connect = on_connect

mqttClient.connect()
#mqttClient.publish("coolcall", "123", qos = 0)
#mqttClient.loop_start()
#mqttClient.subscribe(Topic, qos = 0)  # Pico W开发板订阅主题
print("Ok")

def checkTem():
    #$ADC2= ADC(Pin(28))
    #reading = ADC2.read_u16()*3.3/65535
	#读取ADC通道0的数值
	#并根据ADC电压计算公式得到GPIO26引脚上的电压
    #print("ADC0 voltage = {0:.3f}V \r\n".format(reading))
    print(33)
    #mqttClient.publish("coolcall", "234", qos = 0)
    mqttClient.publish("homeassistant/sensor/office_temp_adc2_source/config", '{ "unique_id": "office_temp_adc2_source", "device_class": "humidity", "name": "office_temp_adc2_source", "state_topic": "homeassistant/sensor/office_temp_adc2_source/state", "unit_of_measurement": "", "value_template": "{{ value_json.text }}" }')
    mqttClient.publish("homeassistant/sensor/office_temp_adc2/config", '{ "unique_id": "office_temp_adc2", "device_class": "humidity", "name": "office_temp_adc2", "state_topic": "homeassistant/sensor/office_temp_adc2/state", "unit_of_measurement": "%", "value_template": "{{ value_json.text }}" }')
    #mqttClient.publish("coolcall", '{ "unique_id": "HA-ESP32-CGQ-TEMP", "device_class": "humidity", "name": "湿度传感器", "state_topic": "homeassistant/sensor/office_temp_adc2/state", "unit_of_measurement": "%", "value_template": "43.70" }', qos = 0)

def sendTem():
    ADC2= ADC(Pin(28))
    reading = round(ADC2.read_u16()*3.3/65535, 4)
    percent = 0.000
    if reading > 2.25:
        percent = 0.000
    elif reading < 1.000:
        percent = 100.000
    else:
        percent = round((2.25 - reading) * 80, 3)
	#读取ADC通道0的数值
	#并根据ADC电压计算公式得到GPIO26引脚上的电压
    print("ADC0 voltage = {0:.3f}V \r\n".format(percent))
    mqttClient.publish("homeassistant/sensor/office_temp_adc2/state", '{ "text": ' + str(percent) + ' }')
    mqttClient.publish("homeassistant/sensor/office_temp_adc2_source/state", '{ "text": ' + str(reading) + ' }')


checkTem()
time.sleep(2)
while True:
    mqttClient.publish("homeassistant/switch/irrigation_1999/config",'{"unique_id": "irrigation_1999", "name": "irrigation_1999", "command_topic": "homeassistant/switch/irrigation_1999/set", "state_topic": "homeassistant/switch/irrigation_1999/state"}')
    mqttClient.subscribe("homeassistant/switch/irrigation_1999/set")
    sendTem() 
    time.sleep(6)
    #mqttClient.publish("coolcall", "234", qos = 0)
    # mqttClient.wait_msg()






