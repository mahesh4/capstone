import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

class Sensor():
	def __init__(self, trig, echo):
		self.GPIO_TRIGGER = trig
		self.GPIO_ECHO = echo
		# Set pins as output and input
		GPIO.setup(trig, GPIO.OUT)  # Trigger
		GPIO.setup(echo, GPIO.IN)      # Echo

	def sense_distance(self):
		"""
		returns distance to nearest object
		"""
		# Speed of sound in cm/s at temperature
		temperature = 25
		speedSound = 33100 + (0.6 * temperature)
		GPIO_TRIGGER = self.GPIO_TRIGGER
		GPIO_ECHO = self.GPIO_ECHO
		print("Ultrasonic Measurement")
		print("Speed of sound is", speedSound /100, "m/s at ", temperature, "deg")

		# Set trigger to False (Low)
		GPIO.output(GPIO_TRIGGER, False)

		# Allow module to settle
		time.sleep(0.5)

		# Send 10us pulse to trigger
		GPIO.output(GPIO_TRIGGER, True)
		# Wait 10us
		time.sleep(0.00001)
		GPIO.output(GPIO_TRIGGER, False)
		start = time.time()
		while GPIO.input(GPIO_ECHO) == 0:
			start = time.time()
		while GPIO.input(GPIO_ECHO) == 1:
			stop = time.time()

		# Calculate pulse length
		elapsed = stop - start

		# Distance pulse travelled in that time is time
		# multiplied by the speed of sound (cm/s)
		distance = elapsed * speedSound

		# That was the distance there and back so halve the value
		distance = distance / 2
		return distance


class Led():

	def __init__(self, green, red):
		"""
		takes pin numbers of green led and red led and inits them
		param green: GPIO number of green led pin
		param red: GPIO number of red led pin
		"""
		self.green_pin = green
		self.red_pin = red
		# if green light: true, if red light: false
		self.state = None
		GPIO.setup(green, GPIO.OUT)
		GPIO.setup(red, GPIO.OUT)

	def set_green(self):
		"""
		turns on green led
		"""
		if not self.state:
			GPIO.output(self.red_pin, GPIO.LOW)
			GPIO.output(self.green_pin, GPIO.HIGH)
			self.state = True

	def set_red(self):
		"""
		turns on red led
		"""
		if self.state or self.state == None:
			GPIO.output(self.green_pin, GPIO.LOW)
			GPIO.output(self.red_pin, GPIO.HIGH)
			self.state = False


class Lane():

	def __init__(self, led, sensor, length, width=3, car_length=5, in_flow_rate=None, out_flow_rate=None):
		self.led = led
		self.sensor = sensor
		self.length = length
		self.width = width
		self.car_length = car_length
		self.in_flow_rate = in_flow_rate
		self.out_flow_rate = out_flow_rate

	def signal_green(self):
		self.led.set_green()

	def signal_red(self):
		self.led.set_red()

	def get_distance(self):
		return self.sensor.sense_distance()

	def get_no_of_vehicles():
		no_of_cars = (self.length - self.get_distance()) / self.car_length
		return int(no_of_cars)


'''class phase():
	lane1, lane2:

	def __init__(self, lane1, lane2):
		self.lane1 = lane1
		self.lane2 = lane2

	def change(self, state):
		if state:
			self.lane1.signal_red()
		else:
			self.lane1.signal_green()

	def get_num_cars():'''
