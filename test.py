import asyncio
import threading
import time
from bleak import BleakClient
from bleak import BleakScanner as scan
from fitness_machine_service import *


#______________________FUNCTIONS FOR TESTING PURPOSES___________________________#
async def find_device(device_name):
    global device_address
    device_list = await scan.discover()
    time.sleep(0.05)
    for device in device_list:
        print(device.name)
        if device.name == device_name:
            device_address = device.address
            return device_address

async def main(address, worker):
    async with BleakClient(address, timeout=10) as client:
        ftms = FitnessMachineService(client)
        worker.issue_message.emit("Connected! Now running")

        current_speed = 80

        while worker.working == True:
            # Print all 'read' characteristics
            worker.green_screen.emit()

            worker.issue_message.emit("Retrieving Speed Range in 3 seconds") 

            supported_speed_range = await ftms.get_speed_range()
            print("Supported speed range:")
            print(supported_speed_range)
            print()
            max_speed = supported_speed_range.max_speed
            min_increment = supported_speed_range.min_increment

            worker.issue_message.emit(str(supported_speed_range)) 

            # TODO: FTM_Status function under construction
            # await ftms.enable_ftm_status_notify()

            # Start receiving notifications from the control point characteristic
            await ftms.enable_cp_indicate()

            # write control request to machine
            await ftms.request_control()
            await asyncio.sleep(5)

            worker.issue_message.emit("Preparing to change speed every 3 seconds") 
            await asyncio.sleep(5)

            # TODO: FTM_Status function under construction
            # ftm_status = await ftms.get_ftm_status()
            # print(ftm_status)

            worker.issue_message.emit(f"Setting current speed: {str(current_speed)}")
            await ftms.set_target_speed(current_speed)
            current_speed += 16
            print(current_speed)
            print()
            
            await asyncio.sleep(3)

            worker.issue_message.emit(f"Setting current speed: {str(current_speed)}")
            await ftms.set_target_speed(current_speed)
            current_speed += 16
            print(current_speed)
            print()
            
            await asyncio.sleep(3)

            worker.issue_message.emit(f"Setting current speed: {str(current_speed)}")

            await ftms.set_target_speed(current_speed)
            current_speed += 16
            print(current_speed)
            print()
                    
            # ftm_status = await ftms.get_ftm_status()
            # print(ftm_status)

            await asyncio.sleep(3)

            
        worker.issue_message.emit("Stopping")
        time.sleep(5)
        worker.red_screen.emit()

        

    # return
    