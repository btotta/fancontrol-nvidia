#!/usr/bin/python
#   nvidia-settings -q [fan:0]/GPUTargetFanSpeed -t     // gets current fan speed 
#   nvidia-settings -q [GPU:0]/GPUCoreTemp -t           // gets current temp
#   nvidia-settings -q [fan:0]/GPUTargetFanSpeed=**     // set target fan speed
#   sudo nvidia-xconfig -a --cool-bits=12 --allow-empty-initial-configuration  
#   enable nvidia coolsbits with allowed fan control and overclock

import time
import subprocess

# default fan speed when below first temp set on 'temp_curve'
default_fan_speed = 0

fan_curve = [25,45,75,100]
temp_curve = [45,60,70,75]


# script made for 1 card with 1 fan


def get_temp():
    return int(subprocess.getoutput('nvidia-settings -q [GPU:0]/GPUCoreTemp -t'))


def get_fan_speed():
    return int(subprocess.getoutput('nvidia-settings -q [fan:0]/GPUTargetFanSpeed -t'))


def set_fan(speed):        

    if get_fan_speed() != speed:
        subprocess.getoutput('nvidia-settings -a GPUFanControlState=1 -a [fan:0]/GPUTargetFanSpeed={}'.format(speed))       


while True:

    time.sleep(3)
    
    current_temp = get_temp()  
    
    # check if the current temp is bellow the first temp on "temp_curve". If so, \
    # set the speed determined on "default_fan_speed"    
    if current_temp < temp_curve[0]:
        set_fan(default_fan_speed)
    
    else:       

        for index, item in enumerate(temp_curve):

            if index < (len(temp_curve)-1):
                next_temp = temp_curve[index+1]                

            if current_temp >= item:
                if current_temp < next_temp:                    
                    set_fan(fan_curve[index])

                if current_temp > temp_curve[-1]:
                    set_fan(fan_curve[-1])

    
    # print('temp {}, fan {}'.format(get_temp(), get_fan_speed()))
    


if '__name__' == '__main__':
    main()
