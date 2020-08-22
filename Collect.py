import numpy as np
import serial
import struct
import time
import os
import time

try:
   ser = serial.Serial("COM6", 115200, timeout = 1)
   print(f"serial upen? {ser.isOpen()}")
except:
   print("serial error")

RESULTTTTTT = []
flag = False

setTime = 2


index_time = time.time()
start_time = time.time()


## Collecting Data
for _ in range(5):

   
   iii = 0 # gesture index

   
   while True:
      now = time.time()
      emgSignal = ser.readline()


         
      ### Data Collecting Window (0~10s)
      if now - start_time < setTime:
         print(f"Collecting gesture {iii} : {emgSignal}")

         # [index, serial데이터, 제스처]로 구성된 array
         RESULTTTTTT.append([index_time - now, emgSignal, iii+1]) 



         
      ### Pausing Window (10~20s)
      elif now - start_time > setTime and now - start_time < 2 * setTime :
         print(f"puase for now...")
         RESULTTTTTT.append([index_time - now, emgSignal, 0])



      ### Repeating   
      else :
         start_time = now
         iii += 1
         # 제스처는 총 5개
         # 0 - 주먹
         # 1 - 손바닥펴기
         # 2 - 검지로 ㅇㅋ 사인
         # 3 - 중지로 ㅇㅋ 사인
         # 4 - 약지로 ㅇㅋ 사인
         if iii > 5: 
            break





### Data 저장
timestr = time.strftime("%Y%m%d_%H%M%S")
PATHHHHHH = os.getcwd() + "\\data\\tmp\\" + timestr + ".txt"
print(PATHHHHHH)
fmt='%s, %s, %s'
np.savetxt(PATHHHHHH, RESULTTTTTT, delimiter=',', fmt=fmt)

      




