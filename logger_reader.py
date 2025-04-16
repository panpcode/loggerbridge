import csv
from modbus_device import ModbusDevice
from register import Register
from modbus_reader import ModbusReader
import sys

# Disable buffering for stdout and stderr for monitoring team to check results in real time
sys.stdout.reconfigure(line_buffering=True)

def load_device_by_category(csv_file, category):
    '''
        Load a specific device and its registers from the CSV file based on the provided category.
    '''
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['category'] == category:
                device = ModbusDevice(ip=row['ip'], port=int(row['port']), unit_id=int(row['unit_id']))
                register = Register(
                    address=int(row['register_address']),
                    name=row['register_name'],
                    scale=int(row['scale']),
                    unit=row['unit']
                )
                return device, [register]
    raise ValueError(f"Device category '{category}' not found in CSV.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Category argument is required.")
        sys.exit(1)

    category = sys.argv[1]  
    try:
        device, registers = load_device_by_category("devices.csv", category)

        print(f"Reading state of {category}...")
        reader = ModbusReader(device=device, registers=registers, category=category)
        reader.read_all_registers()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)