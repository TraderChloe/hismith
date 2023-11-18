import asyncio
import string
from time import sleep
import time
import math
import random
import serial
from bleak import BleakClient

speed =["0004","0105","0206","0307","0408","0509","060a","070b","080c","090d","0a0e","0b0f","0c10","0d11","0e12","0f13","1014","1115","1216","1317","1418","1519","161a","171b","181c","191d","1a1e","1b1f","1c20","1d21","1e22","1f23","2024","2125","2226","2327","2428","2529","262a","272b","282c","292d","2a2e","2b2f","2c30","2d31","2e32","2f33","3034","3135","3236","3337","3438","3539","363a","373b","383c","393d","3a3e","3b3f","3c40","3d41","3e42","3f43","4044","4145","4246","4347","4448","4549","464a","474b","484c","494d","4a4e","4b4f","4c50","4d51","4e52","4f53","5054","5155","5256","5357","5458","5559","565a","575b","585c","595d","5a5e","5b5f","5c60","5d61","5e62","5f63","6064","6165","6266","6367","6468"]
address = "20:22:08:24:07:E9"
uuid = "0000ffe9-0000-1000-8000-00805f9b34fb"
base = "aa040206"

async def button_press_time(ser):
    ser.reset_input_buffer()
    await asyncio.gather(button_reader(ser))
    ser.reset_input_buffer()
    await asyncio.gather(button_reader(ser))
    print("press1")
    ser.reset_input_buffer()
    last_press_time = time.perf_counter()
    await asyncio.gather(button_reader(ser))
    current_time = time.perf_counter()
    time_between_presses = (current_time - last_press_time) * 1000
    print(f'Time between presses: {time_between_presses:.2f} milliseconds')
    return time_between_presses

async def button_reader(ser):
    while True:
        while ser.in_waiting > 0:
            data = await asyncio.to_thread(ser.readline)
            data1 = data.decode('utf-8').strip()
            if 'B' in data1:
                return
        await asyncio.sleep(0.001)


async def rng(n):
   start = 0
   end = n - 1
   random_number = random.randint(start, end)
   return random_number

