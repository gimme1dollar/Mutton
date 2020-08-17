import numpy as np
import serial
import struct
import matplotlib as plt

plt.ion()
fig = plt.figure()

try:
   ser = serial.Serial("COM6", 115200, timeout = 1)
   print(f"serial upen? {ser.isOpen()}")
except:
   print("serial error")

i = 0
x = []
while True:
   message=[]
   for t in range(500):
      tmp = ser.read(4)
      tmp = struct.unpack('f', tmp)
      message.append(tmp)
   print(f"{message}\n")

   # graph plotting
   plt.axis([i-5000, i+5000, -3, 3])

   x.append(i)
   plt.scatter(x, message)
   i += 500
   plt.show()
