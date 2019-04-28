
class sensor(object):
    def __init__(self,name):
        self.name  = name 
    
    def readback(self):
        return 0

class dhtsensor(sensor):
    
    def __init__(self):
        import dht
        import machine
        self.device   = dht.DHT11(machine.Pin(2))
    
    def readback(self):
        self.device.measure()
        return 9*self.device.temperature()/5 + 32

class randsensor(sensor):
    
    def __init__(self,name):
        import numpy as np
        self.rand = np.random
    
    def readback(self):
        return self.rand.rand()

