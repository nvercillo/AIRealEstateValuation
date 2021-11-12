import os
import sys
from dotenv import load_dotenv
from os.path import join, dirname

import numpy

load_dotenv(join(dirname(__file__), "../../.env"))
sys.path.insert(0, "../../")  # import parent folder
from statistics import stdev
from utils.math import Math
from models.property_model import Property
from operator import itemgetter
from controllers.properties_controller import PropertiesController
from matplotlib import pyplot
from numpy import arange
from scipy.optimize import curve_fit
from scipy import stats


SEARCHING_DISTANCE = 2  # km

prop_model = Property()
prop_controller = PropertiesController()


all_props = [prop_model._query_by_id("04dbd09f-ef9f-4dbd-b5e6-54272ab49ba2")]

# objective function
def objective(x, a, b, c):
    return a * x * x + b * x


print("Getting properties")
for p in all_props:
    nearby = prop_controller.query_by_coords_and_filter(
        p.longitude,
        p.latitude,
        filters={"style": p.style, "square_footage": p.square_footage},
        SEARCHING_DISTANCE=SEARCHING_DISTANCE,
    )

    dists = []
    price_deviation = []
    for n in nearby:
        if p.id == n.id:
            continue

        dist_to_node = Math().calc_dist_bw_coords(
            (p.latitude, p.longitude), (n.latitude, n.longitude)
        )
        dists.append((dist_to_node, n))

    dists = sorted(dists, key=itemgetter(0))

    distances = [d[0] for d in dists]

    # standard price deviation
    std_prices = [abs(d[1].sold_price - p.sold_price) for d in dists]

    print("Length of data before preprocessing: ", len(distances))

    # plot input vs output
    pyplot.scatter(distances, std_prices)
    pyplot.show()

    std_dev = stdev(std_prices)
    _3_std_dev = std_dev * 3  # should contain 97.5 % of normally distrubuted data

    ind_to_remove = []

    for i in range(len(std_prices)):
        if std_prices[i] > _3_std_dev:
            ind_to_remove.append(i)

    for i in reversed(ind_to_remove):
        distances.pop(i)
        std_prices.pop(i)

    print("Length of data after removing outliers: ", len(distances))

    # curve fit
    popt, _ = curve_fit(objective, distances, std_prices)

    # summarize the parameter values
    a, b, c = popt

    """ plot input vs output """
    pyplot.scatter(distances, std_prices)

    # define a sequence of inputs between the smallest and largest known inputs
    x_line = arange(min(distances), max(distances), 0.1)

    # calculate the output for the range
    y_line = objective(x_line, a, b, c)

    # create a line plot for the mapping function
    pyplot.plot(x_line, y_line, "--", color="red")
    pyplot.show()

    y = a * x_line ** 2 + b * x_line + c
    pyplot.plot(x_line, y, "r")
    pyplot.show()

    correlation_matrix = numpy.corrcoef(x_line, y)
    correlation_xy = correlation_matrix[0, 1]
    r_squared = correlation_xy ** 2

    print(r_squared)
