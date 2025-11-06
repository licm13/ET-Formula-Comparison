"""
Comparison framework for running multiple PET formulas with same forcing data
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Callable
from ..formulas import *


class PETComparison:
    """
    Framework for comparing different PET formulas with identical forcing data
    """
    
    def __init__(self, forcing_data: pd.DataFrame):
        """
        Initialize comparison framework
        
        Parameters:
        -----------
        forcing_data : pd.DataFrame
            DataFrame containing meteorological forcing data with columns:
            - temperature: Air temperature (°C)
            - relative_humidity: Relative humidity (%)
            - wind_speed: Wind speed (m s-1)
            - net_radiation: Net radiation (MJ m-2 day-1)
            - pressure: Atmospheric pressure (kPa) [optional, default: 101.3]
            - soil_heat_flux: Soil heat flux (MJ m-2 day-1) [optional, default: 0]
            - lai: Leaf Area Index [optional]
            - ndvi: NDVI [optional]
            - soil_moisture: Relative soil moisture [optional]
            - co2: CO2 concentration (ppm) [optional, default: 380]
        """
        self.forcing_data = forcing_data
        self.results = {}
        
        # Set defaults for optional parameters
        if 'pressure' not in forcing_data.columns:
            self.forcing_data['pressure'] = 101.3
        if 'soil_heat_flux' not in forcing_data.columns:
            self.forcing_data['soil_heat_flux'] = 0.0
        if 'co2' not in forcing_data.columns:
            self.forcing_data['co2'] = 380.0
    
    def run_penman_monteith(self):
        """Run FAO-56 Penman-Monteith"""
        pet = penman_monteith(
            temperature=self.forcing_data['temperature'].values,
            relative_humidity=self.forcing_data['relative_humidity'].values,
            wind_speed=self.forcing_data['wind_speed'].values,
            net_radiation=self.forcing_data['net_radiation'].values,
            pressure=self.forcing_data['pressure'].values,
            soil_heat_flux=self.forcing_data['soil_heat_flux'].values,
        )
        self.results['PM'] = pd.Series(pet, index=self.forcing_data.index)
        return self.results['PM']
    
    def run_priestley_taylor(self):
        """Run Priestley-Taylor"""
        pet = priestley_taylor(
            temperature=self.forcing_data['temperature'].values,
            net_radiation=self.forcing_data['net_radiation'].values,
            pressure=self.forcing_data['pressure'].values,
            soil_heat_flux=self.forcing_data['soil_heat_flux'].values,
        )
        self.results['PT'] = pd.Series(pet, index=self.forcing_data.index)
        return self.results['PT']
    
    def run_priestley_taylor_jpl(self):
        """Run PT-JPL"""
        if 'lai' not in self.forcing_data.columns:
            print("Warning: LAI not available, using default LAI=3.0")
            lai = np.ones(len(self.forcing_data)) * 3.0
        else:
            lai = self.forcing_data['lai'].values
        
        if 'soil_moisture' not in self.forcing_data.columns:
            print("Warning: Soil moisture not available, using default SM=0.5")
            soil_moisture = np.ones(len(self.forcing_data)) * 0.5
        else:
            soil_moisture = self.forcing_data['soil_moisture'].values
        
        pet = priestley_taylor_jpl(
            temperature=self.forcing_data['temperature'].values,
            net_radiation=self.forcing_data['net_radiation'].values,
            lai=lai,
            soil_moisture=soil_moisture,
            pressure=self.forcing_data['pressure'].values,
            soil_heat_flux=self.forcing_data['soil_heat_flux'].values,
        )
        self.results['PT-JPL'] = pd.Series(pet, index=self.forcing_data.index)
        return self.results['PT-JPL']
    
    def run_penman_monteith_leuning(self):
        """Run PML"""
        if 'lai' not in self.forcing_data.columns:
            print("Warning: LAI not available, using default LAI=3.0")
            lai = np.ones(len(self.forcing_data)) * 3.0
        else:
            lai = self.forcing_data['lai'].values
        
        result = penman_monteith_leuning(
            temperature=self.forcing_data['temperature'].values,
            relative_humidity=self.forcing_data['relative_humidity'].values,
            wind_speed=self.forcing_data['wind_speed'].values,
            net_radiation=self.forcing_data['net_radiation'].values,
            lai=lai,
            pressure=self.forcing_data['pressure'].values,
            soil_heat_flux=self.forcing_data['soil_heat_flux'].values,
            co2=self.forcing_data['co2'].values,
        )
        self.results['PML'] = pd.Series(result['total'], index=self.forcing_data.index)
        self.results['PML_transpiration'] = pd.Series(result['transpiration'], index=self.forcing_data.index)
        self.results['PML_evaporation'] = pd.Series(result['evaporation'], index=self.forcing_data.index)
        return self.results['PML']
    
    def run_pm_co2_aware(self):
        """Run CO2-aware PM"""
        pet = pm_co2_aware(
            temperature=self.forcing_data['temperature'].values,
            relative_humidity=self.forcing_data['relative_humidity'].values,
            wind_speed=self.forcing_data['wind_speed'].values,
            net_radiation=self.forcing_data['net_radiation'].values,
            co2=self.forcing_data['co2'].values,
            pressure=self.forcing_data['pressure'].values,
            soil_heat_flux=self.forcing_data['soil_heat_flux'].values,
        )
        self.results['PM-CO2'] = pd.Series(pet, index=self.forcing_data.index)
        return self.results['PM-CO2']
    
    def run_pm_co2_lai_aware(self):
        """Run CO2+LAI-aware PM"""
        if 'lai' not in self.forcing_data.columns:
            print("Warning: LAI not available, using default LAI=3.0")
            lai = np.ones(len(self.forcing_data)) * 3.0
        else:
            lai = self.forcing_data['lai'].values
        
        result = pm_co2_lai_aware(
            temperature=self.forcing_data['temperature'].values,
            relative_humidity=self.forcing_data['relative_humidity'].values,
            wind_speed=self.forcing_data['wind_speed'].values,
            net_radiation=self.forcing_data['net_radiation'].values,
            co2=self.forcing_data['co2'].values,
            lai=lai,
            pressure=self.forcing_data['pressure'].values,
            soil_heat_flux=self.forcing_data['soil_heat_flux'].values,
        )
        self.results['PM-CO2-LAI'] = pd.Series(result['total'], index=self.forcing_data.index)
        return self.results['PM-CO2-LAI']
    
    def run_complementary_models(self):
        """Run complementary relationship models"""
        # Bouchet
        result_bouchet = bouchet_complementary(
            temperature=self.forcing_data['temperature'].values,
            relative_humidity=self.forcing_data['relative_humidity'].values,
            net_radiation=self.forcing_data['net_radiation'].values,
            pressure=self.forcing_data['pressure'].values,
            soil_heat_flux=self.forcing_data['soil_heat_flux'].values,
        )
        self.results['CR-Bouchet'] = pd.Series(result_bouchet['potential'], index=self.forcing_data.index)
        
        # Advection-Aridity
        result_aa = advection_aridity_model(
            temperature=self.forcing_data['temperature'].values,
            relative_humidity=self.forcing_data['relative_humidity'].values,
            wind_speed=self.forcing_data['wind_speed'].values,
            net_radiation=self.forcing_data['net_radiation'].values,
            pressure=self.forcing_data['pressure'].values,
            soil_heat_flux=self.forcing_data['soil_heat_flux'].values,
        )
        self.results['CR-AA'] = pd.Series(result_aa['potential'], index=self.forcing_data.index)
        
        # Granger-Gray
        result_gg = granger_gray_model(
            temperature=self.forcing_data['temperature'].values,
            relative_humidity=self.forcing_data['relative_humidity'].values,
            net_radiation=self.forcing_data['net_radiation'].values,
            pressure=self.forcing_data['pressure'].values,
            soil_heat_flux=self.forcing_data['soil_heat_flux'].values,
        )
        self.results['CR-GG'] = pd.Series(result_gg, index=self.forcing_data.index)

        return self.results

    def run_jensen_haise(self):
        """
        Run Jensen-Haise temperature-based formula
        运行 Jensen-Haise 温度法公式

        Requires: temperature, and either (doy, latitude) or radiation
        需要：温度，以及 (日序, 纬度) 或 辐射
        """
        if 'doy' not in self.forcing_data.columns or 'latitude' not in self.forcing_data.columns:
            print("Warning: doy and/or latitude not available, skipping Jensen-Haise")
            print("警告：日序和/或纬度不可用，跳过 Jensen-Haise")
            return None

        pet = jensen_haise(
            temperature=self.forcing_data['temperature'].values,
            doy=self.forcing_data['doy'].values,
            latitude=self.forcing_data['latitude'].values,
        )
        self.results['Jensen-Haise'] = pd.Series(pet, index=self.forcing_data.index)
        return self.results['Jensen-Haise']

    def run_hargreaves(self):
        """
        Run Hargreaves temperature-based formula
        运行 Hargreaves 温度法公式

        Requires: temperature_mean, temperature_max, temperature_min, and (doy, latitude)
        需要：平均温度、最高温度、最低温度，以及 (日序, 纬度)
        """
        required = ['temperature_max', 'temperature_min', 'doy', 'latitude']
        missing = [col for col in required if col not in self.forcing_data.columns]
        if missing:
            print(f"Warning: {missing} not available, skipping Hargreaves")
            print(f"警告：{missing} 不可用，跳过 Hargreaves")
            return None

        pet = hargreaves(
            temperature_mean=self.forcing_data['temperature'].values,
            temperature_max=self.forcing_data['temperature_max'].values,
            temperature_min=self.forcing_data['temperature_min'].values,
            doy=self.forcing_data['doy'].values,
            latitude=self.forcing_data['latitude'].values,
        )
        self.results['Hargreaves'] = pd.Series(pet, index=self.forcing_data.index)
        return self.results['Hargreaves']

    def run_oudin(self):
        """
        Run Oudin temperature-based formula
        运行 Oudin 温度法公式

        Requires: temperature, and (doy, latitude)
        需要：温度，以及 (日序, 纬度)
        """
        if 'doy' not in self.forcing_data.columns or 'latitude' not in self.forcing_data.columns:
            print("Warning: doy and/or latitude not available, skipping Oudin")
            print("警告：日序和/或纬度不可用，跳过 Oudin")
            return None

        pet = oudin(
            temperature=self.forcing_data['temperature'].values,
            doy=self.forcing_data['doy'].values,
            latitude=self.forcing_data['latitude'].values,
        )
        self.results['Oudin'] = pd.Series(pet, index=self.forcing_data.index)
        return self.results['Oudin']

    def run_yang_roderick(self):
        """
        Run Yang-Roderick radiation-based formula
        运行 Yang-Roderick 辐射法公式

        Requires: temperature, net_radiation
        需要：温度、净辐射
        """
        pet = yang_roderick(
            temperature=self.forcing_data['temperature'].values,
            net_radiation=self.forcing_data['net_radiation'].values,
            soil_heat_flux=self.forcing_data['soil_heat_flux'].values,
            pressure=self.forcing_data['pressure'].values,
        )
        self.results['Yang-Roderick'] = pd.Series(pet, index=self.forcing_data.index)
        return self.results['Yang-Roderick']

    def run_penman_monteith_veg(self):
        """
        Run EP_Veg vegetation-aware Penman-Monteith (Liu et al. 2023)
        运行 EP_Veg 植被感知 Penman-Monteith (Liu et al. 2023)

        Requires: temperature, net_radiation, wind_speed, vpd (or RH), lai, co2
        需要：温度、净辐射、风速、vpd (或相对湿度)、叶面积指数、CO2
        """
        required = ['lai']
        missing = [col for col in required if col not in self.forcing_data.columns]
        if missing:
            print(f"Warning: {missing} not available, skipping EP_Veg")
            print(f"警告：{missing} 不可用，跳过 EP_Veg")
            return None

        # Calculate VPD if not directly available
        if 'vpd' in self.forcing_data.columns:
            vpd = self.forcing_data['vpd'].values
        else:
            from ..utils.constants import vapor_pressure_deficit
            vpd = vapor_pressure_deficit(
                temperature=self.forcing_data['temperature'].values,
                relative_humidity=self.forcing_data['relative_humidity'].values,
            )

        # Use default g1 and Aww estimation based on current conditions
        pet = penman_monteith_veg(
            temperature=self.forcing_data['temperature'].values,
            net_radiation=self.forcing_data['net_radiation'].values,
            wind_speed=self.forcing_data['wind_speed'].values,
            vpd=vpd,
            lai=self.forcing_data['lai'].values,
            co2_ppm=self.forcing_data['co2'].values,
            pressure=self.forcing_data['pressure'].values,
            # Auto-estimate g1 and Aww using defaults
            temperature_mean=self.forcing_data['temperature'].mean(),
            moisture_index=1.0,  # Assume moderate moisture
        )
        self.results['EP_Veg'] = pd.Series(pet, index=self.forcing_data.index)
        return self.results['EP_Veg']

    def run_penman_monteith_jarvis(self):
        """
        Run PM-Jarvis with multiplicative stomatal response (Wang et al. 2025)
        运行带乘法气孔响应的 PM-Jarvis (Wang et al. 2025)

        Requires: temperature, net_radiation, wind_speed, vpd, solar_radiation, co2
        需要：温度、净辐射、风速、vpd、太阳辐射、CO2
        """
        required = ['solar_radiation']
        missing = [col for col in required if col not in self.forcing_data.columns]
        if missing:
            print(f"Warning: {missing} not available, skipping PM-Jarvis")
            print(f"警告：{missing} 不可用，跳过 PM-Jarvis")
            return None

        # Calculate VPD if not directly available
        if 'vpd' in self.forcing_data.columns:
            vpd = self.forcing_data['vpd'].values
        else:
            from ..utils.constants import vapor_pressure_deficit
            vpd = vapor_pressure_deficit(
                temperature=self.forcing_data['temperature'].values,
                relative_humidity=self.forcing_data['relative_humidity'].values,
            )

        # Use LAI if available, otherwise use default crop height
        lai = self.forcing_data['lai'].values if 'lai' in self.forcing_data.columns else None

        pet = penman_monteith_jarvis(
            temperature=self.forcing_data['temperature'].values,
            net_radiation=self.forcing_data['net_radiation'].values,
            wind_speed=self.forcing_data['wind_speed'].values,
            vpd=vpd,
            solar_radiation=self.forcing_data['solar_radiation'].values,
            co2_ppm=self.forcing_data['co2'].values,
            lai=lai,
            pressure=self.forcing_data['pressure'].values,
        )
        self.results['PM-Jarvis'] = pd.Series(pet, index=self.forcing_data.index)
        return self.results['PM-Jarvis']

    def run_all(self):
        """
        Run all available PET formulas
        运行所有可用的 PET 公式
        """
        print("Running all PET formulas...")
        print("运行所有 PET 公式...")

        # Classic methods / 经典方法
        print("  - Penman-Monteith (FAO-56)")
        self.run_penman_monteith()

        print("  - Priestley-Taylor")
        self.run_priestley_taylor()

        print("  - Priestley-Taylor JPL")
        self.run_priestley_taylor_jpl()

        print("  - Penman-Monteith-Leuning (PML)")
        self.run_penman_monteith_leuning()

        # CO2-aware methods / CO2感知方法
        print("  - PM with CO2 awareness")
        self.run_pm_co2_aware()

        print("  - PM with CO2+LAI awareness")
        self.run_pm_co2_lai_aware()

        # Complementary relationship models / 互补关系模型
        print("  - Complementary Relationship models")
        self.run_complementary_models()

        # Temperature-based methods / 基于温度的方法
        print("  - Jensen-Haise (temperature-based)")
        self.run_jensen_haise()

        print("  - Hargreaves (temperature-based)")
        self.run_hargreaves()

        print("  - Oudin (temperature-based)")
        self.run_oudin()

        # Radiation-based methods / 基于辐射的方法
        print("  - Yang-Roderick (radiation-based)")
        self.run_yang_roderick()

        # Vegetation-aware methods / 植被感知方法
        print("  - EP_Veg (Liu et al. 2023)")
        self.run_penman_monteith_veg()

        print("  - PM-Jarvis (Wang et al. 2025)")
        self.run_penman_monteith_jarvis()

        print(f"Completed! Computed {len(self.results)} PET estimates.")
        print(f"完成！计算了 {len(self.results)} 个 PET 估算值。")
        return self.results
    
    def get_results_dataframe(self):
        """
        Get all results as a DataFrame
        
        Returns:
        --------
        pd.DataFrame : DataFrame with all PET estimates
        """
        return pd.DataFrame(self.results)
    
    def compute_statistics(self):
        """
        Compute basic statistics across all formulas
        
        Returns:
        --------
        pd.DataFrame : Statistics for each formula
        """
        df = self.get_results_dataframe()
        stats = df.describe()
        
        # Add coefficient of variation
        stats.loc['cv'] = df.std() / df.mean()
        
        return stats
    
    def compute_pairwise_differences(self):
        """
        Compute pairwise differences between formulas
        
        Returns:
        --------
        pd.DataFrame : Mean absolute differences between formulas
        """
        df = self.get_results_dataframe()
        formulas = df.columns
        
        differences = pd.DataFrame(index=formulas, columns=formulas)
        
        for i, formula1 in enumerate(formulas):
            for j, formula2 in enumerate(formulas):
                if i <= j:
                    diff = (df[formula1] - df[formula2]).abs().mean()
                    differences.loc[formula1, formula2] = diff
                    differences.loc[formula2, formula1] = diff
        
        return differences.astype(float)
    
    def compute_correlations(self):
        """
        Compute correlations between formulas
        
        Returns:
        --------
        pd.DataFrame : Correlation matrix
        """
        df = self.get_results_dataframe()
        return df.corr()
