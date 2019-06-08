# Mr. Robot
A Self-Driving Remote Control Car controlled by a browser. All inside a Raspberry Pi

<p align="center">
 <img width="500" src="https://i.imgur.com/t805DXf.png">
<p>

## Hardware
* [Remote control car](https://pt.aliexpress.com/item/Rastar-1-24-4CH-RC-Carros-Cole-o-De-Carros-de-R-dio-Controlado-M-quinas/32681416187.html?spm=a2g0s.9042311.0.0.d642b90aBFGyXD)
* Raspberry Pi
* [L28N Dual Motor Controller](https://pt.aliexpress.com/item/MCIGICM-1pcs-New-Dual-H-Bridge-DC-Stepper-Motor-Drive-Controller-Board-Module-L298N-MOTOR-DRIVER/32355666632.html?spm=a2g0s.9042311.0.0.d642b90aBFGyXD)
* Smartphone External Battery
* 4x AA batteries

### Harware Architecture
The remote control car has 2 DC motors, and I used the L298N module to control them. You can see how to do that [here](https://www.youtube.com/watch?v=AZSiqj0NZgU). Both the motors and the L298N module are powered by 4AA batteries. The Raspberry Pi is powered by an external battery and we have also a Pi Camera with it. Finally, There are a few jump wires connecting the GPIO from the PI to the L298N module.

<p align="center">
 <img width="500" src="https://i.imgur.com/qCoycux.png">
<p>
 
<p align="center">
 <img width="500" src="https://i.imgur.com/IiQeJpG.jpg">
<p>

## Software

### Software Architecture
The main program buids an Self Driving Car object and starts a WebServer for the remote and camera stream. The car is made of a few parts:

* SelfDrivinCar:
  * Handles interaction with the motors for movement and speed
* CarCamera:
  * Handles camera stream and object detection for the stop sign
* WebServer:
  * Creates a webserver to stream the camera and control the car
* TrainData:
  * Handles gathering and saving train data
* CarBrain:
  * Handles the load of the pre-build Machine Learning model and self-driving based on the camera images

### Challenges
Considering that I wanted to run every thing inside the raspberry pi (sever, object detection, tunr prediction, etc) a big concern was always spped and performance. If the turn prediction took more than 500ms the car would miss its turn and miss the road. Although there maybe even more optimizations, the current program makes a prediction+turn in 300ms, which is more than enough for the success of the project.

### Model trainning
To generate data, the train mode saved a frame in a rgb array with the correct command issued by me (forward, left or right). After I gathered a few hundreds of pictures + turn I loaded everything into my computer and used a script to generate even more train data by flipping the images (and adjusting the command accordingly) and also changing the image brightness or colors. 

With all that, I trained several variations of a Deep Learning model using Keras+Tensorflow based on [this Nvidia article](https://devblogs.nvidia.com/deep-learning-self-driving-cars/) and explained in [this video](https://www.youtube.com/watch?v=EaY5QiZwSP4). The model has an image normalization to avoid saturation and make gradients work better, 5 layers of a CNN to handle feature engineering, drop out layer to avoid overfitting, and finally 5 fully connected layers for predicting the turn.

<p align="center">
 <img width="800" src="https://i.imgur.com/8ds6or1.png">
<p>

### Self-driving
The pre-trained model is loaded on the start of the program. Once the command from any browser comes in, a loop starts the self-driving: the process gathers the most recent img, makes the prediction and turns the car.

<p align="center">
 <img width="800" src="https://i.imgur.com/pKZXgAs.png">
<p>

### Object detection
The stop sign detection was made using Haar feature-based cascade classifiers. OpenCV have a very comprehensive functions and you can train your own model following tutorials like [this](https://coding-robin.de/2013/07/22/train-your-own-opencv-haar-classifier.html). This approach is good considering it's very fast and we need speed to detect, classify and take action for every single frame. I used a pre-trained classifier from [here](https://github.com/hamuchiwa/AutoRCCar) and it worked very well for my stop sign.





  
