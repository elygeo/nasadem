import os
import re
import json
from math import floor
import requests
import rasterio
from numpy import asarray, full_like
from affine import Affine
from raster import bilinear_interp

base = "https://e4ftl01.cr.usgs.gov/MEASURES/NASADEM_HGT.001/2000.02.11/"
user = "EARTHDATA_USER"
pass_ = "EARTHDATA_PASS"
NaN = float("nan")
cache = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache")
assert os.path.exists(cache)
session = requests.session()


def sample(lon, lat, out=NaN):
    lon = asarray(lon)
    lat = asarray(lat)
    assert lon.shape == lat.shape
    if isinstance(out, (int, float)):
        out = full_like(lon, out)
    f = f"{cache}/index.json"
    if not os.path.exists(f):
        print("Downloading " + f)
        pattern = '<a href="\w+([ns]\d\d[ew]\d\d\d).zip">'
        html = session.get(base).content.decode()
        json.dump(re.findall(pattern, html), open(f, "w"), indent=2)
    index = set(json.load(open(f)))
    for j in range(floor(lon.min()), floor(lon.max()) + 1):
        j = (j + 180) % 360 - 180
        x = f"w{-j:03}" if j < 0 else f"e{j:03}"
        for k in range(floor(lat.min()), floor(lat.max()) + 1):
            y = f"s{-k:02}" if k < 0 else f"n{k:02}"
            if y + x not in index:
                continue
            f = f"{cache}/{y}{x}.zip"
            if not os.path.exists(f):
                url = f"{base}/NASADEM_HGT_{y}{x}.zip"
                print("Downloading " + f)
                resp = session.get(url)
                if resp.url != url:
                    resp = session.get(
                        resp.url, auth=(os.environ[user], os.environ[pass_])
                    )
                open(f, "wb").write(resp.content)
            dem = rasterio.open(f"zip:{f}!{y}{x}.hgt")
            M = Affine.translation(-0.5, -0.5) * ~dem.meta["transform"]
            xi, yi = M * (lon, lat)
            z = dem.read(1).T
            bilinear_interp(z, xi, yi, out)
    return out
