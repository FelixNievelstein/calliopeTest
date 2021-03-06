import time
import colorsys
import random
import threading
try:
    import numpy
except ImportError:
    exit("This script requires the numpy module\nInstall with: sudo pip install numpy")
from rgbmatrix5x5 import RGBMatrix5x5
from RPi import GPIO
from time import sleep
from models.ColorModel import ColorModel, ColorHelper

# Display timer that resets display
displayTimer = None

# String which defines the current running program.
currentProgram = ""

# Used GPIO Pins
clk = 17
dt = 18
buttonA = 9
buttonB = 10
motor = 21

# Set GPIO Mode and Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buttonA, GPIO.IN)
GPIO.setup(buttonB, GPIO.IN)
GPIO.setup(motor, GPIO.OUT)

# Counter for rotarty encoder
counter = 0
clkLastState = GPIO.input(clk)

# Last state of GPIO for buttons
lastStateBtnA = GPIO.input(buttonA)
lastStateBtnB = GPIO.input(buttonB)

# Configure RGB matrix
rgbmatrix5x5 = RGBMatrix5x5()
rgbmatrix5x5.set_clear_on_exit()
rgbmatrix5x5.set_brightness(0.5)
height = rgbmatrix5x5.height
width = rgbmatrix5x5.width

def clearDisplay():
    for y in range(height):
        for x in range(width):
            rgbmatrix5x5.set_pixel(x, y, 0, 0, 0)
        rgbmatrix5x5.show()

def clearTimer():
    global displayTimer
    if displayTimer is not None:
        displayTimer.cancel()

