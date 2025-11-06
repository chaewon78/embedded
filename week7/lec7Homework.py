import serial
import RPi.GPIO as GPIO
import time

PWMA = 18
AIN1 = 22
AIN2 = 27
PWMB = 23
BIN1 = 25
BIN2 = 24

SPEED = 80
TURN_SPEED = 70

SERIAL_PORT = "/dev/ttyS0"
BAUD_RATE = 9600

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

motor_pins = [PWMA, AIN1, AIN2, PWMB, BIN1, BIN2]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 500)
R_Motor = GPIO.PWM(PWMB, 500)
L_Motor.start(0)
R_Motor.start(0)


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
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 1)
    GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(speed)
    R_Motor.ChangeDutyCycle(speed)


def turn_right(speed):
    GPIO.output(AIN1, 1)
    GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(speed)
    R_Motor.ChangeDutyCycle(speed)


def stop():
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)


def main():
    print(f"블루투스 시리얼 제어 시작... (포트: {SERIAL_PORT})")

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("휴대폰 앱에서 연결을 기다립니다...")

        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()

                if not data:
                    continue

                print(f"수신된 데이터: {data}")

                if data == "b7":
                    print("Go Forward")
                    go_forward(SPEED)
                elif data == "b5":
                    print("Go Backward")
                    go_backward(SPEED)
                elif data == "b4":
                    print("Turn Left")
                    turn_left(TURN_SPEED)
                elif data == "b6":
                    print("Turn Right")
                    turn_right(TURN_SPEED)
                elif data == "b0":
                    print("프로그램 종료 신호 수신...")
                    break
                else:
                    print("Stop")
                    stop()

            time.sleep(0.01)

    except serial.SerialException as e:
        print(f"시리얼 포트 오류: {e}")
        print("라즈베리파이 설정(raspi-config)에서 시리얼 포트가 활성화되었는지 확인하세요.")

    except KeyboardInterrupt:
        print("사용자에 의해 프로그램이 중지되었습니다.")

    finally:
        print("GPIO 정리 및 종료.")
        stop()
        GPIO.cleanup()
        if 'ser' in locals() and ser.is_open:
            ser.close()


if __name__ == "__main__":
    main()
