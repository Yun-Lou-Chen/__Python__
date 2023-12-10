from machine import Pin, PWM
import utime

# 定义音调频率
tones = {'1': 262, '2': 294, '3': 330, '4': 349, '5': 392, '6': 440, '7': 494, '-': 0}
# 定义小星星旋律
melody = "1155665-4433221-5544332-5544332-1155665-4433221"

# 设置D7（GPIO 13）口为IO输出，然后通过PWM控制无缘蜂鸣器发声
beeper = PWM(Pin(4, Pin.OUT), freq=0, duty=1000)

for tone in melody:
    freq = tones[tone]
    if freq:
        beeper.init(duty=1000, freq=freq)  # 调整PWM的频率，使其发出指定的音调
    else:
        beeper.duty(0)  # 空拍时一样不上电
    # 停顿一下 （四四拍每秒两个音，每个音节中间稍微停顿一下）
    utime.sleep_ms(200)
    beeper.duty(0)  # 设备占空比为0，即不上电
    utime.sleep_ms(50)

beeper.deinit()  # 释放PWM
