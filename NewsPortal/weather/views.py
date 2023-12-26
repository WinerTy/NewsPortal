import os

import requests
from django.shortcuts import render
from dotenv import load_dotenv
from django.http import HttpRequest

load_dotenv()

def get_weather(request):
    API = os.getenv('API_KEY')
    input_city = request.GET.get('input_city')
    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={API}&q={input_city}')
    data = response.json()
    if input_city:
        try:
            weather_icon_day = {
                1000: 'icon/clear-day.svg',
                1003: 'icon/partly-cloudy-day.svg',
                1006: 'icon/cloudy.svg',
                1009: 'icon/overcast-day.svg',
                1030: 'icon/fog-day.svg',
                1063: 'icon/partly-cloudy-day-rain.svg',
                1066: 'icon/partly-cloudy-day-snow.svg',
                1069: 'icon/partly-cloudy-day-sleet.svg',
                1072: 'icon/partly-cloudy-day-drizzle.svg',
                1087: 'icon/thunderstorms-day.svg',
                1114: 'icon/partly-cloudy-day-snow.svg',
                1117: 'icon/wind-snow.svg',
                1135: 'icon/fog-day.svg',
                1147: 'icon/fog-day.svg',
                1150: 'icon/partly-cloudy-day-rain.svg',
                1153: 'icon/partly-cloudy-day-snow.svg',
                1168: 'icon/partly-cloudy-day-snow.svg',
                1171: 'icon/overcast-day-snow.svg',
                1180: 'icon/partly-cloudy-day-rain.svg',
                1183: 'icon/partly-cloudy-day-rain.svg',
                1186: 'icon/overcast-day-rain.svg',
                1189: 'icon/overcast-day-rain.svg',
                1192: 'icon/extreme-day-rain.svg',
                1195: 'icon/extreme-day-rain.svg',
                1198: 'icon/overcast-day-drizzle.svg',
                1201: 'icon/extreme-day-drizzle.svg',
                1204: 'icon/partly-cloudy-day-sleet.svg',
                1207: 'icon/overcast-day-sleet.svg',
                1210: 'icon/partly-cloudy-day-snow.svg',
                1213: 'icon/partly-cloudy-day-snow.svg',
                1216: 'icon/overcast-day-snow.svg',
                1219: 'icon/overcast-day-snow.svg',
                1222: 'icon/extreme-day-snow.svg',
                1225: 'icon/extreme-day-snow.svg',
                1237: 'icon/partly-cloudy-day-hail.svg',
                1240: 'icon/overcast-day-rain.svg',
                1243: 'icon/extreme-day-rain.svg',
                1246: 'icon/extreme-day-rain.svg',
                1249: 'icon/overcast-day-sleet.svg',
                1252: 'icon/extreme-day-sleet.svg',
                1255: 'icon/overcast-day-snow.svg',
                1258: 'icon/extreme-day-snow.svg',
                1261: 'icon/overcast-hail.svg',
                1264: 'icon/extreme-night-hail.svg',
                1273: 'icon/thunderstorms-day-rain.svg',
                1276: 'icon/thunderstorms-day-extreme-rain.svg',
                1279: 'icon/thunderstorms-day-overcast-snow.svg',
                1282: 'icon/thunderstorms-day-extreme-snow.svg',
            }
            weather_icon_night ={
                1000: 'icon/clear-night.svg',
                1003: 'icon/partly-cloudy-night.svg',
                1006: 'icon/cloudy.svg',
                1009: 'icon/overcast-night.svg',
                1030: 'icon/fog-night.svg',
                1063: 'icon/partly-cloudy-night-rain.svg',
                1066: 'icon/partly-cloudy-night-snow.svg',
                1069: 'icon/partly-cloudy-night-sleet.svg',
                1072: 'icon/partly-cloudy-night-drizzle.svg',
                1087: 'icon/thunderstorms-night.svg',
                1114: 'icon/partly-cloudy-night-snow.svg',
                1117: 'icon/wind-snow.svg',
                1135: 'icon/fog-night.svg',
                1147: 'icon/fog-night.svg',
                1150: 'icon/partly-cloudy-night-rain.svg',
                1153: 'icon/partly-cloudy-night-snow.svg',
                1168: 'icon/partly-cloudy-night-snow.svg',
                1171: 'icon/overcast-night-snow.svg',
                1180: 'icon/partly-cloudy-night-rain.svg',
                1183: 'icon/partly-cloudy-night-rain.svg',
                1186: 'icon/overcast-night-rain.svg',
                1189: 'icon/overcast-night-rain.svg',
                1192: 'icon/extreme-night-rain.svg',
                1195: 'icon/extreme-night-rain.svg',
                1198: 'icon/overcast-night-drizzle.svg',
                1201: 'icon/extreme-night-drizzle.svg',
                1204: 'icon/partly-cloudy-night-sleet.svg',
                1207: 'icon/overcast-night-sleet.svg',
                1210: 'icon/partly-cloudy-night-snow.svg',
                1213: 'icon/partly-cloudy-night-snow.svg',
                1216: 'icon/overcast-night-snow.svg',
                1219: 'icon/overcast-night-snow.svg',
                1222: 'icon/extreme-night-snow.svg',
                1225: 'icon/extreme-night-snow.svg',
                1237: 'icon/partly-cloudy-night-hail.svg',
                1240: 'icon/overcast-night-rain.svg',
                1243: 'icon/extreme-night-rain.svg',
                1246: 'icon/extreme-night-rain.svg',
                1249: 'icon/overcast-night-sleet.svg',
                1252: 'icon/extreme-night-sleet.svg',
                1255: 'icon/overcast-night-snow.svg',
                1258: 'icon/extreme-night-snow.svg',
                1261: 'icon/overcast-hail.svg',
                1264: 'icon/extreme-night-hail.svg',
                1273: 'icon/thunderstorms-night-rain.svg',
                1276: 'icon/thunderstorms-night-extreme-rain.svg',
                1279: 'icon/thunderstorms-night-overcast-snow.svg',
                1282: 'icon/thunderstorms-night-extreme-snow.svg',

            }

            is_day = data['current']['is_day']
            if is_day == 1:
                icon_code = data['current']['condition']['code']
                icon = weather_icon_day.get(icon_code, 'not-available.svg')
            else:
                icon_code = data['current']['condition']['code']
                icon = weather_icon_night.get(icon_code, 'not-available.svg')

            speed_mps = data['current']['wind_kph'] * 1000 / 3600
            speed = round(speed_mps, 2)
            if speed_mps > 13:
                icon_wind = 'icon/windsock.svg'
            else:
                icon_wind = 'icon/windsock-weak.svg'

            temp = data['current']['temp_c']

            if 20 < temp < 100:
                icon_temp = 'icon/thermometer-warmer.svg'
            if 0 < temp < 20:
                icon_temp = 'icon/thermometer-celsius.svg'
            if temp <= 0:
                icon_temp = 'icon/thermometer-colder.svg'

            tempfeel = data['current']['feelslike_c']
            if 20 < tempfeel < 100:
                icon_feel = 'icon/thermometer-warmer.svg'
            if 0 < tempfeel < 20:
                icon_feel = 'icon/thermometer-celsius.svg'
            if tempfeel < 0:
                icon_feel = 'icon/thermometer-colder.svg'


            info = {
                'city': data['location']['name'],
                'location': data['location']['country'],
                'time': data['location']['localtime'],
                'wind': speed,
                'wind_rat': data['current']['wind_dir'],
                'weather': data['current']['condition']['text'],
                'icon': icon,
                'icon_wind': icon_wind,
                'icon_temp': icon_temp,
                'icon_feel': icon_feel,
                'temp': temp,
                'tempfeel': tempfeel,
            }

        except (KeyError, AttributeError, TypeError, ValueError):
            info = {
                'error': 'Произошла ошибка, проверьте правильность написания города!',
            }
        return render(request, 'weather/weather.html', {'info': info})
    else:
        return render(request, 'weather/weather_error.html',)