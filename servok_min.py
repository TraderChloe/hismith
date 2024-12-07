
import asyncio
import time
from bleak import BleakClient

address = "mac address of your servok"
uuid = "0000ffe9-0000-1000-8000-00805f9b34fb"
current_position = None
speed = None
min_depth = None
max_depth = None
smoothness = None

async def main(address):
    async with BleakClient(address) as client:

        async def send(value):
            param = bytes.fromhex(value)
            await client.write_gatt_char(uuid, param)
        async def set_smoothness(val):
            if 0 <= val <= 10:
                global smoothness
                smoothness=val
                uint8_array = bytearray([204, 9, val, val+9])
                hex_string = ''.join(format(byte, '02x') for byte in uint8_array)
                print(hex_string)
                await send(hex_string)
        async def set_speed(val):
            if 0 <= val <= 100:
                global speed
                speed=val
                uint8_array = bytearray([204, 3, val, val+3])
                hex_string = ''.join(format(byte, '02x') for byte in uint8_array)
                print(hex_string)
                await send(hex_string)
        async def min_depth(val):  # Also check that min is lower than max
            global min_depth, max_depth
            if 0 <= val <= 99 and (not 'max_depth' in globals() or val < max_depth): 
                min_depth = val
                uint8_array = bytearray([204, 7, val, val + 7])
                hex_string = ''.join(format(byte, '02x') for byte in uint8_array)
                print(hex_string)
                await send(hex_string)
            else:
                print("Error: min_depth must be less than max_depth and within valid range.")

        async def max_depth(val):  # Also check that max is larger than min
            global max_depth, min_depth
            if 1 <= val <= 100 and (not 'min_depth' in globals() or val > min_depth): 
                max_depth = val
                uint8_array = bytearray([204, 8, val, val + 8])
                hex_string = ''.join(format(byte, '02x') for byte in uint8_array)
                print(hex_string)
                await send(hex_string)
            else:
                print("Error: max_depth must be greater than min_depth and within valid range.")
        def notification_handler(sender, data):
            global current_position
            current_position = parseresponse(data)
            print(current_position) #Live display of current location of the thrust bar
        def parseresponse(data):
            uint_values = list(data)
            return uint_values[2]

        await client.start_notify("0000ffe4-0000-1000-8000-00805f9b34fb", notification_handler)

        print("Starting")
        await asyncio.sleep(2)
        await set_speed(20)
        await max_depth(100)
        await min_depth(10)
        await set_smoothness(10)
        await asyncio.sleep(10)
        
        await set_speed(0)
        await asyncio.sleep(1)
        print("Stopping")
        await send("cc010001")

asyncio.run(main(address))