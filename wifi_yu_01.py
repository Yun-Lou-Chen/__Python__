

from My_Wifi import myWifi
wifi = myWifi()
config = {"YunLou": "f28203416f", "Home_CCS&Lou": "f28203416f"}

print('===> Running ...')

if wifi.connect2(config):
    while True:
        print('===> Running ...')
        while not wifi.is_connected():
            print('\n!!! ------ 已偵測到 Wifi 斷線, 系統立即嘗試自動重新連線 ------ !!')
            wifi.reconnect()  # 以上一次連線資訊, 重新自動連線
            time.sleep_ms(100)
        time.sleep_ms(1000)
    wifi.disconnect()
    
print('2===> Running ...')
    