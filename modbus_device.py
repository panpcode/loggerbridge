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
            return self.client.open()
        return True

    def disconnect(self):
        if self.client.is_open:
            self.client.close()

    def read_register(self, address, count=1):
        if not self.connect():
            logging.error(f"❌ Could not connect to Modbus server at {self.ip}:{self.port} (Unit ID: {self.unit_id})")
            return None
        return self.client.read_holding_registers(address, count)