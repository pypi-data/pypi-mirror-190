#!/usr/bin/python3

"""
set of utilities for decoding & analysing grib files
"""

from builtins import str
import sys
import gc
import argparse
import os
import logging
import logging.config
import multiprocessing
from multiprocessing import Process
import numpy as np
import pygrib as pg
from molecularprofiles.utils.observatory import get_observatory_coordinates, get_closest_gridpoint
from tqdm import tqdm
from astropy.time import Time
from molecularprofiles.utils.meteorological_constants import (
    STD_NUMBER_DENSITY,
    STD_AIR_PRESSURE,
    STD_AIR_TEMPERATURE,
    DENSITY_SCALE_HEIGHT,
)

ROOTDIR = os.path.dirname(os.path.abspath(__file__))
log_config_file = f"{ROOTDIR}/mdps_log.conf"
logging.config.fileConfig(fname=log_config_file, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def get_altitude_from_geopotential(geop_height, latitude_obs):
    """
    Function to compute the real altitude from the geopotential value at
    a certain coordinates on Earth
    :param geop_height:
    :param latitude_obs: geographical latitude of interest in degrees
    :return: real altitude as fGeoidOffset (in m)
    """
    latitude = np.radians(latitude_obs)
    geop_heightkm = (
        geop_height / 1000.0 / 9.80665
    )  # dividing by the acceleration of gravity on Earth
    cos2lat = np.cos(2 * latitude)
    # convert from geopotential height to geometric altitude:
    # Uses expression 20 from http://www.earth.sinica.edu.tw/~bfchao/publication/eng/2005-Boy&Chao_JGR2005_precise%20evaluation%20of%20atmospheric%20loading%20effects%20on%20earths%20time-variable%20gravity%20field.pdf
    geo_altitude = (1.0 + 0.002644 * cos2lat) * geop_heightkm + (
        1 + 0.0089 * cos2lat
    ) * geop_heightkm * geop_heightkm / 6245.0
    # convert geometric altitude to meter
    return 1.0e3 * geo_altitude  # This is fGeoidOffset


def get_altitude_from_geopotential_height(geop, latitude_obs):
    """
    Function to compute the real altitude from the geopotential value at
    a certain coordinates on Earth
    :param geop_height:
    :param latitude_obs: geographical latitude of interest in degrees
    :return: real altitude as fGeoidOffset (in m)
    """
    latitude = np.radians(latitude_obs)
    geop_km = geop / 1000.0
    cos2lat = np.cos(2 * latitude)
    # convert from geopotential height to geometric altitude:
    # Uses expression 20 from http://www.earth.sinica.edu.tw/~bfchao/publication/eng/2005-Boy&Chao_JGR2005_precise%20evaluation%20of%20atmospheric%20loading%20effects%20on%20earths%20time-variable%20gravity%20field.pdf
    geoid_offset = (1.0 + 0.002644 * cos2lat) * geop_km + (
        1 + 0.0089 * cos2lat
    ) * geop_km * geop_km / 6245.0
    # convert GEOID_OFFSET to meter
    return 1.0e3 * geoid_offset  # This is fGeoidOffset


def date2mjd(year, month, day, hour, minute=0, second=0):
    """
    This function computes the mjd value corresponding to an input date, in the year, month, day, hour format

    Input:
        (integers) year, month, day and hour.
        Optionals: minutes and seconds. If left blank, they are assumed equal 0

    Output:
        (float) mjd
    """

    year = str(int(year))
    month = f"{int(month):02d}"
    day = f"{int(day):02d}"
    hour = f"{int(hour):02d}"
    minute = f"{int(minute):02d}"
    second = f"{int(second):02d}"

    t = Time(
        year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second,
        format="isot",
        scale="utc",
    )
    return round(t.mjd, 2)


def mjd2date(mjd):
    """
    This function computes the date from an input mjd day

     Input: mjd (float)

    Output: year, month, day, hour (integers) corresponding to the mjd input day
    """

    time = Time(mjd, format="mjd")
    return (
        int(time.datetime.year),
        int(time.datetime.month),
        int(time.datetime.day),
        int(time.datetime.hour),
    )


def get_gribfile_variables(file_name):
    """
    Function that returns all the different variable names in a grib file
    :param file_name:
    :return: varname (list): variable names
             varshortname (list): variable short names
    """
    logger.info("opening file...")
    with pg.open(file_name) as grib_file:
        varshortname = []
        varname = []
        grib_file.read(10)[0]
        while True:
            v = grib_file.read(1)[0]
            variable_name = v.name.replace(" ", "")
            variable_short_name = v.shortName
            if variable_name not in varname:
                varname.append(variable_name)
                varshortname.append(variable_short_name)
            else:
                break
    return varname, varshortname


def get_plevels(atmo_parameter):
    """
    The measurements of atmospheres parameters are taking place in various pressure levels.
    This functions returns the indices of these levels where we have measurements
    for the given atmospheric parameter.
    e.g. for GDAS data that should be a range of values [1, 23]

    :param atmo_parameter: Atmospheric parameter from grib file.
    :type atmo_parameter: string

    :return: list with the indices of the pressure levels
    """

    plevels = []
    index = []
    for i in range(len(atmo_parameter)):
        pressure_level = atmo_parameter[i].level
        if pressure_level not in plevels:
            plevels.append(pressure_level)
            index.append(i + 1)
        else:
            break
    return index


def get_grib_file_data(file_name):
    """
    This function opens a grib file, selects the parameters
    (all available: Temperature, Geopotential, RH, ...),
    and creates a dictionary variable with these parameters.
    It also returns the variable name and variable short name

    Input: file_name (string)
           observatory (string). Possible values are 'north' or 'south'
           gridstep (float): grid spacing in degrees.
           Values are 1.0 for GDAS data and 0.75 for ECMWF data.

    Output: a txt file with the exact name as the input file name, but with .txt as extension
    """

    logger.info(f"Working on {file_name}")
    logger.info("getting all variable names...")
    variable_name, variable_short_name = get_gribfile_variables(file_name)
    logger.info(f"indexing the file {file_name} (this might take a while...)")
    grib_file = pg.index(file_name, "shortName", "typeOfLevel")
    logger.info(
        f"selecting the parameters information for {file_name} (this might take a while...)"
    )
    data = []

    for short_name in variable_short_name:
        var = grib_file.select(shortName=short_name, typeOfLevel="isobaricInhPa")
        data.append(var)
        gc.collect()

    datadict = dict(zip(variable_name, data))
    data = None
    gc.collect()
    return variable_name, datadict


def fill_relative_humidity_gaps(rhdata):
    """in case the RH data for Plevels 20 and 50 hPa is not present, this function fills these gaps
    with 0.0"""
    relative_humidity = []
    for i in np.arange(len(rhdata)):
        relative_humidity.append(rhdata[i].values)
    relative_humidity = np.asarray(relative_humidity)

    for i in np.arange(len(relative_humidity)):
        if i * 23 < len(relative_humidity):
            relative_humidity = np.insert(relative_humidity, (i * 23, i * 23), 0.0)
    return relative_humidity


def compute_density(pressure, temperature):
    """Return molecular number density"""
    return STD_NUMBER_DENSITY * pressure / STD_AIR_PRESSURE * STD_AIR_TEMPERATURE / temperature


def compute_wind_direction(u_direction, v_direction):
    """Return wind direction"""
    angle = np.arctan2(-1 * u_direction, -1 * v_direction) * 180.0 / np.pi
    if angle < 0.0:
        angle += 360.0
    direction = angle
    return direction


def compute_wind_speed(u_direction, v_direction):
    """Return wind speed"""
    return np.sqrt(u_direction**2.0 + v_direction**2.0)


def read_grib_file_to_text(file_name, gridstep, observatory=None, lat=None, lon=None):
    """
    This function creates a txt file where the information from the
    get_grib_file_data function is written, together with date, year,
    month, day, hour, pressure level, real height and density.

    Input: file_name (string)
           observatory (string). Possible values are 'north', 'south'
           or any other name. If NOT north or south,
           then the program asks for the coordinates.
           gridstep (float): grid spacing in degrees. Values are 1.0 for GDAS data
           and 0.75 for ECMWF data.
           lat: (float, optional) latitude of the observatory in degrees
           lon: (float, optional) longitude of the observatory in degrees
    Output: a txt file with the exact name as the input file name,
            but with .txt as extension
    """

    if os.path.exists(os.path.splitext(file_name)[0] + ".txt"):
        logger.critical(
            f"Output file {os.path.splitext(file_name)[0]}.txt already exists. Aborting."
        )
        sys.exit()

    vn, datadict = get_grib_file_data(file_name)
    latitude_obs, longitude_obs = None, None

    if observatory:
        latitude_obs, longitude_obs = get_observatory_coordinates(observatory)
    elif lat and lon:
        latitude_obs, longitude_obs = lat, lon

    lat_gridpoint, lon_gridpoint = get_closest_gridpoint(latitude_obs, longitude_obs, gridstep)

    if len(datadict["Temperature"]) != len(datadict["Relativehumidity"]):
        relative_humidity = fill_relative_humidity_gaps(datadict["Relativehumidity"])
    else:
        relative_humidity = []
        for i in np.arange(len(datadict["Relativehumidity"])):
            relative_humidity.append(datadict["Relativehumidity"][i].values)
        relative_humidity = np.asarray(relative_humidity)

    # We create the table file and fill it with the information stored in the above variables,
    # plus the height and density computed form them.

    logger.info("creating the txt file containing the selected data...")
    table_file = open(file_name.split(".")[0] + ".txt", "w")
    print(
        "Date year month day hour MJD P Temp h n n_exp U V wind_speed wind_direction RH",
        file=table_file,
    )

    pbar = tqdm(total=len(datadict["Temperature"]))
    for j in np.arange(len(datadict["Temperature"])):
        pbar.update(1)
        if (type(datadict["Temperature"][j].values) == float) or (
            len(datadict["Temperature"][j].values) == 1
        ):
            if "GeopotentialHeight" in vn:
                height = get_altitude_from_geopotential_height(
                    datadict["GeopotentialHeight"][j].values, latitude_obs
                )
            else:
                height = get_altitude_from_geopotential(
                    datadict["Geopotential"][j].values, latitude_obs
                )
            density = compute_density(
                datadict["Temperature"][j].level, datadict["Temperature"][j].values
            )
            density_exp = density / STD_NUMBER_DENSITY * np.exp(height / DENSITY_SCALE_HEIGHT)
            wind_speed = compute_wind_speed(
                datadict["Ucomponentofwind"][j].values, datadict["Vcomponentofwind"][j].values
            )
            wind_direction = compute_wind_direction(
                datadict["Ucomponentofwind"][j].values, datadict["Vcomponentofwind"][j].values
            )
            mjd = date2mjd(
                datadict["Temperature"][j].year,
                datadict["Temperature"][j].month,
                datadict["Temperature"][j].day,
                datadict["Temperature"][j].hour,
            )
            print(
                int(datadict["Temperature"][j].dataDate),
                datadict["Temperature"][j].year,
                datadict["Temperature"][j].month,
                datadict["Temperature"][j].day,
                datadict["Temperature"][j].hour,
                mjd,
                datadict["Temperature"][j].level,
                datadict["Temperature"][j].values,
                height,
                density,
                density_exp,
                datadict["Ucomponentofwind"][j].values,
                datadict["Vcomponentofwind"][j].values,
                wind_speed,
                wind_direction,
                relative_humidity[j],
                file=table_file,
            )

        else:  # this is just in case the grib file contains more than one grid point
            if "GeopotentialHeight" in vn:
                height = get_altitude_from_geopotential_height(
                    np.float(
                        datadict["GeopotentialHeight"][j].values[
                            (datadict["GeopotentialHeight"][j].data()[1] == lat_gridpoint)
                            & (datadict["GeopotentialHeight"][j].data()[2] == lon_gridpoint)
                        ]
                    ),
                    latitude_obs,
                )
            else:
                height = get_altitude_from_geopotential(
                    np.float(
                        datadict["Geopotential"][j].values[
                            (datadict["Geopotential"][j].data()[1] == lat_gridpoint)
                            & (datadict["Geopotential"][j].data()[2] == lon_gridpoint)
                        ]
                    ),
                    latitude_obs,
                )
            temperature = np.float(
                datadict["Temperature"][j].values[
                    (datadict["Temperature"][j].data()[1] == lat_gridpoint)
                    & (datadict["Temperature"][j].data()[2] == lon_gridpoint)
                ]
            )
            # Why for relative humidity,  wind speed and direction we are not
            # choosing only the grid point closest to
            # ORM, like we do for Geopotential and temperature?
            # I add the selection below
            relative_humidity = np.float(
                datadict["Relativehumidity"][j].values[
                    (datadict["Relativehumidity"][j].data()[1] == lat_gridpoint)
                    & (datadict["Relativehumidity"][j].data()[2] == lon_gridpoint)
                ]
            )
            density = compute_density(datadict["Temperature"][j].level, temperature)
            U_component_of_wind = np.float(
                datadict["Ucomponentofwind"][j].values[
                    (datadict["Ucomponentofwind"][j].data()[1] == lat_gridpoint)
                    & (datadict["Ucomponentofwind"][j].data()[2] == lon_gridpoint)
                ]
            )
            V_component_of_wind = np.float(
                datadict["Vcomponentofwind"][j].values[
                    (datadict["Vcomponentofwind"][j].data()[1] == lat_gridpoint)
                    & (datadict["Vcomponentofwind"][j].data()[2] == lon_gridpoint)
                ]
            )
            wind_speed = compute_wind_speed(U_component_of_wind, V_component_of_wind)
            wind_direction = compute_wind_direction(U_component_of_wind, V_component_of_wind)
            density_exp = density / STD_NUMBER_DENSITY * np.exp(height / DENSITY_SCALE_HEIGHT)
            mjd = date2mjd(
                datadict["Temperature"][j].year,
                datadict["Temperature"][j].month,
                datadict["Temperature"][j].day,
                datadict["Temperature"][j].hour,
            )

            print(
                int(datadict["Temperature"][j].dataDate),
                datadict["Temperature"][j].year,
                datadict["Temperature"][j].month,
                datadict["Temperature"][j].day,
                datadict["Temperature"][j].hour,
                mjd,
                datadict["Temperature"][j].level,
                temperature,
                height,
                density,
                density_exp,
                U_component_of_wind,
                V_component_of_wind,
                wind_speed,
                wind_direction,
                relative_humidity,
                file=table_file,
            )

    table_file.close()
    pbar.close()
    datadict = None


def read_grib_file_to_magic(file_name, gridstep, observatory=None, lat=None, lon=None):
    """
    This function opens a grib file, selects all parameters
    and finally creates a txt file where these parameters, together with date, year, month,
    day, hour, pressure level, real height and density, are written.
    Input: file_name (string)
           observatory (string). Possible values are 'north' or 'south'
           gridstep (float): grid spacing (0.75 degrees for ECMWF and 1.0 degrees for GDAS)
    Output: a txt file with the exact name as the input file name,
            but with .txt as extension in a format that can be read by MARS
    """
    if os.path.exists(os.path.splitext(file_name)[0] + ".txt"):
        logger.critical(
            f"Output file {os.path.splitext(file_name)[0]}.txt already exists. Aborting."
        )
        sys.exit()

    vn, datadict = get_grib_file_data(file_name)

    pressure_level_index = get_plevels(datadict["Temperature"])
    new_pressure_level_index = pressure_level_index[::-1] * int(
        (len(datadict["Temperature"]) / len(pressure_level_index))
    )

    if observatory:
        latitude_obs, longitude_obs = get_observatory_coordinates(observatory)
    else:
        latitude_obs, longitude_obs = lat, lon

    lat_gridpoint, lon_gridpoint = get_closest_gridpoint(latitude_obs, longitude_obs, gridstep)

    # We create the table file and fill it with the information stored in
    # the above variables, plus the height and density computed form them.

    logger.info("creating the txt file containing the selected data...")
    table_file = open(file_name.split(".")[0] + "MAGIC_format.txt", "w")

    for j in np.arange(len(datadict["Temperature"])):

        if (type(datadict["Temperature"][j].values) == float) or (
            len(datadict["Temperature"][j].values) == 1
        ):
            if new_pressure_level_index[j] == 1:
                print(str([0.00] * 34)[1:-1].replace(",", " "), file=table_file)
            if "GeopotentialHeight" in vn:
                height = get_altitude_from_geopotential_height(
                    datadict["GeopotentialHeight"][j].values, latitude_obs
                )
            else:
                height = get_altitude_from_geopotential(
                    datadict["Geopotential"][j].values, latitude_obs
                )

            fields = (
                datadict["Temperature"][j].year - 2000,
                datadict["Temperature"][j].month,
                datadict["Temperature"][j].day,
                datadict["Temperature"][j].hour,
                new_pressure_level_index[j],
                height,
                datadict["Temperature"][j].values,
                datadict["Ucomponentofwind"][j].values,
                datadict["Vcomponentofwind"][j].values,
                RH[j],
            )
            row_str = "{: >6d}{: >6d}{: >6d}{: >6d}{: >6d}{: >10.2f}{: >10.2f}{: >10.2f}{: >10.2f}{: >10.2f}"
            row_str = row_str.format(*fields)
            table_file.write(row_str + "\n")

        else:  # this is just in case the grib file contains more than one grid point
            if new_pressure_level_index[j] == 1:
                print(str([0.00] * 34)[1:-1].replace(",", " "), file=table_file)
            if "GeopotentialHeight" in vn:
                height = np.float(
                    datadict["GeopotentialHeight"][j].values[
                        (datadict["GeopotentialHeight"][j].data()[1] == lat_gridpoint)
                        & (datadict["GeopotentialHeight"][j].data()[2] == lon_gridpoint)
                    ]
                )
            else:
                height = get_altitude_from_geopotential(
                    datadict["Geopotential"][j].values, latitude_obs
                )

            temperature = np.float(
                datadict["Temperature"][j].values[
                    (datadict["Temperature"][j].data()[1] == lat_gridpoint)
                    & (datadict["Temperature"][j].data()[2] == lon_gridpoint)
                ]
            )

            fields = (
                datadict["Temperature"][j].year - 2000,
                datadict["Temperature"][j].month,
                datadict["Temperature"][j].day,
                datadict["Temperature"][j].hour,
                new_pressure_level_index[j],
                height,
                temperature,
                datadict["Ucomponentofwind"][j].values,
                datadict["Vcomponentofwind"][j].values,
                RH[j],
            )
            row_str = "{: >6d}{: >6d}{: >6d}{: >6d}{: >6d}{: >10.2f}{: >10.2f}{: >10.2f}{: >10.2f}{: >10.2f}"
            row_str = row_str.format(*fields)
            table_file.write(row_str + "\n")
    table_file.close()


def read_grib_file_to_magic_from_txt(txt_file):
    """
    :param txt_file:
    :return:
    """
    input_f = open(txt_file, "r")
    output_f = open(txt_file + "MAGIC_format.txt", "w")

    date, year, month, day, hour, mjd, p, T, h, n, U, V, RH = np.loadtxt(
        input_f, usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13), unpack=True, skiprows=1
    )

    pl = np.unique(p)[::-1]
    pl_index = (np.arange(len(pl)) + 1).tolist()
    new_pl_index = pl_index * int((len(T) / len(pl_index)))
    remaining_index = len(p) - len(new_pl_index)
    new_pl_index = new_pl_index + pl_index[:remaining_index]

    pbar = tqdm(total=len(T))
    for j in np.arange(len(T)):
        pbar.update(1)
        if new_pl_index[j] == 1:
            print(str([0.00] * 34)[1:-1].replace(",", " "), file=output_f)

        fields = (
            int(year[j] - 2000),
            int(month[j]),
            int(day[j]),
            int(hour[j]),
            int(new_pl_index[j]),
            h[j],
            T[j],
            U[j],
            V[j],
            RH[j],
        )
        row_str = (
            "{: >6d}{: >6d}{: >6d}{: >6d}{: >6d}{: >10.2f}{: >10.2f}{: >10.2f}{: >10.2f}{: >10.2f}"
        )
        row_str = row_str.format(*fields)
        output_f.write(row_str + "\n")

    pbar.close()


