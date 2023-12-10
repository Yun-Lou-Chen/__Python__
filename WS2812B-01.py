# 
# MicroPython 如此簡單: LED WS2812b (NeoPixel)
# https://yungger.medium.com/micropython-%E5%A6%82%E6%AD%A4%E7%B0%A1%E5%96%AE-led-ws2812b-neopixel-5dca2af92b78
# MyKit_NeoPixel.mpy (1.9up ) https://u.pcloud.link/publink/show?code=XZ6FKoVZIobkT60fhWpHfnDqebEFA0SAkQ5X
# 92b78
# MyKit_NeoPixel.mpy (1.8 down ) https://u.pcloud.link/publink/show?code=XZk7toVZvEVlCj9Y1hy8y01h97j2LV2bT2q7
#

# config 是 JSon 變數 
config = {'pin':4, 'pixels':8, 'bri':5, 'bri_max':254}
# config['pin']     is 14   # GPIO Pin 腳位
# config['pixels']  is 1    # ws2812 燈珠的個數
# config['bri']     is 10   # 預設亮度 (0 ~ 100)
# config['bri_max') is 100  # 最大量 亮度



import utime as time
from MyKit_NeoPixel import myNeoPixel
np = myNeoPixel(config['pin'], config['pixels'], config['bri'])

#------------------------------
# 範例一: 開 / 關 / 閃光燈
# on(): 亮
# off(): 滅
#------------------------------

def test1():
    for _ in range(3):   #  _  沒有變數執行3次 
        np.on() 
        time.sleep_ms(200)
        np.off()
        time.sleep_ms(200)
        
# ----------------------------
#  360色七彩霓虹燈
# on_360(c): c 為 0 ~ 360
# ----------------------------

def test2():
    for c in range(360):
        np.on_360(c)     # 360 色色盤

        

# ----------------------------
# 指定 65535 種 RGB 組合顏色
# on_rgb(): 參數 (r,g,b)
# ----------------------------

def test3():
    for r in range(256):
        np.on_rgb((r, 0, 0),0)     
        np.on_rgb((r, 0, 0),2)     
        np.on_rgb((r, 0, 0),4)     
        np.on_rgb((r, 0, 0),6)     
    for b in range(256):
        np.on_rgb((0, 0, b),2) 

# ------------------------
# 控制指定的單顆燈珠顏色
# pixels: 燈條上的燈珠總數
# on_random(i): 在燈珠順序編號i, 顯示隨機顏色
# 可以將 on_random(i) 改為其他顯示方式, 例如 on(i), on_rgb(i), on_360(i), … 等等
# ------------------------

def test4():
    # 指定燈珠: 單顆燈珠
    for i in range(np.pixels):
        np.on_random(i)
        time.sleep_ms(200)
        np.off(i)
        time.sleep_ms(200)






# for _ in range(1000):
while True:
    test3()