# Sets one of the smiley faces to the rgb matrix
def setFace(number):
    clearDisplay()
    clearTimer()
    if number is 1:
        r = int(234.0)
        g = int(43.0)
        b = int(93.0)
        rgbmatrix5x5.set_pixel(0, 0, r, g, b)
        rgbmatrix5x5.set_pixel(4, 0, r, g, b)
        rgbmatrix5x5.set_pixel(1, 1, r, g, b)
        rgbmatrix5x5.set_pixel(3, 1, r, g, b)
        rgbmatrix5x5.set_pixel(1, 3, r, g, b)
        rgbmatrix5x5.set_pixel(3, 3, r, g, b)
        rgbmatrix5x5.set_pixel(0, 3, r, g, b)
        rgbmatrix5x5.set_pixel(2, 3, r, g, b)
        rgbmatrix5x5.set_pixel(4, 3, r, g, b)
        rgbmatrix5x5.set_brightness(0.16)
        rgbmatrix5x5.show()
    elif number is 2:
        r = int(190.0)
        g = int(112.0)
        b = int(241.0)
        rgbmatrix5x5.set_pixel(1, 0, r, g, b)
        rgbmatrix5x5.set_pixel(3, 0, r, g, b)
        rgbmatrix5x5.set_pixel(1, 3, r, g, b)
        rgbmatrix5x5.set_pixel(2, 3, r, g, b)
        rgbmatrix5x5.set_pixel(3, 3, r, g, b)
        rgbmatrix5x5.set_pixel(0, 4, r, g, b)
        rgbmatrix5x5.set_pixel(4, 4, r, g, b)
        rgbmatrix5x5.set_brightness(0.32)
        rgbmatrix5x5.show()
    elif number is 3:
        r = int(0.0)
        g = int(163.0)
        b = int(248.0)
        rgbmatrix5x5.set_pixel(1, 0, r, g, b)
        rgbmatrix5x5.set_pixel(3, 0, r, g, b)
        rgbmatrix5x5.set_pixel(0, 3, r, g, b)
        rgbmatrix5x5.set_pixel(1, 3, r, g, b)
        rgbmatrix5x5.set_pixel(2, 3, r, g, b)
        rgbmatrix5x5.set_pixel(3, 3, r, g, b)
        rgbmatrix5x5.set_pixel(4, 3, r, g, b)
        rgbmatrix5x5.set_brightness(0.48)
        rgbmatrix5x5.show()
    elif number is 4:
        r = int(79.0)
        g = int(216.0)
        b = int(84.0)
        rgbmatrix5x5.set_pixel(1, 0, r, g, b)
        rgbmatrix5x5.set_pixel(3, 0, r, g, b)
        rgbmatrix5x5.set_pixel(0, 2, r, g, b)
        rgbmatrix5x5.set_pixel(4, 2, r, g, b)
        rgbmatrix5x5.set_pixel(1, 3, r, g, b)
        rgbmatrix5x5.set_pixel(2, 3, r, g, b)
        rgbmatrix5x5.set_pixel(3, 3, r, g, b)        
        rgbmatrix5x5.set_brightness(0.64)
        rgbmatrix5x5.show()
    elif number is 5:
        r = int(251.0)
        g = int(185.0)
        b = int(61.0)
        rgbmatrix5x5.set_pixel(1, 0, r, g, b)
        rgbmatrix5x5.set_pixel(3, 0, r, g, b)
        rgbmatrix5x5.set_pixel(0, 2, r, g, b)
        rgbmatrix5x5.set_pixel(1, 2, r, g, b)
        rgbmatrix5x5.set_pixel(2, 2, r, g, b)
        rgbmatrix5x5.set_pixel(3, 2, r, g, b) 
        rgbmatrix5x5.set_pixel(4, 2, r, g, b)
        rgbmatrix5x5.set_pixel(0, 3, r, g, b)
        rgbmatrix5x5.set_pixel(1, 3, 255, 255, 255)
        rgbmatrix5x5.set_pixel(2, 3, 255, 255, 255)
        rgbmatrix5x5.set_pixel(3, 3, 255, 255, 255)
        rgbmatrix5x5.set_pixel(4, 3, r, g, b)
        rgbmatrix5x5.set_pixel(1, 4, r, g, b)
        rgbmatrix5x5.set_pixel(2, 4, r, g, b)
        rgbmatrix5x5.set_pixel(3, 4, r, g, b)
        rgbmatrix5x5.set_brightness(0.8)
        rgbmatrix5x5.show()
    elif number is 6:
        r = int(243.0)
        g = int(37.0)
        b = int(24.0)
        rgbmatrix5x5.set_pixel(1, 0, r, g, b)
        rgbmatrix5x5.set_pixel(3, 0, r, g, b)
        rgbmatrix5x5.set_pixel(0, 1, r, g, b)
        rgbmatrix5x5.set_pixel(1, 1, r, g, b)
        rgbmatrix5x5.set_pixel(2, 1, r, g, b)
        rgbmatrix5x5.set_pixel(3, 1, r, g, b) 
        rgbmatrix5x5.set_pixel(4, 1, r, g, b)
        rgbmatrix5x5.set_pixel(0, 2, r, g, b)
        rgbmatrix5x5.set_pixel(1, 2, r, g, b)
        rgbmatrix5x5.set_pixel(2, 2, r, g, b)
        rgbmatrix5x5.set_pixel(3, 2, r, g, b) 
        rgbmatrix5x5.set_pixel(4, 2, r, g, b)
        rgbmatrix5x5.set_pixel(1, 3, r, g, b)
        rgbmatrix5x5.set_pixel(2, 3, r, g, b)
        rgbmatrix5x5.set_pixel(3, 3, r, g, b)
        rgbmatrix5x5.set_pixel(2, 4, r, g, b)
        rgbmatrix5x5.set_brightness(1.0)
        rgbmatrix5x5.show()
    else:
        clearDisplay()

