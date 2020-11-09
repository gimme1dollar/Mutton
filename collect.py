import serial
import os
import time
import matplotlib.pyplot as plt


# Open Serial Port
try:
    ser = serial.Serial("COM6", 115200, timeout=1)
    print(f"serial open? {ser.isOpen()}")
except:
    print("serial error")

result = []  # [time, gesture, ch1, ch2, ch1, ch2, ..., ch1, ch2]
collectingTime = 2  # Time for Sampling [s]
preparationTime = 2  # Time for next gesture preparation[s]
n_ch = 2  # number of channel
gesture_name = ['Noise', 'Fist', 'Hand', 'Index Finger', 'Middle Finger', 'Little Finger']
data_iter = 5  # number of sampling loop   

# find current time
now = index_time = time.time()

# Collect sEMG data
for num in range(data_iter):
    print(f"===========Step {num+1}/{data_iter}===========")

    for iii in range(1, len(gesture_name)):
        # Collect noisy sEMG
        start_time = now
        print(f"pause for now...")
        temp = []
        while now - start_time < collectingTime:
            temp.extend([float(i) for i in ser.readline().decode().strip().split(',')[0:n_ch]])
            now = time.time()

        # Add noisy sEMG to result
        result.append([now - index_time, 0] + temp)

        # Collect gesture sEMG
        start_time = now
        print(f"Get ready for gesture: {gesture_name[iii]}")
        temp = []
        while now - start_time < preparationTime:
            temp.extend([float(i) for i in ser.readline().decode().strip().split(',')[0:n_ch]])
            now = time.time()
        start_time = now
        print(f"Collecting gesture: {gesture_name[iii]}")
        while now - start_time < collectingTime:
            temp.extend([float(i) for i in ser.readline().decode().strip().split(',')[0:n_ch]])
            # print(f"Collecting gesture {gesture_name[iii]} : {temp}")
            now = time.time()
        start_time = now
        while now - start_time < preparationTime:
            temp.extend([float(i) for i in ser.readline().decode().strip().split(',')[0:n_ch]])
            now = time.time()

        # Add gesture sEMG to result
        result.append([now - index_time, iii] + temp)

# Save Data
path = os.getcwd() + "\\data\\tmp\\"
file_name = time.strftime("%Y%m%d_%H%M%S") + ".txt"
print(path+file_name)
with open(path + file_name, 'w') as f:
    for data in result:
        s = ", ".join(map(str, data))
        f.write("%s\n" % s)
f.close()

# Plot Graph
plot_index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]]
label_num = [0] * len(gesture_name)
fig, axs = plt.subplots(2, 3, figsize=(30, 20))
fig.suptitle('Sampled EMG Ch1', fontsize=20)
for data in result:
    g = int(data[1])
    axs[plot_index[g][0], plot_index[g][1]].plot(range(len(data[2::2])), data[2::2], label=f"{g}_#{label_num[g]}")
    label_num[g] += 1

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
for data in result:
    g = int(data[1])
    axs[plot_index[g][0], plot_index[g][1]].plot(range(len(data[3::2])), data[3::2], label=f"{g}_#{label_num[g]}")
    label_num[g] += 1

i = 0
for ax in axs.flat:
    ax.set(xlabel='Time', ylabel='Amplitude', ylim=(0, 1))
    ax.set_title(gesture_name[i])
    ax.label_outer()
    ax.legend(loc="upper right")
    i += 1
