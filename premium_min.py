import asyncio
import time
from bleak import BleakClient

#Tested with 3.0 versions. Probably works for 4.0 but haven't got that one.

address = "mac address"
uuid = "0000ffe9-0000-1000-8000-00805f9b34fb"
base = "aa040206"

async def main(address):
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

        async def sawtoothWaveUp(t, lSpeed, hSpeed, teeth):
            tPerTooth = t / teeth
            speedRange = hSpeed - lSpeed
            tPerSpeedIncrement = tPerTooth / speedRange
            for i in range(teeth):
                for o in range(speedRange + 1):
                    currentSpeed = lSpeed + o
                    await set_speed(currentSpeed)
                    time.sleep(tPerSpeedIncrement)

        print("Starting")
        await set_speed(5)
        time.sleep(4) #The machine doesnt seem to like instantly starting with a pattern
        await sawtoothWaveUp(20,5,20,4)
        print("Stopping")
        await set_speed(0)

asyncio.run(main(address))