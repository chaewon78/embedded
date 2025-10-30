import RPi.GPIO as GPIO
import time

BUZZER = 12
SW1 = 5  # 스위치 1번 핀 (BCM)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

p = GPIO.PWM(BUZZER, 440)
p.start(0)  # 듀티 사이클 0 (무음)으로 시작

note_high = 880
note_low = 660
is_playing = False  # 현재 소리가 나는지 상태 저장

try:
    while True:
        if GPIO.input(SW1) == 1:  # 스위치가 눌렸다면
            if not is_playing:  # 소리가 안 나고 있었다면
                p.ChangeDutyCycle(50)  # 소리 켜기
                is_playing = True

            # 경적 소리 반복
            p.changeFrequency(note_high)
            time.sleep(0.1)
            p.changeFrequency(note_low)
            time.sleep(0.1)

        else:  # 스위치가 떼어졌다면
            if is_playing:  # 소리가 나고 있었다면
                p.ChangeDutyCycle(0)  # 소리 끄기
                is_playing = False

        time.sleep(0.01)  # 0.01초마다 스위치 상태 확인

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()