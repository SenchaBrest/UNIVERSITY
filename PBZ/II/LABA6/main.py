import threading
import time
import datetime
from astral import LocationInfo
from astral.sun import sun
from pytz import timezone

city_name = "Москва"
latitude = 55.7558
longitude = 37.6176
timezone_str = "Europe/Moscow"
location = LocationInfo(city_name, "Russia", timezone_str, latitude, longitude)


def get_time_of_dawn_and_dusk():
    current_time = datetime.datetime.now(timezone(timezone_str))

    s = sun(location.observer, date=current_time.date())

    return s["dusk"].astimezone(timezone(timezone_str))


class WateringSystem:
    def __init__(self):
        self.water_level = 0
        self.last_watering_time = datetime.datetime.now()
        self.lock = threading.Lock()

    def manage_water_level(self):
        with self.lock:
            print("Полив начался.")

    def water_for_duration(self, minutes):
        with self.lock:
            print(f"Полив на {minutes} минут")
            time.sleep(minutes * 60)
            self.update_last_watering_time()

    def update_last_watering_time(self):
        self.last_watering_time = datetime.datetime.now()


def water_plants(plant_type, watering_system):
    while True:
        current_time = datetime.datetime.now(timezone(timezone_str))

        if plant_type == 1:
            watering_system.manage_water_level()
        elif plant_type == 2:
            if current_time.hour == 8 or current_time.hour == 20:
                watering_system.water_for_duration(3)
        elif plant_type == 3:
            dusk_time = get_time_of_dawn_and_dusk()
            if current_time - dusk_time > datetime.timedelta():
                if (current_time - watering_system.last_watering_time).days >= 2:
                    watering_system.water_for_duration(2)
        time.sleep(60)


watering_system = WateringSystem()

# thread_1 = threading.Thread(target=water_plants, args=(1, watering_system))
thread_2 = threading.Thread(target=water_plants, args=(2, watering_system))
# thread_3 = threading.Thread(target=water_plants, args=(3, watering_system))

# thread_1.start()
thread_2.start()
# thread_3.start()

# thread_1.join()
thread_2.join()
# thread_3.join()