# Show random number
def setRandom():
    clearDisplay()
    clearTimer()
    setMotor(False)
    number = random.randrange(6)
    white = ColorHelper.whiteColor()    
    global displayTimer
    mDisplayTimer = threading.Timer(3.0, clearRandom)
    mDisplayTimer.start()
    displayTimer = mDisplayTimer
    rgbmatrix5x5.set_brightness(0.64)
    if number is 0:
        rgbmatrix5x5.set_pixel(2, 2, white.r, white.g, white.b)
        rgbmatrix5x5.show()
    elif number is 1:
        rgbmatrix5x5.set_pixel(1, 3, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(3, 1, white.r, white.g, white.b)
        rgbmatrix5x5.show()
    elif number is 2:
        setMotor(True)
        rgbmatrix5x5.set_pixel(0, 4, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(2, 2, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(4, 0, white.r, white.g, white.b)
        rgbmatrix5x5.show()
    elif number is 3:
        rgbmatrix5x5.set_pixel(1, 1, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(1, 3, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(3, 1, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(3, 3, white.r, white.g, white.b)
        rgbmatrix5x5.show()
    elif number is 4:
        rgbmatrix5x5.set_pixel(0, 0, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(0, 4, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(4, 0, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(4, 4, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(2, 2, white.r, white.g, white.b)
        rgbmatrix5x5.show()
    elif number is 5:
        setMotor(True)
        rgbmatrix5x5.set_pixel(1, 0, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(3, 0, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(1, 2, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(3, 2, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(1, 4, white.r, white.g, white.b)
        rgbmatrix5x5.set_pixel(3, 4, white.r, white.g, white.b)
        rgbmatrix5x5.show()


motorTimer = None
def setMotor(enabled):
    global motorTimer 
    if motorTimer is not None:
        motorTimer.cancel()

    if enabled:
        GPIO.output(motor, GPIO.HIGH)
        motorTimer = threading.Timer(1, stopMotor)
        motorTimer.start()
    else:
        stopMotor()
        

def stopMotor():
    GPIO.output(motor, GPIO.LOW)

def clearRandom():
    clearDisplay()
    setMotor(False)

def setRedLight():
    red = ColorModel(238, 34, 12)
    setRoundLight(red)

def setOrangeLight(): 
    orange = ColorModel(255, 138, 16)
    setRoundLight(orange)

# Sets traffic light
def setLight():
    global currentProgram
    global displayTimer
    if currentProgram == "light":
        clearTimer()
        mDisplayTimer = threading.Timer(5.0, setLightOrange)
        mDisplayTimer.start()
        displayTimer = mDisplayTimer
    else:
        clearDisplay()
        rgbmatrix5x5.set_brightness(0.64)
        clearTimer()
    
    setRedLight()

def setLightOrange():
    setOrangeLight()
    global displayTimer
    mDisplayTimer = threading.Timer(2.0, setLightGreen)
    mDisplayTimer.start()
    displayTimer = mDisplayTimer

def setLightGreen():
    green = ColorModel(97, 216, 54)
    setRoundLight(green)
    global displayTimer
    mDisplayTimer = threading.Timer(5.0, setLightOrangeEnd)
    mDisplayTimer.start()
    displayTimer = mDisplayTimer
    setMotor(True)

def setLightOrangeEnd():
    setOrangeLight()
    global displayTimer
    mDisplayTimer = threading.Timer(2.0, endLightProgram)
    mDisplayTimer.start()
    displayTimer = mDisplayTimer

def setRoundLight(color):    
    rgbmatrix5x5.set_pixel(0, 1, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(0, 2, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(0, 3, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(1, 0, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(1, 1, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(1, 2, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(1, 3, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(1, 4, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(2, 0, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(2, 1, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(2, 2, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(2, 3, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(2, 4, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(3, 0, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(3, 1, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(3, 2, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(3, 3, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(3, 4, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(4, 1, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(4, 2, color.r, color.g, color.b)
    rgbmatrix5x5.set_pixel(4, 3, color.r, color.g, color.b)
    rgbmatrix5x5.show()

def endLightProgram(): 
    setRedLight()

# Run script for the program
try:
        clearDisplay()
        while True:
                clkState = GPIO.input(clk)
                dtState = GPIO.input(dt)
                btnAState = GPIO.input(buttonA)
                btnBState = GPIO.input(buttonB)
                if btnAState != lastStateBtnA:
                    if btnAState is 1:
                        setLight()
                        currentProgram = "light"
                    lastStateBtnA = btnAState                    
                if btnBState != lastStateBtnB:
                    if btnBState is 1:
                        setRandom()
                        currentProgram = "random"
                    lastStateBtnB = btnBState
                    currentProgram
                if clkState != clkLastState:
                        if dtState != clkState:
                                counter += 1
                        else:
                                counter -= 1
                        if counter >= 7:
                            counter = 0
                        if counter < 0:
                            counter = 7
                        setFace(counter)
                        currentProgram = "face"

                clkLastState = clkState
                sleep(0.0001)
finally:
        GPIO.cleanup()
