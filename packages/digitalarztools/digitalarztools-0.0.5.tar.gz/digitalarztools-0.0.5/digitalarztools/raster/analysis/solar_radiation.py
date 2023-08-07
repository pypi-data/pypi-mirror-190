from math import sin, cos, tan

import numpy as np


class SolarRadiationAnalysis:
    @classmethod
    def calculate_declination_angle(cls, DOY):
        """
        Declination angle (radians)
        :param DOY: Day of the year
        :return:
        """
        B = 360. / 365 * (DOY - 81)  # (degrees)
        # Computation of cos(theta), where theta is the solar incidence angle relative to the normal to the land surface
        delta = np.arcsin(np.sin(np.deg2rad(23.45)) * np.sin(np.deg2rad(B)))  #
        return delta

    @classmethod
    def calculate_ra_mountain(cls, lon: np.ndarray, DOY: int, hour_loc: float, minutes_loc: float, lon_proy: np.ndarray, lat_proy: np.ndarray, slope: np.ndarray, aspect: np.ndarray):
        """
        Calculates the extra-terrestiral solar radiation or radiation from mountain/slop by using the date, slope and aspect.
        :param lon: longitude raster (np.ndarray)
        :param DOY:  day of the year
        :param hour_loc:
        :param minutes_loc:
        :param lon_proy: x value raster in meter (np.ndarray)
        :param lat_proy: y value raster in meter (np.ndarray)
        :param slope:  slope raster (np.ndarray)
        :param aspect: aspect raster (np.ndarray)
        :return:
        """
        # Constants
        Min_cos_zn = 0.1  # Min value for cos zenith angle
        Max_cos_zn = 1.0  # Max value for cos zenith angle
        Gsc = 1367  # Solar constant (W / m2)

        # Rounded difference of the local time from Greenwich (GMT) (hours):
        offset_GTM = round(lon[int(lon.shape[0] / 2), int(lon.shape[1] / 2)] * 24 / 360)

        try:
            GMT_time = float(hour_loc) - offset_GTM + float(minutes_loc) / 60  # Local time (hours)
            Loc_time = float(hour_loc) + float(minutes_loc) / 60  # Local time (hours)
        except:
            GMT_time = np.float_(hour_loc) - offset_GTM + np.float_(minutes_loc) / 60  # Local time (hours)
            Loc_time = np.float_(hour_loc) + np.float_(minutes_loc) / 60  # Local time (hours)

        print('  Local Time: ', '%0.3f' % np.nanmean(Loc_time))
        print('  GMT Time: ', '%0.3f' % np.nanmean(GMT_time))
        print('  Difference of local time (LT) from Greenwich (GMT): ', offset_GTM)

        # 1. Calculation of extraterrestrial solar radiation for slope and aspect
        # Computation of Hour Angle (HRA = w)
        B = 360. / 365 * (DOY - 81)  # (degrees)
        # Computation of cos(theta), where theta is the solar incidence angle relative to the normal to the land surface
        delta = cls.calculate_declination_angle(DOY)  # Declination angle (radians)
        phi = cls.calculate_latitude_of_pixel(lat_proy)
        s = np.deg2rad(slope)  # Surface slope (radians)
        gamma = np.deg2rad(aspect - 180)  # Surface aspect angle (radians)
        w = cls.w_time(GMT_time, lon_proy, DOY)  # Hour angle (radians)
        a, b, c = cls.constants_for_solar_radiation(delta, s, gamma, phi)
        cos_zn = cls.cos_zenith_angle(a, b, c, w)
        cos_zn = cos_zn.clip(Min_cos_zn, Max_cos_zn)

        print('Average Cos Zenith Angle: ', '%0.3f (Radians)' % np.nanmean(cos_zn))

        dr = 1 + 0.033 * cos(DOY * 2 * np.pi / 365)  # Inverse relative distance Earth-Sun
        # Instant. extraterrestrial solar radiation (W/m2), Allen et al.(2006):
        Ra_inst = Gsc * cos_zn * dr

        # 24-hours extraterrestrial radiation
        # 1.) determine if there are one or two periods of sun
        # 2.) calculate the 24-hours extraterrestrial radiation if there are two periods of sun
        # 3.) calculate the 24-hours extraterrestrial radiation if there is one period of sun

        # 1.) determine amount of sun periods
        Ra_24 = np.zeros(np.shape(lat_proy)) * np.nan
        constant = Gsc * dr / (2 * np.pi)
        TwoPeriod = cls.TwoPeriods(delta, s, phi)  # all input in radians

        # 2.) calculate the 24-hours extraterrestrial radiation (2 periods)
        ID = np.where(np.ravel(TwoPeriod == True))
        Ra_24.flat[ID] = cls.TwoPeriodSun(constant, delta, s.flat[ID], gamma.flat[ID], phi.flat[ID])

        # 3.) calculate the 24-hours extraterrestrial radiation (1 period)
        ID = np.where(np.ravel(TwoPeriod == False))
        Ra_24.flat[ID] = cls.OnePeriodSun(constant, delta, s.flat[ID], gamma.flat[ID], phi.flat[ID])

        # Horizontal surface
        ws = np.arccos(-np.tan(delta) * np.tan(phi))  # Sunrise/sunset time angle

        # Extraterrestial radiation for a horizontal surface for 24-h period:
        Ra_hor_24 = (Gsc * dr / np.pi * (np.sin(delta) * np.sin(phi) * ws + np.cos(delta) * np.cos(phi) * np.sin(ws)))
        # cos_theta_flat = (np.sin(delta) * np.sin(phi) + np.cos(delta) * np.cos(phi) * np.cos(w))

        # Mountain radiation
        Ra_mountain_24 = np.where(Ra_24 > Min_cos_zn * Ra_hor_24, Ra_24 / np.cos(s),
                                  Ra_hor_24)
        Ra_mountain_24[Ra_mountain_24 > 600.0] = 600.0

        return Ra_mountain_24, Ra_inst, cos_zn, dr, phi, delta

    @staticmethod
    def radiation_daily_for_flat_surface(phi, delta):
        """
         Daily 24 hr radiation - For flat terrain only !  which sunset hour angle ws
        :param phi:  latitude in radians
        :param delta: Declination angle (radians)
        :return:
        """
        return np.arccos(-np.tan(phi) * tan(delta))

    @staticmethod
    def w_time(GMT, lon_proy, DOY):
        """
        This function computes the hour angle (radians) of an image given the
        local time, longitude, and day of the year
        :param GMT:
        :param lon_proy:  longitude raster
        :param DOY:  day of the year
        :return: hour angle of the image
        """
        nrow, ncol = lon_proy.shape

        # Difference of the local time (LT) from Greenwich Mean Time (GMT) (hours):
        delta_GTM = lon_proy[int(nrow / 2), int(ncol / 2)] * 24 / 360
        if np.isnan(delta_GTM):
            delta_GTM = np.nanmean(lon_proy) * np.nanmean(lon_proy) * 24 / 360

        # Local Standard Time Meridian (degrees):
        LSTM = 15 * delta_GTM

        # Ecuation of time (EoT, minutes):
        B = 360. / 365 * (DOY - 81)  # (degrees)
        EoT = 9.87 * sin(np.deg2rad(2 * B)) - 7.53 * cos(np.deg2rad(B)) - 1.5 * sin(np.deg2rad(B))

        # Net Time Correction Factor (minutes) at the center of the image:
        TC = 4 * (lon_proy - LSTM) + EoT  # Difference in time over the longitude
        LST = GMT + delta_GTM + TC / 60  # Local solar time (hours)
        HRA = 15 * (LST - 12)  # Hour angle HRA (degrees)
        w = np.deg2rad(HRA)  # Hour angle HRA (radians)
        return w

    @staticmethod
    def constants_for_solar_radiation(delta, s, gamma, phi):
        """
        Based on Richard G. Allen 2006 equation 11
        determines constants for calculating the exterrestial solar radiation
        B = 360. / 365 * (DOY - 81)  # (degrees)
        # Computation of cos(theta), where theta is the solar incidence angle relative to the normal to the land surface
        delta = np.arcsin(np.sin(np.deg2rad(23.45)) * np.sin(np.deg2rad(B)))  # Declination angle (radians)

        :param delta:
        :param s: slope in radians
        :param gamma: slope direction in radians
        :param phi:  latitude in radians
        :return:
        """
        a = np.sin(delta) * np.cos(phi) * np.sin(s) * np.cos(gamma) - np.sin(delta) * np.sin(phi) * np.cos(s)
        b = np.cos(delta) * np.cos(phi) * np.cos(s) + np.cos(delta) * np.sin(phi) * np.sin(s) * np.cos(gamma)
        c = np.cos(delta) * np.sin(s) * np.sin(gamma)

        return a, b, c

    @staticmethod
    def cos_zenith_angle(a, b, c, w):
        """
        Based on Richard G. Allen 2006
        Calculate the cos zenith angle of the image by using the hour angle of the image and constants
        :param a:
        :param b:
        :param c:
        :param w:
        :return:
        """
        angle = -a + b * np.cos(w) + c * np.sin(w)

        return angle

    @staticmethod
    def TwoPeriods(delta, s, phi):
        """
        Based on Richard G. Allen 2006
        Create a boolean map with True values for places with two sunsets
        :param delta:
        :param s:
        :param phi:
        :return:
        """
        TwoPeriods = (np.sin(s) > np.ones(s.shape) * np.sin(phi) * np.cos(delta) + np.cos(phi) * np.sin(delta))

        return TwoPeriods

    @classmethod
    def OnePeriodSun(cls, constant, delta, s, gamma, phi):
        '''
        Based on Richard G. Allen 2006
        Calculate the 24-hours extraterrestrial radiation when there is one sun period
        '''
        sunrise, sunset = cls.SunHours(delta, s, gamma, phi)
        vals = cls.IntegrateSlope(constant, sunrise, sunset, delta, s, gamma, phi)

        return vals

    @classmethod
    def TwoPeriodSun(cls, constant, delta, s, gamma, phi):
        """
        Based on Richard G. Allen 2006
        Calculate the 24-hours extraterrestrial radiation when there are two sun period
        :param constant:
        :param delta:
        :param s:
        :param gamma:
        :param phi:
        :return:
        """
        A1, A2 = cls.SunHours(delta, s, gamma, phi)
        a, b, c = cls.constants_for_solar_radiation(delta, s, gamma, phi)
        riseSlope, setSlope = cls.BoundsSlope(a, b, c)
        B1 = np.maximum(riseSlope, setSlope)
        B2 = np.minimum(riseSlope, setSlope)
        Angle_B1 = cls.cos_zenith_angle(a, b, c, B1)
        Angle_B2 = cls.cos_zenith_angle(a, b, c, B2)

        B1[abs(Angle_B1) > 0.001] = np.pi - B1[abs(Angle_B1) > 0.001]
        B2[abs(Angle_B2) > 0.001] = -np.pi - B2[abs(Angle_B2) > 0.001]

        # Check if two periods really exist
        ID = np.ravel_multi_index(np.where(np.logical_and(B2 >= A1, B1 >= A2) == True), a.shape)
        Val = cls.IntegrateSlope(constant, B2.flat[ID], B1.flat[ID], delta, s.flat[ID], gamma.flat[ID], phi.flat[ID])
        ID = ID[Val < 0]

        # Finally calculate resulting values
        vals = np.zeros(B1.shape)

        vals.flat[ID] = (cls.IntegrateSlope(constant, A1.flat[ID], B2.flat[ID], delta, s.flat[ID], gamma.flat[ID], phi.flat[ID]) +
                         cls.IntegrateSlope(constant, B1.flat[ID], A2.flat[ID], delta, s.flat[ID], gamma.flat[ID], phi.flat[ID]))
        ID = np.ravel_multi_index(np.where(vals == 0), a.shape)
        vals.flat[ID] = cls.IntegrateSlope(constant, A1.flat[ID], A2.flat[ID], delta, s.flat[ID], gamma.flat[ID], phi.flat[ID])

        return vals

    @staticmethod
    def BoundsSlope(a, b, c):
        """
        Based on Richard G. Allen 2006 equation 13
        This function calculates candidate values for sunrise and sunset hour angles
        :param a:
        :param b:
        :param c:
        :return:
        """
        Div = (b ** 2 + c ** 2)
        Div[Div <= 0] = 0.00001
        sinB = (a * c + b * np.sqrt(b ** 2 + c ** 2 - a ** 2)) / Div
        sinA = (a * c - b * np.sqrt(b ** 2 + c ** 2 - a ** 2)) / Div

        sinB[sinB < -1] = -1;
        sinB[sinB > 1] = 1  # Limits see appendix A.2.i
        sinA[sinA < -1] = -1;
        sinA[sinA > 1] = 1  # Limits see appendix A.2.i

        sunrise = np.arcsin(sinA)
        sunset = np.arcsin(sinB)

        return sunrise, sunset

    @staticmethod
    def BoundsHorizontal(delta, phi):
        """
        Based on Richard G. Allen 2006
        This function calculates sunrise hours based on earth inclination and latitude
        If there is no sunset or sunrise hours the values are either set to 0 (polar night) or pi (polar day)
        :param delta:
        :param phi:
        :return:
        """
        bound = np.arccos(-np.tan(delta) * np.tan(phi))
        bound[abs(delta + phi) > np.pi / 2] = np.pi
        bound[abs(delta - phi) > np.pi / 2] = 0

        return bound

    @classmethod
    def SunHours(cls, delta, slope, slopedir, lat):
        # Define sun hours in case of one sunlight period
        a, b, c = cls.constants_for_solar_radiation(delta, slope, slopedir, lat)
        riseSlope, setSlope = cls.BoundsSlope(a, b, c)
        bound = cls.BoundsHorizontal(delta, lat)

        Calculated = np.zeros(slope.shape, dtype=bool)
        RiseFinal = np.zeros(slope.shape)
        SetFinal = np.zeros(slope.shape)

        # First check sunrise is not nan
        # This means that their is either no sunrise (whole day night) or no sunset (whole day light)
        # For whole day light, use the horizontal sunrise and whole day night a zero..
        Angle4 = cls.cos_zenith_angle(a, b, c, -bound)
        RiseFinal[np.logical_and(np.isnan(riseSlope), Angle4 >= 0.0)] = -bound[np.logical_and(np.isnan(riseSlope), Angle4 >= 0.0)]
        Calculated[np.isnan(riseSlope)] = True

        # Step 1 > 4
        Angle1 = cls.cos_zenith_angle(a, b, c, riseSlope)
        Angle2 = cls.cos_zenith_angle(a, b, c, -bound)

        ID = np.ravel_multi_index(np.where(np.logical_and(np.logical_and(Angle2 < Angle1 + 0.001, Angle1 < 0.001), Calculated == False) == True), a.shape)
        RiseFinal.flat[ID] = riseSlope.flat[ID]
        Calculated.flat[ID] = True
        # step 5 > 7
        Angle3 = cls.cos_zenith_angle(a, b, c, -np.pi - riseSlope)

        ID = np.ravel_multi_index(np.where(np.logical_and(np.logical_and(-bound < (-np.pi - riseSlope), Angle3 <= 0.001), Calculated == False) == True), a.shape)
        RiseFinal.flat[ID] = -np.pi - riseSlope.flat[ID]
        Calculated.flat[ID] = True

        # For all other values we use the horizontal sunset if it is positive, otherwise keep a zero
        RiseFinal[Calculated == False] = -bound[Calculated == False]

        # Then check sunset is not nan or < 0
        Calculated = np.zeros(slope.shape, dtype=bool)

        Angle4 = cls.cos_zenith_angle(a, b, c, bound)
        SetFinal[np.logical_and(np.isnan(setSlope), Angle4 >= 0.0)] = bound[np.logical_and(np.isnan(setSlope), Angle4 >= 0.0)]
        Calculated[np.isnan(setSlope)] = True

        # Step 1 > 4
        Angle1 = cls.cos_zenith_angle(a, b, c, setSlope)
        Angle2 = cls.cos_zenith_angle(a, b, c, bound)

        ID = np.ravel_multi_index(np.where(np.logical_and(np.logical_and(Angle2 < Angle1 + 0.001, Angle1 < 0.001), Calculated == False) == True), a.shape)
        SetFinal.flat[ID] = setSlope.flat[ID]
        Calculated.flat[ID] = True
        # step 5 > 7
        Angle3 = cls.cos_zenith_angle(a, b, c, np.pi - setSlope)

        ID = np.ravel_multi_index(np.where(np.logical_and(np.logical_and(bound > (np.pi - setSlope), Angle3 <= 0.001), Calculated == False) == True), a.shape)
        SetFinal.flat[ID] = np.pi - setSlope.flat[ID]
        Calculated.flat[ID] = True

        # For all other values we use the horizontal sunset if it is positive, otherwise keep a zero
        SetFinal[Calculated == False] = bound[Calculated == False]

        #    Angle4 = AngleSlope(a,b,c,bound)
        #    SetFinal[np.logical_and(Calculated == False,Angle4 >= 0)] = bound[np.logical_and(Calculated == False,Angle4 >= 0)]

        # If Sunrise is after Sunset there is no sunlight during the day
        SetFinal[SetFinal <= RiseFinal] = 0.0
        RiseFinal[SetFinal <= RiseFinal] = 0.0

        return RiseFinal, SetFinal

    @staticmethod
    def IntegrateSlope(constant, sunrise, sunset, delta, s, gamma, phi):
        """
        Based on Richard G. Allen 2006 equation 5
        Calculate the 24 hours extraterrestrial radiation
        :param constant:
        :param sunrise:
        :param sunset:
        :param delta:
        :param s:
        :param gamma:
        :param phi:
        :return:
        """
        # correct the sunset and sunrise angels for days that have no sunset or no sunrise
        SunOrNoSun = np.logical_or(((np.abs(delta + phi)) > (np.pi / 2)), ((np.abs(delta - phi)) > (np.pi / 2)))
        integral = np.zeros(s.shape)
        ID = np.where(np.ravel(SunOrNoSun == True))

        # No sunset
        IDNoSunset = np.where(np.ravel(abs(delta + phi.flat[ID]) > (np.pi / 2)))
        if np.any(IDNoSunset) == True:
            sunset1 = np.pi
            sunrise1 = -np.pi
            integral.flat[IDNoSunset] = constant * (np.sin(delta) * np.sin(phi) * np.cos(s) * (sunset1 - sunrise1)
                                                    - np.sin(delta) * np.cos(phi) * np.sin(s) * np.cos(gamma) * (sunset1 - sunrise1)
                                                    + np.cos(delta) * np.cos(phi) * np.cos(s) * (np.sin(sunset1) - np.sin(sunrise1))
                                                    + np.cos(delta) * np.sin(phi) * np.sin(s) * np.cos(gamma) * (np.sin(sunset1) - np.sin(sunrise1))
                                                    - np.cos(delta) * np.sin(s) * np.sin(gamma) * (np.cos(sunset1) - np.cos(sunrise1)))

        # No sunrise
        elif np.any(IDNoSunset) == False:
            integral.flat[IDNoSunset == False] = constant * (np.sin(delta) * np.sin(phi) * np.cos(s) * (0)
                                                             - np.sin(delta) * np.cos(phi) * np.sin(s) * np.cos(gamma) * (0)
                                                             + np.cos(delta) * np.cos(phi) * np.cos(s) * (np.sin(0) - np.sin(0))
                                                             + np.cos(delta) * np.sin(phi) * np.sin(s) * np.cos(gamma) * (np.sin(0) - np.sin(0))
                                                             - np.cos(delta) * np.sin(s) * np.sin(gamma) * (np.cos(0) - np.cos(0)))

        ID = np.where(np.ravel(SunOrNoSun == False))
        integral.flat[ID] = constant * (np.sin(delta) * np.sin(phi) * np.cos(s) * (sunset - sunrise)
                                        - np.sin(delta) * np.cos(phi) * np.sin(s) * np.cos(gamma) * (sunset - sunrise)
                                        + np.cos(delta) * np.cos(phi) * np.cos(s) * (np.sin(sunset) - np.sin(sunrise))
                                        + np.cos(delta) * np.sin(phi) * np.sin(s) * np.cos(gamma) * (np.sin(sunset) - np.sin(sunrise))
                                        - np.cos(delta) * np.sin(s) * np.sin(gamma) * (np.cos(sunset) - np.cos(sunrise)))

        return integral

    @classmethod
    def calculate_latitude_of_pixel(cls, lat: np.ndarray):
        """

        :param lat:
        :return:
        """
        return np.deg2rad(lat)  # latitude of the pixel (radians)

    @staticmethod
    def calculate_extraterrestrial_daily_radiation(ws_angle, phi, dr, delta, nrow, ncol, Gsc_const=1367):
        """
        caclulate Extraterrestrial daily radiation, Ra (W/m2):
        :param ws_angle:   Daily 24 hr radiation - For flat terrain only
        :param phi:  lat in rad
        :param dr: nverse relative distance Earth-Sun
        :param delta: delination angle in radian
        :param nrow:  no of rows
        :param ncol: no of cols
        :param Gsc_const:  Solar constant (W / m2) value is  1367
        :return:
        """
        Ra24_flat = (Gsc_const / np.pi * dr * (ws_angle * np.sin(phi[int(nrow / 2), int(ncol / 2)]) * np.sin(delta) +
                                               np.cos(phi[int(nrow / 2), int(ncol / 2)]) * np.cos(delta) * np.sin(ws_angle)))
        return Ra24_flat

    @staticmethod
    def calculate_daily_solar_radiation(Ra_mountain_24, Transm_24):
        """
        calculate daily radiation if transmissivity is available method 2
        :param Ra_mountain_24: diation from mountain or slop using calculate_ra_mountain
        :param Transm_24: SolarRadiationAnalysis.calculate_hourly_solar_radiation
        :return:
        """
        return Ra_mountain_24 * Transm_24

    @staticmethod
    def calculate_transmissivity_correction(Transm_inst: np.ndarray):
        """
        :param Transm_inst: either through dataset like MERRA or using  SolarRadiationAnalysis.calculate_instant_transmissivity(Rs_inst, Ra_inst)
        :return:
        """
        # Atmospheric emissivity, by Bastiaanssen (1995):
        transm_corr = np.copy(Transm_inst)
        transm_corr[Transm_inst < 0.001] = 0.1
        transm_corr[Transm_inst > 1] = 1
        return transm_corr

    @staticmethod
    def calculate_instantaneous_incoming_short_wavelength_radiation(Ra_inst:np.ndarray, transmissivity_correction: np.ndarray):
        """
        calculate hourly radiation if transmissivity is available method 2
        :param Ra_inst: radiation from mountain or slop using calculate_ra_mountain
        :param transmissivity_correction: transmissivity correction using  SolarRadiationAnalysis.calculate_transmissivity_correction
        :return:
        """
        # Instantaneous incoming short wave radiation (W/m2):
        Rs_inst = Ra_inst * transmissivity_correction
        return Rs_inst

    @staticmethod
    def calculate_daily_transmissivity(Rs_24, Ra_mountain_24):
        """
        calculate daily transmissivity if radiation is available method 1
        :param Rs_24: daily radiation can be extracted from MERRA swgdn_MERRA_W-m-2
        :param Ra_mountain_24: Radiation from mountain or slop using calculate_ra_mountain
        :return:
        """

        return Rs_24 / Ra_mountain_24

    @staticmethod
    def calculate_instant_transmissivity(Rs_instant, Ra_inst):
        """
        calculate hourly transmissivity if radiation is available method 1
        :param Rs_instant: instantenous short wavelength radiation (W/m2):  which can be extracted from MERRA swgdn_MERRA_W-m-2
        :param Ra_inst: Radiation from mountain or slop using calculate_ra_mountain
        :return:
        """

        return Rs_instant / Ra_inst

    @staticmethod
    def calculate_daily_solar_radiation_from_extraterrestrial_radiation(Ra24_flat, Transm_24):
        """

        :param Ra24_flat: daily extraterrestrial_radiation using SolarRadiationAnalysis.calculate_extraterrestrial_daily_radiation
        :param Transm_24: daily transmissivity using SolarRadiationAnalysis.calculate_daily_transmissivity
        :return:
        """
        return Ra24_flat * Transm_24
