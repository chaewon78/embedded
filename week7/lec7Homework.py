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
    print(f"Starting... (Port: {SERIAL_PORT})")

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("Connecting...")

        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()

                if not data:
                    continue

                print(f"Send Data: {data}")

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
                    print("exit...")
                    break
                else:
                    print("Stop")
                    stop()

            time.sleep(0.01)

    except serial.SerialException as e:
        print(f"Serial port error: {e}")


    except KeyboardInterrupt:
        print("Program exit")

    finally:
        print("GPIO exit")
        stop()
        GPIO.cleanup()
        if 'ser' in locals() and ser.is_open:
            ser.close()


if __name__ == "__main__":
    main()

