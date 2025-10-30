import RPi.GPIO as GPIO
import time

BUZZER = 12
SW_PINS = [5, 6, 13, 19]  # 스위치 4개 핀
NUM_SWITCHES = len(SW_PINS)

# 4개 스위치에 할당할 음 (도, 미, 솔, 높은 도)
NOTES = [262, 330, 392, 523]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 부저 설정
GPIO.setup(BUZZER, GPIO.OUT)

# 스위치 4개 설정
for pin in SW_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

p = GPIO.PWM(BUZZER, NOTES[0])  # 첫번째 음(도)으로 초기화
p.start(0)  # 듀티 사이클 0 (무음)으로 시작

current_note_index = -1  # 현재 눌린 스위치 없음 (-1)

try:
    while True:
        new_values = [GPIO.input(pin) for pin in SW_PINS]

        pressed_index = -1

        # 4개 스위치 중 하나라도 눌렸는지 확인
        if 1 in new_values:
            pressed_index = new_values.index(1)  # 몇 번째 스위치가 눌렸는지 확인

        if pressed_index != -1:  # 어떤 스위치든 눌려있다면
            # 이전에 눌린 스위치와 다르다면 (음 변경)
            if current_note_index != pressed_index:
                p.ChangeFrequency(NOTES[pressed_index])
                p.ChangeDutyCycle(50)  # 소리 켜기
                current_note_index = pressed_index

        else:  # 아무 스위치도 눌려있지 않다면
            # 이전에 소리가 나고 있었다면
            if current_note_index != -1:
                p.ChangeDutyCycle(0)  # 소리 끄기
                current_note_index = -1

        time.sleep(0.02)  # 0.02초마다 상태 확인

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()