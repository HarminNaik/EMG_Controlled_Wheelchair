from machine import Pin, PWM, ADC
import utime

potMin = 224
potMax = 760

potPin = 26
EMGPin = 27

#Pins connecting to L298N motor driver
IN1_pin = Pin(6, Pin.OUT)
IN2_pin = Pin(7, Pin.OUT)
IN3_pin = Pin(8, Pin.OUT)
IN4_pin = Pin(9, Pin.OUT)
enA_pin = Pin(4, Pin.OUT)
enB_pin = Pin(5, Pin.OUT)

#PWM output for enable pins for speed control
enA = PWM(enA_pin)
enB = PWM(enB_pin)

enA.freq(1000)
enB.freq(1000)

#Potentiometer for speed control
pot = ADC(potPin)

EMG = ADC(EMGPin)

prevEMGValue = 0
nextEMGValue = 0

def Map(oldValue, oldBot, oldTop, newBot, newTop):
    slope = (newTop - newBot) / (oldTop - oldBot)
    constant = ((newTop + newBot) - (slope*(oldTop + oldBot))) / 2
    newValue = (slope * oldValue) + constant
    return int(newValue)

while True:
    #Reading the potentiometer for speed control
    potValue = pot.read_u16()
    PWM_Out = Map(potValue, potMin, potMax, 0, 65535)
    
    utime.sleep(0.0001)
    enA.duty_u16(PWM_Out)
    enB.duty_u16(PWM_Out)
    
    #EMG signal processing for control
    nextEMGValue = EMG.read_u16()
    
    if(nextEMGValue >= prevEMGValue):
        increasing = True
        peak = nextEMGValue
        
    else:
        increasing = False
        peak = 0
    
    if(not increasing):
        #Conditional statements for motor control
        if(peak >= 1985 and peak <= 14895):
            # 0 to 0.75V: Forward
            forward = not forward
            # toggle between move forward and stop
            if(forward):
                IN1_pin.value(True)
                IN2_pin.value(False)
                IN3_pin.value(True)
                IN4_pin.value(False)
                
            if(not forward):
                IN1_pin.value(False)
                IN2_pin.value(False)
                IN3_pin.value(False)
                IN4_pin.value(False)
            
        elif(peak >= 16880 and peak <= 31775):
            # 0.85 to 1.6V: Left Turn
            IN1_pin.value(True)
            IN2_pin.value(False)
            IN3_pin.value(False)
            IN4_pin.value(True)
            
        elif(peak >= 33760 and peak <= 48655):
            # 1.7 to 2.45V: Right Turn
            IN1_pin.value(False)
            IN2_pin.value(True)
            IN3_pin.value(True)
            IN4_pin.value(False)
            
        elif(peak >= 50460 and peak <= 65535):
            # 2.55 to 3.3V: Backward
            IN1_pin.value(False)
            IN2_pin.value(True)
            IN3_pin.value(False)
            IN4_pin.value(True)
            
        else:
            # by default, slowly move forward
            IN1_pin.value(True)
            IN2_pin.value(False)
            IN3_pin.value(True)
            IN4_pin.value(False)
            
            PWM_Out = 2500
        
    prevEMGValue = nextEMGValue