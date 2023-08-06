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
""" The acwater module calls Polymer (Hygeos) using EnPT (GFZ/EnMAP) parameters.

"""

from polymer.main import run_atm_corr, Level2

from acwater.polymer_enmap import BANDS_ENMAP, BANDS_ENMAP_VNIR, params_enmap
from acwater.level1_enmap import Level1_ENMAP

from enpt.options.config import EnPTConfig

import numpy as np
import logging
from os.path import expanduser, isfile
import os

def polymer_ac_enmap(enmap_l1b, level2='memory', config: EnPTConfig = None, detector='vnir'):
    """The polymer_ac_enmap function calls polymer using EnMAP data specific parameters

    :param enmap_l1b: the object of EnMAP level 1 data
    :param level2: the file name for the output data or 'memory", the latter is default for using with EnPT
    :param config: of EnPTConfig type must contain:
        * CPUs: number of CPUs, here combined with number of threads, if threads not given.
        * threads: number of threads for specifying number of threads.
        * blocksize: size in rows for each thread in multiprocessing
        * auto_download_ecmwf: for using reanalyses ERA5 data
    :param detector: "vnir" for visible to near infrared or "merge" to include shortwave infrared (swir) detector
    :return: level2 data object
    """
    print(detector)
    logger = enmap_l1b.logger or logging.getLogger(__name__)

    logger.info("Running polymer...")

    # use config of EnPT
    if config is not None:
        assert isinstance(config, EnPTConfig)
        blocksize = config.blocksize
        # threads number is combined with number of CPUs, but n threads can be larger if given
        threads = config.threads if int(
            config.threads) != -1 else -1 if config.CPUs is None else int(config.CPUs)

        # ancillary_source = 'reanalysis' if config.auto_download_ecmwf else 'climatology'
        #fixme: once climatology option is fixed, it can be triggered by config.auto_download_ecmwf, as in:
        # for now just give warning:
        ancillary_source = 'reanalysis'
        if not config.auto_download_ecmwf:
            logger.warning("Currently only tested with ERA5 data, i.e. set True for \"auto_download_ecmwf\"")
    else:
        blocksize = 100
        threads = -1
        ancillary_source = 'reanalysis'

    # check for key file, required in downloading ancillary data
    home = expanduser("~")
    if ancillary_source == 'reanalysis' and \
       not isfile(home + "/.cdsapirc") and \
       not ('CDSAPI_URL' in os.environ and 'CDSAPI_KEY' in os.environ):
        logger.error("Missing CDS API key, see ACwater Polymer instructions")
    elif ancillary_source == 'climatology' and not isfile(home + "/.netrc") and not isfile(home + "/.urs_cookies"):
        logger.error("Missing NASA Earthdata key file, see ACwater Polymer instructions")

    # check input for detector name
    assert detector in ['vnir', 'merge', 'vnswir']

    # select detector band
    if detector == 'vnir':

        bands_wavelength = BANDS_ENMAP_VNIR['wavelength']  # enmap_l1b.meta.vnir.wvl_center8

        ibands_vnir = [bands_wavelength.index(b) for b in enmap_l1b.vnir.detector_meta.wvl_center]

        l1_enmap = Level1_ENMAP(enmap_l1b,
                                blocksize=blocksize,
                                bands_wavelength=bands_wavelength,
                                detector_name=detector,
                                ancillary=ancillary_source)

        bands_to_use = [
            423.03, 428.8, 434.29, 439.58, 444.72, 449.75, 454.7, 459.59, 464.43, 469.25, 474.05, 478.84,
            483.63, 488.42, 493.23, 498.05, 502.9, 507.77, 512.67, 517.6, 522.57, 527.58, 532.63, 537.72,
            542.87, 548.06, 553.3, 558.6, 563.95, 569.36, 574.83, 580.36, 585.95, 591.6, 597.32, 603.1, 608.95,
            614.86, 620.84, 626.9, 633.02, 639.21, 645.47, 651.8, 658.2,
            664.67, 671.21, 677.83, 684.51, 691.26, 698.08, 704.97, 711.92, 718.95, 726.03, 733.19,
            740.4, 747.68, 755.01,
            769.86, 777.37,
        ]
        band_cloudmask = 863.03  # vnir

    elif detector == 'merge' or detector == 'vnswir':
        # vnir and swir
        bands_wavelength = BANDS_ENMAP['wavelength']

        ibands_vnir = [bands_wavelength.index(b) for b in enmap_l1b.vnir.detector_meta.wvl_center]
        ibands_swir = [bands_wavelength.index(b) for b in enmap_l1b.swir.detector_meta.wvl_center]

        from enpt.processors.orthorectification import VNIR_SWIR_Stacker

        # ------------------------------
        # # corregistration vnir to swir
        enmap_l1b.swir.data = enmap_l1b.transform_swir_to_vnir_raster(enmap_l1b.swir.data)

        data_geoarray = VNIR_SWIR_Stacker(vnir=enmap_l1b.vnir.data,
                                          swir=enmap_l1b.swir.data,
                                          vnir_wvls=enmap_l1b.meta.vnir.wvl_center,
                                          swir_wvls=enmap_l1b.meta.swir.wvl_center
                                          ).compute_stack(algorithm='order_by_wvl')

        # solution 1: use vnir object as data carrier
        enmap_l1b.vnir.data = data_geoarray
        # cannot delete, thus reduce size (issue with int8)
        enmap_l1b.swir.data[:] = enmap_l1b.swir.data[:].astype(dtype='float16')
        # instantiate class
        l1_enmap = Level1_ENMAP(enmap_l1b,
                                blocksize=blocksize,
                                bands_wavelength=bands_wavelength,
                                ancillary = ancillary_source)

        # solution 2: use geoarray + metadata + configuration
        # fixme: data_object is needed includin vnir + swir, as well as detector metadata (lat, lons
        # enmap_l1b = Level1_ENMAP(data_geoarray, detector_meta= enmap_l1b.vnir.detector_meta, platform_meta=enmap_l1b.meta, blocksize=blocksize)

        # # solution 3: construct new Detector Class or re-write existing one
        # (ex. EnMAP_Detector_SensorGeo, where enmap_l1b.vnswir = EnMAP_Detector_SensorGeo('vnswir', '', config)

        # ------------------------------------------------------------
        # selection based on absorption features (H20, O3)
        # reference: https://amt.copernicus.org/articles/11/3205/2018/
        bands_to_use = [
            423.03, 428.80, 434.29, 439.58, 444.72, 449.75, 454.70,
            459.59, 464.43, 469.25, 474.05, 478.84,
            483.63, 488.42, 493.23, 498.05, 502.90, 507.77, 512.67,
            517.60, 522.57, 527.58, 532.63, 537.72,
            542.87, 548.06, 553.30, 558.60, 563.95, 569.36, 574.83,
            580.36, 585.95, 591.60, 597.32, 603.10,
            608.95, 614.86, 620.84, 626.90, 639.21, 645.47, 651.80,
            658.20, 747.68, 755.01, 777.37,
            784.93, 792.54, 800.20, 807.91, 815.67, 831.30,
            839.18, 847.10, 855.05,
            871.05, 879.09,
            887.16, 895.25, 903.36, 904.78, 911.49, 914.44, 919.64,
            924.23, 927.80, 934.16, 935.98, 944.17,
            944.23,
            952.37, 954.42, 960.57, 964.74, 968.78, 975.17, 976.99,
            985.21, 985.73, 996.4, 1007.2,
            1018.1,
            # include swir for a complete spectrum
            1029.1, 1040.2, 1051.3, 1062.6, 1074.0, 1085.4, 1096.9, 1108.5, 1120.1, 1131.8, 1143.5,
            1155.3, 1167.1, 1179.0, 1190.9, 1202.8, 1214.8, 1226.7, 1238.7, 1250.7, 1262.7, 1274.7, 1286.7,
            1298.7, 1310.7, 1322.7, 1334.7, 1346.6, 1487.8, 1499.4, 1510.9, 1522.3, 1533.7, 1545.1, 1556.4,
            1567.7, 1578.9, 1590.1, 1601.2, 1612.3, 1623.3, 1634.3, 1645.3, 1656.2, 1667.0, 1677.8, 1688.5,
            1699.2, 1709.9, 1720.5, 1731.0, 1741.5, 1752.0, 1762.4, 1772.7, 1969.9, 1979.3, 1988.7, 1998.0,
            2007.2, 2016.4, 2025.6, 2034.8, 2043.9, 2052.9, 2061.9, 2070.9, 2079.9, 2088.8, 2097.6, 2106.4,
            2115.2, 2124.0, 2132.7, 2141.3, 2150.0, 2158.6, 2167.1, 2175.7, 2184.2, 2192.6, 2201.0, 2209.4,
            2217.8, 2226.1, 2234.4, 2242.6, 2250.8, 2259.0, 2267.2, 2275.3, 2283.4, 2291.4, 2299.4, 2307.4,
            2315.4, 2323.3, 2331.2, 2339.1, 2346.9, 2354.7, 2362.5, 2370.2, 2377.9, 2385.6, 2393.3, 2400.9,
            2408.5, 2416.1, 2423.6, 2431.1, 2438.6
        ]

        band_cloudmask = 863.03  # vnir

    else:
        raise NotImplementedError

    if level2 == 'memory':
        level2_object = Level2('memory')
    elif isinstance(level2, Level2):
        level2_object = level2
    else:
        # level2 is file name
        level2_object = Level2(filename=level2, fmt='netcdf4', overwrite=True)

    K_NO2, K_OZ, calib = params_enmap(bands_wavelength)

    # for testing
    # block = enmap_l1b.read_block(size=(30, 1000), offset=(0, 0), bands=bands_to_use)
    # blocks = enmap_l1b.blocks(bands_to_use)

    product = run_atm_corr(l1_enmap,
                           level2=level2_object,
                           multiprocessing=threads,
                           # params for enmap, using 'GENERIC' as sensor attribute
                           bands_corr=bands_to_use,
                           bands_oc=bands_to_use,
                           bands_rw=bands_wavelength,
                           calib=calib,
                           K_OZ=K_OZ,
                           K_NO2=K_NO2,
                           band_cloudmask=band_cloudmask,
                           thres_Rcloud=0.2,
                           thres_Rcloud_std=0.04
                           # datasets=default_datasets.extend(analysis_datasets)),
                           )


    if detector == 'vnir':
        enmap_l2a_vnir = product.Rw[:, :, ibands_vnir]
        enmap_l2a_swir = np.ones(enmap_l1b.swir.data.shape, dtype=np.float) / config.scale_factor_boa_ref
    elif detector == 'merge' or detector == 'vnswir':
        enmap_l2a_vnir = product.Rw[:, :, ibands_vnir]
        enmap_l2a_swir = product.Rw[:, :, ibands_swir]
        enmap_l2a_swir = enmap_l1b.transform_vnir_to_swir_raster(enmap_l2a_swir)

    # Feature for other products can be returned separately as in:
    # return enmap_l2a_vnir, enmap_l2a_swir, product.logchl, product.bbs, product.bitmask, product.Rgli, product.Rnir
    # or combined in an additional output as in
    # enmap_products = {'polymer_logchl' : product.logchl / config.scale_factor_boa_ref,
    #                 'polymer_bbs' : product.bbs / config.scale_factor_boa_ref,
    #                 'polymer_rgli' : product.Rgli / config.scale_factor_boa_ref,
    #                 'polymer_rnir' : product.Rnir / config.scale_factor_boa_ref,
    #                 'polymer_bitmask' : product.bitmask / config.scale_factor_boa_ref}



    return enmap_l2a_vnir, enmap_l2a_swir
