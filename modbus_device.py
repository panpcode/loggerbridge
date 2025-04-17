from pyModbusTCP.client import ModbusClient
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModbusDevice:

    def __init__(self, ip, port, unit_id):
        self.ip = ip
        self.port = port
        self.unit_id = unit_id
        self.client = ModbusClient(host=self.ip, port=self.port, unit_id=self.unit_id, auto_open=True)

    def connect(self):
        if not self.client.is_open:
            if not self.client.open():
                logging.error(f"❌ Could not connect to Modbus server at {self.ip}:{self.port} (Unit ID: {self.unit_id})")
                return False
        return True

    def close(self):
        if self.client.is_open:
            self.client.close()
            logging.info("🔌 Disconnected from Modbus server.")

    def read_register(self, address, count=1):
        '''
            This reads holding registers
        '''
        if not self.connect():
            return None
        values = self.client.read_holding_registers(address, count)
        if values is None:
            logging.error(f"❌ Failed to read from address {address}")
        # else:
        #     logging.info(f"📖 Read from address {address}: {values}")
        return values
    
    def read_input_register(self, address, count=1):
        '''
            Read input registers  
        '''
        if not self.connect():
            return None
        values = self.client.read_input_registers(address, count)
        if values is None:
            logging.error(f"❌ Failed to read input register at address {address}")
        # else:
        #     logging.info(f"📖 Read input register at address {address}: {values}")
        return values

    def write_register(self, address, value):
        '''
            Write a value to a specific Modbus register.
            We will need that for powering on/off the inverter.
        '''
        if not self.connect():
            return False
        success = self.client.write_single_register(address, value)
        if success:
            logging.info(f"✅ Wrote value {value} to register {address}")
        else:
            logging.error(f"❌ Failed to write value {value} to register {address}")
        return success

    def write_registers(self, address, values):
        '''
            This method writes multiple values to consecutive Modbus registers.
        '''
        if not self.connect():
            return False
        success = self.client.write_multiple_registers(address, values)
        if success:
            logging.info(f"✅ Wrote values {values} starting at register {address}")
        else:
            logging.error(f"❌ Failed to write values {values} starting at register {address}")
        return success
