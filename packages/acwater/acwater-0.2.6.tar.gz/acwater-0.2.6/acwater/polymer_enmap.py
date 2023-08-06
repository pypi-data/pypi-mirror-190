# -*- coding: utf-8 -*-
#
# Atmospheric correction of EnMAP hyperspectral data for water surfaces
# acwater.py is a wrapper for Polymer (Hygeos) to run the Polymer algorithmus in EnPT (GFZ-Potsdam)
#
# Copyright (C) 2020  by Alfred Wegener Institute (AWI), Helmholtz Centre for Polar and Marine Research
# Astrid Bracher (AWI Bremerhaven, abracher@awi.de),
# Mariana Soppa (AWI Bremerhaven, msoppa@awi.de), and
# Brenner Silva (AWI Bremerhaven, bsilva@awi.de)
#
# This software was developed at the Alfred-Wegener-Institute, Bremerhaven, supported by the DLR Space Administration
# with funds of the German Federal Ministry of Economic Affairs and Energy
# (on the basis of a decision by the German Bundestag:50 EE 1529) and contributions from GFZ, Potsdam.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Please note that for proposed application of this software, specific terms do apply to the software dependencies:
# - Polymer is distributed under its own licence (https://www.hygeos.com/polymer/licence)
# - EnPT is free software (GPLv3), with dependencies (https://gitext.gfz-potsdam.de/EnMAP/GFZ_Tools_EnMAP_BOX/EnPT/-/blob/master/LICENSE)
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
""" The polymer_enmap module contains specifications and parameters of EnPT data for running polymer.

Detector parameters (e.g. wavelengths) are provided by the EnMAP Core Science Team.
Atmospheric parameters require ancillary data for
ozone (O2), nitrogen dioxide (NO2), and the extraterrestrial radiation (solar spectrum).

"""

import numpy as np

import pandas as pd
from os.path import join
from scipy.interpolate import interp1d

import os
import pkgutil
from pathlib import PurePath

try:
    dir_polymer = PurePath(os.path.dirname(pkgutil.get_loader("polymer").path)).parent
    dir_common = os.path.join(dir_polymer,'auxdata','common')
except:
    dir_common = PurePath(os.path.dirname(pkgutil.get_loader("enpt").path)).parent.parent
    aux = [aux for aux in os.listdir(dir_common) if aux.startswith('polymer')]
    aux = [aux for aux in aux if os.path.isdir(os.path.join(dir_common,aux,'auxdata','common'))][0]
    dir_polymer = os.path.join(dir_common,aux)
    dir_common = os.path.join(dir_polymer,'auxdata','common')

assert (os.path.isdir(dir_common))

