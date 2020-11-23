from jemble import JemBleUart
from network import Bluetooth
from jemrange import JemRange
from app.robot import Robot
import _thread
import time
robot_rx_uuid = "6E400002-B5A3-F393-E0A9-E50E24DCCFFF"
robot = Robot()
robot.start()
def robot_cb_handler(chr):
    events = chr.events()
    if  events & Bluetooth.CHAR_WRITE_EVENT:
        try:
            pwms = chr.value().decode().strip().split(",")
            left = int(float(pwms[0]))
            right = int(float(pwms[1]))
            print("robot.move(%d, %d)" % (left, right))
            robot.move(left, right)
        except Exception as e:
            print("Failed to get robot data %s" % e)

ble = JemBleUart(aux_rx_uuid=robot_rx_uuid, aux_handler=robot_cb_handler)
