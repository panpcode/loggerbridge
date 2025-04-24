import argparse
import csv
import logging
from modbus_device import ModbusDevice
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_devices_from_csv(csv_file, category, action):
    '''
        Load all devices and their appropriate register addresses based on the action (start/stop).
        For the froniusDatamanager category, iterate over all unit IDs from 1 to the specified unit_id.
    '''
    devices = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Skip lines that are comments (if any)
            if row['category'].startswith('#'):
                continue

            if row['category'] == category:
                p_id = row.get('p-id', 'N/A')
                if category == "froniusDatamanager":
                    # Special case: Start from unit_id = 2 for IP 10.101.1.168
                    if row['ip'] == "10.101.1.168":
                        start_unit_id = 2
                    else:
                        start_unit_id = 1

                    # Iterate over all unit IDs ONLY for froniusDatamanager
                    max_unit_id = int(row['unit_id'])
                    for unit_id in range(start_unit_id, max_unit_id + 1):
                        device = ModbusDevice(ip=row['ip'], port=int(row['port']), unit_id=unit_id)
                        if action == "start":
                            register_address = int(row['register_start_addr'])
                        elif action == "stop":
                            register_address = int(row['register_stop_addr'])
                        else:
                            raise ValueError("Invalid action. Use 'start' or 'stop'.")
                        devices.append((device, register_address, p_id))
                else:
                    device = ModbusDevice(ip=row['ip'], port=int(row['port']), unit_id=int(row['unit_id']))
                    if action == "start":
                        register_address = int(row['register_start_addr'])
                    elif action == "stop":
                        register_address = int(row['register_stop_addr'])
                    else:
                        raise ValueError("Invalid action. Use 'start' or 'stop'.")
                    devices.append((device, register_address, p_id))
    if not devices:
        raise ValueError(f"No devices found for category '{category}' in the CSV file.")
    return devices

def control_logger(device, register_address, action, category, p_id):
    '''
        Control the logger by writing to the appropriate register address.
    '''
    START_VALUE = 1
    STOP_VALUE = 0   

    if category == "huawei":
        # Special logic for Huawei
        # Start register set to 0 - Stop register set to 0
        if action == "start":
            value = 0  
            action_text = "Starting"
        elif action == "stop":
            value = 0  
            action_text = "Stopping"
        else:
            logging.error(f"❌ Failed - {p_id} state with IP {device.ip} : Invalid action. Use 'start' or 'stop'.")
            return
    else:
        # Default logic for other categories
        if action == "start":
            value = START_VALUE
            action_text = "Starting"
        elif action == "stop":
            value = STOP_VALUE
            action_text = "Stopping"
        else:
            logging.error(f"❌ Failed - {p_id} state with IP {device.ip} : Invalid action. Use 'start' or 'stop'.")
            return

    result = device.write_register(register_address, value)
    if result:
        logging.info(f"✅ SUCCESS - {p_id} state with IP {device.ip} : Signal to {action} sent successfully.")
    else:
        logging.error(f"❌ Failed - {p_id} state with IP {device.ip} : Failed to send signal to {action}.")

def execute_action_in_parallel(devices, action, category):
    '''
        Execute the start/stop action on multiple devices in parallel using ThreadPoolExecutor.
    '''
    max_workers = 10  # we can discuss with Konstantinos the value for Linux server 
    task_timeout = 30  # timeout for each task (secs)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(control_logger, device, register_address, action, category, p_id) for device, register_address, p_id in devices]

        for future in as_completed(futures):
            try:
                future.result(timeout=task_timeout)  # Wait for the task to complete with a timeout
            except TimeoutError:
                logging.error("Task timed out.")
            except Exception as e:
                logging.error(f"Error during parallel execution: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control the logger (start/stop).")
    parser.add_argument("action", choices=["start", "stop"], help="Action to perform on the logger (start or stop).")
    parser.add_argument("category", help="Device category (e.g., huawei, sungrow, froniusGen24, froniusDatamanager).")
    args = parser.parse_args()

    try:
        devices = load_devices_from_csv("all_devices.csv", args.category, args.action)
        logging.info(f"Executing '{args.action}' action on devices in category '{args.category}' in parallel...")
        execute_action_in_parallel(devices, args.action, args.category)
    except ValueError as e:
        logging.error(f"Error: {e}")