# wavelength center of ENMAP bands, source: ECST
# obtained after stacking VNIR and SWIR ordered by wavelength
BANDS_ENMAP = dict([('wavelength',
                   [423.03, 428.8, 434.29, 439.58, 444.72, 449.75, 454.7, 459.59, 464.43, 469.25, 474.05, 478.84,
                    483.63, 488.42, 493.23, 498.05, 502.9, 507.77, 512.67, 517.6, 522.57, 527.58, 532.63, 537.72,
                    542.87, 548.06, 553.3, 558.6, 563.95, 569.36, 574.83, 580.36, 585.95, 591.6, 597.32, 603.1, 608.95,
                    614.86, 620.84, 626.9, 633.02, 639.21, 645.47, 651.8, 658.2, 664.67, 671.21, 677.83, 684.51, 691.26,
                    698.08, 704.97, 711.92, 718.95, 726.03, 733.19, 740.4, 747.68, 755.01, 762.41, 769.86, 777.37,
                    784.93, 792.54, 800.2, 807.91, 815.67, 823.46, 831.3, 839.18, 847.1, 855.05, 863.03, 871.05, 879.09,
                    887.16, 895.25, 903.36, 904.78, 911.49, 914.44, 919.64, 924.23, 927.8, 934.16, 935.98, 944.17,
                    944.23,
                    952.37, 954.42, 960.57, 964.74, 968.78, 975.17, 976.99, 985.21, 985.73, 996.4, 1007.2,
                    1018.1, 1029.1, 1040.2, 1051.3, 1062.6, 1074.0, 1085.4, 1096.9, 1108.5, 1120.1, 1131.8, 1143.5,
                    1155.3, 1167.1, 1179.0, 1190.9, 1202.8, 1214.8, 1226.7, 1238.7, 1250.7, 1262.7, 1274.7, 1286.7,
                    1298.7, 1310.7, 1322.7, 1334.7, 1346.6, 1487.8, 1499.4, 1510.9, 1522.3, 1533.7, 1545.1, 1556.4,
                    1567.7, 1578.9, 1590.1, 1601.2, 1612.3, 1623.3, 1634.3, 1645.3, 1656.2, 1667.0, 1677.8, 1688.5,
                    1699.2, 1709.9, 1720.5, 1731.0, 1741.5, 1752.0, 1762.4, 1772.7, 1969.9, 1979.3, 1988.7, 1998.0,
                    2007.2, 2016.4, 2025.6, 2034.8, 2043.9, 2052.9, 2061.9, 2070.9, 2079.9, 2088.8, 2097.6, 2106.4,
                    2115.2, 2124.0, 2132.7, 2141.3, 2150.0, 2158.6, 2167.1, 2175.7, 2184.2, 2192.6, 2201.0, 2209.4,
                    2217.8, 2226.1, 2234.4, 2242.6, 2250.8, 2259.0, 2267.2, 2275.3, 2283.4, 2291.4, 2299.4, 2307.4,
                    2315.4, 2323.3, 2331.2, 2339.1, 2346.9, 2354.7, 2362.5, 2370.2, 2377.9, 2385.6, 2393.3, 2400.9,
                    2408.5, 2416.1, 2423.6, 2431.1, 2438.6]),
                  ('band_names',
                   ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15',
                    'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29',
                    'B30', 'B31', 'B32', 'B33', 'B34', 'B35', 'B36', 'B37', 'B38', 'B39', 'B40', 'B41', 'B42', 'B43',
                    'B44', 'B45', 'B46', 'B47', 'B48', 'B49', 'B50', 'B51', 'B52', 'B53', 'B54', 'B55', 'B56', 'B57',
                    'B58', 'B59', 'B60', 'B61', 'B62', 'B63', 'B64', 'B65', 'B66', 'B67', 'B68', 'B69', 'B70', 'B71',
                    'B72', 'B73', 'B74', 'B75', 'B76', 'B77', 'B78', 'B79', 'B80', 'B81', 'B82', 'B83', 'B84', 'B85',
                    'B86', 'B87', 'B88', 'B89', 'B90', 'B91', 'B92', 'B93', 'B94', 'B95', 'B96', 'B97', 'B98', 'B99',
                    'B100', 'B101', 'B102', 'B103', 'B104', 'B105', 'B106', 'B107', 'B108', 'B109', 'B110', 'B111',
                    'B112', 'B113', 'B114', 'B115', 'B116', 'B117', 'B118', 'B119', 'B120', 'B121', 'B122', 'B123',
                    'B124', 'B125', 'B126', 'B127', 'B128', 'B129', 'B130', 'B131', 'B132', 'B133', 'B134', 'B135',
                    'B136', 'B137', 'B138', 'B139', 'B140', 'B141', 'B142', 'B143', 'B144', 'B145', 'B146', 'B147',
                    'B148', 'B149', 'B150', 'B151', 'B152', 'B153', 'B154', 'B155', 'B156', 'B157', 'B158', 'B159',
                    'B160', 'B161', 'B162', 'B163', 'B164', 'B165', 'B166', 'B167', 'B168', 'B169', 'B170', 'B171',
                    'B172', 'B173', 'B174', 'B175', 'B176', 'B177', 'B178', 'B179', 'B180', 'B181', 'B182', 'B183',
                    'B184', 'B185', 'B186', 'B187', 'B188', 'B189', 'B190', 'B191', 'B192', 'B193', 'B194', 'B195',
                    'B196', 'B197', 'B198', 'B199', 'B200', 'B201', 'B202', 'B203', 'B204', 'B205', 'B206', 'B207',
                    'B208', 'B209', 'B210', 'B211', 'B212']),
                    ('wavelength_pm',
                     [42303, 42880, 43429, 43958, 44472, 44975, 45470, 45959, 46443, 46925, 47405, 47884, 48363, 48842,
                      49323, 49805, 50290, 50777, 51266, 51760, 52257, 52758, 53263, 53772, 54287, 54805, 55329, 55860,
                      56395, 56936, 57483, 58036, 58595, 59160, 59732, 60310, 60895, 61486, 62084, 62690, 63302, 63921,
                      64547, 65179, 65820, 66467, 67121, 67783, 68451, 69126, 69808, 70497, 71192, 71895, 72603, 73319,
                      74040, 74768, 75501, 76241, 76986, 77737, 78493, 79254, 80020, 80791, 81567, 82346, 83130, 83918,
                      84710, 85505, 86303, 87105, 87909, 88716, 89525, 90336, 90478, 91149, 91444, 91964, 92423, 92780,
                      93416, 93598, 94417, 94423, 95237, 95442, 96057, 96474, 96878, 97517, 97699, 98521, 98573, 99640,
                      100720, 101810, 102909, 104020, 105130, 106259, 107400, 108540, 109690, 110850, 112009, 113180,
                      114350, 115530, 116709, 117900, 119090, 120280, 121480, 122670, 123870, 125070, 126270, 127470,
                      128670, 129870, 131070, 132270, 133470, 134660, 148780, 149940, 151090, 152230, 153370, 154510,
                      155640, 156770, 157890, 159010, 160120, 161230, 162330, 163430, 164530, 165620, 166700, 167780,
                      168850, 169920, 170990, 172050, 173100, 174150, 175200, 176240, 177270, 196990, 197930, 198870,
                      199800, 200720, 201640, 202560, 203480, 204390, 205290, 206190, 207090, 207990, 208880, 209760,
                      210640, 211519, 212400, 213269, 214130, 215000, 215860, 216710, 217569, 218419, 219260, 220100,
                      220940, 221780, 222610, 223440, 224260, 225080, 225900, 226719, 227530, 228340, 229140, 229940,
                      230740, 231540, 232330, 233119, 233910, 234690, 235469, 236250, 237019, 237790, 238560, 239330,
                      240090, 240850, 241610, 242360, 243110, 243860])
                    ])

