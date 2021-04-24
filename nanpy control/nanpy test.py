import nanpy
import pprint

# Initialise connection
connection = nanpy.SerialManager(device="/dev/ttyUSB0")
a = nanpy.ArduinoApi(connection=connection)

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

FORMAT = '%-20s = %20s'

print((FORMAT + ' V') % ('read_vcc', a.vcc.read()))
print((FORMAT + ' sec') % ('millis', a.api.millis() / 1000.0))

print('')
print('================================')
print('firmware classes:')
print('================================')
print('status:')
pprint.pprint(a.connection.classinfo.firmware_class_status)
print('unknown ids:')
pprint.pprint(a.connection.classinfo.unknown_firmware_ids)

print('')
print('================================')
print('pins:')
print('================================')

print(FORMAT % ('total_pin_count', a.pin.count))
print(FORMAT % ('digital_names', a.pin.names_digital))
print(FORMAT % ('analog_names', a.pin.names_analog))

for pin_number in range(a.pin.count):
    print('---------- pin_number=%s ---------------' % pin_number)
    pin = a.pin.get(pin_number)
    dump(
        pin,
        'name pin_number pin_number_analog is_digital is_analog avr_pin mode digital_value analog_value programming_function'.split())
    if pin.pwm.available:
        print('--- pwm ---')
        dump(pin.pwm, '''frequency frequencies_available base_divisor divisor divisors_available
                            timer_mode
                            timer_register_name_a
                            timer_register_name_b
                            wgm
        '''.split())

print('')
print('================================')
print('defines:')
print('================================')
dump_dict(a.define.as_dict)

print('')
print('================================')
print('registers:')
print('================================')
for x in a.register.names:
    r = a.register.get(x)
    if r.size == 2:
        v = '0x%04X' % (r.value)
    else:
        v = '  0x%02X' % (r.value)

    print('%-20s = %s @0x%2X (size:%s)' % (r.name, v, r.address, r.size))

