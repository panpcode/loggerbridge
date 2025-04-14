class Register:
    ''' 
        This class represents a Modbus register, which includes its address,
        name, scale factor, and unit. It also provides a method to process
        the raw value read from the register.
    '''
    def __init__(self, address, name, scale=1, unit=""):
        self.address = address
        self.name = name
        self.scale = scale
        self.unit = unit

    def process_value(self, raw_value):
        if raw_value is not None:
            return raw_value * self.scale
        return None