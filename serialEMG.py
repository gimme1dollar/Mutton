import numpy as np
import serial
import struct
import time

try:
   ser = serial.Serial("COM6", 115200, timeout = 1)
   print(f"serial upen? {ser.isOpen()}")
except:
   print("serial error")

i = 0
start_time = time.time()
message=[]
while True:
   message.append(ser.readline())


   print(f"{time.time() - start_time} : {len(message)}")
   
   '''
   for t in range(500):
      tmp = ser.read()
      tmp = struct.unpack('f', tmp)
      message.append(tmp)
   print(f"{message}\n")
   '''
