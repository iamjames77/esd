import threading
import send  # `send.py`를 가져옵니다.
import receive  # `receive.py`를 가져옵니다.

# 송신 쓰레드
def sender_thread():
    try:
        while True:
            user_input = input("Enter a message to send: ")
            send.send_message(user_input)
    except KeyboardInterrupt:
        print("Sender stopped.")
    finally:
        send.GPIO.cleanup()

# 수신 쓰레드
def receiver_thread():
    try:
        while True:
            received = receive.receive_message()
            if received:
                print(f"Received: {received}")
    except KeyboardInterrupt:
        print("Receiver stopped.")
    finally:
        receive.GPIO.cleanup()

if __name__ == "__main__":
    try:
        # 송신 및 수신 쓰레드 생성
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