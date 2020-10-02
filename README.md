# NASADEM sampling library for Python

Geoffrey Ely, [Elygeo Consulting](https://elygeo.com)

Given lon and lat coordinate NumPy arrays, download the necessary
[NASADEM](https://lpdaac.usgs.gov/news/release-nasadem-data-products/) tiles
and sample points with bilinear interpolation.

A [NASA Earthdata login account](https://urs.earthdata.nasa.gov/users/new) is
required, and login credentials are set via the environmental variables
EARTHDATA_USER and EARTHDATA_PASS.

Install:

    git clone git@github.com:elygeo/nasadem.git
    pip3 install -e nasadem

Example:

    import numpy
    import nasadem
    lon, lat = numpy.meshgrid([-131, -130, -129], [40, 41])
    elevation = nasadem.sample(lon, lat)

