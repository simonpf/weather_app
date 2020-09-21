from weather_app.app import smhpy

def test_smhpy(capsys):
    """
    Ensure that add_temperature_plot adds temperature markers to plot.
    """
    smhpy()
    captured = capsys.readouterr()

    assert "T [C]" in captured.out
    assert "P [mm/h]" in captured.out
    assert "Temperature" in captured.out
    assert "Precipitation" in captured.out
    assert "Time" in captured.out
