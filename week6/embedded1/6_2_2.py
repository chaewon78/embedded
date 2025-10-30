import RPi.GPIO as GPIO
import time

BUZZER = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

p = GPIO.PWM(BUZZER, 440)

note_high = 880  # 높은 '라' (A5)
note_low = 660  # 높은 '미' (E5)

try:

    # 높은 음 재생
    p.start(50)  # 50% 듀티 사이클로 시작
    p.ChangeFrequency(note_high)
    time.sleep(0.3)  # 0.3초간 재생

    # 낮은 음 재생
    p.ChangeFrequency(note_low)
    time.sleep(0.3)  # 0.3초간 재생

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()