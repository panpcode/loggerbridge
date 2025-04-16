import argparse
from modbus_device import ModbusDevice

def control_logger(device, register_address, action):
    START_VALUE = 1
    STOP_VALUE = 0   

    if action == "start":
        value = START_VALUE
        action_text = "Starting"
    elif action == "stop":
        value = STOP_VALUE
        action_text = "Stopping"
    else:
        print("Invalid action. Use 'start' or 'stop'.")
        return

    print(f"{action_text} the logger...")
    result = device.write_register(register_address, value)
    print(f"Result: {result}")
    if result:
        print(f"Logger {action}ed successfully.")
    else:
        print(f"Failed to {action} the logger.")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Control the logger (start/stop).")
    parser.add_argument("action", choices=["start", "stop"], help="Action to perform on the logger (start or stop).")
    args = parser.parse_args()

    # Define Modbus devices
    froniusGen24 = ModbusDevice(ip="10.108.1.51", port=502, unit_id=1)
    froniusDatamanager = ModbusDevice(ip="10.100.2.161", port=502, unit_id=1)

    try:
        START_STOP_REGISTER = 40241
        control_logger(froniusDatamanager, START_STOP_REGISTER, args.action)
    finally:
        froniusGen24.close()