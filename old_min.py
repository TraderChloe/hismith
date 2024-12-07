import asyncio
import time
from bleak import BleakClient

speed =["0004","0105","0206","0307","0408","0509","060a","070b","080c","090d","0a0e","0b0f","0c10","0d11","0e12","0f13","1014","1115","1216","1317","1418","1519","161a","171b","181c","191d","1a1e","1b1f","1c20","1d21","1e22","1f23","2024","2125","2226","2327","2428","2529","262a","272b","282c","292d","2a2e","2b2f","2c30","2d31","2e32","2f33","3034","3135","3236","3337","3438","3539","363a","373b","383c","393d","3a3e","3b3f","3c40","3d41","3e42","3f43","4044","4145","4246","4347","4448","4549","464a","474b","484c","494d","4a4e","4b4f","4c50","4d51","4e52","4f53","5054","5155","5256","5357","5458","5559","565a","575b","585c","595d","5a5e","5b5f","5c60","5d61","5e62","5f63","6064","6165","6266","6367","6468"]
address = "mac address"
uuid = "0000ffe9-0000-1000-8000-00805f9b34fb"
base = "aa040206"

async def main(address):
    async with BleakClient(address) as client:
        async def set_speed(percentage):
            percentage=int(percentage)
            if (percentage<0):
                percentage=0
            if (percentage>100):
                percentage=100
            param = bytes.fromhex("aa04"+speed[percentage])
            await client.write_gatt_char(uuid, param)
            print(param)
            print("Speed: "+str(percentage))

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
        time.sleep(4)
        await sawtoothWaveUp(20,5,20,4)
        print("Stopping")
        await set_speed(0)

asyncio.run(main(address))