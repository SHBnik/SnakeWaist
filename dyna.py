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

        # Data Byte Length
        self.LEN_MX_MOVE_SPEED          = 2

        # Protocol version
        self.PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

        # Default setting
        self.DXL1_ID                     = 18                 
        self.DXL2_ID                     = 9                  
        self.DXL3_ID                     = 1                  
        self.DXL4_ID                     = 7                 
        self.BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
        self.DEVICENAME                  = 'COM5'    # Check which port is being used on your controller
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

        # Open port
        self.portHandler.openPort()


        # Set port baudrate
        self.portHandler.setBaudRate(self.BAUDRATE)

        self.set_wheel_mode(self.DXL1_ID)
        self.set_wheel_mode(self.DXL2_ID)
        self.set_wheel_mode(self.DXL3_ID)
        self.set_wheel_mode(self.DXL4_ID)

        
        self.enable_torque(self.DXL1_ID)
        self.enable_torque(self.DXL2_ID)
        self.enable_torque(self.DXL3_ID)
        self.enable_torque(self.DXL4_ID)



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


    def move(self, dir, speed):

        speed = self.map_dyna(speed)
        speed = self.prepare_packet(speed)
        zero = self.prepare_packet(0)

        if dir == 0:
            self.groupSyncWrite.addParam(self.DXL1_ID, speed)
            self.groupSyncWrite.addParam(self.DXL2_ID, zero)
            self.groupSyncWrite.addParam(self.DXL3_ID, speed)
            self.groupSyncWrite.addParam(self.DXL4_ID, zero)
        elif dir == 1:
            self.groupSyncWrite.addParam(self.DXL1_ID, zero)
            self.groupSyncWrite.addParam(self.DXL2_ID, speed)
            self.groupSyncWrite.addParam(self.DXL3_ID, speed)
            self.groupSyncWrite.addParam(self.DXL4_ID, zero)
        elif dir == 2:
            self.groupSyncWrite.addParam(self.DXL1_ID, zero)
            self.groupSyncWrite.addParam(self.DXL2_ID, speed)
            self.groupSyncWrite.addParam(self.DXL3_ID, zero)
            self.groupSyncWrite.addParam(self.DXL4_ID, speed)
        elif dir == 3:
            self.groupSyncWrite.addParam(self.DXL1_ID, speed)
            self.groupSyncWrite.addParam(self.DXL2_ID, zero)
            self.groupSyncWrite.addParam(self.DXL3_ID, zero)
            self.groupSyncWrite.addParam(self.DXL4_ID, speed)
        elif dir == 4:
            self.groupSyncWrite.addParam(self.DXL1_ID, speed)
            self.groupSyncWrite.addParam(self.DXL2_ID, speed)
            self.groupSyncWrite.addParam(self.DXL3_ID, speed)
            self.groupSyncWrite.addParam(self.DXL4_ID, speed)




        self.groupSyncWrite.txPacket()


        self.groupSyncWrite.clearParam()



        

        

    

    

