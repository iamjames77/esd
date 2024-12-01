import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
RECEIVER_PIN = 18  # 수신할 레이저 센서 핀 번호
GPIO.setmode(GPIO.BCM)
GPIO.setup(RECEIVER_PIN, GPIO.IN)

# 비트 전송 간격과 임계치 (수신 속도와 노이즈 필터링 조정)
TRANSMISSION_SPEED = 0.02
THRESHOLD_DURATION = TRANSMISSION_SPEED / 2

def receive_message():
    binary_message = ''
    last_time = time.time()
    
    print("Waiting for message...")
    while True:
        current_state = GPIO.input(RECEIVER_PIN)
        current_time = time.time()
        
        # 신호가 꺼진 경우
        if not current_state:
            duration = current_time - last_time
            if duration >= TRANSMISSION_SPEED * 10:  # 종료 신호
                break
            elif duration >= THRESHOLD_DURATION:
                binary_message += '1' if duration >= TRANSMISSION_SPEED else '0'
                last_time = current_time
    
    # 아스키 코드로 변환
    message = ''.join(
        chr(int(binary_message[i:i+8], 2))
        for i in range(0, len(binary_message), 8)
    )
    return message

try:
    while True:
        received = receive_message()
        print(f"Received: {received}")
except KeyboardInterrupt:
    print("Reception stopped.")
finally:
    GPIO.cleanup()