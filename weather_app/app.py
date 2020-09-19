import numpy as np
import datetime
from weather_app.api import lookup_location, SMHIForecast
from weather_app.render import AsciiGraph

def smhpy():
    """
    SMHPY command line application.

    This function implements the SMHPY command line application.
    It request the current forecast and plots predicted
    temperatures and precipitation to standard out.
    """
    lat, lon = lookup_location()
    forecast = SMHIForecast(lat, lon)

    x = np.linspace(0, 24, 24)
    t = forecast.interpolate(x, "temperature")
    p = forecast.interpolate(x, "precipitation")

    g = AsciiGraph(height=20, color=True)
    g.add_precipitation_plot(x, p)
    g.add_temperature_plot(x, t)
    t0 = forecast.reference_time
    t1 = t0 + datetime.timedelta(seconds=24 * 3600)
    g.set_time_range(t0, t1)
    g.render()
