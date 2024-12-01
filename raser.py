import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
LASER_PIN = 18  # 사용할 GPIO 핀 번호 (예: GPIO 18)

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LASER_PIN, GPIO.HIGH)  # 레이저 켜기
        print("Laser ON")
        time.sleep(0.05)
        
        GPIO.output(LASER_PIN, GPIO.LOW)  # 레이저 끄기
        print("Laser OFF")
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Program stopped")
    GPIO.cleanup()  # GPIO 설정 정리