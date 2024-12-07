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
                     await set_speed(currentSpeed)
                     time.sleep(tPerSpeedIncrement)

        async def sawtoothWaveDown(t, lSpeed, hSpeed, teeth): 
             tPerTooth = t / teeth
             speedRange = hSpeed - lSpeed
             tPerSpeedDecrement = tPerTooth / speedRange
             for i in range(teeth):
                for o in range(speedRange + 1):
                    currentSpeed = hSpeed - o
                    await set_speed(currentSpeed)
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
                    await set_speed(hSpeed)
                    time.sleep(tPerBlunt)
                    stage=1
                if(stage==1):
                 for o in range(speedRange + 1):
                    currentSpeed = hSpeed - o
                    await set_speed(currentSpeed)
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
                    await set_speed(hSpeed)
                    time.sleep(tPerBlunt)
                    stage=1
                if(stage==1):
                 for o in range(speedRange + 1):
                    currentSpeed = lSpeed + o
                    await set_speed(currentSpeed)
                    time.sleep(tPerSpeedIncrement)

        async def squareWave(t, lSpeed, hSpeed, squareCount):
            tPerSquare = t / squareCount
            quarterTPerSquare=tPerSquare/4
            for i in range(squareCount):
                await set_speed(lSpeed)
                time.sleep(quarterTPerSquare)
                await set_speed(hSpeed)
                time.sleep(quarterTPerSquare*2)
                await set_speed(lSpeed)
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
                        await set_speed(currentSpeed)
                        time.sleep(tPerSpeedIncrement)
                    stage=1
                if(stage==1):
                 for o in range(speedRange + 1):
                    currentSpeed = hSpeed - o
                    await set_speed(currentSpeed)
                    time.sleep(tPerSpeedIncrement)

        async def sawtoothWaveRampUp(t, lSpeed, hSpeed, teeth,hIncrement): 
            tPerTooth = t / teeth
            speedRange = hSpeed - lSpeed
            for i in range(teeth):
                tPerSpeedIncrement = tPerTooth / speedRange
                for o in range(speedRange + 1):
                    currentSpeed = lSpeed + o
                    await set_speed(currentSpeed)
                    time.sleep(tPerSpeedIncrement)
                speedRange=speedRange+hIncrement