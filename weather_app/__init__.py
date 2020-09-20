"""
weather_app
===========

The weather_app package provides functions to access SMHI weather
forecasts.
"""
import weather_app.api as api

def get_temperature_forecast(hours):
    """
    Retrieve current SMHI predicted temperatures.

    Linearly interpolates the current SMHI temperature forecast to the
    given array of lead times.

    Args:
        hours(array): 1D array containing the lead times in hours for which
            to compute the temperature.

    Returns:
        Array containing the predicted temperatures.
    """
    lat, lon = api.lookup_location()
    forecast = api.SMHIForecast(lat, lon)
    return forecast.interpolate(hours, "temperature")

def get_precipitation_forecast():
    """
    Retrieve current SMHI predicted precipitation .

    Linearly interpolates the current SMHI precipitation forecast to the
    given array of lead times. Precipitation here includes rain, snow, graupel
    or hail.

    Args:
        hours(array): 1D array containing the lead times in hours for which
            to compute the precipitation.

    Returns:
        Array containing the predicted temperatures.
    """
    lat, lon = api.lookup_location()
    forecast = api.SMHIForecast(lat, lon)
    return forecast.interpolate(hours, "precipitation")
