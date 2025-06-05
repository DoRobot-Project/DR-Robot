import os
import pyarrow as pa

from dora import Node
from Robotic_Arm.rm_robot_interface import *


def main():

    node = Node()

    arm = RoboticArm(rm_thread_mode_e.RM_TRIPLE_MODE_E)
    ip = os.getenv("ARM_IP", "192.168.1.18")    # 如果未设置，默认使用 "192.168.1.18"
    port = int(os.getenv("ARM_PORT", "8080"))   # 如果未设置，默认使用 8080

    handle = arm.rm_create_robot_arm(ip, port)
    print("机械臂ID：", handle.id)
    software_info = arm.rm_get_arm_software_info()
    if software_info[0] == 0:
        print("\n================== Arm Software Information ==================")
        print("Arm Model: ", software_info[1]['product_version'])
        print("Algorithm Library Version: ", software_info[1]['algorithm_info']['version'])
        print("Control Layer Software Version: ", software_info[1]['ctrl_info']['version'])
        print("Dynamics Version: ", software_info[1]['dynamic_info']['model_version'])
        print("Planning Layer Software Version: ", software_info[1]['plan_info']['version'])
        print("==============================================================\n")
    else:
        print("\nFailed to get arm software information, Error code: ", software_info[0], "\n")

    for _event in node:



if __name__ == "__main__":
    main()
