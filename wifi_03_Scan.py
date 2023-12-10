# 具體資訊為：(ssid, bssid, channel, RSSI, security, hidden)
# – ssid：服務集標識，Service Set Identifier 的縮寫，通俗地說，是無線網熱點的名稱
# – bssid：48 個二進制位，6 個位元組，可以理解為訪問點的 MAC 地址
# – channel：通道號
# – RSSI：訊號強度（Received signal strength indicator），正常訊號強度應為 -40dbm ~ -85dbm之間，小於 -90dbm 的訊號則很糟糕，幾乎無法連接
# – security：安全連接方式，包含以下幾種：
# 0 – open
# 1 – WEP
# 2 – WPA-PSK
# 3 – WPA2-PSK
# 4 – WPA/WPA2-PSK
# 
# – 可見還是隱藏：
# 0 – visible
# 1 – hidden
import network
import binascii
 
wlan = network.WLAN(network.STA_IF) 
wlan.active(True) 
access_points = wlan.scan()
 
# 按訊號強弱排序
access_points.sort(key=lambda x:x[3], reverse=True)
 
for ssid, bssid, channel, RSSI, security, hidden in access_points:
    print(ssid, binascii.hexlify(bssid), channel, RSSI, security, hidden)

