from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import logging

# Optional: Enable logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# Configuration
SMARTLOGGER_IP = '10.102.19.160'  # IP of the Huawei SmartLogger
SMARTLOGGER_PORT = 502            # Modbus TCP port
UNIT_ID = 1                       # Modbus unit ID of the device

# Connect to SmartLogger
client = ModbusTcpClient(SMARTLOGGER_IP, port=SMARTLOGGER_PORT)

def read_all_registers(start_address, end_address):
    '''
    Read all registers from the specified range and print their values.
    '''
    try:
        for address in range(start_address, end_address + 1):
            # Read a single register
            response = client.read_input_registers(address, count=1, slave=UNIT_ID)
            if not response.isError():
                value = response.registers[0]
                print(f"Register {address}: {value}")
            else:
                print(f"Error reading register {address}")
    except Exception as e:
        print(f"Exception while reading registers: {str(e)}")

if client.connect():
    print("Connected to Huawei SmartLogger")

    # Specify the range of registers to read
    START_ADDRESS = 40500  # Example start address
    END_ADDRESS = 40600    # Example end address

    # Read all registers in the specified range
    read_all_registers(START_ADDRESS, END_ADDRESS)

    client.close()
else:
    print("Failed to connect to SmartLogger.")