BANDS_ENMAP_VNIR_WVL = [423.03, 428.8, 434.29, 439.58, 444.72, 449.75, 454.7, 459.59, 464.43, 469.25, 474.05, 478.84,
                    483.63, 488.42, 493.23, 498.05, 502.9, 507.77, 512.67, 517.6, 522.57, 527.58, 532.63, 537.72,
                    542.87, 548.06, 553.3, 558.6, 563.95, 569.36, 574.83, 580.36, 585.95, 591.6, 597.32, 603.1, 608.95,
                    614.86, 620.84, 626.9, 633.02, 639.21, 645.47, 651.8, 658.2, 664.67, 671.21, 677.83, 684.51, 691.26,
                    698.08, 704.97, 711.92, 718.95, 726.03, 733.19, 740.4, 747.68, 755.01, 762.41, 769.86, 777.37,
                    784.93, 792.54, 800.2, 807.91, 815.67, 823.46, 831.3, 839.18, 847.1, 855.05, 863.03, 871.05, 879.09,
                    887.16, 895.25, 903.36, 911.49, 919.64, 927.8, 935.98, 944.17, 952.37, 960.57, 968.78, 976.99,
                    985.21]

BANDS_ENMAP_SWIR_WVL = [904.78, 914.44, 924.23, 934.16, 944.23, 954.42, 964.74, 975.17, 985.73, 996.4, 1007.2,
                    1018.1, 1029.1, 1040.2, 1051.3, 1062.6, 1074., 1085.4, 1096.9, 1108.5, 1120.1, 1131.8,
                    1143.5, 1155.3, 1167.1, 1179., 1190.9, 1202.8, 1214.8, 1226.7, 1238.7, 1250.7, 1262.7,
                    1274.7, 1286.7, 1298.7, 1310.7, 1322.7, 1334.7, 1346.6, 1487.8, 1499.4, 1510.9, 1522.3,
                    1533.7, 1545.1, 1556.4, 1567.7, 1578.9, 1590.1, 1601.2, 1612.3, 1623.3, 1634.3, 1645.3,
                    1656.2, 1667., 1677.8, 1688.5, 1699.2, 1709.9, 1720.5, 1731., 1741.5, 1752., 1762.4, 1772.7,
                    1969.9, 1979.3, 1988.7, 1998., 2007.2, 2016.4, 2025.6, 2034.8, 2043.9, 2052.9, 2061.9,
                    2070.9, 2079.9, 2088.8, 2097.6, 2106.4, 2115.2, 2124., 2132.7, 2141.3, 2150., 2158.6, 2167.1,
                    2175.7, 2184.2, 2192.6, 2201., 2209.4, 2217.8, 2226.1, 2234.4, 2242.6, 2250.8, 2259., 2267.2,
                    2275.3, 2283.4, 2291.4, 2299.4, 2307.4, 2315.4, 2323.3, 2331.2, 2339.1, 2346.9, 2354.7,
                    2362.5, 2370.2, 2377.9, 2385.6, 2393.3, 2400.9, 2408.5, 2416.1, 2423.6, 2431.1, 2438.6]

