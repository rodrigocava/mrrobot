import CarCamera
import Utils

import RPi.GPIO as GPIO
import numpy as np
import threading
import time

class SelfDrivingCar(object):
	def __init__(self,_params):
		self.drive = False
		self.log_photos = False
		self.train_mode = False
		self.current_direction = []

		self.name = _params['car_params']['name']
		self.width = _params['car_params']['width']
		self.height = _params['car_params']['height']
		self.verbose = _params['car_params']['verbose']
		self.config = _params['car_params']['car_config']
		self.channels = _params['car_params']['channels']
		self.default_speed = self.config['SPEED']['default']


		# Init Trainning mode
		if('train_data_params' in _params): 
			import TrainData
			self.train_data = TrainData.TrainData(_params['train_data_params'])
			self.train_mode = True

		# Init Self-driving mode
		if('brain_params' in _params): 
			from CarBrain import CarBrain
			self.brain = CarBrain(_params['brain_params'])
		
		# Init parts
		self.init_pins()
		self.camera = CarCamera.CarCamera(_params['camera_params'])

	"""
	Init methods
	"""
	def init_pins(self):
		Utils.print_log("Init. Pins",1)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		for direction in self.config:
			GPIO.setup(self.config[direction]["pin"],GPIO.OUT)

		# set initial speed
		self.speed = GPIO.PWM(self.config['SPEED']["pin"],100)
		self.speed.start(self.config['SPEED']["default"])
		
		# set all pins to false to begin
		self.stop()

	def train(self):
		self.train_data_params['car'] = self
		self.train_data = TrainData.TrainData(self.train_data_params)

	def self_drive(self):
		from CarBrain import SelfDriving
		SelfDriving(self)

	def set_speed(self,_speed):
		self.speed.ChangeDutyCycle(_speed)

	def stop(self,_directions=[]):
		if(len(_directions) == 0):
			Utils.print_log("Stoping",2)
			directions = self.config
		else:
			directions = _directions

		for direction in directions:
			GPIO.output(self.config[direction]["pin"],False)

		self.current_direction = directions

	def move(self,_directions):
		Utils.print_log("Move "+_directions[0],2)
		if(_directions != self.current_direction):

			#Increase speed when turning to give more juicy to 2 motors
			if(_directions[0] != 'FORWARD'):
				s = int(self.default_speed*1.2)
				if(s > 100): s = 100
				self.set_speed(s) 
			else:
				self.set_speed(self.default_speed) 
		
			# Move
			for direction in _directions:
				GPIO.output(self.config[direction]["pin"],True)

			self.current_direction = _directions

	def log_and_move(self,_directions):
		if (self.train_mode):
			self.train_data.log_train_data(_directions,self)
		else:
			self.move(_directions)

		t = time.time()
		if(self.log_photos):
			self.camera.save_frame(_directions[0])
			t = Utils.print_log('Saved photo',2,t)

	def shutdown(self):
		Utils.print_log("Shuting down...")
		GPIO.cleanup()
		
		if(self.train_data):
			self.train_data.save()
		