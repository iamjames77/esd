import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
LASER_PIN = 18  # 송신 레이저 핀 번호
BIT_DURATION = 0.02 # 비트 전송 간격 (초)

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_PIN, GPIO.OUT)

def send_bit(bits):
    for bit in bits:
        if bit == '1':
            GPIO.output(LASER_PIN, GPIO.HIGH)  # 레이저 ON
        else:
            GPIO.output(LASER_PIN, GPIO.LOW)  # 레이저 OFF
        time.sleep(BIT_DURATION)
    GPIO.output(LASER_PIN, GPIO.LOW)

def send_protocol(protocol):
    if protocol == 'msg':
        send_bit('111110')

def send_msg_size(msg_size):
    msg_size_bit = f'{msg_size:04b}'
    send_bit(msg_size_bit)
    print(msg_size_bit)

def send_message(message):
    for char in message:
        binary_representation = f'{ord(char):08b}'  # 각 문자를 8비트 이진수로 변환
        send_bit(binary_representation)

try:
    while True:
        message = input("Enter message to send: ")
        #프로토콜 전송
        send_protocol('msg')
        msg_size = len(message)
        #메시지의 크가 255를 초과하는 경우 나눠서 전송
        byte_sent = 0
        while byte_sent < msg_size:
            msg_chunk_size = 15 if byte_sent + 15 < msg_size else msg_size - byte_sent
            send_msg_size(msg_chunk_size)
            print(message[byte_sent:byte_sent + msg_chunk_size])
            send_message(message[byte_sent:byte_sent + msg_chunk_size])
            byte_sent += msg_chunk_size
        print(f"Message sent at {time.time()}, TRANSMISSION_SPEED: {BIT_DURATION}")
except KeyboardInterrupt:
    print("Transmitter stopped.")
finally:
    GPIO.cleanup()