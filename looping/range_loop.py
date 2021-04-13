#!/usr/bin/python3
import datetime

# Initialise current time
now = datetime.datetime.now().time()
date = datetime.date(1, 1, 1)
timedelta_now = datetime.timedelta(hours=datetime.datetime.now().hour,
                                   minutes=datetime.datetime.now().minute)
print("timedelta_now = ", timedelta_now)

# Initialise variables
# Light
start_hour = 8
start_min = 30
stop_hour = 17
stop_min = 15
# Pump
pump_repeat = int(input("Please enter a number of times the pump should "
                        "repeat: "))
print("pump_repeat = ", pump_repeat)
repeats = pump_repeat - 1
pump_during = 10
print("pump_during = ", pump_during)
# Air
air_on_hour = 0
air_on_min = 8

# Convert times
# Light
start_light = datetime.time(start_hour, start_min)
stop_light = datetime.time(stop_hour, stop_min)
print("start_light = ", start_light)
print("stop_light = ", stop_light)
datetime_start = datetime.datetime.combine(date, start_light)
datetime_stop = datetime.datetime.combine(date, stop_light)
time_light_on = datetime_stop - datetime_start
timedelta_start_light = datetime.timedelta(hours=start_hour, minutes=start_min)
print("time_light_on = ", time_light_on)
# Air
time_air_on = datetime.time(air_on_hour, air_on_min)
timedelta_air_on = datetime.timedelta(hours=air_on_hour, minutes=air_on_min)
print("time_air_on = ", time_air_on)
print("timedelta_air_on = ", timedelta_air_on)
# Pump
time_pump_on = datetime.time(00, pump_during)
datetime_pump_on = datetime.datetime.combine(date, time_pump_on)
timedelta_pump_on = datetime.timedelta(hours=00, minutes=pump_during)
pump_interval = time_light_on // pump_repeat
print("time_pump_on = ", time_pump_on)
print("datetime_pump_on = ", datetime_pump_on)
print("pump_interval = ", pump_interval)

# Initialise lists
pump_start_times = []
pump_stop_times = []
air_start_times = []
air_stop_times = []

# Determine first list
while repeats > 0:
    pump_start_times.append(timedelta_start_light +
                            (pump_interval * repeats))
    repeats = repeats - 1
pump_start_times.reverse()
pump_start_times.insert(0, timedelta_start_light)

# Determine other lists depending on first
for times in pump_start_times:
    pump_stop_times.append(times + timedelta_pump_on)
    air_start_times.append(times - timedelta_air_on)

# Print results
for i in pump_start_times:
    print(i)
for i in pump_stop_times:
    print(i)
for i in air_start_times:
    print(i)

# Set outputs
print("timedelta_now = ", timedelta_now)

# Set outputs
#teller = len(pump_start_times)
#print("Number of elements in the list: ", teller)
#print(len(pump_start_times))
#for times in pump_start_times:
output_on = 0
for times in range(len(pump_start_times)):
    print(times)
    if pump_start_times[times] < timedelta_now < pump_stop_times[times]:
        print("pump_start_times[times] = ", pump_start_times[times])
        print("timedelta_now = ", timedelta_now)
        print("pump_stop_times[times] = ", pump_stop_times[times])
        print("ON")
        output_on = 1
    else:
        print("off")

if output_on == 1:
    print("OUTPUT ON")
    output_on = 0
else:
    print("OUTPUT OFF")
