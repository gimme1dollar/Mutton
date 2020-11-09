import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import serial
import os
import time
import random

# Open Serial Port
try:
    ser = serial.Serial("COM6", 115200, timeout=1)
    print(f"serial open? {ser.isOpen()}")
except:
    print("serial error")


gesture_name = ['Noise', 'Fist', 'Hand', 'Index Finger', 'Middle Finger', 'Little Finger']
n_gesture_test = 3  # Number of gestures used in a RT model accuracy
n_ch = 2  # Number of channels
update_len = 1  # Number of sEMG data required for the next CNN input, default : latency 0.1s
flushTime = 1  # Time for flushing old sEMG data
testTime = 3  # Time for classifying gestures
true_label = []  # True label
pred_label = []  # Predicted label
acc = []  # Model RT Accuracy


# Generate Random gesture label
g_label = [random.randrange(0, len(gesture_name), 1)]
for i in range(n_gesture_test-1):
    tmp = random.randrange(0, len(gesture_name), 1)
    while tmp == g_label[i]:
        tmp = random.randrange(0, len(gesture_name), 1)
    g_label.append(tmp)


# Load Trained model
path = os.getcwd() + "\\data\\model\\"
model = tf.keras.models.load_model(path+'my_model')
model.summary()
seq_len = model.layers[0].input.shape[1]  # CNN input size(window length)


# Receive sEMG from a Cyton Board
emgSignal = np.empty([1, seq_len, n_ch])
start = time.time()
for i in range(seq_len):
    emgSignal[0, i, :] = [float(i) for i in ser.readline().decode().strip().split(',')[0:n_ch]]
now = time.time()
print(f"Full Data Received at {now - start}s")


for ii in range(n_gesture_test):
    # Flush old sEMG
    print("pause for now...")
    tol = 0
    while tol <= flushTime:
        start = time.time()
        emgSignal = np.append(emgSignal, [[[float(i) for i in ser.readline().decode().strip().split(',')[0:n_ch]]]],
                              axis=1)
        emgSignal = np.delete(emgSignal, 0, axis=1)
        tol += time.time() - start

    print(f"Get ready for gesture: {gesture_name[g_label[ii]]}")
    time.sleep(2)

    # Classify gestures
    print(f"Collecting gesture: {gesture_name[g_label[ii]]}")
    tol = 0
    while tol <= testTime:
        start = time.time()
        for i in range(update_len):
            emgSignal = np.append(emgSignal, [[[float(i) for i in ser.readline().decode().strip().split(',')[0:n_ch]]]],
                                  axis=1)
        emgSignal = np.delete(emgSignal, np.s_[0:update_len], axis=1)

        # Gesture Classification
        predictions = model.predict(emgSignal)[0]
        prediction_label = int(np.where(predictions == max(predictions))[0])

        # Save Results
        pred_label.append(prediction_label)
        true_label.append(g_label[ii])

        # Update Model RT accuracy
        if len(acc) != 0:
            if prediction_label == g_label[ii]:
                acc.append((len(acc) * acc[-1] + 1) / (len(acc) + 1))
            else:
                acc.append((len(acc) * acc[-1]) / (len(acc) + 1))
        else:
            acc.append(float(prediction_label == g_label[ii]))

        tol += time.time() - start
        # Show Result
        print("Eclipsed Time : {:.3f} \t Predicted: {:d} \t True: {:d} \t Accuracy : {:.3f}".format(tol, prediction_label, g_label[ii], acc[-1]))


# Plot Model RT accuracy
fig = plt.figure()
line1, = plt.plot(acc, label = 'RT Accuracy')
plt.legend(loc = 'upper right')
plt.title('Model RT Accuracy')
plt.xlabel('Data')
plt.ylabel('Label')
plt.show()


# Plot Classification Result Graph
fig = plt.figure()
plt.plot(pred_label, label = 'Predicted Label')
plt.plot(true_label, label = 'True Label')
plt.legend(loc = 'upper right')
plt.title('Classification Result Graph')
plt.xlabel('Data')
plt.ylabel('Label')
plt.show()

print("Model RT Accuracy on {:d} data : {:.3f}%".format(len(pred_label), 100*acc[-1]))
tmp = np.delete(np.array(pred_label), np.where(np.array(pred_label) == 0))
tmp2 = np.delete(np.array(true_label), np.where(np.array(pred_label) == 0))
print("Model RT Accuracy on {:d} data (Removed Zero Label): {:.3f}%".format(len(pred_label), 100*sum(tmp == tmp2)/len(tmp)))

'''
# Realtime Graph Plotting
ax1.plot(graph_x, acc)
ax1.lines[0].set_xdata(graph_x)
ax1.lines[0].set_ydata(acc)

line1, = ax2.plot(graph_x, pred_label)
line2, = ax2.plot(graph_x, true_label)
ax2.legend((line1, line2), ('prediction', 'true'))
ax2.lines[0].set_xdata(graph_x)
ax2.lines[0].set_ydata(pred_label)

fig.gca().relim()
fig.gca().autoscale_view()
plt.pause(0.0001)
'''