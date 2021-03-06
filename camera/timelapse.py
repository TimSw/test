#!/usr/bin/python3
import time
import picamera

camera = picamera.PiCamera(resolution=(1280, 720), framerate=30)
# Rotate 90°
camera.rotation = 90
# Set ISO to the desired value
camera.iso = 100
# Wait for the automatic gain control to settle
time.sleep(2)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g
for filename in camera.capture_continuous("images/img{counter:03d}.jpg"):
    print("Captured %s" % filename)
    time.sleep(300)  # wait 5 minutes