def run_in_paraller(function_name, file_list, gridstep, observatory=None, lat=None, lon=None):
    """
    Converts in parallel a list of grib files.
    :param function_name: The function to convert the grib files. It can be either read_grib_file_to_magic or
    read_grib_file_to_text
    :type function_name: string
    :param file_list: name of the file containing the list of grib files to process
    :type file_list: string
    :param gridstep: DAS  granularity - distance between the grid points where we have data from DAS
    :type gridstep: float
    :param observatory: The location of the observatory, north or south
    :type observatory: string
    :param lat: The geographical latitude of the observatory
    :type lat: float
    :param lon: The geographical longitude of the observatory
    :type lon: float
    """

    fname = open(file_list)
    line = fname.readline()
    list_of_gribfiles = []
    while line:
        list_of_gribfiles.append(line[:-1])
        line = fname.readline()

    p = multiprocessing.Pool()
    for grib_file in list_of_gribfiles:
        p.map(function_name, [grib_file, gridstep, observatory, lat, lon])

    p.close()
    p.join()


def merge_txt_from_grib(txtfile, output_file="merged_from_grib.txt"):
    """Merges text files created from different grib2 files to one text file"""

    lf = open(txtfile, "r")
    outfile = open(output_file, "w")

    line = lf.readline()
    first = True
    while line:
        datafile = open(line[:-1], "r")
        if first:
            dataline = datafile.readline()
        else:
            datafile.readline()
            dataline = datafile.readline()

        while dataline:
            print(dataline[:-1], file=outfile)
            dataline = datafile.readline()
        first = False
        datafile.close()
        line = lf.readline()
    lf.close()
    outfile.close()


