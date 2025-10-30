import RPi.GPIO as GPIO
import time

BUZZER = 12

# 도, 레, 미, 파, 솔, 라, 시, 높은 도
scale = [262, 294, 330, 349, 392, 440, 494, 523]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

p = GPIO.PWM(BUZZER, 262)  # 262(도)로 초기화

try:
    for freq in scale:
        p.start(50)  # 50% 듀티 사이클로 시작
        p.ChangeFrequency(freq)  # (수정) C가 대문자
        time.sleep(0.5)  # 0.5초간 연주
        p.stop()  # 정지
        time.sleep(0.1)  # 다음 음 전 0.1초 쉼

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()