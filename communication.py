import threading
import send
import receive
import time

BIT_DURATION = 0.02

def sender_thread():
    try:
        while True:
            message = input("Enter message to send: ")
            #프로토콜 전송
            send.send_protocol('msg')
            msg_size = len(message)
            #메시지의 크가 255를 초과하는 경우 나눠서 전송
            byte_sent = 0
            while byte_sent < msg_size:
                msg_chunk_size = 15 if byte_sent + 15 < msg_size else msg_size - byte_sent
                send.send_msg_size(msg_chunk_size)
                print(message[byte_sent:byte_sent + msg_chunk_size])
                send.send_message(message[byte_sent:byte_sent + msg_chunk_size])
                byte_sent += msg_chunk_size
            print(f"Message sent at {time.time()}, TRANSMISSION_SPEED: {BIT_DURATION}")
    except KeyboardInterrupt:
        print("Transmitter stopped.")
    finally:
        send.GPIO.cleanup()

def receiver_thread():
    try:
        while True:
            receive.receive_protocol()
            received_message = ''
            while True:
                msg_size = receive.receive_msg_size()
                if (msg_size == 0):
                    break
                received_message += receive.receive_message(msg_size)     
            print(f"Received message: {received_message}, Time: {time.time()}, Transmission Speed: {BIT_DURATION}")
    except KeyboardInterrupt:
        print("Receiver stopped.")
    finally:
        receive.GPIO.cleanup()

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