def print_help():
    print("Usage: python grib_utils.py <options>")
    print("Options are:")
    print("        -r         <grib_file_name> <gridstep> <observatory>")
    print("                   note that <gridstep> is 0.75deg for ECMWF data")
    print("                   and 1.0 deg for GDAS data")
    print("        -rmagic    <grib_file_name> <observatory> <gridstep>")
    print("                   note that <gridstep> is 0.75deg for ECMWF data")
    print("                   and 1.0 deg for GDAS data")
    print("        -mjd       <mjd>")
    print("        -date      <yyyy-mm-dd-hh>")
    print("        -merge or -m <list_of_txt_files> <output_name>")
    print(" ")
    print("                   Note: with the -r or -rmagic option, if a txt file")
    print("                   containing a list of grib files is passed instead")
    print("                   of a single grib file, the processing is run in parallel")
    print("                   using a certain number of CPU's")


# if __name__ == "__main__":

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--grib_file", help="the grib file to process")
parser.add_argument(
    "-gridstep",
    help="the gridstep in degrees. If GDAS or GFS data, gridstep=1.0 deg; "
    "If ECMWF data, gridstep=0.75 deg",
    type=float,
)
parser.add_argument(
    "-o",
    "--observatory",
    help="north or south. If no observatory is provided, "
    "then the system asks for the coordinates of interest",
)
parser.add_argument(
    "-c",
    "--coordinates",
    nargs=2,
    help="latitude and longitude of the place " "of interest, in degrees",
    type=float,
)
parser.add_argument(
    "-r",
    action="store_true",
    help="<grib_file_name> <gridstep> <observatory> \n "
    "note that <gridstep> is 0.75deg for ECMWF data \n"
    "and 1.0 deg for GDAS data. If a txt file containing \n "
    "a list of grib files is passed instead of a single \n "
    "grib file, the processing is run in parallel \n"
    "using a certain number of CPUs",
)
parser.add_argument(
    "-rmagic",
    action="store_true",
    help="<grib_file_name> <observatory> <gridstep> \n "
    "note that <gridstep> is 0.75deg for ECMWF data \n "
    "and 1.0 deg for GDAS data.  If a txt file containing \n "
    "a list of grib files is passed instead of a single \n "
    "grib file, the processing is run in parallel \n"
    "using a certain number of CPUs",
)
parser.add_argument(
    "--parallel",
    action="store_true",
    help="if a txt file containing a list of grib files is passed as -g option,"
    "it opens them and extracts information in parallel, one grib file per"
    "CPU",
)
parser.add_argument(
    "-mjd",
    help="if selected, transforms MJD information into date in YYYY MM DD HH format",
    type=float,
)
parser.add_argument(
    "-date", help="if selected, transforms date information into MJD format", type=str
)
parser.add_argument(
    "-m",
    "--merge",
    nargs="+",
    help="followed by a filename containing a list of txt files, \n "
    "it merges them into a single txt file",
)


