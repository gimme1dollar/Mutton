import numpy as np
import serial
import os
import time
import matplotlib.pyplot as plt

try:
    ser = serial.Serial("COM6", 115200, timeout=1)
    print(f"serial open? {ser.isOpen()}")
except:
    print("serial error")

result_list = []  # [time, gesture, ch1, ch2, ch1, ch2, ..., ch1, ch2]
setTime = 2  # [s]
preparationTime = 1  # [s]
# window_size = 60  # Number of EMG Samples in one CNN input
ch_n = 2
gesture_name = ['Noise', 'Fist', 'Hand', 'Index Finger', 'Middle Finger', 'Little Finger']
data_iter = 5

now = index_time = time.time()

## Collecting Data
for num in range(data_iter):
    print(f"===========Step {num}/{data_iter}===========")

    for iii in range(1, len(gesture_name)):
        ### Pause
        start_time = now
        print(f"pause for now...")
        temp = []
        while now - start_time < setTime:
            temp.extend([float(i) for i in ser.readline().decode().strip().split(',')[0:ch_n]])
            now = time.time()
        result_list.append([now - index_time, 0] + temp)
        '''
        temp = []
        for i in range(window_size):
            temp.extend([float(i) for i in ser.readline().decode().strip().split(',')[0:ch_n]])
            
        now = time.time()
        result_list.append([now - index_time, 0] + temp)
        '''


        ### Collect Gesture Data
        start_time = now
        print(f"Get ready for gesture: {gesture_name[iii]}")
        temp = []
        while now - start_time < preparationTime:
            temp.extend([float(i) for i in ser.readline().decode().strip().split(',')[0:ch_n]])
            now = time.time()
        start_time = now
        print(f"Collecting gesture: {gesture_name[iii]}")
        while now - start_time < setTime:
            temp.extend([float(i) for i in ser.readline().decode().strip().split(',')[0:ch_n]])
            # print(f"Collecting gesture {gesture_name[iii]} : {temp}")
            now = time.time()
        result_list.append([now - index_time, iii] + temp)
        '''
        temp = []
        for i in range(window_size):
            temp.extend([float(i) for i in ser.readline().decode().strip().split(',')[0:ch_n]])
            print(f"Collecting gesture {iii+1} : {temp}")
        now = time.time()
        result_list.append([now - index_time, iii] + temp)
        '''


### Saving Data
path = os.getcwd() + "\\data\\tmp\\"
file_name = time.strftime("%Y%m%d_%H%M%S") + ".txt"
print(path+file_name)
with open(path + file_name, 'w') as f:
    for data in result_list:
        s = ", ".join(map(str, data))
        f.write("%s\n" % s)
f.close()
# fmt = '%f, %f, %f, %d'
# fmt = "%s"
# np.savetxt(path, result_list, fmt=fmt, delimiter=',')



### Graph Plotting
plot_index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]]
label_num = [0] * len(gesture_name)
fig, axs = plt.subplots(2, 3, figsize=(30, 20))
fig.suptitle('Sampled EMG Ch1', fontsize=20)
for data in result_list:
    axs[plot_index[data[1]][0], plot_index[data[1]][1]].plot(range(len(data[2::2])), data[2::2], label=f"{data[1]}_#{label_num[data[1]]}")
    label_num[data[1]] += 1
'''
for data in result_list:
    if data[1] == 0:
        label_num[0] += 1
        axs[0, 0].plot(range(window_size), data[2::2], label=f"0_#{label_num[0]}")
    elif data[1] == 1:
        label_num[1] += 1
        axs[0, 1].plot(range(window_size), data[2::2], label=f"1_#{label_num[1]}")
    elif data[1] == 2:
        label_num[2] += 1
        axs[0, 2].plot(range(window_size), data[2::2], label=f"2_#{label_num[2]}")
    elif data[1] == 3:
        label_num[3] += 1
        axs[1, 0].plot(range(window_size), data[2::2], label=f"3_#{label_num[3]}")
    elif data[1] == 4:
        label_num[4] += 1
        axs[1, 1].plot(range(window_size), data[2::2], label=f"4_#{label_num[4]}")
    elif data[1] == 5:
        label_num[5] += 1
        axs[1, 2].plot(range(window_size), data[2::2], label=f"5_#{label_num[5]}")
'''

i = 0
for ax in axs.flat:
    ax.set(xlabel='Time', ylabel='Amplitude', ylim=(0, 1))
    ax.set_title(gesture_name[i])
    ax.label_outer()
    ax.legend(loc="upper right")
    i += 1

label_num = [0] * len(gesture_name)
fig, axs = plt.subplots(2, 3, figsize=(30, 20))
fig.suptitle('Sampled EMG Ch2', fontsize=20)
for data in result_list:
    axs[plot_index[data[1]][0], plot_index[data[1]][1]].plot(range(len(data[3::2])), data[3::2], label=f"{data[1]}_#{label_num[data[1]]}")
    label_num[data[1]] += 1
'''
for data in result_list:
    if data[1] == 0 or data[1] == 1:
        label_num[0] += 1
        axs[0, 0].plot(range(window_size), data[3::2], label=f"0_#{label_num[0]}")
    elif data[1] == 2:
        label_num[1] += 1
        axs[0, 1].plot(range(window_size), data[3::2], label=f"1_#{label_num[1]}")
    elif data[1] == 3:
        label_num[2] += 1
        axs[0, 2].plot(range(window_size), data[3::2], label=f"2_#{label_num[2]}")
    elif data[1] == 4:
        label_num[3] += 1
        axs[1, 0].plot(range(window_size), data[3::2], label=f"3_#{label_num[3]}")
    elif data[1] == 5:
        label_num[4] += 1
        axs[1, 1].plot(range(window_size), data[3::2], label=f"4_#{label_num[4]}")
    elif data[1] == 6:
        label_num[5] += 1
        axs[1, 2].plot(range(window_size), data[3::2], label=f"5_#{label_num[5]}")
'''

i = 0
for ax in axs.flat:
    ax.set(xlabel='Time', ylabel='Amplitude', ylim=(0, 1))
    ax.set_title(gesture_name[i])
    ax.label_outer()
    ax.legend(loc="upper right")
    i += 1
