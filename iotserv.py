import asyncio
import json
from aiohttp import web
import socketio
import numpy as np
import timeseries

ts  = timeseries.series()
sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)


async def readfromesp():
    """
       Reads from IoT device, stores data in timeseries class, and 
       broads data to websocket 
    """
    try:
        reader, writer = await asyncio.open_connection("192.168.0.112",9999) 
        while True:
            await asyncio.sleep(1)
            raw = await reader.read(100)
            data = json.loads(raw.decode())
            print(data['rdbk'])
            ts.add(dpt(data['rdbk']))
            await sio.emit('my response', {'data': data['rdbk']},
                           namespace='/test')
    except Exception as e:
        print("Could not connect to device" , e)


async def randgen():
    """Example of how to send server generated events to clients."""
    while True:
        await asyncio.sleep(1)
        data = np.random.rand()
        await sio.emit('my response', {'data': 'Server generated event %f' %  data},
                       namespace='/test')


async def index(request):
    with open('app.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('connect', namespace='/test')
async def test_connect(sid, environ):
    await sio.emit('my response', {'data': 'Connected', 'count': 0}, 
                   namespace='/test')

@sio.on('disconnect request', namespace='/test')
async def disconnect_request(sid):
    await sio.disconnect(sid, namespace='/test')




app.router.add_get('/', index)

if __name__ == '__main__':
    sio.start_background_task(readfromesp)
    web.run_app(app)
