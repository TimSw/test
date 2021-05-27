import nanpy
import time

print("CONNECT")
# Initialise connection
# connection = nanpy.SerialManager(device="/dev/ttyUSB0")
connection = nanpy.SerialManager(device="/dev/ttyUSB0")
arduino = nanpy.ArduinoApi(connection=connection)

# Define pin's
D0 = 0      # D0/RX - PD0
D1 = 1      # D1/TX - PD1
D2 = 2      # D2 - PD2
D3 = 3      # D3 - PD3
D4 = 4      # D4 - PD4
D5 = 5      # D5 - PD5
D6 = 6      # D6 - PD6
D7 = 7      # D7 - PD7

D8 = 8      # D8 - PB0
D9 = 9      # D9 - PB1
D10 = 10    # D10 - PB2
D11 = 11    # D11 - PB3
D12 = 12    # D12 - PB4
D13 = 13    # D13 - PB5

A0 = 14     # D14 - A0 - PC0 - ADC[0]
A1 = 15     # D15 - A1 - PC1 - ADC[1]
A2 = 16     # D16 - A2 - PC2 - ADC[2]
A3 = 17     # D17 - A3 - PC3 - ADC[3]
A4 = 18     # D18 - A4 - PC4 - ADC[4] - SDA
A5 = 19     # D19 - A5 - PC5 - ADC[5] - SCL

# Control outputs
time.sleep(5)
print("DEFINE")
arduino.pinMode(D0, arduino.OUTPUT)
arduino.pinMode(D1, arduino.OUTPUT)
arduino.pinMode(D2, arduino.OUTPUT)
arduino.pinMode(D3, arduino.OUTPUT)
arduino.pinMode(D4, arduino.OUTPUT)
arduino.pinMode(D5, arduino.OUTPUT)
arduino.pinMode(D6, arduino.OUTPUT)
arduino.pinMode(D7, arduino.OUTPUT)
time.sleep(5)
arduino.digitalWrite(D0, arduino.LOW)
print("OUTPUT HIGH")
time.sleep(5)
arduino.digitalWrite(D1, arduino.LOW)
print("OUTPUT HIGH")
time.sleep(5)
arduino.digitalWrite(D2, arduino.LOW)
print("OUTPUT HIGH")
time.sleep(5)
arduino.digitalWrite(D3, arduino.LOW)
print("OUTPUT HIGH")
time.sleep(5)
arduino.digitalWrite(D4, arduino.LOW)
print("OUTPUT HIGH")
time.sleep(5)
arduino.digitalWrite(D5, arduino.LOW)
print("OUTPUT HIGH")
time.sleep(5)
arduino.digitalWrite(D6, arduino.LOW)
print("OUTPUT HIGH")
time.sleep(5)
arduino.digitalWrite(D7, arduino.LOW)
print("OUTPUT HIGH")
time.sleep(5)
arduino.digitalWrite(D0, arduino.HIGH)
print("OUTPUT LOW")
time.sleep(5)
arduino.digitalWrite(D1, arduino.HIGH)
print("OUTPUT LOW")
time.sleep(5)
arduino.digitalWrite(D2, arduino.HIGH)
print("OUTPUT LOW")
time.sleep(5)
arduino.digitalWrite(D3, arduino.HIGH)
print("OUTPUT LOW")
time.sleep(5)
arduino.digitalWrite(D4, arduino.HIGH)
print("OUTPUT LOW")
time.sleep(5)
arduino.digitalWrite(D5, arduino.HIGH)
print("OUTPUT LOW")
time.sleep(5)
arduino.digitalWrite(D6, arduino.HIGH)
print("OUTPUT LOW")
time.sleep(5)
arduino.digitalWrite(D7, arduino.HIGH)
print("OUTPUT LOW")
time.sleep(5)
print("STOP")
