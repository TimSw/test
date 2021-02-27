#!/usr/bin/python3
import time
import RPi.GPIO as GPIO

# 1. First set up RPi.GPIO (as described here)
GPIO.setmode(GPIO.BOARD)

mode = GPIO.getmode()
print(mode)

GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)

# 2. To set an output high:
GPIO.output(29, GPIO.HIGH)
# or
# GPIO.output(12, 1)
# or
# GPIO.output(12, True)

print("1 AAN")
time.sleep(5)

GPIO.output(31, GPIO.HIGH)
print("2 AAN")
time.sleep(5)

GPIO.output(33, GPIO.HIGH)
print("3 AAN")
time.sleep(5)

GPIO.output(35, GPIO.HIGH)
print("4 AAN")
time.sleep(5)


# 3. To set an output low:
GPIO.output(29, GPIO.LOW)
# or
# GPIO.output(12, 0)
# or
# GPIO.output(12, False)

print("1 UIT")
time.sleep(5)

GPIO.output(31, GPIO.LOW)
print("2 UIT")
time.sleep(5)

GPIO.output(33, GPIO.LOW)
print("3 UIT")
time.sleep(5)

GPIO.output(35, GPIO.LOW)
print("4 UIT")
time.sleep(5)


GPIO.output(29, GPIO.HIGH)
print("1 AAN")
time.sleep(5)

GPIO.output(31, GPIO.HIGH)
print("2 AAN")
time.sleep(5)

GPIO.output(33, GPIO.HIGH)
print("3 AAN")
time.sleep(5)

GPIO.output(35, GPIO.HIGH)
print("4 AAN")
time.sleep(5)


GPIO.output(29, GPIO.LOW)
print("1 UIT")
time.sleep(5)

GPIO.output(31, GPIO.LOW)
print("2 UIT")
time.sleep(5)

GPIO.output(33, GPIO.LOW)
print("3 UIT")
time.sleep(5)

GPIO.output(35, GPIO.LOW)
print("4 UIT")
time.sleep(5)


GPIO.cleanup()
print("CLEANUP")
