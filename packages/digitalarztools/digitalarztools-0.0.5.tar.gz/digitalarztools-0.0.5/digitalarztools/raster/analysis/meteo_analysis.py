from datetime import datetime

import numpy as np
import pandas as pd

from digitalarztools.raster.band_process import BandProcess
from digitalarztools.raster.rio_raster import RioRaster


class MeteoAnalysis:
    @staticmethod
    def get_datasets_date_range(dates: pd.DatetimeIndex) -> (str, str, str, str):
        """
        :param dates: request dates
        :return: merra and geos start and end date in %Y-%m-%d string format based on requested dates
        """

        # merra_last_date = MERRA.get_last_available_date()
        # # merra_last_date = datetime.strptime("2022-12-01", "%Y-%m-%d")
        # merra_dates = dates[dates < merra_last_date]
        # geos_dates = dates[dates >= merra_last_date]
        # start_date_merra = datetime.strftime(merra_dates[0], "%Y-%m-%d") if not merra_dates.empty else ""
        # end_date_merra = datetime.strftime(merra_dates[-1], "%Y-%m-%d") if not merra_dates.empty else ""
        # start_date_geos = datetime.strftime(geos_dates[0], "%Y-%m-%d") if not geos_dates.empty else ""
        # end_date_geos = datetime.strftime(dates[-1], "%Y-%m-%d") if not dates.empty else ""
        #
        # return start_date_merra, end_date_merra, start_date_geos, end_date_geos
        return '2022-02-08', '2022-02-15', '', '2022-02-15'

    @staticmethod
    def calculate_wind_and_humidity(start_date, end_date, start_date_merra, end_date_merra, start_date_geos,
                                    end_date_geos,
                                    Temp_folder, Pres_folder, Hum_folder, hum_out_folder, vwind_folder, uwind_folder,
                                    wind_out_folder, nodata_value=-9999):
        """
        calculate wind and humidity of at different dates and save it in wind and humidity out folder
        all folder are list of folder for merra and geos, 0 index have merra and 1 index have geos
        :param start_date:
        :param end_date:
        :param start_date_merra:
        :param end_date_merra:
        :param start_date_geos:
        :param end_date_geos:
        :param Temp_folder: list of Temperature data folder of merra and geos
        :param Pres_folder: list of Air Pressure data folder of mera and geos
        :param Hum_folder: list of Humidity data folder of merra and geos
        :param hum_out_folder:  list of humidity out folder for merra and geos
        :param vwind_folder: v wind
        :param uwind_folder:  u wind
        :param wind_out_folder: list of window out folder for merra ang geos
        :param nodata_value:
        """
        Dates = pd.date_range(start_date, end_date, freq="D")

        for Date in Dates:
            idx = -1
            if start_date_merra != "" and datetime \
                    .strptime(start_date_merra, "%Y-%m-%d") <= Date <= datetime.strptime(end_date_merra, "%Y-%m-%d"):
                idx = 0
            if start_date_geos != "" and datetime \
                    .strptime(start_date_geos, "%Y-%m-%d") <= Date <= datetime.strptime(end_date_geos, "%Y-%m-%d"):
                idx = 1
            if idx != -1:
                Day = Date.day
                Month = Date.month
                Year = Date.year

                temp_file_one = Temp_folder[idx].format(yyyy=Year, mm=Month, dd=Day)
                pressure_file_one = Pres_folder[idx].format(yyyy=Year, mm=Month, dd=Day)
                humidity_file_one = Hum_folder[idx].format(yyyy=Year, mm=Month, dd=Day)
                out_folder_one = hum_out_folder[idx].format(yyyy=Year, mm=Month, dd=Day)

                u_wind_file_one = uwind_folder[idx].format(yyyy=Year, mm=Month, dd=Day)
                v_wind_file_one = vwind_folder[idx].format(yyyy=Year, mm=Month, dd=Day)
                out_folder_one_wind = wind_out_folder[idx].format(yyyy=Year, mm=Month, dd=Day)

                # geo_out, proj, size_X, size_Y = Open_array_info(Tempfile_one)
                temp_raster = RioRaster(temp_file_one)
                nodata_value = nodata_value if temp_raster.get_nodata_value() is None else temp_raster.get_nodata_value()
                temp_data = temp_raster.get_data_array(band=1)
                temp_data = temp_data - 273.15
                temp_data[temp_data < -900] = nodata_value
                pressure_data = RioRaster(pressure_file_one).get_data_array(band=1)
                humidity_data = RioRaster(humidity_file_one).get_data_array(1)
                pressure_data[pressure_data < 0] = nodata_value
                humidity_data[humidity_data < 0] = nodata_value
                u_wind_data = RioRaster(u_wind_file_one).get_data_array(band=1)
                v_wind_data = RioRaster(v_wind_file_one).get_data_array(band=1)

                # gapfilling
                v_wind_data = BandProcess.gap_filling(v_wind_data, nodata_value)
                u_wind_data = BandProcess.gap_filling(u_wind_data, nodata_value)
                temp_data = BandProcess.gap_filling(temp_data, nodata_value)
                pressure_data = BandProcess.gap_filling(pressure_data, nodata_value)
                humidity_data = BandProcess.gap_filling(humidity_data, nodata_value)

                es_data = 0.6108 * np.exp((17.27 * temp_data) / (temp_data + 237.3))
                hum_data = np.minimum((1.6077717 * humidity_data * pressure_data / es_data), 1) * 100
                hum_data = hum_data.clip(0, 100)

                out_crs = temp_raster.get_crs()
                out_transform = temp_raster.get_geo_transform()
                # Save_as_tiff(out_folder_one, HumData, geo_out, "WGS84")
                RioRaster.write_to_file(out_folder_one, hum_data, out_crs, out_transform, nodata_value)

                wind_data = np.sqrt(v_wind_data ** 2 + u_wind_data ** 2)
                # Save_as_tiff(out_folder_one_wind, WindData, geo_out, "WGS84")
                RioRaster.write_to_file(out_folder_one_wind, wind_data, out_crs, out_transform, nodata_value)

    @staticmethod
    def calculate_hourly_saturated_vapour_pressure(Temp_inst):
        """
            Hourly Saturation Vapor Pressure at the air temperature (kPa):
        :param Temp_inst: hourly Tmperature
        :return:
        """
        return 0.6108 * np.exp(17.27 * Temp_inst / (Temp_inst + 237.3))

    @staticmethod
    def calculate_daily_saturated_vapour_pressure(Temp_24):
        """
            Daily  Saturation Vapor Pressure at the air temperature (kPa):
        :param Temp_24: daily Temperature
        :return:
        """
        return 0.6108 * np.exp(17.27 * Temp_24 / (Temp_24 + 237.3))

    @staticmethod
    def calculate_latent_heat_of_vapourization(Surface_temp):
        """
        :param Surface_temp: RioLandsat.calculate_surface_temperature
        :return:
        """
        return (2.501 - 2.361e-3 * (Surface_temp - 273.15)) * 1E6

    @staticmethod
    def calculate_hourly_actual_vapour_pressure(RH_inst, sat_vapour_inst):
        """
        Hourly Actual vapour pressure (kPa), FAO 56, eq 19.:
        :param RH_inst: hourly Relative Humidity from Humidity_MERRA_Percentage_1_hourly
        :param sat_vapour_inst: hourly saturated vapour pressure
        :return:
        """
        return RH_inst * sat_vapour_inst / 100

    @staticmethod
    def calculate_daily_actual_vapour_pressure(RH_24, sat_vapour_24):
        """
        Daily Actual vapour pressure (kPa), FAO 56, eq 19.:
        :param RH_24: Daily Relative Humidity from Humidity_MERRA_Percentage_1_daily
        :param sat_vapour_24: daily saturated vapour pressure
        :return:
        """
        return RH_24 * sat_vapour_24 / 100

    @staticmethod
    def calculate_atmospheric_pressure(dem_arr: np.ndarray):
        """
        # Atmospheric pressure for altitude:
        :param dem: elevation data
        :return:
        """
        return 101.3 * np.power((293 - 0.0065 * dem_arr) / 293, 5.26)

    @staticmethod
    def calculate_psychrometric_constant(air_pressure: np.ndarray):
        """
        Psychrometric constant (kPa / °C), FAO 56, eq 8.:
        :param air_pressure:
        :return:
        """
        return 0.665E-3 * air_pressure

    @staticmethod
    def calculate_slope_of_saturated_vapour_pressure(sat_vp_24, Temp_24):
        """
        Slope of satur vapour pressure curve at air temp (kPa / °C)
        :param sat_vp_24: daily saturated vapour pressure
        :param Temp_24: daily temperature
        :return:
        """
        return 4098 * sat_vp_24 / np.power(Temp_24 + 237.3, 2)

    @classmethod
    def calculate_wind_speed_friction(cls, h_obst, Wind_inst, zx, lai, ndvi, surf_albedo, water_mask, surf_roughness_equation_used):
        """
        Function to calculate the windspeed and friction by using the Raupach or NDVI model
        :param h_obst:
        :param Wind_inst: instantaneous wind using MERRA dataset of Wind
        :param zx: Wind speed measurement height mostly used as 2 for MERRA
        :param lai: Leaf Area Index
        :param ndvi:
        :param surf_albedo:
        :param water_mask:
        :param surf_roughness_equation_used:
        :return: surface_rough, wind speed at blending height, and friction velocity
        """

        # constants
        k_vk = 0.41  # Von Karman constant
        h_grass = 0.12  # Grass height (m)
        cd = 5  # Free parameter for displacement height, default = 20.6
        # 1) Raupach model
        # zom_Raupach = Raupach_Model(h_obst, cd, lai)

        # 2) NDVI model
        # zom_NDVI = NDVI_Model(ndvi, surf_albedo, water_mask)

        if surf_roughness_equation_used == 1:
            Surf_roughness = cls.Raupach_Model(h_obst, cd, lai)
        else:
            Surf_roughness = cls.NDVI_Model(ndvi, surf_albedo, water_mask)

        Surf_roughness[Surf_roughness < 0.001] = 0.001

        zom_grass = 0.123 * h_grass
        # Friction velocity for grass (m/s):
        ustar_grass = k_vk * Wind_inst / np.log(zx / zom_grass)
        print('u*_grass = ', '%0.3f (m/s)' % np.mean(ustar_grass))
        # Wind speed (m/s) at the "blending height" (200m):
        u_200 = ustar_grass * np.log(200 / zom_grass) / k_vk
        print('Wind speed at the blending height, u200 =', '%0.3f (m/s)' % np.mean(u_200))
        # Friction velocity (m/s):
        ustar_1 = k_vk * u_200 / np.log(200 / Surf_roughness)

        return Surf_roughness, u_200, ustar_1

    @staticmethod
    def Raupach_Model(h_obst, cd, LAI):
        """
        Function for the Raupach model to calculate the surface roughness (based on Raupach 1994)
        """
        # constants
        cw = 2.0
        LAIshelter = 2.5

        # calculate psi
        psi = np.log(cw) - 1 + np.power(2.0, -1)  # Vegetation influence function

        # Calculate Ustar divided by U
        ustar_u = np.power((0.003 + 0.3 * LAI / 2), 0.5)
        ustar_u[LAI < LAIshelter] = 0.3

        # calculate: 1 - d/hv
        inv_d_hv = (1 - np.exp(-1 * np.power((cd * LAI), 0.5))) / np.power((cd * LAI), 0.5)

        # Calculate: surface roughness/hv
        zom_hv = inv_d_hv * np.exp(-0.41 / ustar_u - psi)

        # Calculate: surface roughness
        zom_Raupach = zom_hv * h_obst

        return zom_Raupach

    @staticmethod
    def NDVI_Model(NDVI, Surf_albedo, water_mask):
        """
        Function for the NDVI model to calculate the surface roughness
        """
        zom_NDVI = np.exp(1.096 * NDVI / Surf_albedo - 5.307)
        zom_NDVI[water_mask == 1.0] = 0.001
        zom_NDVI[zom_NDVI > 10.0] = 10.0

        return (zom_NDVI)
