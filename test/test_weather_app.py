"""Tests for the weather_app main module."""
from datetime import datetime
import numpy as np
from random import randint

from weather_app.api import lookup_location, SMHIForecast
from weather_app import get_temperature_forecast


def test_temperature_forecast():
    """
    Ensure that forecast is correctly interpolated to given
    hours.
    """
    lat, lon = lookup_location()
    forecast = SMHIForecast(lat, lon)

    t_0 = (forecast.time[1] - forecast.reference_time).total_seconds() / 3600
    t_1 = (forecast.time[5] - forecast.reference_time).total_seconds() / 3600

    hours = np.linspace(t_0, t_1, randint(2, 20))
    temperature_forecast = get_temperature_forecast(hours)

    assert temperature_forecast[0] == forecast.temperature[1]
    assert temperature_forecast[-1] == forecast.temperature[5]
