import zmq
import threading
import pyarrow as pa
from dora import Node


# IPC Address
ipc_address = "ipc:///tmp/dora-zeromq"


node = Node()
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind(ipc_address)
running_server = True


def recv_server():
    while running_server:
        try:
            message = socket.recv_string()
            if message:
                print("recieve:", message)
                node.send_output("message", pa.array(message))
        except Exception as e:
            print("recv error:", e)
            break



if __name__ == "__main__":
    # Start server
    server_thread = threading.Thread(target=recv_server)
    server_thread.start()

    for event in node:
        if event["type"] == "INPUT":
            if event["id"] == "message":
                message = event["value"].to_pylist()
                socket.send_string(message.decode())
            pass
        elif event["type"] == "STOP":
            break
    
    # Close server 
    running_server = False
    server_thread.join()

    # Close zmq
    socket.close()
    context.term()
