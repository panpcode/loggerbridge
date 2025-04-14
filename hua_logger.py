from modbus_device import ModbusDevice
from register import Register
from modbus_reader import ModbusReader

if __name__ == "__main__":
    
    # here we can accept a list of devices
    device1 = ModbusDevice(ip="10.100.7.163", port=502, unit_id=100)

    # here we can accept a list of registers 
    registers = [
        Register(address=40543, name="Plant Status", scale=1, unit="")
    ]

    # creating a ModbusReader object to read all the provided registers
    reader = ModbusReader(device=device1, registers=registers)
    reader.read_all_registers()
