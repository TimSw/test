#!/usr/bin/python3
import datetime

now = datetime.datetime.now().time()

start_hour = 8
start_min = 30
stop_hour = 17
stop_min = 15

air_on_min = 8
air_on_hour = 0
time_air_on = datetime.time(0, air_on_min)

date = datetime.date(1, 1, 1)

start_light = datetime.time(start_hour, start_min)
stop_light = datetime.time(stop_hour, stop_min)
print("start_light = ", start_light)
print("stop_light = ", stop_light)

datetime_start = datetime.datetime.combine(date, start_light)
datetime_stop = datetime.datetime.combine(date, stop_light)
time_light_on = datetime_stop - datetime_start
print("time_light_on = ", time_light_on)

datetime_air_on = datetime.datetime.combine(date, time_air_on)
datetime_delta_air_on = datetime.timedelta(hours=air_on_hour, minutes=air_on_min)
print("time_air_on = ", time_air_on)
print("datetime_air_on = ", datetime_air_on)
print("datetime_delta_air_on = ", datetime_delta_air_on)

pump_repeat = int(input("Please enter a number of times the pump should "
                        "repeat: "))
print("pump_repeat = ", pump_repeat)

pump_during = 10
print("pump_during = ", pump_during)

time_pump_on = datetime.time(00, pump_during)
print("time_pump_on = ", time_pump_on)

pump_interval = time_light_on // pump_repeat
print("pump_interval = ", pump_interval)

start_times = []
print("start_times 1 = ", start_times)

stop_times = []

while pump_repeat > 1:
    start_times.append(time_light_on + (pump_interval * pump_repeat))
    pump_repeat = pump_repeat - 1

print("start_times 2 = ", start_times)
start_times.reverse()
print("start_times 3 = ", start_times)

# start_times.insert(0, datetime_start)
datetime_start_light = datetime.timedelta(hours=start_hour, minutes=start_min)
# start_times.insert(0, start_light)
start_times.insert(0, datetime_start_light)
print("start_times 4 = ", start_times)

start_times_air = []

for times in start_times:
    print(times)
    start_times_air.append(times - datetime_delta_air_on)

for i in start_times_air:
    print(i)

subtract = start_times[1] - start_times[0]
print(subtract)
print("start_times = ", start_times)
print("start_times_air = ", start_times_air)

def check()
    if start_times[0] < now < s