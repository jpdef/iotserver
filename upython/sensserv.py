import uasyncio as asyncio
import errno
import sensor
import gc 

class server:
    
    def __init__(self,sensor):
        self.sensor = sensor
        self.dpt = 0 

    async def handle(self,reader,writer):
        while True:
            await asyncio.sleep(5)
            msg = "{\"rdbk\":%f}" % (self.dpt)
            print(msg)
            try:
                yield from writer.awrite(msg)
            except OSError as e:
                print('Client Disconnected')
                yield from writer.aclose()
                break
        

    async def readback_loop(self):
        while True:
             await asyncio.sleep(1)
             self.dpt = (self.dpt + self.sensor.readback())/2
   

    def run(self):
        gc.enable
        loop   = asyncio.get_event_loop()
        coro   = asyncio.start_server(self.handle, '0.0.0.0', 9999)
        serv_task   = loop.create_task(coro)
        rdbk_task   = loop.create_task(self.readback_loop())
        
        
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        
        # Close the server
        loop.close()

