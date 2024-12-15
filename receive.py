import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
RECEIVER_PIN = 17  # 수신 레이저 센서 핀 번호
BIT_DURATION = 0.02  # 비트 전송 간격 (송신기와 동일)
THRESHOLD_DURATION = BIT_DURATION

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(RECEIVER_PIN, GPIO.IN)

def receive_bit(bit_count):
    received_bit = ''
    for i in range(bit_count):
        received_bit += '0' if GPIO.input(RECEIVER_PIN) == GPIO.HIGH else '1'
        time.sleep(BIT_DURATION)
    return received_bit

def receive_protocol():
    print('receiving protocol...')
    while True:
        current_state = 0 if GPIO.input(RECEIVER_PIN) == GPIO.HIGH else 1
        if current_state:
            time.sleep(BIT_DURATION)
            received_protocol = receive_bit(5)
            print(received_protocol)
            if (received_protocol == '11110'):
                print("connected")
                return
        time.sleep(BIT_DURATION)

def receive_msg_size():
    msg_size_bit = receive_bit(4)
    msg_size = int(msg_size_bit, 2)
    print(f'Message Size: {msg_size}')
    return msg_size


def receive_message(msg_size):
    msg_bit = receive_bit(msg_size * 8)

    # 8비트씩 읽어 아스키 문자로 변환
    message = ''.join(
        chr(int(msg_bit[i:i+8], 2))
        for i in range(0, len(msg_bit), 8)
    )
    print(message)
    return message

try:
    while True:
        receive_protocol()
        received_message = ''
        while True:
            msg_size = receive_msg_size()
            if (msg_size == 0):
                break
            received_message += receive_message(msg_size)     
        print(f"Received message: {received_message}, Time: {time.time()}, Transmission Speed: {BIT_DURATION}")
except KeyboardInterrupt:
    print("Receiver stopped.")
finally:
    GPIO.cleanup()