from modbus_device import ModbusDevice
from register import Register
from modbus_reader import ModbusReader

if __name__ == "__main__":
    
    # here we can accept a list of devices
    huawei = ModbusDevice(ip="10.100.7.163", port=502, unit_id=100)
    sunGrow = ModbusDevice(ip="10.100.2.163", port=502, unit_id=247)
    froniusGen24 = ModbusDevice(ip="10.108.1.51", port=502, unit_id=1)
    froniusDatamanager = ModbusDevice(ip="10.100.2.161", port=502, unit_id=3)

    # here we can accept a list of registers 
    huaRegisters = [
        Register(address=40543, name="Plant Status", scale=1, unit="")
    ]

    sungrowRegister = [
        Register(address=8001, name="Plant Status", scale=1, unit="")
    ]

    froniusGen24Register = [
        Register(address=40241, name="PV inverter state", scale=1, unit="")
    ]

    froniusDatamanagerRegister = [
        Register(address=40241, name="Plant Status", scale=1, unit="")
    ]
    
    # creating a ModbusReader object to read all the provided registers
    reader = ModbusReader(device=froniusDatamanager, registers=froniusDatamanagerRegister)
    reader.read_all_registers()
