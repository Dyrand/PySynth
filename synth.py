import io
import sys
import math
import struct
import random

byteOrder = 'little'
sampleRate = 44100 #HZ
bitsPerSample = 16
numChannels = 2
numSeconds = 4
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

    totalSamples = sampleRate*numSeconds
    

    frequency = 1000
    phase = math.pi
    
    t = 0
    y = 0
    generators = 6
    base_f = 320
    amplitude = list()
    for i in range(generators):
        amplitude.append(random.random())

    #amplitude = [
                 #random.random(),
                 #random.random(),
                 #random.random(),
                 #random.random(),
                 #random.random(),
                 #random.random(),
                #]
    for i in range(generators):
        amplitude[i] *= 1
        
    print(amplitude)
    total = sum(amplitude)
    ratio = [x/total for x in amplitude]


    frequency = list()
    for i in range(1,generators*2,2):
        frequency.append(i)
        
    frequency = [x*base_f for x in frequency]

    phase = [
             random.random(),
             random.random(),
             random.random(),
             random.random(),
             random.random(),
             random.random()
            ]
    
    while t < numSeconds:
        
        for i in range(0,generators):
            y += ratio[i]*32767*math.sin(t*math.pi*2*frequency[i] + phase[i])
        if y > 32767:
            y = 32767
        elif y < -32767:
            y = -32767
        
        file.write(int(y).to_bytes(2,byteorder = byteOrder,signed = True))
        file.write(int(y).to_bytes(2,byteorder = byteOrder,signed = True))
        t += (1/sampleRate)
        
        if t > 1 and t < 1.0001:
            base_f = 1.01
            for i in range(generators):
                frequency[i] *= base_f
        elif t > 2 and t < 2.0001:
            base_f = 1.01
            for i in range(generators):
                frequency[i] *= base_f
        elif t > 3 and t < 3.0001:
            base_f = 1.01
            for i in range(generators):
                frequency[i] *= base_f
                   
    #Write actual size of file - 8
    fileSize = file.tell()
    file.seek(4)
    file.write(int(fileSize - 8).to_bytes(4,byteorder = byteOrder,signed = False))
    file.seek(40)
    file.write(int(fileSize - 44).to_bytes(4, byteorder = byteOrder, signed = False))
    
    