def get_bands_dict(bands_enmap_wvl):
    bands_enmap_dict = [[b,c,d,i] for i,(b,c,d) in enumerate(zip(BANDS_ENMAP['wavelength'],BANDS_ENMAP['band_names'],BANDS_ENMAP['wavelength_pm'])) if b in bands_enmap_wvl]
    bands_enmap_dict = list(map(list, zip(*bands_enmap_dict)))
    keys = list(BANDS_ENMAP.keys())
    keys.append('index')
    bands_enmap_dict ={k:v for k,v in zip(keys,bands_enmap_dict)}
    return bands_enmap_dict

BANDS_ENMAP_SWIR= get_bands_dict(BANDS_ENMAP_SWIR_WVL)
BANDS_ENMAP_VNIR = get_bands_dict(BANDS_ENMAP_VNIR_WVL)


# FIXME: review set up for the climatology
#  (e.g. K_OZ and K_NO2): investigate SCIATRAN and SeaDAS, currently uses SeaDAS as in hico

def params_enmap(band_names):
    # BANDS_ENMAP = bands_enmap(wavelengths)/100

    band_wavelengths = [BANDS_ENMAP['wavelength'][BANDS_ENMAP['wavelength'].index(b)] for b in band_names]

    # --------------------------------------------------------------------------------
    # detector calibration
    # set to one
    calib = {b: 1. for b in band_names}

    # --------------------------------------------------------------------------------
    # K_OZ:  Total ozone optical depth for 1000 DU

    # get ancillary data
    ozone_file = 'k_oz.csv'  # afglus atmospheric profile [350, 900 nm]
    k_oz_data = pd.read_csv(join(dir_common, ozone_file), comment="#")

    # interpolate to enmap bands
    k_oz = interp1d(k_oz_data.wavelength, k_oz_data.K_OZ, bounds_error=False, fill_value=0.)
    K_OZ_ENMAP = {b: k for b, k in zip(band_names, k_oz(np.array(band_wavelengths)))}

    # --------------------------------------------------------------------------------
    # K_NO2: NO2 optical depth

    # get ancillary data,
    from polymer.hico import K_NO2_HICO  # same as K_OZ_HICO / SeaDAS

    # interpolate to enmap bands
    f_no2 = interp1d(list(K_NO2_HICO.keys()), list(K_NO2_HICO.values()), bounds_error=False, fill_value=0.)
    K_NO2_ENMAP = {b: k for b, k in zip(band_names, f_no2(np.array(band_wavelengths)))}

    return K_NO2_ENMAP, K_OZ_ENMAP, calib


def solar_spectrum(band_names):

    band_wavelengths = [BANDS_ENMAP['wavelength'][BANDS_ENMAP['wavelength'].index(b)] for b in band_names]

    # --------------------------------------------------------------------------------
    # Solar spectrum

    try:
        # get ancillary data
        solar_spectrum_file = 'f0.txt'  # source <https://oceancolor.gsfc.nasa.gov/docs/rsr/f0.txt>
        solar_data = pd.read_csv(join(dir_common, solar_spectrum_file),
                                 delimiter=r"\s+|\t+|\s+\t+|\t+\s+", skiprows=15, header=None, engine='python')
        # interpolate to enmap bands
        F0 = interp1d(solar_data[0], solar_data[1])
        F0_ENMAP = np.array(F0(np.array(band_wavelengths)), dtype='float32')
    except:
        # get ancillary data
        solar_spectrum_file = 'SOLAR_SPECTRUM_WMO_86'  # source: polymer <http://download.hygeos.com/POLYMER/auxdata>
        solar_data = pd.read_csv(join(dir_common, solar_spectrum_file), sep=' ')
        # interpolate to enmap bands
        F0 = interp1d(solar_data['lambda(nm)'], solar_data['Sl(W.m-2.nm-1)'])
        F0_ENMAP = np.array(F0(np.array(band_wavelengths)) * 100., dtype='float32')

    return F0_ENMAP

