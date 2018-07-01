import Utils

import keras.backend.tensorflow_backend
from keras.backend import clear_session
from keras.models import load_model
import tensorflow as tf
import threading
import time

"""
Predictions
"""
class CarBrain(object):
	def __init__(self,_params):
		Utils.print_log("Init. Model",1)
		self.model = load_model(_params['model'])
		self.graph = tf.get_default_graph()
			
	def get_direction(self,_image):
		t = time.time()
		
		res =  self.model.predict(_image, batch_size=1)
		t = Utils.print_log('Model Predict',3,t)
		
		max_val = 0
		for idx,val in enumerate(res[0]):
			if val > max_val:
				max_val = val
				move = idx	

		direction = []
		if move == 0:
			direction = ['FORWARD']
		elif move == 1:
			direction = ['RIGHT','FORWARD']
		elif move == 2:
			direction = ['LEFT','FORWARD']
		return direction

"""
Self Drive Thread
"""
class SelfDriving(object):

	def __init__(self,_car):
		self.car = _car
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True
		thread.start()

	def run(self):
		with self.car.brain.graph.as_default():
			while (self.car.drive):
				# If it finds a stop sing, stop for 3s
				if(self.car.camera.stop_detected):
					self.car.stop(self.car.current_direction)
					time.sleep(3)
					self.car.current_direction = []

				# Get image
				image = self.car.camera.last_img

				# Make prediction
				direction = self.car.brain.get_direction(image)

				# If new direction, change
				if(direction != self.car.current_direction):
					self.car.stop(self.car.current_direction)
					self.car.move(direction)
				
				Utils.print_log('Driving '+direction[0],2)
				print("\n")
		self.car.stop()