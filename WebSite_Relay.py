# Filename: main.py
# Raspberry Pi Pico W
# 匯入Pico W MicroPython模組
import rp2 # 匯入rp2模組，該模組包含專門用於RP2040的函數和類
import network  # 匯入network模組，用於連接WiFi
import ubinascii # 匯入ubinascii模組，用於將MAC地址轉換為十六進制字串
import machine # 匯入machine模組，用於GPIO控制
import urequests as requests # 匯入urequests模組，用於HTTP請求
import time # 匯入time模組，用於延時
import socket # # 匯入socket模組，用於建立套接字
# 設定國家/地區程式碼以避免發生可能的錯誤
# CN/US/DE/DK/GB/JP(國家或地區程式碼：中國/美國/德國/丹麥/英國/日本)
rp2.country('TW') # 這裡設定Pico W的國家/地區程式碼為中國
wlan = network.WLAN(network.STA_IF) # 建立WLAN連接對象
wlan.active(True) # 啟動WLAN介面

# 查看Pico W開發板無線WiFi的MAC地址
# 獲取MAC地址，並將其轉換為十六進制字串
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('Pico W MAC地址=' + mac)   # 顯示Pico W開發板十六進制MAC地址

# ssid = 'Home_CCS&Lou'    # 設定WiFi名稱 (ssid: service set identifier)
ssid = 'f28203416f'    # 設定WiFi名稱 (ssid: service set identifier)
psw = 'f28203416f'  # 設定WiFi密碼

# ssid = '所使用的WiFi名稱'    # 設定WiFi名稱 (ssid: service set identifier)
# psw = '所使用的WiFi密碼'  # 設定WiFi密碼

wlan.connect(ssid, psw)  # 連接到WiFi網路

timeout = 10   # 設定最長等待連接時間為10秒
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3: # 如果WiFi連接成功或者失敗
        break # 跳出循環
    timeout -= 1
    print('等待連接!')
    time.sleep(1) # 延時1秒

# 定義Pico W板載LED閃亮函數
def onboard_led_blink(blink_numbers):
    onboard_led = machine.Pin('LED', machine.Pin.OUT) # 建立GPIO控制對象
    for i in range(blink_numbers):
        onboard_led.value(1)  # 點亮LED
        # onboard_led.on()  # 另一種點亮LED的方法
        time.sleep(0.5)  
        onboard_led.value(0) # 熄滅LED
        # onboard_led.off() # 另一種熄滅LED的方法
        time.sleep(0.5)

wlan_status = wlan.status() # 獲取當前WiFi連接狀態
onboard_led_blink(wlan_status) # 根據WiFi連接狀態控制LED

# 處理連接錯誤
if wlan_status != 3: # 如果WiFi連接失敗
    raise RuntimeError('WiFi連接失敗!') # 拋出異常
else:
    print('WiFi已連接...')
    status = wlan.ifconfig() # 獲取WiFi介面組態資訊
    print('IP地址=' + status[0]) # 輸出IP地址

# 定義載入HTML頁面函數  
def get_html(html_name):
    with open(html_name, 'r') as file: # 打開HTML檔案
        html = file.read() # 讀取HTML內容
    return html

# 打開HTTP Web伺服器套接字socket
addr = socket.getaddrinfo('192.168.71.137', 80)[0][-1] # 獲取IP地址和連接埠號
s = socket.socket() # 建立socket對象
s.bind(addr) # 繫結socket到IP地址和連接埠號
# 開始監聽連接埠號，最多隻允許1個客戶端連接
s.listen(1)

print('正在監聽', addr)

onboard_led = machine.Pin('LED', machine.Pin.OUT)

# 進入循環，監聽連接
while True:
    try:
        # 接受客戶端連接，獲取連接和地址
        cl, addr = s.accept()
        print('客戶機連接來自', addr)
        # 接收客戶端請求消息
        r = cl.recv(1024)
        r = str(r)
        # 在請求消息中尋找是否有開/關LED的命令
        onboard_led_on = r.find('?onboard_led=1')
        onboard_led_off = r.find('?onboard_led=0')
        print('LED=', onboard_led_on)
        print('LED=', onboard_led_off)
        # 若找到'?onboard_led=1'，則開LED
        if onboard_led_on > -1:
            print('開LED')
            onboard_led.value(1)
        # 若找到'?onboard_led=0'，則關LED
        if onboard_led_off > -1:
            print('關LED')
            onboard_led.value(0)
        # 獲取HTML檔案內容
        response = get_html('index.html')
        # 傳送HTTP響應頭
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        # 傳送HTML檔案內容
        cl.send(response)
        # 關閉客戶端套接字
        cl.close()
    # 若發生OSError錯誤，則關閉客戶端套接字並輸出相關資訊
    except OSError as e:
        cl.close()
        print('關閉連接')
