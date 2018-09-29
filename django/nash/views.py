import nashbargain as nb
import json
from django.shortcuts import render,redirect
import numpy as np
from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from pymongo import MongoClient



client = MongoClient('mongodb',27017)
db = client.traffic_report
	
def write_db(data):
	lane_data = db.lane_data
	return lane_data.insert_one(data).inserted_id

@login_required(login_url='/signin')
def index(request):
	#cache.set('test','cache works')
	return render(request,'project.html',cache.get("sensor"))	

def nash(request):
	if request.method != "POST":
		return HttpResponse("send data using post request for finding nash solution")
        brk = np.array(json.loads(request.POST['brk']))
        util = np.array(json.loads(request.POST['util']))
        n = nb.nashsolution(brk,util)
        return HttpResponse(json.dumps(n.find_global_max().astype('float64').tolist()))

def sensor(request):
	if request.method == "POST":
		data = json.loads(request.body)
		cache.set("sensor",data)
		write_db(data)
		return HttpResponse("successfully received sensor data")

def signin(request):
	if request.method == "POST":
        	username = request.POST['username']
        	password = request.POST['password']
        	user = authenticate(username=username, password=password)
        	if request.POST.get('signin',None):
            		if user is not None:
                		if user.is_active:
                    			login(request, user)
                    			return redirect(request.GET.get('next','/'))
                		else:
                    			return render(request, "index.html",{'msg':"account banned"})
            		else:
                		return render(request,"index.html",{'msg':"invalid user"})	
        	elif request.POST.get('signup',None):
            		if user is None:
                		user = User.objects.create_user(username=username,password=password)
                		user.save()
                		return render(request, "index.html", {'msg':'successfully registered, sign in to continue'})
            		else:
                		return render(request, "index.html", {'msg':'username already exists'})             
	else: 
		return render(request,"index.html")

def signout(request):
	logout(request)
	return HttpResponse("logged out successfully")

def data(request):
	return JsonResponse(cache.get("sensor"), safe = False)	
