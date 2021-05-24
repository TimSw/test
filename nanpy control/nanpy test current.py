import nanpy
import time

# Initialise connection
# connection = nanpy.SerialManager(device="/dev/ttyUSB0")
connection = nanpy.SerialManager(device="/dev/ttyUSB1")
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

# Initialise parameters
ACTectionRange = 10         # 5A, 10A, 20A
VREF = 5                    # 5V
ACCurrtntValue = 0
peakVoltage = 0
voltageVirtualValue = 0     # Vrms

for i in range(5):
    peakVoltage = arduino.analogRead(A0)   # read peak voltage
    print("peakVoltage = ", peakVoltage)
    time.sleep(1)

# peakVoltage = peakVoltage / 5
# print("peakVoltage / 5 = ", peakVoltage)

# change the peak voltage to the Virtual Value of voltage
voltageVirtualValue = peakVoltage * 0.707
print("voltageVirtualValue = ", voltageVirtualValue)

# The circuit is amplified by 2 times, so it is divided by 2
voltageVirtualValue = (voltageVirtualValue / 1024 * VREF ) / 2
print("voltageVirtualValue = ", voltageVirtualValue)

ACCurrtntValue = voltageVirtualValue * ACTectionRange

print(ACCurrtntValue)


