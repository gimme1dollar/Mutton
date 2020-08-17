import numpy as np
import serial
import time
import struct

try:
   ser = serial.Serial("COM6", 115200, timeout = 1)
   print(f"serial open? {ser.isOpen()}")
except:
   print(f"serial error")

   

while True:
   label = []
   message = []
   for i in range(500):
      tmp = np.random.random()
      label.append(tmp)
      tmp = struct.pack('f', tmp)
      ser.write(tmp)
      message.append(tmp)
   print(f"writer sending : {label}\n")
   #ser.write(b'\n')
    
