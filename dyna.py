from dynamixel_sdk import *
import math
import time

class motors:
    def __init__(self):
        # Control table address
        self.ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
        self.ADDR_MX_MOVE_SPEED         = 32
        self.ADDR_MX_CW_ANGLE_LIMIT     = 6
        self.ADDR_MX_CCW_ANGLE_LIMIT    = 8 
        self.ADDR_MX_GOAL_POSITION      = 30
        self.ADDR_MX_TORQUE_LIMIT       = 34

        # Data Byte Length
        self.LEN_MX_MOVE_SPEED          = 2
        self.LEN_MX_GOAL_POSITION          = 2

        # Protocol version
        self.PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

        # Default setting
        self.DXL1_ID                     = 18                 
        self.DXL2_ID                     = 9                  
        self.DXL3_ID                     = 1                  
        self.DXL4_ID                     = 2                 
        self.BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
        self.DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                        # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

        self.TORQUE_ENABLE               = 1                 # Value for enabling the torque
        self.TORQUE_DISABLE              = 0                 # Value for disabling the torque
        self.DXL_MINIMUM_POSITION_VALUE  = 100           # Dynamixel will rotate between this value
        self.DXL_MAXIMUM_POSITION_VALUE  = 1023            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
        self.DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold
        
        # Initialize PortHandler instance
        # Set the port path
        # Get methods and members of PortHandlerLinux or PortHandlerWindows
        self.portHandler = PortHandler(self.DEVICENAME)

        # Initialize PacketHandler instance
        # Set the protocol version
        # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
        self.packetHandler = PacketHandler(self.PROTOCOL_VERSION)

        # Initialize GroupSyncWrite instance
        self.groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, self.ADDR_MX_MOVE_SPEED, self.LEN_MX_MOVE_SPEED)
        # self.groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, self.ADDR_MX_GOAL_POSITION, self.LEN_MX_GOAL_POSITION)

        # Open port
        self.portHandler.openPort()


        # Set port baudrate
        self.portHandler.setBaudRate(self.BAUDRATE)

        # wheel
        self.set_wheel_mode(self.DXL1_ID)
        self.set_wheel_mode(self.DXL2_ID)
        self.set_wheel_mode(self.DXL3_ID)
        self.set_wheel_mode(self.DXL4_ID)


        # joint
        # self.set_joint_mode(self.DXL1_ID)
        # self.set_joint_mode(self.DXL2_ID)
        # self.set_joint_mode(self.DXL3_ID)
        # self.set_joint_mode(self.DXL4_ID)

        
        self.enable_torque(self.DXL1_ID)
        self.enable_torque(self.DXL2_ID)
        self.enable_torque(self.DXL3_ID)
        self.enable_torque(self.DXL4_ID)

        self.set_torque_limit(self.DXL1_ID, 400)
        self.set_torque_limit(self.DXL2_ID, 400)
        self.set_torque_limit(self.DXL3_ID, 400)
        self.set_torque_limit(self.DXL4_ID, 400)


        zero = self.prepare_packet(0)
        self.groupSyncWrite.addParam(self.DXL4_ID, zero)
        self.groupSyncWrite.addParam(self.DXL3_ID, zero)
        self.groupSyncWrite.addParam(self.DXL2_ID, zero)
        self.groupSyncWrite.addParam(self.DXL1_ID, zero)
        self.groupSyncWrite.txPacket()
        self.groupSyncWrite.clearParam()




    def set_wheel_mode(self, ID):
        self.packetHandler.write2ByteTxRx(self.portHandler, ID, self.ADDR_MX_CW_ANGLE_LIMIT, 0)
        self.packetHandler.write2ByteTxRx(self.portHandler, ID, self.ADDR_MX_CCW_ANGLE_LIMIT, 0)

    def set_torque_limit(self, ID, torque):
        self.packetHandler.write2ByteTxRx(self.portHandler, ID, self.ADDR_MX_TORQUE_LIMIT, torque) 
        
    def set_joint_mode(self, ID):
        self.packetHandler.write2ByteTxRx(self.portHandler, ID, self.ADDR_MX_CW_ANGLE_LIMIT, 0)
        self.packetHandler.write2ByteTxRx(self.portHandler, ID, self.ADDR_MX_CCW_ANGLE_LIMIT, 1023)

    def enable_torque(self, ID):
        self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_MX_TORQUE_ENABLE, self.TORQUE_ENABLE)

    def disable_torque(self, ID):
        self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_MX_TORQUE_ENABLE, self.TORQUE_DISABLE)

    def prepare_packet(self, speed):
        return [DXL_LOBYTE(int(speed)), DXL_HIBYTE(int(speed))]

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def constrain(self, value, min, max):
        if value >= max:    return max
        elif value <= min:  return min
        else:               return value

    def map_dyna(self, value):
        if value >= 0:  return value + 1024
        elif value < 0: return -1 * value

    def stop_motors(self):
        self.disable_torque(self.DXL1_ID)
        self.disable_torque(self.DXL2_ID)
        self.disable_torque(self.DXL3_ID)
        self.disable_torque(self.DXL4_ID)

    def home(self):
        self.set_joint_mode(self.DXL1_ID)
        self.set_joint_mode(self.DXL2_ID)
        self.set_joint_mode(self.DXL3_ID)
        self.set_joint_mode(self.DXL4_ID)

        self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL1_ID, self.ADDR_MX_GOAL_POSITION, 231)
        self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL2_ID, self.ADDR_MX_GOAL_POSITION, 213)
        self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL3_ID, self.ADDR_MX_GOAL_POSITION, 216)
        self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL4_ID, self.ADDR_MX_GOAL_POSITION, 379)

        time.sleep(2)
        self.set_wheel_mode(self.DXL1_ID)
        self.set_wheel_mode(self.DXL2_ID)
        self.set_wheel_mode(self.DXL3_ID)
        self.set_wheel_mode(self.DXL4_ID)


    def move(self, dir, speed1, speed2, speed3, speed4):

        # self.pos_e1 = self.pos_e1 + speed1
        # self.pos_e2 = self.pos_e2 + speed2
        # self.pos_e3 = self.pos_e3 + speed3
        # self.pos_e4 = self.pos_e4 + speed4 

        speed1 = self.map_dyna(speed1)
        speed1 = self.prepare_packet(speed1)
        zero = self.prepare_packet(0)

        speed2 = self.map_dyna(speed2)
        speed2 = self.prepare_packet(speed2)

        speed3 = self.map_dyna(speed3)
        speed3 = self.prepare_packet(speed3)

        speed4 = self.map_dyna(speed4)
        speed4 = self.prepare_packet(speed4)

        if dir == 0: 
            self.groupSyncWrite.addParam(self.DXL1_ID, zero)
            self.groupSyncWrite.addParam(self.DXL2_ID, speed2)
            self.groupSyncWrite.addParam(self.DXL3_ID, speed3)
            self.groupSyncWrite.addParam(self.DXL4_ID, zero)
        elif dir == 1:
            self.groupSyncWrite.addParam(self.DXL1_ID, speed1)
            self.groupSyncWrite.addParam(self.DXL2_ID, zero)
            self.groupSyncWrite.addParam(self.DXL3_ID, zero)
            self.groupSyncWrite.addParam(self.DXL4_ID, speed4)
        elif dir == 2:
            self.groupSyncWrite.addParam(self.DXL1_ID, speed1)
            self.groupSyncWrite.addParam(self.DXL2_ID, zero)
            self.groupSyncWrite.addParam(self.DXL3_ID, speed3)
            self.groupSyncWrite.addParam(self.DXL4_ID, zero)
        elif dir == 3:
            self.groupSyncWrite.addParam(self.DXL1_ID, zero)
            self.groupSyncWrite.addParam(self.DXL2_ID, speed2)
            self.groupSyncWrite.addParam(self.DXL3_ID, zero)
            self.groupSyncWrite.addParam(self.DXL4_ID, speed4)
        elif dir == 4:
            self.groupSyncWrite.addParam(self.DXL1_ID, speed1)
            self.groupSyncWrite.addParam(self.DXL2_ID, speed2)
            self.groupSyncWrite.addParam(self.DXL3_ID, speed3)
            self.groupSyncWrite.addParam(self.DXL4_ID, speed4)
        elif dir == 5:
            self.groupSyncWrite.addParam(self.DXL1_ID, zero)
            self.groupSyncWrite.addParam(self.DXL2_ID, zero)
            self.groupSyncWrite.addParam(self.DXL3_ID, zero)
            self.groupSyncWrite.addParam(self.DXL4_ID, zero)
        #####################################################
        # if dir == 0:
        #     self.groupSyncWrite.addParam(self.DXL1_ID, speed1)
        #     self.groupSyncWrite.addParam(self.DXL2_ID, zero)
        #     self.groupSyncWrite.addParam(self.DXL3_ID, zero)
        #     self.groupSyncWrite.addParam(self.DXL4_ID, zero)
        # elif dir == 1:
        #     self.groupSyncWrite.addParam(self.DXL1_ID, zero)
        #     self.groupSyncWrite.addParam(self.DXL2_ID, speed2)
        #     self.groupSyncWrite.addParam(self.DXL3_ID, zero)
        #     self.groupSyncWrite.addParam(self.DXL4_ID, zero)
        # elif dir == 2:
        #     self.groupSyncWrite.addParam(self.DXL1_ID, zero)
        #     self.groupSyncWrite.addParam(self.DXL2_ID, zero)
        #     self.groupSyncWrite.addParam(self.DXL3_ID, speed3)
        #     self.groupSyncWrite.addParam(self.DXL4_ID, zero)
        # elif dir == 3:
        #     self.groupSyncWrite.addParam(self.DXL1_ID, zero)
        #     self.groupSyncWrite.addParam(self.DXL2_ID, zero)
        #     self.groupSyncWrite.addParam(self.DXL3_ID, zero)
        #     self.groupSyncWrite.addParam(self.DXL4_ID, speed4)
        # elif dir == 4:
        #     self.groupSyncWrite.addParam(self.DXL1_ID, speed1)
        #     self.groupSyncWrite.addParam(self.DXL2_ID, speed2)
        #     self.groupSyncWrite.addParam(self.DXL3_ID, speed3)
        #     self.groupSyncWrite.addParam(self.DXL4_ID, speed4)
        # elif dir == 5:
        #     self.groupSyncWrite.addParam(self.DXL1_ID, zero)
        #     self.groupSyncWrite.addParam(self.DXL2_ID, zero)
        #     self.groupSyncWrite.addParam(self.DXL3_ID, zero)
        #     self.groupSyncWrite.addParam(self.DXL4_ID, zero)



        self.groupSyncWrite.txPacket()

        #time.sleep(2.5)
        self.groupSyncWrite.clearParam()



        

        

    

    

