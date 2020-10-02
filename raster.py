"""
2D raster operations
"""
import numpy
from numpy import empty, zeros, arange, asarray, minimum, maximum

NaN = float("nan")


def bilinear_interp(f, x, y, out=NaN):
    m, n = f.shape[:2]
    i = (x >= 0) & (x <= m - 1) & (y >= 0) & (y <= n - 1)
    j = minimum(maximum(x.astype("i"), 0), m - 2)
    k = minimum(maximum(y.astype("i"), 0), n - 2)
    x -= j
    y -= k
    f = (
        (1 - x) * (1 - y) * f[j, k]
        + (1 - x) * y * f[j, k + 1]
        + x * (1 - y) * f[j + 1, k]
        + x * y * f[j + 1, k + 1]
    )
    if isinstance(out, (int, float)):
        f[~i] = out
        return f
    out[i] = f[i]
    return out


def upsample2(f):
    """
    Up-sample a 2D array by a factor of 2 by interpolation.
    Result is scaled by a factor of 4.
    """
    n = [f.shape[0] * 2 - 1, f.shape[1] * 2 - 1] + list(f.shape[2:])
    g = empty(n, f.dtype)
    g[0::2, 0::2] = 4 * f
    g[0::2, 1::2] = 2 * (f[:, :-1] + f[:, 1:])
    g[1::2, 0::2] = 2 * (f[:-1, :] + f[1:, :])
    g[1::2, 1::2] = f[:-1, :-1] + f[1:, 1:] + f[:-1, 1:] + f[1:, :-1]
    return g


def upsample3(f):
    """
    Up-sample a 2D array by a factor of 3 by interpolation.
    Result is scaled by a factor of 9.
    """
    n = [f.shape[0] * 3 - 2, f.shape[1] * 3 - 2] + list(f.shape[2:])
    g = empty(n, f.dtype)
    g[0::3, 0::3] = 9 * f
    g[0::3, 1::3] = 6 * f[:, :-1] + 3 * f[:, 1:]
    g[0::3, 2::3] = 6 * f[:, 1:] + 3 * f[:, :-1]
    g[1::3, 0::3] = 6 * f[:-1, :] + 3 * f[1:, :]
    g[2::3, 0::3] = 6 * f[1:, :] + 3 * f[:-1, :]
    g[1::3, 1::3] = 4 * f[:-1, :-1] + f[1:, 1:] + 2 * (f[:-1, 1:] + f[1:, :-1])
    g[1::3, 2::3] = 4 * f[:-1, 1:] + f[1:, :-1] + 2 * (f[:-1, :-1] + f[1:, 1:])
    g[2::3, 1::3] = 4 * f[1:, :-1] + f[:-1, 1:] + 2 * (f[1:, 1:] + f[:-1, :-1])
    g[2::3, 2::3] = 4 * f[1:, 1:] + f[:-1, :-1] + 2 * (f[1:, :-1] + f[:-1, 1:])
    return g


def downsample(f, d):
    """
    Down-sample a 2D array by a factor d, with averaging.
    Result is scaled by a factor of d squared.
    """
    n = f.shape
    n = (n[0] + 1) // d, (n[1] + 1) // d
    g = zeros(n, f.dtype)
    for k in range(d):
        for j in range(d):
            g += f[j::d, k::d]
    return g


def downsample_sphere(f, d):
    """
    Down-sample node-registered spherical surface with averaging. The indices
    of the 2D array f are longitude and latitude. d is the decimation interval
    which should be odd to preserve nodal registration.
    """
    if d == 1:
        return f
    assert d % 2 == 1
    f = asarray(f)
    m, n = f.shape[:2]
    i = arange(d) - (d - 1) // 2
    jj = arange(0, m, d)
    kk = arange(0, n, d)
    g = zeros([jj.size, kk.size], f.dtype)
    jj, kk = numpy.ix_(jj, kk)
    for dk in i:
        k = n - 1 - abs(n - 1 - abs(dk + kk))
        for dj in i:
            j = (jj + dj) % m
            g = g + f[j, k]
    if g.dtype.kind == "i":
        g[:, 0] = g[:, 0].mean() + 0.5
        g[:, -1] = g[:, -1].mean() + 0.5
    else:
        g[:, 0] = g[:, 0].mean()
        g[:, -1] = g[:, -1].mean()
    return g
