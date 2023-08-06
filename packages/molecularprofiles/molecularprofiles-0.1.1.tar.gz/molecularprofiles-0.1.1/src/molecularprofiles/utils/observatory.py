"""
Module containing functionality allows to get observatory's coordinates
and select meteorological data depending on the season for the South and North hemisphere

"""

import numpy as np
import os
import logging
import logging.config

ROOTDIR = os.path.dirname(os.path.abspath(__file__))
log_config_file = f"{ROOTDIR}/mdps_log.conf"
logging.config.fileConfig(fname=log_config_file, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def ddmmss2deg(degrees, minutes, seconds):
    """
    This function computes the value, in degrees, of an angle expressed in degrees, minutes, seconds
    Input: (integers) degrees, minutes, seconds
    Output: (float) angle in degrees
    """

    if degrees > 0.0:
        angle = degrees + (minutes / 60.0) + (seconds / 3600.0)
    else:
        angle = degrees - (minutes / 60.0) - (seconds / 3600.0)
    return angle


def get_observatory_coordinates(observatory):
    """Give latitude, longitude of the observatory"""
    if observatory == "north":
        latitude = ddmmss2deg(28, 45, 42.462)
        longitude = ddmmss2deg(-17, 53, 26.525)
        return latitude, longitude
    elif observatory == "south":
        latitude = ddmmss2deg(-24, 40, 24.8448)
        longitude = ddmmss2deg(-70, 18, 58.4712)
        return latitude, longitude
    else:
        logger.error("Unknown observatory!")
        latitude = np.float(input("Observatory latitude (in degrees):"))
        longitude = np.float(input("Observatory longitude (in degrees):"))
        return latitude, longitude


def get_winter_months():
    """Return winter months for the North hemisphere"""
    return [1, 2, 3, 4, 11, 12]


def get_summer_months():
    """Return summer months for the North hemisphere"""
    return [6, 7, 8, 9, 10]


def get_all_months():
    """Return all months for any hemisphere"""
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


def get_intermediate_months():
    """Return spring/autumn months for the North hemisphere"""
    return [5, 6, 10, 11]


def get_epoch(epoch):
    """Return the season for the North hemisphere"""
    valid_epochs = {
        "winter": get_winter_months(),
        "summer": get_summer_months(),
        "intermediate": get_intermediate_months(),
        "all": get_all_months(),
    }
    return valid_epochs[epoch]


def get_south_winter_months():
    """Return winter months for the South hemisphere"""
    return [5, 6, 7, 8, 9, 10]


def get_south_summer_months():
    """Return summer months for the South hemisphere"""
    return [1, 2, 3, 4, 5, 10, 11, 12]


def get_south_epoch(epoch):
    """Return the season for the South hemisphere"""
    valid_epochs = {
        "winter": get_south_winter_months(),
        "summer": get_south_summer_months(),
        "all": get_all_months(),
    }
    return valid_epochs[epoch]


def select_new_epochs_dataframe_north(dataframe_atmo_profile, epoch_text):
    """
    Select part of dataframe rows for a given season (North)
    The selection is date-based
    """

    epoch = get_epoch(epoch_text)

    if epoch_text == "winter":
        condition = (
            (dataframe_atmo_profile.month == epoch[0])
            | (dataframe_atmo_profile.month == epoch[1])
            | (dataframe_atmo_profile.month == epoch[2])
            | (dataframe_atmo_profile.month == epoch[3])
            | ((dataframe_atmo_profile.month == epoch[4]) & (dataframe_atmo_profile.day > 15))
            | (dataframe_atmo_profile.month == epoch[5])
        )
        new_dataframe_atmo_profile = dataframe_atmo_profile[condition]

    elif epoch_text == "summer":
        condition = (
            ((dataframe_atmo_profile.month == epoch[0]) & (dataframe_atmo_profile.day > 20))
            | (dataframe_atmo_profile.month == epoch[1])
            | (dataframe_atmo_profile.month == epoch[2])
            | (dataframe_atmo_profile.month == epoch[3])
        )
        new_dataframe_atmo_profile = dataframe_atmo_profile[condition]

    elif epoch_text == "intermediate":
        condition = (
            (dataframe_atmo_profile.month == epoch[0])
            | ((dataframe_atmo_profile.month == epoch[1]) & (dataframe_atmo_profile.day <= 20))
            | ((dataframe_atmo_profile.month == epoch[2]) & (dataframe_atmo_profile.day > 5))
            | ((dataframe_atmo_profile.month == epoch[3]) & (dataframe_atmo_profile.day <= 15))
        )
        new_dataframe_atmo_profile = dataframe_atmo_profile[condition]

    return new_dataframe_atmo_profile


def select_new_epochs_dataframe_south(dataframe_atmo_profile, epoch_text):
    """
    Select part of dataframe rows for a given season (South)
    The selection is date-based
    """

    epoch = get_south_epoch(epoch_text)

    if epoch_text == "summer":
        condition = (
            (dataframe_atmo_profile.month == epoch[0])
            | (dataframe_atmo_profile.month == epoch[1])
            | (dataframe_atmo_profile.month == epoch[2])
            | (dataframe_atmo_profile.month == epoch[3])
            | ((dataframe_atmo_profile.month == epoch[4]) & (dataframe_atmo_profile.day < 15))
            | ((dataframe_atmo_profile.month == epoch[5]) & (dataframe_atmo_profile.day > 15))
            | (dataframe_atmo_profile.month == epoch[6])
            | (dataframe_atmo_profile.month == epoch[7])
        )
    elif epoch_text == "winter":
        condition = (
            ((dataframe_atmo_profile.month == epoch[0]) & (dataframe_atmo_profile.day > 15))
            | (dataframe_atmo_profile.month == epoch[1])
            | (dataframe_atmo_profile.month == epoch[2])
            | (dataframe_atmo_profile.month == epoch[3])
            | (dataframe_atmo_profile.month == epoch[4])
            | ((dataframe_atmo_profile.month == epoch[5]) & (dataframe_atmo_profile.day < 15))
        )
    new_dataframe_atmo_profile = dataframe_atmo_profile[condition]
    return new_dataframe_atmo_profile


def select_new_epochs_dataframe_density_north(dataframe_atmo_profile, epoch_text):
    """
    Select part of dataframe rows for a given season (North)
    The selection is based on the value of the atmospheric molecular density
    """

    if epoch_text == "summer":
        condition = dataframe_atmo_profile[
            (dataframe_atmo_profile.n_exp > 0.88) & (dataframe_atmo_profile.P == 125)
        ]
    elif epoch_text == "winter":
        condition = dataframe_atmo_profile[
            (dataframe_atmo_profile.n_exp < 0.8375) & (dataframe_atmo_profile.P == 125)
        ]
    elif epoch_text == "intermediate":
        condition = dataframe_atmo_profile[
            (dataframe_atmo_profile.n_exp < 0.88)
            & (dataframe_atmo_profile.n_exp > 0.8375)
            & (dataframe_atmo_profile.P == 125)
        ]
    new_dataframe_atmo_profile = dataframe_atmo_profile[
        dataframe_atmo_profile.MJD.isin(condition.MJD)
    ]
    return new_dataframe_atmo_profile


def select_new_epochs_dataframe_density_south(dataframe_atmo_profile, epoch_text):
    """
    Select part of dataframe rows for a given season (South)
    The selection is based on the value of the atmospheric molecular density
    """

    if epoch_text == "summer":
        condition = dataframe_atmo_profile[
            (dataframe_atmo_profile.n_exp > 0.88) & (dataframe_atmo_profile.P == 125)
        ]
    elif epoch_text == "winter":
        condition = dataframe_atmo_profile[
            (dataframe_atmo_profile.n_exp < 0.88) & (dataframe_atmo_profile.P == 125)
        ]
    new_dataframe_atmo_profile = dataframe_atmo_profile[
        dataframe_atmo_profile.MJD.isin(condition.MJD)
    ]
    return new_dataframe_atmo_profile


def select_epoch(file, epoch_text):
    """
    Select part of the txt converted grib2 data for a given season.
    The selection is based on the value of the atmospheric molecular density
    """

    global months, month
    logger.info("loading and selecting data")
    file = open(file)
    (
        date,
        year,
        month,
        day,
        hour,
        mjd,
        pressure,
        temperature,
        height,
        n_density,
        u_component,
        v_component,
        relative_humidity,
    ) = np.loadtxt(
        file, usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13), unpack=True, skiprows=1
    )

    epoch = get_epoch(epoch_text)

    if epoch_text == "all":
        condition = month < 13
    elif epoch_text == "winter":
        condition = (
            (month == epoch[0]) | (month == epoch[1]) | (month == epoch[2]) | (month == epoch[3])
        )
    elif epoch_text == "summer":
        condition = (month == epoch[0]) | (month == epoch[1]) | (month == epoch[2])
    elif epoch_text == "intermediate":
        condition = (
            (month == epoch[0])
            | (month == epoch[1])
            | (month == epoch[2])
            | (month == epoch[3])
            | (month == epoch[4])
        )
    date = date[condition]
    modified_julian_date = mjd[condition]
    height = height[condition]
    number_density = n_density[condition]
    pressure = pressure[condition]
    temperature = temperature[condition]
    u_wind_component = u_component[condition]
    v_wind_component = v_component[condition]
    relative_humidity = relative_humidity[condition]

    # print(date, year, month, day, hour, modified_julian_date, pressure, height, number_density, temperature, u_wind_component, v_wind_component, relative_humidity)
    return (
        date,
        year,
        month,
        day,
        hour,
        modified_julian_date,
        pressure,
        height,
        number_density,
        temperature,
        u_wind_component,
        v_wind_component,
        relative_humidity,
    )


