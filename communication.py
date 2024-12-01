import threading
import send
import receive

TRANSMISSION_SPEED = 0.02

def sender_thread():
    try:
        while True:
            user_input = input("Enter a message to send: ")
            send.send_message(user_input, TRANSMISSION_SPEED)
    except KeyboardInterrupt:
        print("Sender stopped.")
    finally:
        send.cleanup()

def receiver_thread():
    try:
        while True:
            received = receive.receive_message(TRANSMISSION_SPEED)
            print(f"Received: {received}")
    except KeyboardInterrupt:
        print("Receiver stopped.")
    finally:
        receive.cleanup()

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