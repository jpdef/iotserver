import time

class datapoint:
    def __init__(self,num):
        self.num  = num
        self.time = time.time()
    
    def set(self,num):
        self.num = num
        self.time= time.time()

    def get(self):
        return (self.num, self.time)



class series:
    def __init__(self,buff_len=288): # 288= 24*6 = 1day 5 min measurements
        self.buff_index = 0
        self.buff_len = buff_len 
        self.buffer = [ datapoint(0) for x in range(0,self.buff_len) ] 
        self.avg  =  0
        self.low  =  0
        self.high =  0
        self.curr = datapoint(0)
        self.itr = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.itr == self.buff_len:
            self.itr = 0
            raise StopIteration
        else:
            self.itr += 1
            return self.buffer[self.itr-1]

    def add(self,dpt):
        self.curr = dpt
        self.set_stats(dpt)
        delta_sec = dpt.get()[1] - self.buffer[self.buff_index].get()[1]  
        print("delta seconds" , delta_sec)
        if ( delta_sec >= 30 ) : 
            print("adding to buffer")
            self.add_buffer()

    def add_buffer(self):
        self.buff_index += 1
        if self.buff_index == self.buff_len :
           self.buff_index = 0
        self.buffer[self.buff_index] = datapoint(self.avg)


    def get(self):
        return self.buffer
    
    def set_stats(self,dpt):
        num,time = dpt.get()
        self.avg  = (self.avg + num )/2.0
        self.low  = num if self.low > num else self.low
        self.high = num if self.high < num else self.high

    def get_stats(self):
        return [self.avg,self.low,self.high]

    def get_dpt(self):
        return self.curr


