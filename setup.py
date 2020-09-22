import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="weather_app_simon",
    version="0.0.2",
    author="Simon Pfreundschuh",
    author_email="simon.pfreundschuh@chalmers.se",
    description="My first package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simonpf/weatherapp",
    packages=setuptools.find_packages(), # Searches modules in current directory.
    python_requires='>=3.6',
    install_requires=[
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "smhpy=weather_app.app:smhpy"
        ]
    }
)
