import os
import logging

import requests
from django.core.mail import mail_admins
from django.shortcuts import render
from dotenv import load_dotenv
from .weather_icon import weather_icon_day, weather_icon_night

load_dotenv()
logger = logging.getLogger('django.request')
def get_weather(request):
    logger.info('TEST')
    API = os.getenv('API_KEY')
    input_city = request.GET.get('input_city')
    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={API}&q={input_city}')
    data = response.json()
    if input_city:
        try:

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
            logger.error("An error occurred in your_view: %s")
            subject = 'Error occurred in your_view'
            message = 'Error occurred in your_view'
            mail_admins(subject, message, fail_silently=False)

        except requests.exceptions.ConnectTimeout:
            info = {
                'error': 'Не удалось обработать ваш запрос, попробуйте еще раз!'
            }
            subject = 'Error occurred in your_view'
            message = 'Error occurred in your_view'
            mail_admins(subject, message, fail_silently=False, from_email=os.getenv('Email'))
        return render(request, 'weather/weather.html', {'info': info})
    else:
        return render(request, 'weather/weather_error.html',)