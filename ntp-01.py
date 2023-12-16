config = {"Home_CCS&Lou":"f28203416f", "YunLo": "f28203416f"}

from My_Wifi import myWifi
# from mpython import *
import ntptime
import time


wifi = myWifi()
if wifi.connect2(config):
    print("同步前本地时间：%s" %str(time.localtime()))
    ntptime.hoet = 'time.google.com'
    ntptime.NTP_DELTA = 3155644800

    ntptime.settime()
    print("同步后本地时间：%s" %str(time.localtime()))    
    print('===> Run your script HERE !!! <===')
    wifi.disconnect()
    
 
 
 
#  
# if wifi.connect2(config):
#     while True:
#         print('===> Running ...')
#         while not wifi.is_connected():
#             print('\n!!! ------ 已偵測到 Wifi 斷線, 系統立即嘗試自動重新連線 ------ !!')
#             wifi.reconnect()  # 以上一次連線資訊, 重新自動連線
#             time.sleep_ms(100)
#         time.sleep_ms(1000)
#     wifi.disconnect()    
