import traffic
import RPi.GPIO as GPIO
import time
import numpy as np


GPIO.setmode(GPIO.BOARD)

#led initialization
led1 = traffic.Led(19,21)
led2 = traffic.Led(22,24)
led3 = traffic.Led(29,31)
led4 = traffic.Led(35,37)


#sensor initialization
sensor1 = traffic.Sensor(8,10)
sensor2 = traffic.Sensor(11,13)
sensor3 = traffic.Sensor(16,18)
sensor4 = traffic.Sensor(5,7)

#lane initialization
lane1 = traffic.Lane(led1,sensor1,30)
lane2 = traffic.Lane(led2,sensor2,30)
lane3 = traffic.Lane(led3,sensor3,30)
lane4 = traffic.Lane(led4,sensor4,30)


lanes = [lane1,lane2,lane3,lane4]

signal_state = np.full((4,4),False,dtype=bool)
np.fill_diagonal(signal_state,True)
interval = 10
brkpnt = [-l.lane_length for l in lanes]


url = "http://ec2-35-154-245-161.ap-south-1.compute.amazonaws.com/nash"


def utilities():
    utils = np.empty((4,4))
    for i in range(4):
        utils[i] = [l.return_utility(s) for l,s in zip(lanes,signal_state[i])]
    return (-utils)


def next_interval():
    lane_info = {
        "lane1":lane1.get_distance(),
        "lane2":lane2.get_distance(),
        "lane3":lane3.get_distance(),
        "lane4":lane4.get_distance()
    }

    for l in lanes:
        l.calc_utility()
    
    data = {
        "brk":brkpnt,
        "util":utilities().tolist(),
        "data":lane_info
    }

    req = urllib2.Request(url, data, {'Content-Type': 	'application/json'})
    f = urllib2.urlopen(req)
    response = json.loads(f.read())
    f.close()
    next_phase = [False] * 4
    next_phase[response["next_phase"]] = True
    for l,s in zip(lanes,next_phase):
        l.signal_change(s)
    time.sleep(interval)

try:
    init_phase = [True] + [False]*3
    for l,i in zip(lanes,init_phase):
        l.signal_change(i)
    while(1):
        next_interval()
except:
    print "error"
finally:
    GPIO.cleanup()


    
    

    


    
            