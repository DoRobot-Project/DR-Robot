
import pyarrow as pa
from dora import Node

node = Node()

if __name__ == "__main__":

    for event in node:
        if event["type"] == "INPUT":
            if event["id"] == "image_top":
                image = event["value"].to_pylist()

                # 转换为json格式

                #通过pa Arrow发送
                node.send_output("message", pa.Arrow())
            pass
        elif event["type"] == "STOP":
            break
    
