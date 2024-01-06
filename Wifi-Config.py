config = {"Home_CCS&Lou":"f28203416f", "yunlou": "f28203416f"}

from My_Wifi import myWifi
# from mpython import *
import ntptime
import utime
cnt = 0

def change_timezone(timezone_offset):
    # 
    # 需要匯入 ntptime utime
    #
    # 從 NTP 伺服器獲取 UTC 時間
    ntptime.settime()
    # UTC 時間
    utc_time = utime.time()
    # 計算時區調整後的時間
    local_time = utc_time + timezone_offset
    # 轉換為本地時間元組
    local_time_tuple = utime.localtime(local_time)
    # 輸出本地時間
#     print("Local Time:", local_time_tuple)


def check_wifi():
    if wifi.connect2(config):
        while True:
            cnt = 0
            print(f'===> Running ...{cnt}')
            while not wifi.is_connected():
                print('\n!!! ------ 已偵測到 Wifi 斷線, 系統立即嘗試自動重新連線 ------ !!')
                wifi.reconnect()  # 以上一次連線資訊, 重新自動連線
                utime.sleep_ms(100)
            utime.sleep_ms(1000)
    else
       print('Wifi 不存在')
    #     wifi.disconnect()


wifi = myWifi()
 
 



# if wifi.connect2(config):
#     print("同步前本地时间：%s" %str(utime.localtime()))
#     change_timezone(7)
#     print("同步后本地时间：%s" %str(utime.localtime()))    
#     print('===> Run your script HERE !!! <===')
# #     wifi.disconnect()
# else:
#     print('\n\nconnect error')
#    
