"""
Unit tests for the weaterapp.api module.
"""
from weather_app.api import lookup_location, SMHIForecast


def test_lookup_location():
    """
    Ensure that location lookup returns tuple of float values.
    """
    lat, lon = lookup_location()
    assert type(lat) == float
    assert type(lon) == float


def test_smhi_api():
    """
    Obtain weather forecast for Göteborg and assert that
    attributes are non-empty.
    """
    forecast = SMHIForecast(57.42, 11.58)

    assert len(forecast.time) > 0
    assert len(forecast.temperature) > 0
    assert len(forecast.precipitation) > 0
    assert len(forecast.cloud_cover) > 0
    assert len(forecast.symbol) > 0
