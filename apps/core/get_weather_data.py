import requests
from rest_framework import status

from weather.settings import WEATHER_API_ACCESS_KEY, WEATHER_API_BASE_URL


def GetWeatherData(city):
    params = {'access_key': WEATHER_API_ACCESS_KEY,
              'query': city}
    response = requests.get(url=WEATHER_API_BASE_URL,
                            params=params)

    if response.status_code == status.HTTP_200_OK:

        weather_data = response.json()
        if weather_data.get('error') is not None:
            return {
                "error_type": weather_data['error']['type'],
                'error_info': weather_data['error']['info']
            }
        return {
            'location_name': weather_data['location']['name'],
            'location_country': weather_data['location']['country'],
            'location_region': weather_data['location']['region'],
            'location_timezone': weather_data['location']['timezone_id'],
            'location_temperature': weather_data['current']['temperature'],
            'location_weather_icons': weather_data['current']['weather_icons'],
            'location_weather_descriptions': weather_data['current']['weather_descriptions'],
        }
