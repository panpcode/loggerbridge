import argparse
import csv
import logging
from modbus_device import ModbusDevice

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_device_from_csv(csv_file, category, action):
    '''
        Load the device and the appropriate register address based on the action (start/stop).
    '''
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # skip any comments (while testing)
            if row['category'].startswith('#'):
                continue

            if row['category'] == category:
                device = ModbusDevice(ip=row['ip'], port=int(row['port']), unit_id=int(row['unit_id']))
                if action == "start":
                    register_address = int(row['register_start_addr'])
                elif action == "stop":
                    register_address = int(row['register_stop_addr'])
                else:
                    raise ValueError("Invalid action. Use 'start' or 'stop'.")
                return device, register_address
    raise ValueError(f"Device category '{category}' not found in CSV.")

def control_logger(device, register_address, action):
    '''
        Control the logger by writing to the appropriate register address.
    '''
    START_VALUE = 1
    STOP_VALUE = 0   

    if action == "start":
        value = START_VALUE
        action_text = "Starting"
    elif action == "stop":
        value = STOP_VALUE
        action_text = "Stopping"
    else:
        logging.error("Invalid action. Use 'start' or 'stop'.")
        return

    # logging.info(f"{action_text} the logger on device (IP: {device.ip}, Port: {device.port}, Unit ID: {device.unit_id})...")
    result = device.write_register(register_address, value)
    if result:
        logging.info(f"Signal to {action} the logger sent successfully to device (IP: {device.ip}, Port: {device.port}, Unit ID: {device.unit_id}).")
    else:
        logging.error(f"Failed to {action} the logger on device (IP: {device.ip}, Port: {device.port}, Unit ID: {device.unit_id}).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control the logger (start/stop).")
    parser.add_argument("action", choices=["start", "stop"], help="Action to perform on the logger (start or stop).")
    parser.add_argument("category", help="Device category (e.g., huawei, sungrow, froniusGen24, froniusDatamanager).")
    args = parser.parse_args()

    try:
        device, register_address = load_device_from_csv("all_devices.csv", args.category, args.action)
        control_logger(device, register_address, args.action)
    except ValueError as e:
        logging.error(f"Error: {e}")