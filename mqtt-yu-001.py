# test_MQTT_Sub.py - IoT 訊息指令接收測試
config = {"wifi": {"Sunny_Xiaomi":"f28203416f",
                          "YunLo":"f28203416f",
                   "Home_CCS&Lou": "f28203416f"},
          "mqtt": {'server'   : 'fax6.ynhn.com',
                   'port'     :  18883,
                   'user'     : 'lou',
                   'password' : 'f28203416f',
                   'topic'    : 'makerbase/color_sorting/'}}
# -------------------------
# ================ 除非你手癢, 不然以下可以不用任何修改 =========================

def run_iot():
    global run_status, led_status
    mqtt.subscribe(config['mqtt']['topic']+'#')   # 連線後, 訂閱該主題內的所有資料 
    while not mqtt.is_stop:
        mqtt.check()
        time.sleep_ms(100)

# 訂閱者: 每秒檢查是否有新發佈的資料, 有則接收
def receive(topic, msg):
    topic = bytes2str(topic).strip()
    msg = bytes2str(msg)
    print("Received <== {} : {}".format(topic, msg))

if __name__ == '__main__':
    import utime as time
    from My_Wifi     import myWifi
    from My_NetMQTT  import myMQTT, bytes2str

    mqtt = myMQTT() 
    wifi = myWifi()
    mqtt.on_message = receive

    if wifi.connect2(config['wifi']):
#       if mqtt.connect():
        if mqtt.connect(config['mqtt']['server'],
                   user=config['mqtt']['user'],
               password=config['mqtt']['password'],
                   port=config['mqtt']['port']):
#         if mqtt.connect('mqttgo.io'):
            print('ok.....')
            print('----')
            run_iot()
            
            
        mqtt.disconnect()
        wifi.disconnect()