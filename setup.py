from setuptools import setup

NAME = "nasadem"

setup(
    name=NAME,
    modules=[NAME],
    install_requires=["requests", "numpy", "affine", "rasterio"],
)
