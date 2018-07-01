import Utils

from picamera import PiCamera
import picamera.array
from PIL import Image
import numpy as np
import threading
import time
import cv2
import io

"""
Car Camera
"""
class CarCamera(object):
	def __init__(self,_params):
		Utils.print_log("Init. Camera",1)

		self.stream = True
		self.stop_detected = False
		self.path = _params['path']

		self.picam = PiCamera()
		self.picam.rotation = 180
		self.picam.framerate = 10
		self.picam.resolution = (_params['width'], _params['height'])

		self.last_img = np.zeros([1,240,320,3])
		self.last_img_bytes = b'a'
				
		time.sleep(1) # Gives a second so camera warms up

	def save_frame(self,_turn):
		name = str(Utils.ms_epoch())+":"+str(_turn)
		self.picam.capture(self.path+"/train_photos/"+name+".jpg")

"""
Camera Stream
"""
class CameraStream(object):
	def __init__(self,_car):
		self.car = _car
		self.camera = self.car.camera
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True
		thread.start()
	
	def run(self):
		self.detection = ObjectDetection()
		while (self.camera.stream):
			# Make a RGBarray capture
			raw_capture = picamera.array.PiRGBArray(self.camera.picam)
			self.camera.picam.capture(raw_capture, format='rgb', use_video_port=True)

			# Run object detection
			img = self.detection.detect(raw_capture.array.astype('uint8'))
			self.camera.stop_detected = self.detection.stop_detected

			# Save frame
			image_array = np.zeros([1,240,320,3])
			image_array[0] = img
			self.camera.last_img = image_array

			# Transform frame in bytes and save it
			img = Image.fromarray(img.astype('uint8'), mode='RGB')
			f = io.BytesIO()
			img.save(f, "JPEG")
			self.camera.last_img_bytes = f.getvalue() 

"""
Object Detection
"""
class ObjectDetection(object):
	def __init__(self):
		self.stop_detected = False
		self.classifier = cv2.CascadeClassifier('config/stop_sign.xml')

	def detect(self, _image):
		# detection
		cascade_obj = self.classifier.detectMultiScale(
			_image,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30),
			flags=cv2.CASCADE_SCALE_IMAGE
		)

		# draw a rectangle around the objects
		if (len(cascade_obj)):
			self.stop_detected = True
			for (x_pos, y_pos, width, height) in cascade_obj:
				cv2.rectangle(_image, (x_pos+5, y_pos+5), (x_pos+width-5, y_pos+height-5), (255, 255, 255), 2)
				cv2.putText(_image, 'STOP', (x_pos, y_pos-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)			
		else:
			self.stop_detected = False

		return _image


