import csv
from modbus_device import ModbusDevice
from register import Register
from modbus_reader import ModbusReader
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# disabling buffering for stdout and stderr when monitoring to check results in real time
sys.stdout.reconfigure(line_buffering=True)

def load_devices_by_category(csv_file, category):
    '''
        Load all devices and their registers from the CSV file based on the provided category.
        For the froniusDatamanager category, iterate over all unit IDs from 1 to the specified unit_id.
        For other categories, load the device and its registers without iteration.
    '''
    devices = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # skip any comments (while testing)
            if row['category'].startswith('#'):
                continue

            if row['category'] == category:
                if category == "froniusDatamanager":
                    # Iterate over all unit IDs ONLY for froniusDatamanager
                    max_unit_id = int(row['unit_id'])  
                    for unit_id in range(1, max_unit_id + 1): 
                        device = ModbusDevice(ip=row['ip'], port=int(row['port']), unit_id=unit_id)
                        register = Register(
                            address=int(row['register_status_addr']),
                            name=f"{row['register_name']} (Unit ID: {unit_id})",
                            scale=int(row['scale']),
                            unit=row['unit']
                        )
                        devices.append((device, [register]))
                else:
                    device = ModbusDevice(ip=row['ip'], port=int(row['port']), unit_id=int(row['unit_id']))
                    register = Register(
                        address=int(row['register_status_addr']),
                        name=row['register_name'],
                        scale=int(row['scale']),
                        unit=row['unit']
                    )
                    devices.append((device, [register]))
    if not devices:
        raise ValueError(f"No devices found for category '{category}' in the CSV file.")
    return devices

def read_device(device, registers, category):
    '''
        Read all registers for a single device.
    '''
    try:
        print(f"Reading device at IP: {device.ip}, Port: {device.port}, Unit ID: {device.unit_id}, State register: {registers[0].address}")
        reader = ModbusReader(device=device, registers=registers, category=category)
        reader.read_all_registers()
    except Exception as e:
        print(f"Error reading device at IP: {device.ip}, Port: {device.port}, Unit ID: {device.unit_id}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Category argument is required.")
        sys.exit(1)

    category = sys.argv[1]  
    try:
        devices = load_devices_by_category("all_devices.csv", category)

        print(f"Reading state of devices in category '{category}' in parallel...")
        # default_workers = min(32, os.cpu_count() + 4)
        with ThreadPoolExecutor() as executor:
            # parallel reading 
            futures = [executor.submit(read_device, device, registers, category) for device, registers in devices]

            # w8 for all tasks to complete
            for future in as_completed(futures):
                try:
                    future.result() 
                except Exception as e:
                    print(f"Error during parallel execution: {e}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)