async def main (address):
    serial_port = 'COM3'  # Example port, adjust as needed
    baudrate = 9600  # Adjust as needed

    # Create a serial connection
    ser = serial.Serial(serial_port, baudrate)#, timeout=1)

    # Start the button reader in the background
    asyncio.create_task(button_reader(ser))

    async with BleakClient(address) as client:

        async def linearRamp(start_speed,end_speed,seconds):
            if start_speed<end_speed:
                change=end_speed-start_speed
                increment=seconds/change
                current_speed=start_speed
                for i in range(change):
                    current_speed=current_speed+1
                    await set_speed(current_speed)
                    sleep(increment)
            elif start_speed>end_speed:
                change=start_speed-end_speed
                increment=seconds/change
                current_speed=start_speed
                for i in range(change):
                    current_speed=current_speed-1
                    await set_speed(current_speed)
                    sleep(increment)

        async def sawtoothWaveUp(t, lSpeed, hSpeed, teeth): 
            tPerTooth = t / teeth
            speedRange = hSpeed - lSpeed
            tPerSpeedIncrement = tPerTooth / speedRange
            for i in range(teeth):
                 for o in range(speedRange + 1):
                     currentSpeed = lSpeed + o
                     await hismith(currentSpeed)
                     time.sleep(tPerSpeedIncrement)

        async def sawtoothWaveDown(t, lSpeed, hSpeed, teeth): 
             tPerTooth = t / teeth
             speedRange = hSpeed - lSpeed
             tPerSpeedDecrement = tPerTooth / speedRange
             for i in range(teeth):
                for o in range(speedRange + 1):
                    currentSpeed = hSpeed - o
                    await hismith(currentSpeed)
                    time.sleep(tPerSpeedDecrement)

        async def bluntSawtoothWaveDown(t, lSpeed, hSpeed, teeth,bluntPct): 
            tPerTooth = t / teeth
            tPerBlunt=tPerTooth*bluntPct
            tPerRampDown=tPerTooth-tPerBlunt
            speedRange = hSpeed - lSpeed
            tPerSpeedDecrement = tPerRampDown / speedRange
            for i in range(teeth):
                stage=0
                if (stage==0):
                    await hismith(hSpeed)
                    time.sleep(tPerBlunt)
                    stage=1
                if(stage==1):
                 for o in range(speedRange + 1):
                    currentSpeed = hSpeed - o
                    await hismith(currentSpeed)
                    time.sleep(tPerSpeedDecrement)

        async def bluntSawtoothWaveUp(t, lSpeed, hSpeed, teeth,bluntPct): 
            tPerTooth = t / teeth
            tPerBlunt=tPerTooth*bluntPct
            tPerRampUp=tPerTooth-tPerBlunt
            speedRange = hSpeed - lSpeed
            tPerSpeedIncrement = tPerRampUp / speedRange
            for i in range(teeth):
                stage=0
                if (stage==0):
                    await hismith(hSpeed)
                    time.sleep(tPerBlunt)
                    stage=1
                if(stage==1):
                 for o in range(speedRange + 1):
                    currentSpeed = lSpeed + o
                    await hismith(currentSpeed)
                    time.sleep(tPerSpeedIncrement)

        async def squareWave(t, lSpeed, hSpeed, squareCount):
            tPerSquare = t / squareCount
            quarterTPerSquare=tPerSquare/4
            for i in range(squareCount):
                await hismith(lSpeed)
                time.sleep(quarterTPerSquare)
                await hismith(hSpeed)
                time.sleep(quarterTPerSquare*2)
                await hismith(lSpeed)
                time.sleep(quarterTPerSquare)

        async def triangleWave(t, lSpeed, hSpeed, triangleCount): 
            tPerTriangle = t / triangleCount
            speedRange = hSpeed - lSpeed
            tPerSpeedIncrement = tPerTriangle / speedRange/2
            for i in range(triangleCount):
                stage=0
                if (stage==0):
                    for o in range(speedRange + 1):
                        currentSpeed = lSpeed + o
                        await hismith(currentSpeed)
                        time.sleep(tPerSpeedIncrement)
                    stage=1
                if(stage==1):
                 for o in range(speedRange + 1):
                    currentSpeed = hSpeed - o
                    await hismith(currentSpeed)
                    time.sleep(tPerSpeedIncrement)

        async def sawtoothWaveRampUp(t, lSpeed, hSpeed, teeth,hIncrement): 
            tPerTooth = t / teeth
            speedRange = hSpeed - lSpeed
            for i in range(teeth):
                tPerSpeedIncrement = tPerTooth / speedRange
                for o in range(speedRange + 1):
                    currentSpeed = lSpeed + o
                    await hismith(currentSpeed)
                    time.sleep(tPerSpeedIncrement)
                speedRange=speedRange+hIncrement

        async def hismith(s):
                 await set_speed(s)

        async def set_speed(percentage):
            param = bytes.fromhex("aa04"+speed[percentage])
            model_number = await client.write_gatt_char(uuid, param)

        async def rampArray(array):
            for i in range(len(array)):
                await linearRamp(array[i][0],array[i][1],array[i][2])
                sleep(array[i][3])
  
        testing=[
            [0,4,5,20],
            [4,2,30,20],   
        ]

        
        print("Start")

        async def measure(s):
            await set_speed(s)
            print("Measuring rotation speed")
            time_between_presses = await button_press_time(ser)
            print(f'Total time between two button presses: {time_between_presses:.2f} milliseconds')
            return int(time_between_presses)
        
        #its called exciting cause its the new math thing
        async def exciting(t,inSpeed,outSpeed):
            await set_speed(inSpeed)
            sleep(int(t)/1000)
            await set_speed(outSpeed)
            ser.reset_input_buffer()
            await asyncio.gather(button_reader(ser))

        #repeating the exciting function
        async def repeatE(c,th,ti,inS,osS):
            #dividing by a thing, this should be calculated but its manual for now
            th=th/ti
            for _ in range(c):
                await exciting(th,inS,osS)


        #if I instantly start to measure stuff then it glicthes out
        #so letting it run a tiny bit to clear out the bugs x3
        await set_speed(10)
        sleep(6)

        
        await set_speed(0)
        s30=await measure(30)
        await set_speed(0)
        sleep(2)
        s20=await measure(20)
        await set_speed(0)
        sleep(2)
        s4=await measure(4)
        await set_speed(0)
        sleep(2)
        #s50=await measure(50)
        #await set_speed(0)
        print(s20)
        print(s30)
        #print(s50)
        print(s4)
        sleep(3)
        #completed measurements
        
        await repeatE(15,s20,4,20,4)
        # (count of rotations, 
        # time per rotation at speed 20,
        #  time divided by this, #cause of inertia, basically turn the speed up for a short amount of time and it coasts
        #  speed going in,
        #  speed coming out)

        #different tests
        #await repeatE(15,s4,1,4,30)
        #await repeatE(20)
        #await rampArray(training)
        #await bluntSawtoothWaveDown(30,10,20,5,0.4)


        print("Stopping")
        await set_speed(0)

        #this currently just errors or glitches out
        try:
            await asyncio.gather(button_reader)
        except asyncio.CancelledError:
            print("Task was canceled")

asyncio.run(main(address))
