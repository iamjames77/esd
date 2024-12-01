import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
RECEIVER_PIN = 17  # 수신 레이저 센서 핀 번호
BIT_DURATION = 0.02  # 비트 전송 간격 (송신기와 동일)
THRESHOLD_DURATION = BIT_DURATION

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(RECEIVER_PIN, GPIO.IN)

def receive_message():
    binary_message = ''
    last_time = time.time()
    connect = False
    print("Waiting for message...")
    while True:
        current_state = 0 if GPIO.input(RECEIVER_PIN) == GPIO.HIGH else 1
        current_time = time.time()
        
        # 신호가 꺼진 경우만 관심
        if connect:
            binary_message += '1' if current_state else '0'
            if(current_time - last_time > 10 * THRESHOLD_DURATION):
                print(binary_message)
                break
            if (current_state == 1):
                last_time = current_time

        if(current_state and connect == False):
            print("connected")
            connect = True
            last_time = current_time
        time.sleep(BIT_DURATION)

    # 8비트씩 읽어 아스키 문자로 변환
    message = ''.join(
        chr(int(binary_message[i:i+8], 2))
        for i in range(0, len(binary_message), 8)
    )
    return message

try:
    while True:
        received_message = receive_message()
        print(f"Received message: {received_message}, Time: {time.time()}, Transmission Speed: {BIT_DURATION}")
except KeyboardInterrupt:
    print("Receiver stopped.")
finally:
    GPIO.cleanup()