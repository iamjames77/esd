import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
RECEIVER_PIN = 18  # 수신할 레이저 센서 핀 번호
GPIO.setmode(GPIO.BCM)
GPIO.setup(RECEIVER_PIN, GPIO.IN)

# 전송 속도 및 임계값
TRANSMISSION_SPEED = 0.05  # 송신 시간 간격과 동일하게 설정
THRESHOLD_DURATION = TRANSMISSION_SPEED / 2

def receive_message():
    binary_message = ''
    last_time = time.time()

    print("Waiting for message...")
    while True:
        current_state = GPIO.input(RECEIVER_PIN)
        current_time = time.time()

        # 신호 감지
        if current_state == GPIO.HIGH:
            duration = current_time - last_time

            if duration >= THRESHOLD_DURATION:  # 유효한 신호로 간주
                binary_message += '1'
            else:
                binary_message += '0'

            last_time = current_time

        # 일정 시간 동안 신호 없음 -> 종료
        if current_time - last_time > TRANSMISSION_SPEED * 10:
            break

    # 8비트씩 아스키 문자로 변환
    try:
        message = ''.join(
            chr(int(binary_message[i:i+8], 2))
            for i in range(0, len(binary_message), 8)
        )
        return message
    except ValueError:
        return "Invalid data"

try:
    while True:
        received = receive_message()
        if received:
            print(f"Received: {received}")
except KeyboardInterrupt:
    print("Reception stopped.")
finally:
    GPIO.cleanup()