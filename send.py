import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
LASER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_PIN, GPIO.OUT)

# 비트 전송 간격 (전송 속도 조정)
TRANSMISSION_SPEED = 0.02

def send_message(message, speed=TRANSMISSION_SPEED):
    # 아스키 코드로 변환
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    print(f"Sending: {message}")
    print(f"Binary: {binary_message}")
    
    # 데이터 전송
    for bit in binary_message:
        GPIO.output(LASER_PIN, GPIO.HIGH if bit == '1' else GPIO.LOW)
        time.sleep(speed)
    
    # 데이터 끝 신호 (길게 끌기)
    GPIO.output(LASER_PIN, GPIO.LOW)
    time.sleep(speed * 10)


def cleanup():
    GPIO.cleanup()