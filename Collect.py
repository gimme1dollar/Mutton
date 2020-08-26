import numpy as np
import serial
import struct
import time
import os
import time

try:
    ser = serial.Serial("COM6", 115200, timeout=1)
    print(f"serial open? {ser.isOpen()}")
except:
    print("serial error")


result_list = [] # [index, gesture, [ch1, ch2], [ch1, ch2]...]
flag = False
setTime = 4  # [s]
window_length = 10  # Number of EMG Samples in one CNN input
ch_n = 2
normalized = 200 #[uV]
gesture_n = 5
data_iter = 1

now = start_time = index_time = time.time()

## Collecting Data
for _ in range(data_iter):

    # 제스처는 총 5개
    # 0 - noise
    # 1 - 주먹
    # 2 - 손바닥펴기
    # 3 - 검지로 ㅇㅋ 사인
    # 4 - 중지로 ㅇㅋ 사인
    # 5 - 약지로 ㅇㅋ 사인
    iii = 0  # gesture index

    while iii < gesture_n + 1:
        ### Data Collecting Window (0~setTime)
        print(f"Collecting gesture {iii}")
        while now - start_time < setTime:
            temp = []
            for i in range(window_length):
                temp.extend([normalized * float(i) for i in ser.readline().decode().strip().split(',')[0:ch_n]])
                print(f"Collecting gesture {iii} : {temp}")
            now = time.time()
            result_list.append([now - index_time, iii+1] + temp)


        ### Pausing Window (setTime~2*setTime)
        print(f"pause for now...")
        while now - start_time < 2 * setTime:
            temp = []
            for i in range(window_length):
                temp.extend([normalized * float(i) for i in ser.readline().decode().strip().split(',')[0:ch_n]])
            now = time.time()
            result_list.append([now - index_time, 0] + temp)


        ### Repeating
        start_time = now
        iii += 1

### Data 저장
timestr = time.strftime("%Y%m%d_%H%M%S")
path = os.getcwd() + "\\data\\tmp\\" + timestr + ".txt"
print(path)
#fmt = '%f, %f, %f, %d'
fmt = "%s"
np.savetxt(path, result_list, fmt=fmt, delimiter=',')
