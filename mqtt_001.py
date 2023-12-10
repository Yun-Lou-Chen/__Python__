# Filename: pico_w_mqtt.py
import network
from umqtt.simple import MQTTClient
import time
from machine import Pin
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("Home_CCS&Lou","f28203416f") 
# station.connect("使用者使用的WiFi名稱","使用者使用的WiFi密碼") 
time.sleep(8)
# led_onBoard = machine.Pin('LED',machine.Pin.OUT)
led_onBoard = machine.Pin(25,machine.Pin.OUT)   # 內建LED 25 or 'LED'
led_onBoard.value(0)
led_external = Pin(16, Pin.OUT)
led_external.value(0)

led_17 = Pin(17, Pin.OUT)
led_17.value(0)

BrokerAddr = '192.168.71.121'   # 指定的MQTT伺服器: test.mosquitto.org
# 其他的MQTT伺服器：broker.hivemq.com, mqtt.p2hp.com等
mqttPort = 18883  # 1883為指定的MQTT伺服器連接埠號
ClientID = "Pico_W"  # 設定PICO_W為Pico W開發板裝置ID
Topic = "LED"  # 設定MQTT主題為LED

def sub_callback(topic, msg):
    topic = str(topic,'utf-8')
    msg = str(msg,'utf-8')
    command= msg.strip()
    print((topic, command))  # 顯示主題和命令消息
    if command == "1":  # "開燈"命令消息
        led_onBoard.value(1)
        led_external.value(1)
        led_17.on()
    if command == "0":  # "關燈"命令消息
        led_onBoard.value(0)
        led_external.value(0)
        led_17.off()
# 將Pico W開發板連接到指定的MQTT伺服器
mqttClient = MQTTClient(ClientID, BrokerAddr, mqttPort, 'lou', 'f28203416f', keepalive = 300)
mqttClient.set_callback(sub_callback)
mqttClient.connect()
mqttClient.publish("MQTT_Test", "Start", qos = 0)
mqttClient.subscribe(Topic, qos = 0)  # Pico W 開發板訂閱主題
print("Ok")

while True:
    mqttClient.wait_msg()
    time.sleep(1)
