import zmq
import threading
import pyarrow as pa
from dora import Node
import json
import base64


# IPC Address
ipc_address = "ipc:///tmp/dora-zeromq"

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind(ipc_address)

running_server = True


def recv_server():
    while running_server:
        try:
            # 接收 multipart 消息
            message_parts = socket.recv_multipart(flags=0)
            if message_parts:
                # 假设接收到的消息是简单的字符串
                message = b'|'.join(message_parts).decode('utf-8')
                print("Received:", message)
        except Exception as e:
            print("recv error:", e)
            break



if __name__ == "__main__":
    # Start server
    server_thread = threading.Thread(target=recv_server)
    server_thread.start()

    node = Node()

    for event in node:
        if event["type"] == "INPUT":
            event_id = event["id"]
            buffer_bytes = event["value"].to_numpy().tobytes()
            
            # 将 buffer 转为 bytes 并进行 base64 编码
            # encoded_buffer = base64.b64encode(buffer_bytes).decode('utf-8')  # 编码为 base64 字符串

            # data = {
            #     "event_id": event_id,
            #     "buffer": encoded_buffer  # 注意：如果 buffer 是二进制数据（bytes），不能直接放入 JSON，需要先进行编码（如 base64）
            # }
            
            # 处理接收到的数据
            print(f"Send event: {event_id}")
            print(f"Buffer size: {len(buffer_bytes)} bytes")

            try:
                socket.send_multipart([
                    event_id.encode('utf-8'),
                    buffer_bytes
                ], flags=zmq.NOBLOCK)
            except zmq.Again:
                print("Socket would block, skipping send this frame...")
            
        elif event["type"] == "STOP":
            break
    
    # Close server 
    running_server = False
    server_thread.join()

    # Close zmq
    socket.close()
    context.term()



