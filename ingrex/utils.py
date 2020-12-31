"""Map Utils"""
from math import pi, sin, cos, tan, asin, radians, sqrt, log


class IngrexError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class BadRequest(Exception):
    def __init__(self, *args, **kwargs):
        pass


class ServerError(Exception):
    def __init__(self, *args, **kwargs):
        pass


def calc_tile(lng, lat, z):
    tile_counts = [1, 1, 1, 40, 40, 80, 80, 320, 1E3, 2E3, 2E3, 4E3, 8E3, 16E3, 16E3, 32E3]
    r_lat = radians(lat)
    tile_count = tile_counts[z]
    x_tile = int((lng + 180.0) / 360.0 * tile_count)
    y_tile = int((1.0 - log(tan(r_lat) + (1 / cos(r_lat))) / pi) / 2.0 * tile_count)
    return x_tile, y_tile


def calc_dist(lat1, lng1, lat2, lng2):
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    d_lat = lat1 - lat2
    d_lng = lng1 - lng2
    a = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lng/2)**2
    c = 2 * asin(sqrt(a))
    m = 6367.0 * c * 1000
    return m


def point_in_poly(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def transform(wg_lat, wg_lon):
    """
    transform(latitude,longitude) , WGS84
    return (latitude,longitude) , GCJ02
    """
    a = 6378245.0
    ee = 0.00669342162296594323
    if out_of_china(wg_lat, wg_lon):
        mg_lat = wg_lat
        mg_lon = wg_lon
        return mg_lat, mg_lon
    d_lat = transformLat(wg_lon - 105.0, wg_lat - 35.0)
    d_lon = transformLon(wg_lon - 105.0, wg_lat - 35.0)
    rad_lat = wg_lat / 180.0 * pi
    magic = sin(rad_lat)
    magic = 1 - ee * magic * magic
    sqrt_magic = sqrt(magic)
    d_lat = (d_lat * 180.0) / ((a * (1 - ee)) / (magic * sqrt_magic) * pi)
    d_lon = (d_lon * 180.0) / (a / sqrt_magic * cos(rad_lat) * pi)
    mg_lat = wg_lat + d_lat
    mg_lon = wg_lon + d_lon
    return mg_lat, mg_lon


def out_of_china(lat, lon):
    if lon < 72.004 or lon > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False


def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(y * pi) + 40.0 * sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * sin(y / 12.0 * pi) + 320 * sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(x * pi) + 40.0 * sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * sin(x / 12.0 * pi) + 300.0 * sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret
