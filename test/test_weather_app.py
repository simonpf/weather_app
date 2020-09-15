"""Tests for the weather_app main module."""
from weather_app import get_precipitation_forecast

def test_precipitation_forecast():
    """
    Ensure consistency of precipitation forecast by comparing 2h-resolution
    forecast to a sub-sampled 1h-resolution forecast.
    """
    hours = range(24)
    forecast_1h = get_precipitation_forecast(hours)
    assert len(forecast_1h) == 24

    hours = range(0, 24, 2)
    forecast_2h = get_precipitation_forecast(hours)
    assert len(forecast_2h) == 12

    assert all(forecast_1h[::2] == forecast_2h)
