import datetime as dt
import argparse
import time
import json
import os

"""
Utils
"""

def wait(_time):
	time.sleep(_time)

def epoch():
    return str(int(time.time()))

def ms_epoch():
    return int((dt.datetime.utcnow() - dt.datetime(1970,1,1)).total_seconds() * 1000)

def get_root():
	return os.path.normpath(os.path.dirname(__file__))

def get_password():
	root = get_root()
	with open(os.path.join(root, "../config/password.txt")) as in_file:
		password = in_file.read().strip()
	return password

def print_log(_msg,_identation=0,_time=0):
	ident = '	'*_identation
	if (_time != 0):
		t = time.time() - _time
		if(t > 60):
			t = round(t/60,2)
			unit = 'm'
		elif(t > 3600):
			t = round(t/3600,2)
			unit = 'h'
		else:
			unit = 's'
		print(('%s %s. Time: %s %s')%(ident,_msg,t,unit))
		return time.time()
	else:
		print(('%s %s')%(ident,_msg))

def get_args():
	parser = argparse.ArgumentParser(prog='drive')
	parser.add_argument('--train', help='Set for train mode', action="store_true", default=False)
	parsed_args = parser.parse_args()
	return parsed_args

def get_params(_train):
	with open('config/config.json') as f:
		data = json.load(f)
	params = {
		'car_params': {
			 'width': data['width']
			,'height': data['height']
			,'name': data['title']
			,'pigame': data['pigame']
			,'verbose': data['verbose']
			,'channels': data['channels']
			,'car_config': data['car_config']
		}

		,'camera_params':{
			 'path': data['train_data_storage']
			,'width': data['width']
			,'height': data['height']
		}
		
		,'webserver_params':{
			 'require_login': data['required_login']
			,'port': data['port']
			,'cookie': data['cookie']
			,'car': None
		}
	}

	if(_train):
		params['train_data_params'] = {
				 'path': data['train_data_storage']
				,'width': data['width']
				,'height': data['height']
				,'channels': data['channels']
			}
	else: 
		params['brain_params'] = {
				'model': data['model']
			}
	return params