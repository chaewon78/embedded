import RPi.GPIO as GPIO
import time

# --- 모터 핀 ---
PWMA = 18
AIN1 = 22
AIN2 = 27
PWMB = 23
BIN1 = 25
BIN2 = 24

# --- 스위치 핀 (BCM) ---
SW1_FWD = 5  # 앞
SW2_RIGHT = 6  # 오른쪽
SW3_LEFT = 13  # 왼쪽
SW4_BACK = 19  # 뒤

# --- 설정 ---
SPEED = 80  # 주행 속도 (0~100)
TURN_SPEED = 70  # 회전 속도 (0~100)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# --- 모터 핀 설정 ---
motor_pins = [PWMA, AIN1, AIN2, PWMB, BIN1, BIN2]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# --- 스위치 핀 설정 ---
switch_pins = [SW1_FWD, SW2_RIGHT, SW3_LEFT, SW4_BACK]
for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# --- PWM 객체 생성 및 시작 ---
L_Motor = GPIO.PWM(PWMA, 500)
R_Motor = GPIO.PWM(PWMB, 500)
L_Motor.start(0)
R_Motor.start(0)


# --- 모터 제어 함수 ---
def go_forward(speed):
    GPIO.output(AIN1, 1)
    GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 1)
    GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(speed)
    R_Motor.ChangeDutyCycle(speed)


def go_backward(speed):
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(speed)
    R_Motor.ChangeDutyCycle(speed)


def turn_left(speed):
    # 왼쪽 바퀴 뒤로, 오른쪽 바퀴 앞으로 (제자리 회전)
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 1)
    GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(speed)
    R_Motor.ChangeDutyCycle(speed)


def turn_right(speed):
    # 왼쪽 바퀴 앞으로, 오른쪽 바퀴 뒤로 (제자리 회전)
    GPIO.output(AIN1, 1)
    GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(speed)
    R_Motor.ChangeDutyCycle(speed)


def stop():
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)


print("Task 2: Ready for switch control. (Press Ctrl+C to exit)")

try:
    while True:
        # 스위치 상태 읽기
        fwd_pressed = GPIO.input(SW1_FWD)
        right_pressed = GPIO.input(SW2_RIGHT)
        left_pressed = GPIO.input(SW3_LEFT)
        back_pressed = GPIO.input(SW4_BACK)

        # 우선순위: 전진/후진 > 좌/우 회전
        if fwd_pressed == 1:
            print("SW1: Forward")
            go_forward(SPEED)
        elif back_pressed == 1:
            print("SW4: Backward")
            go_backward(SPEED)
        elif left_pressed == 1:
            print("SW3: Turn Left")
            turn_left(TURN_SPEED)
        elif right_pressed == 1:
            print("SW2: Turn Right")
            turn_right(TURN_SPEED)
        else:
            # 아무것도 안 눌렸으면 정지
            stop()

        time.sleep(0.05)  # 짧은 대기

except KeyboardInterrupt:
    pass

print("Stopping motors and cleaning up GPIO...")
stop()
GPIO.cleanup()