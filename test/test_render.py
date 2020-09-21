from weather_app.render import AsciiGraph
import datetime
import numpy as np

def test_temperature_plot(capsys):
    """
    Ensure that add_temperature_plot adds temperature markers to plot.
    """
    graph = AsciiGraph()
    x = np.linspace(0, 2 * np.pi, 21)
    y = np.sin(x)
    graph.add_temperature_plot(x, y)
    graph.render()

    captured = capsys.readouterr()

    assert graph.temperature_marker in captured.out
    assert "T [C]" in captured.out

def test_precipitation_plot(capsys):
    """
    Ensure that add_precipitation_plot adds precipitation markers to plot.
    """
    graph = AsciiGraph()
    x = np.linspace(0, 2 * np.pi, 21)
    y = 10 * np.sin(x)
    graph.add_precipitation_plot(x, y)
    graph.render()

    captured = capsys.readouterr()

    assert graph.precipitation_marker in captured.out
    assert "P [mm/h]" in captured.out

def test_set_time_range(capsys):
    """
    Ensure adds times to plot.
    """
    graph = AsciiGraph()
    x = np.linspace(0, 2 * np.pi, 21)
    y = np.sin(x)

    t0 = datetime.datetime.now()
    t1 = t0 + datetime.timedelta(seconds=24 * 60 * 60)
    graph.set_time_range(t0, t1)
    graph.render()

    captured = capsys.readouterr()

    assert ":" in captured.out