def get_closest_gridpoint(lat, lon, gridstep):
    """
    :param lat: float
    :param lon: float
    :param gridstep: float. Step in which the grid is divided (0.75 degrees for ECMWF data
    and 1.0 degrees for GDAS data)
    :return: nearest grid point
    """
    step = gridstep  # grid step in degrees
    lons_grid = np.zeros(int(360 / step) + 1)
    lats_grid = np.zeros(int(180 / step) + 1)

    # getting the grid points:
    for i in range(len(lons_grid)):
        # lons_grid[i] = step * i
        lons_grid[i] = -180 + step * i
    for i in range(len(lats_grid)):
        lats_grid[i] = -90 + step * i

    logger.info(f"Latidude of interest is {lat:5.2f}")
    # logger.info(f"Longitude of interest is {(lon % 360):5.2f}")
    logger.info(f"Longitude of interest is {lon:5.2f}")
    nearest_lat = find_nearest(lats_grid, lat)
    logger.info(f"nearest latitude is {nearest_lat:4.1f}")
    # nearest_lon = find_nearest(lons_grid, lon % 360)
    nearest_lon = find_nearest(lons_grid, lon)
    logger.info(f"nearest longitude is {nearest_lon:5.1f}")
    return nearest_lat, nearest_lon


def find_nearest(grid_position, value):
    """Function to find the nearest grid position to a given latitude or longitude"""
    return grid_position[np.abs(grid_position - value).argmin()]
