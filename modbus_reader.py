import logging, sys

# Disable buffering for stdout and stderr for monitoring team to check results in real time
sys.stdout.reconfigure(line_buffering=True)

class ModbusReader:
    
    def __init__(self, device, registers, category=None, p_id=None):
        self.device = device
        self.registers = registers
        self.category = category
        self.p_id = p_id  

    def read_all_registers(self):
        '''
            Read all registers from the Modbus device and log the results.
            This method iterates through the list of registers and logs the
            results of reading each register.
        '''
        for reg in self.registers:
            try:
                if self.category == "sungrow":
                    raw_value = self.device.read_input_register(reg.address)  # Sungrow devices use input registers
                else:
                    raw_value = self.device.read_register(reg.address)  # Default = Holding Registers

                if raw_value is not None and len(raw_value) > 0:
                    if self.category in ["froniusDatamanager"]:
                        if raw_value == [7]:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : RUNNING")
                        elif raw_value == [6]:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : STOPPED")
                        else:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : {raw_value} {reg.unit}")
                    elif self.category in ["froniusGen24"]:
                        if raw_value == [7]:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : RUNNING")
                        elif raw_value == [1]:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : STOPPED")
                        else:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : {raw_value} {reg.unit}")
                    elif self.category in ["huawei"]:
                        if raw_value == [1]:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : RUNNING")
                        elif raw_value == [4]:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : STOPPED")
                        elif raw_value == [3]:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : STARTING")
                        else:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : {raw_value} {reg.unit}")
                    elif self.category in ["sungrow"]:
                        if raw_value == [1]:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : RUNNING")
                        elif raw_value == [0]:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : STOPPED")
                        else:
                            logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : {raw_value} {reg.unit}")
                    else:
                        logging.info(f"✅ SUCCESS - {self.p_id} state with IP {self.device.ip} : {raw_value} {reg.unit}")
                else:
                    logging.error(f"❌ Failed - {self.p_id} state with IP {self.device.ip} : No data returned")
            except Exception as e:
                logging.error(f"❌ Failed - {self.p_id} state with IP {self.device.ip} : Exception - {e}")