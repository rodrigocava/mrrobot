import Utils

import numpy as np
import pickle
import time

"""
Train Data
"""
class TrainData(object):
	def __init__(self,_params):
		Utils.print_log("Init. Train data",1)
		self.image_array = [np.zeros((_params['height'],_params['width'],_params['channels']))]
		self.label_array = [np.zeros((3))]
		self.labels = np.zeros((3,3))
		for i in range(3):
			self.labels[i,i] = 1
		
		self.path = _params['path']
		self.saved_frames = 0

	def save(self):
		train = self.image_array[1:]
		label = self.label_array[1:]
		if(len(train) > 0):
			Utils.print_log("Saving train data. Total frames to be saved: "+str(self.saved_frames),2)
			name = self.path+'/'+str(Utils.epoch())+'.pkl'

			with open(name,'w') as f:
				pickle.dump([train, label], f)
		else:
			Utils.print_log("No frames to save")

	def log_train_data(self,_directions,_car):
		turn = _directions[0]
		if((turn != 'BACKWARDS')):
			t = time.time()
			
			# Capture frame
			image = _car.camera.last_img[0]

			# Move, wait a bit and stop
			_car.move(_directions)
			time.sleep(0.3)
			_car.stop()
			if(_car.verbose): t = Utils.print_log('move',2,t)
			
			# Stack frame
			self.image_array.append(image)
			if(_car.verbose): t = Utils.print_log('stack image array',2,t)

			# Stack Label
			label_code = _car.config[turn]["label_code"]
			self.label_array.append(self.labels[label_code])
			if(_car.verbose): t = Utils.print_log('stack label array',2,t)

			self.saved_frames += 1