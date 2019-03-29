import os
import pyowm


def weather_msg(result):
    try:
        response = currentweather(result)
    except BaseException:
        response = "I'm having trouble getting the weather. Try again?"
    return response


def currentweather(result):
    owm = pyowm.OWM(os.environ['WEATHER_API_KEY'])
    try:
        location = result.parameters['address']['city']
    except BaseException:
        location = "New York, NY"

    try:
        forecast = owm.weather_at_place(location)
        observation = forecast.get_weather()
        weather_detail = observation.get_detailed_status()
        temperature = observation.get_temperature('fahrenheit')
        current_temp = temperature['temp']
        max_temp = temperature['temp_max']
        min_temp = temperature['temp_min']
        response = ("It is currently %s°F (high of %s°F and low of %s°F)"
                    " in %s. The current weather is %s.") % (
            current_temp, max_temp, min_temp, location, weather_detail)
        return response
    except BaseException:
        response = ("Looks like I couldn't get the weather "
                    "in %s right now. Try again?") % (
                    location)
        return response

    return 0
