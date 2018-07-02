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
This 

### Software Architecture
The main program buids an Self Driving Car object and starts a WebServer for the remote and camera stream. The car is made of a few parts:

* SelfDrivinCar:
  * Handles interaction with the motors for movement and speed
* CarCamera:
  * Handles camera stream and object detection for the stop sign
* WebServer:
  * Creates a webserver to stream the camera and control
* TrainData:
  * Handles gathering and saving train data
* CarBrain:
  * Handles the load of the pre-build Machine Learning model and self-driving based on the camera images
  
