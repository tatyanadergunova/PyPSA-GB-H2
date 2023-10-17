# -*- coding: utf-8 -*-
"""
Creating heat demand profiles using the bdew method.

Installation requirements
-------------------------
This example requires at least version v0.1.4 of the oemof demandlib. Install
by:
    pip install 'demandlib>=0.1.4,<0.2'
Optional:
    pip install matplotlib

SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: Stephen Bosch

SPDX-License-Identifier: MIT

"""
import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import demandlib.bdew as bdew

# read example temperature series
filename = "temperature_GB_2010.csv"
dirname = os.getcwd()
datapath = os.path.join(dirname, filename)

if not os.path.isfile(datapath):
    msg = (
        "The file {0} could not be found in the current working directory.\n "
        "This could happen due to the following reasons:\n"
        "* you forgot to download the example data from the repository\n"
        "* the filename is wrong\n"
        "* the file is not located in {1}\n"
        "Download the file from the demandlib repository and copy it to the "
        "right directory.\nAlternatively you can adapt the name of the file "
        "or the name of the directory in the example script."
    )
    print(msg.format(filename, dirname))
    exit(0)

temperature = pd.read_csv(datapath)["temperature"]


# The following dictionary is create by "workalendar"
# pip install workalendar
# >>> from workalendar.europe import UnitedKingdom
# >>> cal = UnitedKingdom ()
# >>> holidays = dict(cal.holidays(2010))


ann_demands_per_type = {"efh": 78000, "mfh": 22000, "ghd": 140000}

holidays = {
    datetime.date(2010, 1, 1): 'New year',
    datetime.date(2010, 4, 2): 'Good Friday',
    datetime.date(2010, 4, 4): 'Easter Sunday',
    datetime.date(2010, 4, 5): 'Easter Monday',
    datetime.date(2010, 5, 3): 'Early May Bank Holiday',
    datetime.date(2010, 5, 31): 'Spring Bank Holiday',
    datetime.date(2010, 8, 30): 'Late Summer Bank Holiday',
    datetime.date(2010, 12, 25): 'Christmas Day',
    datetime.date(2010, 12, 26): 'Boxing Day',
    datetime.date(2010, 12, 27): 'Christmas Shift',
    datetime.date(2010, 12, 28): 'Boxing Day Shift'
}

# Create DataFrame for 2010
demand = pd.DataFrame(
    index=pd.date_range(
        datetime.datetime(2010, 1, 1, 0), periods=8760, freq="H"
    )
)

# Single family house (efh: Einfamilienhaus)
demand["efh"] = bdew.HeatBuilding(
    demand.index,
    holidays=holidays,
    temperature=temperature,
    shlp_type="EFH",
    building_class=1,
    wind_class=1,
    annual_heat_demand=ann_demands_per_type["efh"],
    name="EFH",
).get_bdew_profile()

# Multi family house (mfh: Mehrfamilienhaus)
demand["mfh"] = bdew.HeatBuilding(
    demand.index,
    holidays=holidays,
    temperature=temperature,
    shlp_type="MFH",
    building_class=2,
    wind_class=0,
    annual_heat_demand=ann_demands_per_type["mfh"],
    name="MFH",
).get_bdew_profile()

# Industry, trade, service (ghd: Gewerbe, Handel, Dienstleistung)
demand["ghd"] = bdew.HeatBuilding(
    demand.index,
    holidays=holidays,
    temperature=temperature,
    shlp_type="ghd",
    wind_class=0,
    annual_heat_demand=ann_demands_per_type["ghd"],
    name="ghd",
).get_bdew_profile()

# Plot demand of building
ax = demand.plot()
ax.set_xlabel("Date")
ax.set_ylabel("Heat demand in kW")
plt.show()

print("Annual consumption: \n{}".format(demand.sum()))

print(demand)

demand.to_csv('heat_demand_GB_2010.csv', index = True)