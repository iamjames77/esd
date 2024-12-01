import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
LASER_PIN = 18  # 송신 레이저 핀 번호
BIT_DURATION = 0.1  # 비트 전송 간격 (초)

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_PIN, GPIO.OUT)

def send_message(message):
    for char in message:
        binary_representation = f'{ord(char):08b}'  # 각 문자를 8비트 이진수로 변환
        for bit in binary_representation:
            if bit == '1':
                GPIO.output(LASER_PIN, GPIO.HIGH)  # 레이저 ON
            else:
                GPIO.output(LASER_PIN, GPIO.LOW)  # 레이저 OFF
            time.sleep(BIT_DURATION)
        # 문자 간 구분을 위한 짧은 레이저 OFF
        GPIO.output(LASER_PIN, GPIO.LOW)
        time.sleep(BIT_DURATION * 2)

try:
    while True:
        message = input("Enter message to send: ")
        send_message(message)
        print("Message sent.")
except KeyboardInterrupt:
    print("Transmitter stopped.")
finally:
    GPIO.cleanup()