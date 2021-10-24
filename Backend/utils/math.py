from math import sin, cos, sqrt, atan2, radians, pi
from numpy import arccos


class Math:
    def __init__(self):
        self.R = 6373.0  # approximate radius of earth in km

    """ return value is in kms """

    def calc_dist_bw_coords(self, coords1, coords2):
        lat1 = radians(coords1[0])
        lon1 = radians(coords1[1])
        lat2 = radians(coords2[0])
        lon2 = radians(coords2[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = self.R * c

        return distance

    def calc_max_lon_deviance(self, d):
        lon2 = arccos(-2 * pow(sin(d / (2 * self.R)), 2) + 1)

        lon2 = lon2 * 180 / pi  # convert back to degrees
        return lon2

    def calc_max_lat_deviance(self, d, lat1):
        lat1 = radians(lat1)

        lat2 = arccos(-2 * pow(sin(d / (2 * self.R)), 2) / pow(cos(lat1), 2) + 1)

        lat2 = lat2 * 180 / pi  # convert back to degreees
        return lat2

    def mode(self, _list):
        _list.sort()

        mode = None
        count = 0

        l_mode = None
        l_count = 0

        for l in _list:
            if l != l_mode:
                if l_mode is not None and l_count > count:
                    count = l_count
                    mode = l_mode

                l_mode = l
                l_count = 1
            else:
                l_count += 1
        if l_mode is not None and l_count > count:
            count = l_count
            mode = l_mode

        return mode
