import RPi.GPIO as GPIO

def performIOT(pin_no,state):
    print(f"swith {state} at pin {pin_no}")
    pin_no=int(pin_no)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(pin_no,GPIO.OUT)
    if state=='OFF':
        GPIO.output(pin_no,GPIO.HIGH)
        return ('OK swith OFF')
    else:
        GPIO.output(pin_no,GPIO.LOW)
        return ('OK swith ON')
