import io
import sys
import math
import struct
import random
import winsound
import wave
from tkinter import Tk, Canvas, Frame, BOTH

class Example(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.initUI()
        self.canvas = Canvas(self)
        self.xprev = 0
        self.yprev = 200

    def initUI(self):
        self.parent.title("Waveform")
        self.pack(fill=BOTH,expand=1)
        

    def drawLine(self,amplitude):
        newy = scale_to(240,10,-32767,32767,amplitude)
        #print([self.xprev,self.yprev,self.xprev+10,newy])
        self.canvas.create_line(self.xprev,self.yprev,self.xprev+1,int(newy))
        self.xprev += 1
        self.yprev = newy
        self.canvas.pack(fill=BOTH,expand=1)
        
byteOrder = 'little'

def mult(x,y):
    return x*y

def generate_list(length, type_of):
    list_ = list()
    if type_of == 'zeros':
        list_ = [0 for i in range(length)]
    elif type_of == 'ones':
        list_ = [1 for i in range(length)]
    elif type_of == 'rand':
        list_ = [random.random() for i in range(length)]
    elif type_of == 'closed_harmonic':
        list_ = [i for i in range(1,length*2,2)]
    elif type_of == 'open_harmonic':
        list_ = [i for i in range(1,length+1)]
    return list_

def generate_ratios(list_):
    total = 0
    for i in range(len(list_)):
        total += list_[i].amplitude
    if total != 0:
        ratio = [x.amplitude/total for x in list_]
    else:
        ratio = [0 for i in range(len(list_))]
    return ratio

def apply_to_list(func, list_, *args):
    for i in range(len(list_)):
        list_[i] = func(list_[i],*args)
    return list_

def write_mono_float_to_file(file, channels, value):
    for i in range(channels):
        file.write(int(value).to_bytes(2,byteorder = byteOrder,signed = True))

class oscillator:
    """An oscillator class for waves"""
    def __init__(self,amplitude_=1,frequency_=1,phase_=0):
        self.amplitude = amplitude_
        self.frequency = frequency_
        self.phase     = phase_
    def get_value(self,time):
        return self.amplitude*math.sin(time*math.pi*2*self.frequency+self.phase)

def amplify(value, amplification):
    return value*amplification

def calc_max(osc):
    max_ = 0
    for i in range(len(osc)):
        max_ += osc[i].amplitude
    return max_

def calc_min(osc):
    min_ = 0
    for i in range(len(osc)):
        min_ -= osc[i].amplitude
    return min_

def scale_to(new_min,new_max,cur_min,cur_max,value):
    m = (new_max-new_min)/(cur_max-cur_min)
    b = new_max-(m*cur_max)
    return m*value+b

def outwav(screen):
    sampleRate = 44100 #HZ
    bitsPerSample = 16
    numChannels = 2
    fileSize = 0

    with open('sound.wav', 'wb') as file:
        header = struct.pack('4sI4s4sIHHIIHH4sI',
                    b'RIFF', # Magic Number
                    0,       # Size of file in byes
                    b'WAVE', # File Type Header
                    b'fmt ', # Format chunk marker
                    16,      # Length of format
                    1,       # Type of foramt
                    numChannels,
                    sampleRate,
                    int((sampleRate*bitsPerSample*numChannels)/8),
                    int((bitsPerSample*numChannels/8)),      
                    bitsPerSample,
                    b'data', # data chunk header
                    0        # Size of the data section
                    )
        file.write(header)
        fulloutput = bytearray()
        fulloutput += header

        #Variables
        numSeconds = 1
        numOscillators = 6
        t = 0
        y = 0
        base_frequency = 155
        
        osc = [oscillator(1,base_frequency*(i+1)) for i in range(0,numOscillators)]

        totalSamples = sampleRate*numSeconds
        #for i in range(numOscillators):
            #osc[i].phase = i * (math.pi/(100*random.random()))
            #osc[i].amplitude = 100/(i+10)

        osc[0].frequency = 330
        osc[1].frequency = 660
        osc[2].frequency = 990
        osc[3].frequency = 1320
        osc[4].frequency = 1650
        osc[5].frequency = 1980
        #osc[6].frequency = 0
        #osc[7].frequency = 0
        #osc[8].frequency = 0
        
        osc[0].amplitude = 1
        osc[1].amplitude = 1.3
        osc[2].amplitude = .42
        osc[3].amplitude = .3
        osc[4].amplitude = .2
        osc[5].amplitude = .07
        #osc[6].amplitude = 0
        #osc[7].amplitude = 0
        #osc[8].amplitude = 0
        
        max_value = calc_max(osc)
        min_value = calc_min(osc)


        output = bytearray()

        yprev = 0
        
        while t < numSeconds:
            
            for i in range(len(osc)):
                y += osc[i].get_value(t)

            max_value = calc_max(osc)
            min_value = calc_min(osc)
            if(random.random() == 0.992):
                osc[random.randrange(0,len(osc))].amplitude *= 1+(random.random()/10)
                #print(osc[random.randrange(0,len(osc))].amplitude)
            if(random.random() == 0.98):
                osc[random.randrange(0,len(osc))].amplitude /= 1+(random.random()/10)
            y = scale_to(-32767,32767,min_value,max_value,y)
            
            for i in range(numChannels):
                values = struct.pack('h',int(y))
                output += values
                fulloutput += values
                

            screen.drawLine(y)    
                
            t += (1/sampleRate)
            y = 0
            max_value = calc_max(osc)
            min_value = calc_min(osc)


        file.write(output)
        
        #Write actual size of file - 8
        fileSize = file.tell()
        file.seek(4)
        file.write(int(fileSize - 8).to_bytes(4,byteorder = byteOrder,signed = False))
        file.seek(40)
        file.write(int(fileSize - 44).to_bytes(4, byteorder = byteOrder, signed = False))

    
def main():
    root = Tk()
    ex = Example(root)
    root.geometry("400x250+300+300")
    outwav(ex)
    root.mainloop()

if __name__ == '__main__':
    main()