if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    if args.grib_file:
        if args.observatory:
            if args.grib_file.lower().endswith((".grib", ".grb", ".txt", ".dat", ".grib2")):
                if args.r and not args.parallel:
                    read_grib_file_to_text(
                        args.grib_file, args.gridstep, observatory=args.observatory
                    )
                elif args.rmagic:
                    read_grib_file_to_magic(
                        args.grib_file, args.gridstep, observatory=args.observatory
                    )
                elif args.r and args.parallel:
                    logger.info("EXECUTING THIS")
                    run_in_paraller(
                        read_grib_file_to_text,
                        args.grib_file,
                        args.gridstep,
                        observatory=args.observatory,
                    )
                elif args.rmagic and args.parallel:
                    run_in_paraller(
                        read_grib_file_to_magic,
                        args.grib_file,
                        args.gridstep,
                        observatory=args.observatory,
                    )
            else:
                logger.critical("file extension not recognized. Exiting")
                sys.exit()
        elif not args.observatory and args.coordinates:
            lat, lon = args.coordinates
            if args.grib_file.lower().endswith((".grib", ".grb", ".txt", ".dat", ".grib2")):
                if args.r:
                    read_grib_file_to_text(args.grib_file, args.gridstep, lat=lat, lon=lon)
                elif args.rmagic:
                    read_grib_file_to_magic(args.grib_file, args.gridstep, lat=lat, lon=lon)
                elif args.r and args.parallel:
                    run_in_paraller(
                        read_grib_file_to_text, args.grib_file, args.gridstep, lat=lat, lon=lon
                    )
                elif args.rmagic and args.parallel:
                    run_in_paraller(
                        read_grib_file_to_magic, args.grib_file, args.gridstep, lat=lat, lon=lon
                    )
            else:
                logger.critical("file extension not recognized. Exiting")
                sys.exit()
        else:
            logger.error(
                "Too many options. Please specify either observatory only, or coordinates only"
            )

    elif args.mjd:
        print(mjd2date(args.mjd))

    elif args.date:
        date = args.date.split("-")
        print(date2mjd(int(date[0]), int(date[1]), int(date[2]), int(date[3])))

    elif args.merge:
        if isinstance(args.merge, list) and len(args.merge) == 2:
            merge_txt_from_grib(args.merge[0], output_file=args.merge[1])
        else:
            merge_txt_from_grib(args.merge[0])
