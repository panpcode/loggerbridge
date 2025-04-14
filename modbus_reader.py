import logging

class ModbusReader:
    
    def __init__(self, device, registers):
        self.device = device
        self.registers = registers

    def read_all_registers(self):
        '''
            Read all registers from the Modbus device and log the results.
            This method iterates through the list of registers and logs the
            results of reading each register.
        '''
        for reg in self.registers:
            try:
                raw_value = self.device.read_register(reg.address)
                if raw_value is not None and len(raw_value) > 0:
                    logging.info(f"✅ SUCCESS - {reg.name} (Address: {reg.address}): {raw_value} {reg.unit}")
                else:
                    logging.error(f"❌ Failed to read {reg.name} (Address: {reg.address}) - No data returned")
            except Exception as e:
                logging.error(f"❌ Exception while reading {reg.name} (Address: {reg.address}): {e}")