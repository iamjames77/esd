import threading
import time
import crc
import RPi.GPIO as GPIO

# GPIO 핀 설정
LASER_PIN = 18  # 송신 레이저 핀 번호
RECEIVER_PIN = 17  # 수신 레이저 센서 핀 번호
BIT_DURATION = 0.02 # 비트 전송 간격 (초)

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_PIN, GPIO.OUT)
GPIO.setup(RECEIVER_PIN, GPIO.IN)

polynomial = 0b1011
crc_bits = 3

send_list = []
list_pointer = 0

timeout = 5

def compute_CRC(data, polynomial, crc_bits):
    data += '0' * crc_bits

    poly_bits = bin(polynomial)[2:]
    poly_len = len(poly_bits)

    data_bits = list(data)
    for i in range(len(data_bits) - crc_bits):
        if data_bits[i] == '1':  # 현재 비트가 1이면 나눗셈 수행
            for j in range(poly_len):
                data_bits[i + j] = str(int(data_bits[i + j]) ^ int(poly_bits[j]))  # XOR 연산

    # 나머지 (CRC 값) 반환
    crc = ''.join(data_bits[-crc_bits:])
    return crc

def send_bit(bits):
    for bit in bits:
        if bit == '1':
            GPIO.output(LASER_PIN, GPIO.HIGH)  # 레이저 ON
        else:
            GPIO.output(LASER_PIN, GPIO.LOW)  # 레이저 OFF
        time.sleep(BIT_DURATION)
    GPIO.output(LASER_PIN, GPIO.LOW)

def send_protocol(protocol):
    if protocol == 'MSG':
        send_bit('111110')
    elif protocol == 'HANDSHAKE':
        send_bit('110111')
    elif protocol == 'HANDSHAKE REPLY':
        send_bit('110110')

def send_msg_size(msg_size):
    msg_size_bit = f'{msg_size:04b}'
    send_bit(msg_size_bit)
    

def send_msg_index(index):
    msg_index = f'{index:06b}'
    send_bit(msg_index)


def send_message(message):
    Total_message = ''
    for char in message:
        binary_representation = f'{ord(char):08b}'  # 각 문자를 8비트 이진수로 변환
        send_bit(binary_representation)
        Total_message += binary_representation
    return Total_message

def receive_bit(bit_count):
    received_bit = ''
    for i in range(bit_count):
        received_bit += '0' if GPIO.input(RECEIVER_PIN) == GPIO.HIGH else '1'
        time.sleep(BIT_DURATION)
    return received_bit

def receive_protocol(timeout):
    start_time = time.time()
    while True:
        current_state = 0 if GPIO.input(RECEIVER_PIN) == GPIO.HIGH else 1
        if current_state:
            time.sleep(BIT_DURATION)
            received_protocol = receive_bit(5)
            print(received_protocol)
            if (received_protocol == '11110'):
                return 'MSG RECEIVE'
            elif (received_protocol == '10111'):
                return 'HANDSHAKE'
            elif (received_protocol == '10110'):
                return 'HANDSHAKE REPLY'
        time.sleep(BIT_DURATION)

        if (time.time() - start_time >= timeout):
            return

def receive_msg_size():
    msg_size_bit = receive_bit(4)
    msg_size = int(msg_size_bit, 2)
    print(f'Message Size: {msg_size}')
    return msg_size


def receive_message(msg_size):
    msg_bit = receive_bit(msg_size * 8)
    crc_bit = receive_bit(crc_bits)
    if(compute_CRC(msg_bit, polynomial, crc_bits) == crc_bit):
        # 8비트씩 읽어 아스키 문자로 변환
        message = ''.join(
            chr(int(msg_bit[i:i+8], 2))
            for i in range(0, len(msg_bit), 8)
        )
        return message
    else:
        print('error')

def sender_thread():
    try:
        while True:
            message = input("Enter message to send: ")
            #프로토콜 전송
            msg_size = len(message)
            msg_chunk = msg_size // 15
            #메시지의 크기가 15를 초과하는 경우 나눠서 전송
            fail_count = 0
            while True:
                send_protocol('HANDSHAKE')
                send_msg_size(msg_chunk)
                received_protocol = receive_protocol(5)
                if (received_protocol == 'HANDSHAKE REPLY'):
                    received_msg_size = receive_msg_size()
                    if(msg_chunk == received_msg_size):
                        break
                fail_count += 1
                print(f'fail_count {fail_count}/10')
                if(fail_count == 10):
                    break
            if (fail_count == 10):
                print("connection error")
                continue
            byte_sent = 0
            global list_pointer
            while byte_sent < msg_size:
                msg_chunk_size = 15 if byte_sent + 15 < msg_size else msg_size - byte_sent
                send_list.append([msg_chunk_size, list_pointer, message[byte_sent:byte_sent + msg_chunk_size]])
                laser(list_pointer)
                list_pointer += 1
                byte_sent += msg_chunk_size
    except KeyboardInterrupt:
        print("Transmitter stopped.")
    finally:
        GPIO.cleanup()

def receiver_thread():
    try:
        while True:
            while (received_protocol = receive_protocol(float('inf'))) == 'HANDSHAKE:
                received_msg_size = receive_msg_size()
                send_protocol('HANDSHAKE REPLY')
                send_msg_size(received_msg_size)
            if(received_protocol == 'MSG RECEIVE'):
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

def laser(index):
    top_send_element = send_list[index]
    send_msg_size(top_send_element[0])
    send_msg_index(top_send_element[1])
    Total_message = send_message(top_send_element[2])
    crc = compute_CRC(Total_message, polynomial, crc_bits)
    send_bit(crc)
    print(f"Message sent at {time.time()}, TRANSMISSION_SPEED: {BIT_DURATION}")


if __name__ == "__main__":
    try:
        # 송신 및 수신을 위한 쓰레드 생성
        sender = threading.Thread(target=sender_thread, daemon=True)
        receiver = threading.Thread(target=receiver_thread, daemon=True)

        # 쓰레드 시작
        sender.start()
        receiver.start()
        
        # 메인 쓰레드 대기
        sender.join()
        receiver.join()
    except KeyboardInterrupt:
        print("Communication stopped.")
    finally:
        GPIO.cleanup()