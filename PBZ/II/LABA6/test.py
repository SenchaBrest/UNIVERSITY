from astral import LocationInfo
from astral.sun import sun
from pytz import timezone
import datetime

# Задаем информацию о местоположении (широта и долгота)
city_name = "Москва"
latitude = 55.7558  # Широта Москвы
longitude = 37.6176  # Долгота Москвы
timezone_str = "Europe/Moscow"  # Часовой пояс Москвы

# Создаем объект с информацией о местоположении
location = LocationInfo(city_name, "Russia", timezone_str, latitude, longitude)

# Указываем дату и временную зону для которой нужно определить время события
current_time = datetime.datetime.now(timezone(timezone_str))

# Получаем информацию о солнце для указанной даты и местоположения
s = sun(location.observer, date=current_time.date())

# Выводим время наступления ночи (сумерек) и времени рассвета
dusk_time = s["dusk"].astimezone(timezone(timezone_str))
dawn_time = s["dawn"].astimezone(timezone(timezone_str))

print(f"Время наступления ночи сегодня в {city_name}: {dusk_time.strftime('%H:%M:%S')}")
print(f"Время окончания ночи сегодня в {city_name}: {dawn_time.strftime('%H:%M:%S')}")
