from django.shortcuts import render
from django.http import HttpResponse
import RPi.GPIO as GPIO
import time
import json
import traffic
import atexit

GPIO.setmode(GPIO.BOARD)
led1 = traffic.Led(19,21)
led2 = traffic.Led(22,24)
led3 = traffic.Led(29,31)
led4 = traffic.Led(35,37)
# Create your views here.
def index(request):
	if request.method != "POST":
		return render(request,"control.html")
	val = json.loads(request.body)
	val = val.values()
	led = [led1,led2,led3,led4]
	for l,v in zip(led,val):
		if v:
			l.set_green()
		else:
			l.set_red()
	return HttpResponse("successfully changed")
def exit_handler():
	GPIO.cleanup()

atexit.register(exit_handler)
