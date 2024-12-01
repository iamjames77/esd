import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
LASER_PIN = 18  # 송신 레이저 모듈 핀 번호

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_PIN, GPIO.OUT)

# 전송 속도
TRANSMISSION_SPEED = 0.05  # 송신 속도 (수신 측과 동일해야 함)

def send_message(message):
    # 메시지를 이진수로 변환 (ASCII 기준)
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    print(f"Sending: {message}")
    print(f"Binary: {binary_message}")

    # 이진수 데이터를 전송
    for bit in binary_message:
        GPIO.output(LASER_PIN, GPIO.HIGH if bit == '1' else GPIO.LOW)
        time.sleep(TRANSMISSION_SPEED)
    
    # 송신 종료 신호
    GPIO.output(LASER_PIN, GPIO.LOW)
    time.sleep(TRANSMISSION_SPEED * 10)

try:
    while True:
        user_input = input("Enter a message to send: ")
        send_message(user_input)
except KeyboardInterrupt:
    print("Transmission stopped.")
finally:
    GPIO.cleanup()  # GPIO 설정 정리