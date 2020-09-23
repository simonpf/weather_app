Usage
=====

The `weather_app` package can be used in two ways:

1. As a command line application to display the predicted temperature
   and precipitation for the next 24 hours.
2. As a Python module providing access to the current SMHI
   weather forecast.

Command line application
------------------------

To access the current SMHI weather forecast from the command line, type:

.. code-block:: bash

   $ smhpy


Python module
-------------

The `weather_app` package provides the :code:`weather_app` import module
providing access to the current SMHI weather forecast.

.. code-block:: Python

   import weather_app

   hours = range(24)
   temperature = weather_app.get_temperature_prediction(hours)
