import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import serial
import os
import time
import keyboard
import random

## Open Serial Port
try:
    ser = serial.Serial("COM6", 115200, timeout=1)
    print(f"serial open? {ser.isOpen()}")
except:
    print("serial error")

## Initial Setting
#gesture_name = ['Noise', 'Fist', 'Index Finger', 'Middle Finger', 'Ring Finger', 'Little Finger', 'Hand']
gesture_name = ['Noise', 'Fist', 'Hand', 'Index Finger', 'Middle Finger', 'Little Finger']
gesture_iter = 20       # Number of gesture sampling
ch_n = 2
update_len = 1          # Number of EMG Samples before updating CNN input, set for latency 0.1s
true_glab_list = [0]    # True Gesture Label
pred_glab_list = [0]    # Model Prediction Gesture Label
acc = [0.0]             # Realtime Model Accuracy


# Generate Random gesture label
g_label = [0]
for i in range(gesture_iter-1):
    tmp = random.randrange(0, len(gesture_name), 1)
    while tmp == g_label[i] :
        tmp = random.randrange(0, len(gesture_name), 1)
    g_label.append(tmp)


## Load Trained Model
path = os.getcwd() + "\\data\\Model\\"
model = tf.keras.models.load_model(path+'my_model')
model.summary()
seq_len = model.layers[0].input.shape[1]  # CNN input size(window size)


## Receive EMG from Cyton Board
emgSignal = np.empty([1, seq_len, ch_n])
start = time.time()
for i in range(seq_len):
    emgSignal[0, i, :] = [float(i) for i in ser.readline().decode().strip().split(',')[0:ch_n]]
now = time.time()
print(f"Full Data Received : {now - start}s")


fig, (ax1, ax2) = plt.subplots(1, 2)
graph_x = [0]
for ii in range(gesture_iter):
    '''
    if keyboard.is_pressed('q'):
        print(f"Exit Program")
        break
    elif keyboard.is_pressed('a'):
        print(f"Press s to continue...")
        while True:
            if keyboard.is_pressed('s'):
                break
    '''

    # Pause to flush emgSignal
    print("pause for now...")
    tol = 0
    while tol <= 1:
        start = time.time()
        emgSignal = np.append(emgSignal, [[[float(i) for i in ser.readline().decode().strip().split(',')[0:ch_n]]]],
                              axis=1)
        emgSignal = np.delete(emgSignal, 0, axis=1)
        tol += time.time() - start

    print(f"Get ready for gesture: {gesture_name[g_label[ii]]}")
    time.sleep(2)

    # Receiving Signal and Classifying
    print(f"Collecting gesture: {gesture_name[g_label[ii]]}")
    tol = 0
    while tol <= 3:
        start = time.time()
        for i in range(update_len):
            emgSignal = np.append(emgSignal, [[[float(i) for i in ser.readline().decode().strip().split(',')[0:ch_n]]]],
                                  axis=1)
        emgSignal = np.delete(emgSignal, np.s_[0:update_len], axis=1)

        # Gesture Classification
        predictions = model.predict(emgSignal)[0]
        pred_g_label = int(np.where(predictions == max(predictions))[0])

        # Save Results
        pred_glab_list.append(pred_g_label)
        true_glab_list.append(g_label[ii])
        if pred_g_label == g_label[ii]:
            acc.append((len(acc)*acc[-1] + 1)/(len(acc)+1))
        else:
            acc.append((len(acc)*acc[-1])/(len(acc)+1))

        graph_x.append(ii)
        '''
        # Realtime Graph Plotting
        ax1.plot(graph_x, acc)
        ax1.lines[0].set_xdata(graph_x)
        ax1.lines[0].set_ydata(acc)

        line1, = ax2.plot(graph_x, pred_glab_list)
        line2, = ax2.plot(graph_x, true_glab_list)
        ax2.legend((line1, line2), ('prediction', 'true'))
        ax2.lines[0].set_xdata(graph_x)
        ax2.lines[0].set_ydata(pred_glab_list)

        fig.gca().relim()
        fig.gca().autoscale_view()
        plt.pause(0.0001)
        '''
        tol += time.time() - start
        # Show Result
        print("Eclipsed Time : {:.3f} \t Predicted: {:d} \t True: {:d} \t Accuracy : {:.3f}".format(tol, pred_g_label, g_label[ii], acc[-1]))


print("Realtime Accuracy : {:.3f}".format(acc[-1]))

# Plot Graph
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(graph_x, acc)
line1, = ax2.plot(graph_x, pred_glab_list)
line2, = ax2.plot(graph_x, true_glab_list[:len(true_glab_list)])
ax2.legend((line1, line2), ('prediction', 'true'), loc = 'upper right')
plt.show()

# Plot Graph
fig = plt.figure()
line1, = plt.plot(graph_x, pred_glab_list)
line2, = plt.plot(graph_x, true_glab_list[:len(true_glab_list)])
fig.legend((line1, line2), ('prediction', 'true'), loc = 'upper right')
plt.show()

tmp = np.delete(np.array(pred_glab_list), np.where(np.array(pred_glab_list) == 0))
tmp2 = np.delete(np.array(true_glab_list), np.where(np.array(pred_glab_list) == 0))
print("Accuracy Removed Zero : {:.3f}".format(sum(tmp == tmp2)/len(tmp)))
