"""
The weather_app.api module
==========================

This module contains the SMHIForecast class, which provides access to
to the SMHI forecast web API. Furthermore, the module provides the
lookup_location() function, which can be used to determine the latitude
and longitude coordinates of the system executing the function.
"""
import datetime
import json
import urllib
import urllib.request
import numpy as np

SMHI_REQUEST_URL = (
    "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/"
    "version/2/geotype/point/lon/{lon}/lat/{lat}/data.json"
)


def _parse_time(time):
    format = "%Y-%m-%dT%H:%M:%SZ"
    return datetime.datetime.strptime(time, format)


def lookup_location():
    """
    Geolocation lookup of current position.

    Determines latitude and longitude coordinates of the system's position
    using the ipinfo.io service.

    Returns:
        Tuple (lat, lon) containing the latitude and longitude coordinates
        associated with the IP from which the request is performed.

    """
    response = urllib.request.urlopen("https://ipinfo.io/json")
    data = json.loads(response.read())
    coordinates = data["loc"]
    lat, lon = coordinates.split(",")
    return float(lat), float(lon)


class SMHIForecast:
    """
    SMHI weather forecast.

    This class provides an interfact to the current SMHI weather forecast.
    A single forecast contains predictions for the next 10 days at varying
    temporal resolution.

    Attributes:
        reference_time(datetime.datetime): The time at which the forecast was
        produced.
        time(list): The times, given as datetime.datetime objects, of the
        predictions in this forecasts.
        temperature(list): The predicted temperature in deg. C.
        cloud_cover(list): The predicted cloud cover given as fraction in [0, 1].
        precipitation(list): The predicted mean precipitation intensity in mm/h.
        symbol(list): Symbolic representation of weather situtation. See
        opendata.smhi.se_ for reference.

.. _opendata.smhi.se: https://opendata.smhi.se/apidocs/metfcst/parameters.html#27symbols
    """

    def __make_request__(self):
        """Requests forecast from SMHI opendata."""
        url = SMHI_REQUEST_URL.format(lat=self.lat, lon=self.lon)
        try:
            response = urllib.request.urlopen(url)
        except:
            url = SMHI_REQUEST_URL.format(lat=57.42, lon=11.58)
            response = urllib.request.urlopen(url)
        self.data = json.loads(response.read())

    def __parse_forecast__(self):
        """
        Parses the forecast received from SMHI and stores relevant
           data in class attributes.
        """
        self.reference_time = _parse_time(self.data["referenceTime"])
        self.time = []
        self.temperature = []
        self.cloud_cover = []
        self.precipitation = []
        self.symbol = []
        for forecast in self.data["timeSeries"]:
            self.time.append(_parse_time(forecast["validTime"]))
            parameters = forecast["parameters"]
            for parameter in parameters:
                if parameter["name"] == "t":
                    temperature = parameter["values"][0]
                    self.temperature.append(temperature)
                if parameter["name"] == "tcc_mean":
                    cloud_cover = parameter["values"][0]
                    self.cloud_cover.append(cloud_cover)
                if parameter["name"] == "pmean":
                    precipitation = parameter["values"][0]
                    self.precipitation.append(precipitation)
                if parameter["name"] == "Wsymb2":
                    symbol = parameter["values"][0]
                    self.symbol.append(symbol)

    def __init__(self, latitude, longitude):
        """
        Fetch SMHI forecast for given location.

        Params:
            latitude(float): The latitude coordinate for which to request the forecast.
                Must lie within the SMHI forecast domain.
            longitude(float): The longitude coordinate for which to request the forecast.
                Must lie within the SMHI forecast domain.
        """
        self.lat = latitude
        self.lon = longitude
        self.__make_request__()
        self.__parse_forecast__()

    def interpolate(self, hours, variable = "temperature"):
        """
        Interpolate forecast variable to given times.

        Params:
            hours(1D array): 1-dimensional array containing the time in hours after
            the forecasts reference time.
            variable(str): String containing the attribute name to interpolate
            to the given times.

        Returns:
            1D array containing the predicted values of the variable for the given
            times.

        Throws:
            ValueError when the variable is not an attribute of the SMHIForecast
            class
        """
        try:
            y = getattr(self, variable)
        except:
            raise ValuError(f"'{variable}' is not an attribute of SMHIForecast.")

        x = np.array([(t - self.reference_time).total_seconds() / 3600 for t in self.time])
        return np.interp(hours, x, y)



