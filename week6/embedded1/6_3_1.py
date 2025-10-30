import RPi.GPIO as GPIO
import time

# 왼쪽 모터 핀
PWMA = 18
AIN1 = 22
AIN2 = 27

# 오른쪽 모터 핀
PWMB = 23
BIN1 = 25
BIN2 = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 왼쪽 모터 설정
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)

# 오른쪽 모터 설정
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# PWM 객체 생성 (주파수 500Hz)
L_Motor = GPIO.PWM(PWMA, 500)
R_Motor = GPIO.PWM(PWMB, 500)

# PWM 시작 (듀티 사이클 0 = 정지)
L_Motor.start(0)
R_Motor.start(0)

try:
    while True:
        # --- 정방향 50% ---
        GPIO.output(AIN1, 1)  # L: 정방향
        GPIO.output(AIN2, 0)
        GPIO.output(BIN1, 1)  # R: 정방향
        GPIO.output(BIN2, 0)
        L_Motor.ChangeDutyCycle(50)  # L: 속도 50%
        R_Motor.ChangeDutyCycle(50)  # R: 속도 50%
        time.sleep(1.0)

        # --- 정지 (Coast) ---
        L_Motor.ChangeDutyCycle(0)  # L: 속도 0%
        R_Motor.ChangeDutyCycle(0)  # R: 속도 0%
        time.sleep(1.0)

except KeyboardInterrupt:
    pass

L_Motor.stop()
R_Motor.stop()
GPIO.cleanup()