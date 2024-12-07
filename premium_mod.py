import asyncio
import string
from time import sleep
import time
import math
import serial
from bleak import BleakClient

address = "mac address"
uuid = "0000ffe9-0000-1000-8000-00805f9b34fb"
base = "aa040206"

async def button_press_time(ser):
    ser.reset_input_buffer()
    await asyncio.gather(button_reader(ser))
    ser.reset_input_buffer()
    await asyncio.gather(button_reader(ser))
    print("press 1")
    ser.reset_input_buffer()
    last_press_time = time.perf_counter()
    await asyncio.gather(button_reader(ser))
    current_time = time.perf_counter()
    time_between_presses = (current_time - last_press_time) * 1000
    print(f'Time between presses: {time_between_presses:.2f} milliseconds')
    await asyncio.sleep(0.001)  # Add a short delay to allow other tasks to run
    return time_between_presses

async def button_reader(ser):
    while True:
        while ser.in_waiting > 0:
            data = await asyncio.to_thread(ser.readline)
            data1 = data.decode('utf-8').strip()
            if 'B' in data1:
                return
        await asyncio.sleep(0.001)  # Add a short delay to allow other tasks to run

''' this is not needed for now
async def send_data_to_arduino(ser, data_to_send):
    encoded_data = data_to_send.encode('utf-8')
    await asyncio.to_thread(ser.write, encoded_data)
    await asyncio.sleep(0.001)'''


async def main (address):
    serial_port = 'COM4'  # Example port, adjust as needed
    baudrate = 9600  # Adjust as needed

    # Create a serial connection
    ser = serial.Serial(serial_port, baudrate)#, timeout=1)

    # Start the button reader in the background
    asyncio.create_task(button_reader(ser))

    async with BleakClient(address) as client:
        async def set_speed(speed):
            if 0 < speed < 100:
                uint8_array = bytearray([0xAA, 4, speed, speed + 4])
                print(uint8_array)
                hex_string = ''.join(format(byte, '02x') for byte in uint8_array)
                print(hex_string)
                param = bytes.fromhex(hex_string)
                print(param)
                model_number = await client.write_gatt_char(uuid, param)
            else:
                print("Error: Speed value out of range. Must be between 0 and 100.")

        async def measure(speed):
            await set_speed(speed)
            time_between_presses = await button_press_time(ser)
            print(f'Total time between two button presses: {time_between_presses:.2f} milliseconds')
            return int(time_between_presses)
        
        async def twoSpeedThrust(time_between_speed_change,inSpeed,outSpeed): #<-this is called a function, basically sets of commands
            await set_speed(inSpeed)                   #sets speed
            sleep(int(time_between_speed_change)/1000) #waits for the calculated time
            await set_speed(outSpeed)                  #sets a different speed for the rest of the thrust
            ser.reset_input_buffer()                   #clears the button's state
            await asyncio.gather(button_reader(ser))   #waits for the click at the back, before returning to the loop

        async def repeatTwoSpeedThrust(count,time_per_rotation_at_this_speed,rotationDivider,inSpeed,outSpeed):
            time_between_speed_change=time_per_rotation_at_this_speed/rotationDivider #So if yu divide by 2, then its half a rotation
            for _ in range(count):                                                    #this is a loop
                await twoSpeedThrust(time_between_speed_change,inSpeed,outSpeed)      #calling the function above this one

     
        #some thrust measurements, these will vary a lot from time to time so measure your own.
        s20=1067
        s30=751
        s10=1926
        
        
        #await set_speed(10)
        #sleep(6)
        '''
        s20=await measure(20)
        await set_speed(0)
        sleep(2)
        s10=await measure(10)
        await set_speed(0)
        sleep(2)
        s30=await measure(30)
        await set_speed(0)
        sleep(2)
        '''

        print(s10,s20,s30)
        await set_speed(10)
        ser.reset_input_buffer()
        await asyncio.gather(button_reader(ser))

        await repeatTwoSpeedThrust(3,s20,2,20,5)


        print("Stopping")
        await set_speed(0)

        try:
            await asyncio.gather(button_reader)
        except asyncio.CancelledError:
            print("Task was canceled")

asyncio.run(main(address))
