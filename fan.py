#!/usr/bin/python
#   nvidia-settings -q [fan:0]/GPUTargetFanSpeed -t     // gets current fan speed 
#   nvidia-settings -q [GPU:0]/GPUCoreTemp -t           // gets current temp
#   nvidia-settings -q [fan:0]/GPUTargetFanSpeed=**     // set target fan speed
#   sudo nvidia-xconfig -a --cool-bits=12 --allow-empty-initial-configuration  \
#   enable nvidia coolsbits with allowed fan control and overclock - needed for this script to work

import time
import subprocess

# default fan speed when current temp is below the first temp set on 'temp_curve'
default_fan_speed = 0

fan_curve = [25,45,75,100]
temp_curve = [55,60,70,75]


def get_temp():
    return int(subprocess.getoutput('nvidia-settings -q [GPU:0]/GPUCoreTemp -t'))


def get_fan_speed():
    return int(subprocess.getoutput('nvidia-settings -q [fan:0]/GPUTargetFanSpeed -t'))


def set_fan(speed):
    if get_fan_speed() != speed:
        subprocess.getoutput('nvidia-settings -a GPUFanControlState=1 -a GPUTargetFanSpeed={}'.format(speed))
        # print('fan speed set {}, temp {}'.format(speed, get_temp()))


while True:

    time.sleep(3)
    current_temp = get_temp()    
    
    if current_temp < temp_curve[0]:
        set_fan(default_fan_speed)

    if current_temp >= temp_curve[-1]:
        set_fan(fan_curve[-1])
    
    else:       

        for index, item in enumerate(temp_curve):

            if current_temp >= temp_curve[index] and current_temp < temp_curve[index+1]:
                set_fan(fan_curve[index])
 
    #print('temp {}, fan {}'.format(get_temp(), get_fan_speed()))
