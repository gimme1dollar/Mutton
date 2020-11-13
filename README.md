# Mutton
EMG Based Virtual Keyboard for developing Watchband-shaped IoT device input system   
  
         
## Hand Gesture Pilot Test Method
```bash
(1) Data Acquisition from OpenBCI cyton board - 250Hz raw data
(2) sEMG Feature Extraction - 25Hz featured data
(3) Model Training - Convolutional Neural Network(CNN) model
```


## Result
* CNN model
![6](https://user-images.githubusercontent.com/48921426/98654983-50029800-2382-11eb-98c6-fe4aaa827521.png)

* sEMG Feature Graph
![1](https://user-images.githubusercontent.com/48921426/98647788-b7b3e580-2378-11eb-8fef-4a6cca076aa6.png)
![2](https://user-images.githubusercontent.com/48921426/98647798-bbe00300-2378-11eb-8c37-1e9874cdf2e5.png)

* Realtime Classification Training & Test    
:: Classifying 6 gestures (exploting fist/hand/index/middle/little finger buttons + 1 noise) with 2-channel  
:: Training Elapsed Time on 50 epochs : 226s  
:: Classification Delay : 0.4s  
:: Validation Dataset Accuracy : about 85.5%  
:: Test Dataset Accuracy : about 66.2%  
![4](https://user-images.githubusercontent.com/48921426/98647813-c0a4b700-2378-11eb-9702-893219ca254b.png)


## Publication
* 2018 학부생 연구프로그램(UGRP) 수상작 (최우수상)  
(https://www.youtube.com/watch?v=WyyjaKbNtxU)  
* Feasibility Study on Pin Electrode for sEMG_Interface.pdf  
https://drive.google.com/file/d/1wE2IgJxHEIAFnnFYu4O8L4EcwqfiJtKd/view?usp=sharing  
