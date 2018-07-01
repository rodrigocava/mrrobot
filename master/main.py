from Parts import Utils, WebServer, SelfDrivingCar

if(__name__ == "__main__"):
	# Get arguments
	args = Utils.get_args()
	
	# Get Parameters
	parameters = Utils.get_params(args.train)
	
	# Build car
	car = SelfDrivingCar.SelfDrivingCar(parameters)

	# Start webserver
	car.webserver = WebServer.LocalServer(parameters['webserver_params'], car)	

	# Run !
	print('>> Ready to roll!')
	car.webserver.stream()