import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
RECEIVER_PIN = 17  # 수신 레이저 센서 핀 번호
BIT_DURATION = 0.02  # 비트 전송 간격 (송신기와 동일)

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(RECEIVER_PIN, GPIO.IN)

def receive_bits(bit_count):
    """
    지정된 수의 비트를 수신하고 문자열로 반환
    """
    bits = ''
    for _ in range(bit_count):
        bit = '1' if GPIO.input(RECEIVER_PIN) == GPIO.HIGH else '0'
        bits += bit
        time.sleep(BIT_DURATION)
    return bits

def receive_protocol():
    """
    프로토콜 시작을 감지
    """
    while True:
        bits = receive_bits(6)  # 프로토콜 시작 비트(6비트) 수신
        if bits == '111111':
            print("Protocol detected: msg")
            return

def receive_message_size():
    """
    메시지 크기(16비트) 수신
    """
    size_bits = receive_bits(16)  # 메시지 크기는 16비트
    message_size = int(size_bits, 2)  # 이진수를 정수로 변환
    print(f"Message size received: {message_size} bytes")
    return message_size

def receive_message(message_size):
    """
    메시지 내용 수신 (크기 기반)
    """
    message_bits = receive_bits(message_size * 8)  # 메시지 크기(바이트) * 8비트
    # 8비트씩 잘라 아스키 문자로 변환
    message = ''.join(
        chr(int(message_bits[i:i+8], 2))
        for i in range(0, len(message_bits), 8)
    )
    return message

try:
    while True:
        print("Waiting for protocol...")
        
        # 1. 프로토콜 데이터 수신
        receive_protocol()
        
        # 2. 메시지 크기 수신
        message_size = receive_message_size()
        
        # 3. 메시지 수신
        received_message = receive_message(message_size)
        
        print(f"Received message: {received_message}")
except KeyboardInterrupt:
    print("Receiver stopped.")
finally:
    GPIO.cleanup()