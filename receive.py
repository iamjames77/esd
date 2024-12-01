import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
RECEIVER_PIN = 17  # 수신 레이저 센서 핀 번호
BIT_DURATION = 0.1  # 비트 전송 간격 (송신기와 동일)
THRESHOLD_DURATION = BIT_DURATION / 2  # 신호 감지 임계값

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(RECEIVER_PIN, GPIO.IN)

def receive_message():
    binary_message = ''
    last_time = time.time()
    
    print("Waiting for message...")
    while True:
        current_state = GPIO.input(RECEIVER_PIN)
        current_time = time.time()
        
        # 신호가 꺼진 경우만 관심
        if not current_state:
            duration = current_time - last_time
            if duration >= BIT_DURATION * 10:  # 종료 신호
                break
            elif duration >= THRESHOLD_DURATION:
                binary_message += '1' if duration >= BIT_DURATION else '0'
                last_time = current_time

    # 8비트씩 읽어 아스키 문자로 변환
    message = ''.join(
        chr(int(binary_message[i:i+8], 2))
        for i in range(0, len(binary_message), 8)
    )
    return message

try:
    while True:
        received_message = receive_message()
        print(f"Received message: {received_message}")
except KeyboardInterrupt:
    print("Receiver stopped.")
finally:
    GPIO.cleanup()