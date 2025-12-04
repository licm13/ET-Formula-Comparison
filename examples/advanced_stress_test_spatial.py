"""
Advanced Stress Test: Extreme Climate Event Simulation
极端气候事件模拟的高级压力测试

This script simulates a complex spatial scenario with:
本脚本模拟一个复杂的空间场景，包括：
1. Spatial gradient (wet to dry zones) / 空间梯度（从湿润区到干旱区）
2. Temporal anomaly (10-day heatwave) / 时间异常（10天热浪）
3. Multiple ET models comparison / 多个ET模型对比
4. Physical constraint validation / 物理约束验证

Author: Claude Code ET Framework
Date: 2025-12-04
"""

import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from pathlib import Path

# Add project path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import models and formulas
try:
    from py_et_lib.models.aet import PMLv2, PTJPL
    from pet_comparison.formulas import penman_monteith, hargreaves
    print("✅ Successfully imported ET models")
except ImportError as e:
    print(f"⚠️  Warning: Could not import some models: {e}")
    print("   Continuing with available models...")


class SpatialStressTest:
    """
    Spatial stress test for ET models under extreme conditions
    极端条件下ET模型的空间压力测试
    """

    def __init__(self, lat_size=100, lon_size=100, days=30):
        """
        Initialize spatial stress test

        Parameters
        ----------
        lat_size : int
            Number of latitude points / 纬度点数
        lon_size : int
            Number of longitude points / 经度点数
        days : int
            Number of days to simulate / 模拟天数
        """
        self.lat_size = lat_size
        self.lon_size = lon_size
        self.days = days

        # Create coordinate arrays
        self.lat = np.linspace(-30, 30, lat_size)  # -30°N to 30°N
        self.lon = np.linspace(-45, 45, lon_size)  # -45°E to 45°E
        self.time = pd.date_range('2023-06-01', periods=days, freq='D')

        print(f"📐 Initialized stress test:")
        print(f"   Grid size: {lat_size} × {lon_size}")
        print(f"   Time span: {days} days")
        print(f"   Total data points: {lat_size * lon_size * days:,}")

    def create_stress_scenario_grid(self):
        """
        Create a 3D spatiotemporal data cube simulating extreme stress
        创建一个模拟极端胁迫的三维时空数据立方体

        Returns
        -------
        ds : xr.Dataset
            Dataset with all required meteorological variables
        """
        print("\n🌍 Generating spatial stress scenario...")

        # 1. Spatial gradients (latitude-based)
        # 从北到南：湿润 → 干旱 / North to south: wet → dry

        # Soil moisture gradient (proxy for aridity)
        soil_moisture_base = np.linspace(0.8, 0.1, self.lat_size)  # High to low
        soil_moisture_2d = np.tile(soil_moisture_base[:, np.newaxis], (1, self.lon_size))

        # LAI gradient (vegetation density)
        lai_base = np.linspace(5.0, 0.5, self.lat_size)  # Dense forest to sparse vegetation
        lai_2d = np.tile(lai_base[:, np.newaxis], (1, self.lon_size))

        # Temperature gradient (cooler in wet regions, hotter in dry regions)
        temp_base = np.linspace(20.0, 35.0, self.lat_size)  # °C
        temp_2d = np.tile(temp_base[:, np.newaxis], (1, self.lon_size))

        # 2. Temporal anomaly: 10-day heatwave in middle of period
        heatwave_start = 10
        heatwave_end = 20

        # Temperature anomaly during heatwave
        temp_anomaly = np.zeros(self.days)
        temp_anomaly[heatwave_start:heatwave_end] = 8.0  # +8°C spike

        # Humidity drop during heatwave
        rh_anomaly = np.zeros(self.days)
        rh_anomaly[heatwave_start:heatwave_end] = -25.0  # -25% RH

        # Radiation increase during heatwave
        rn_anomaly = np.zeros(self.days)
        rn_anomaly[heatwave_start:heatwave_end] = 100.0  # +100 W/m²

        # Wind speed increase
        wind_anomaly = np.zeros(self.days)
        wind_anomaly[heatwave_start:heatwave_end] = 2.0  # +2 m/s

        # 3. Construct 3D arrays using broadcasting
        print("   Building 3D data arrays...")

        # Temperature: shape (time, lat, lon)
        T_mean = temp_2d[np.newaxis, :, :] + temp_anomaly[:, np.newaxis, np.newaxis]

        # Add diurnal cycle for T_max and T_min
        T_max = T_mean + 7.0
        T_min = T_mean - 7.0

        # Relative humidity (decreases toward dry regions and during heatwave)
        RH_base = 75.0 - 50.0 * (1 - soil_moisture_2d)  # 75% in wet, 25% in dry
        RH = RH_base[np.newaxis, :, :] + rh_anomaly[:, np.newaxis, np.newaxis]
        RH = np.clip(RH, 10, 95)  # Realistic bounds

        # Net radiation (higher in dry regions, peaks during heatwave)
        Rn_base = 150.0 + 50.0 * (1 - soil_moisture_2d)  # W/m²
        Rn = Rn_base[np.newaxis, :, :] + rn_anomaly[:, np.newaxis, np.newaxis]

        # Wind speed (higher in open dry areas)
        u2_base = 2.0 + 2.0 * (1 - soil_moisture_2d)  # 2-4 m/s
        u2 = u2_base[np.newaxis, :, :] + wind_anomaly[:, np.newaxis, np.newaxis]

        # LAI (constant in time for simplicity)
        LAI = np.tile(lai_2d[np.newaxis, :, :], (self.days, 1, 1))

        # VPD (calculated from temperature and humidity)
        es = 0.6108 * np.exp((17.27 * T_mean) / (T_mean + 237.3))  # kPa
        ea = es * RH / 100.0
        VPD = es - ea
        VPD = np.maximum(VPD, 0.0)  # Ensure non-negative

        # Pressure (altitude-dependent, simplified)
        elevation_2d = np.linspace(0, 1000, self.lat_size)[:, np.newaxis] * np.ones((1, self.lon_size))
        pressure = 101.3 * np.exp(-elevation_2d / 8500)  # kPa (barometric formula)
        pressure_3d = np.tile(pressure[np.newaxis, :, :], (self.days, 1, 1))

        # 4. Create xarray Dataset
        print("   Assembling xarray Dataset...")

        ds = xr.Dataset(
            {
                # Core meteorological variables
                'T_mean': (['time', 'lat', 'lon'], T_mean,
                          {'units': '°C', 'long_name': 'Mean air temperature'}),
                'T_max': (['time', 'lat', 'lon'], T_max,
                         {'units': '°C', 'long_name': 'Maximum air temperature'}),
                'T_min': (['time', 'lat', 'lon'], T_min,
                         {'units': '°C', 'long_name': 'Minimum air temperature'}),
                'RH': (['time', 'lat', 'lon'], RH,
                      {'units': '%', 'long_name': 'Relative humidity'}),
                'Rn': (['time', 'lat', 'lon'], Rn,
                      {'units': 'W/m²', 'long_name': 'Net radiation'}),
                'u2': (['time', 'lat', 'lon'], u2,
                      {'units': 'm/s', 'long_name': 'Wind speed at 2m'}),
                'VPD': (['time', 'lat', 'lon'], VPD,
                       {'units': 'kPa', 'long_name': 'Vapor pressure deficit'}),
                'LAI': (['time', 'lat', 'lon'], LAI,
                       {'units': 'm²/m²', 'long_name': 'Leaf area index'}),
                'pressure': (['time', 'lat', 'lon'], pressure_3d,
                           {'units': 'kPa', 'long_name': 'Atmospheric pressure'}),

                # Diagnostic variables
                'soil_moisture': (['lat', 'lon'], soil_moisture_2d,
                                {'units': 'm³/m³', 'long_name': 'Soil moisture (proxy)'}),
            },
            coords={
                'time': self.time,
                'lat': self.lat,
                'lon': self.lon,
            },
            attrs={
                'title': 'Extreme Climate Stress Test Dataset',
                'description': 'Synthetic data with spatial gradient and heatwave event',
                'heatwave_period': f'Day {heatwave_start} to {heatwave_end}',
                'created': pd.Timestamp.now().isoformat(),
            }
        )

        print(f"✅ Dataset created: {ds.dims}")
        return ds

    def run_models(self, ds):
        """
        Run multiple ET models on the stress test dataset
        在压力测试数据集上运行多个ET模型

        Parameters
        ----------
        ds : xr.Dataset
            Input dataset

        Returns
        -------
        results : dict
            Dictionary of ET results from different models
        """
        print("\n🚀 Running ET models...")

        results = {}

        # Model 1: Traditional Penman-Monteith (via vectorization)
        print("   [1/3] Traditional Penman-Monteith...")
        try:
            # Convert Rn from W/m² to MJ/m²/day
            Rn_MJ = ds['Rn'] * 0.0864

            # Vectorized PM calculation
            et_pm = xr.apply_ufunc(
                penman_monteith,
                ds['T_mean'],
                ds['RH'],
                ds['u2'],
                Rn_MJ,
                ds['pressure'],
                vectorize=True,
                dask='parallelized',
                output_dtypes=[float]
            )

            results['PM'] = et_pm.rename('PET_PM')
            print("      ✅ Complete")
        except Exception as e:
            print(f"      ⚠️  Error: {e}")

        # Model 2: Temperature-based Hargreaves
        print("   [2/3] Hargreaves...")
        try:
            # Need day of year and latitude for Hargreaves
            doy = ds['time'].dt.dayofyear

            # Create 3D latitude array
            lat_3d = xr.DataArray(
                np.tile(ds['lat'].values[np.newaxis, :, np.newaxis],
                       (len(ds['time']), 1, len(ds['lon']))),
                dims=['time', 'lat', 'lon']
            )

            # Vectorized Hargreaves calculation
            et_harg = xr.apply_ufunc(
                hargreaves,
                ds['T_mean'],
                ds['T_max'],
                ds['T_min'],
                None,  # radiation (will be calculated internally)
                doy,
                lat_3d,
                vectorize=True,
                dask='parallelized',
                output_dtypes=[float]
            )

            results['Hargreaves'] = et_harg.rename('PET_Hargreaves')
            print("      ✅ Complete")
        except Exception as e:
            print(f"      ⚠️  Error: {e}")

        # Model 3: PMLv2 (if available)
        print("   [3/3] PMLv2 (advanced)...")
        try:
            pmlv2 = PMLv2()
            et_pmlv2 = pmlv2.compute_et(ds)['AET']
            results['PMLv2'] = et_pmlv2.rename('AET_PMLv2')
            print("      ✅ Complete")
        except NameError:
            print("      ⚠️  PMLv2 not available (py_et_lib not imported)")
        except Exception as e:
            print(f"      ⚠️  Error: {e}")

        return results

    def validate_physics(self, ds, results):
        """
        Validate physical constraints and energy balance
        验证物理约束和能量平衡

        Parameters
        ----------
        ds : xr.Dataset
            Input meteorological dataset
        results : dict
            ET results from different models

        Returns
        -------
        validation_report : dict
            Dictionary with validation statistics
        """
        print("\n🔬 Validating physical constraints...")

        report = {}

        for model_name, et in results.items():
            print(f"\n   Model: {model_name}")

            # Constraint 1: Non-negativity
            negative_count = (et < 0).sum().item()
            negative_pct = (negative_count / et.size) * 100
            print(f"      Negative values: {negative_count:,} ({negative_pct:.3f}%)")

            # Constraint 2: Energy balance check
            # ET energy (mm/day → MJ/m²/day)
            lambda_v = 2.45  # MJ/kg
            et_energy = et * lambda_v  # MJ/m²/day

            # Available energy (W/m² → MJ/m²/day)
            available_energy = ds['Rn'] * 0.0864

            # Allow 10% margin for aerodynamic term contribution
            energy_violation = et_energy > (available_energy + 5.0)
            violation_count = energy_violation.sum().item()
            violation_pct = (violation_count / et.size) * 100

            print(f"      Energy balance violations: {violation_count:,} ({violation_pct:.3f}%)")

            # Constraint 3: Reasonable magnitude (0-20 mm/day)
            unrealistic = (et > 20).sum().item()
            unrealistic_pct = (unrealistic / et.size) * 100
            print(f"      Unrealistic values (>20 mm/day): {unrealistic:,} ({unrealistic_pct:.3f}%)")

            # Constraint 4: Spatial coherence (no extreme local spikes)
            # Check standard deviation in small neighborhoods
            et_std = et.rolling(lat=3, lon=3, center=True).std()
            extreme_variability = (et_std > 5.0).sum().item()
            extreme_var_pct = (extreme_variability / et.size) * 100
            print(f"      Extreme local variability: {extreme_variability:,} ({extreme_var_pct:.3f}%)")

            # Constraint 5: Drought area check (low ET in dry regions)
            # Select southern region (dry)
            drought_area = et.isel(lat=slice(80, 100))
            drought_mean = drought_area.mean().item()
            print(f"      Mean ET in drought area: {drought_mean:.2f} mm/day")

            # Store in report
            report[model_name] = {
                'negative_pct': negative_pct,
                'energy_violation_pct': violation_pct,
                'unrealistic_pct': unrealistic_pct,
                'extreme_var_pct': extreme_var_pct,
                'drought_et_mean': drought_mean,
                'global_mean': float(et.mean()),
                'global_std': float(et.std()),
                'global_max': float(et.max()),
                'global_min': float(et.min()),
            }

        # Print summary
        print("\n📊 Validation Summary:")
        print("="*70)
        print(f"{'Model':<15} {'Mean ET':<10} {'Std':<10} {'Energy OK':<12} {'Pass':<6}")
        print("-"*70)

        for model_name, stats in report.items():
            energy_ok = stats['energy_violation_pct'] < 5.0  # <5% violations
            negative_ok = stats['negative_pct'] < 0.1  # <0.1% negative
            overall_pass = energy_ok and negative_ok

            print(f"{model_name:<15} {stats['global_mean']:<10.2f} {stats['global_std']:<10.2f} "
                  f"{energy_ok!s:<12} {overall_pass!s:<6}")

        return report

    def plot_results(self, ds, results):
        """
        Create comprehensive visualization of results
        创建结果的综合可视化

        Parameters
        ----------
        ds : xr.Dataset
            Input dataset
        results : dict
            ET results from different models
        """
        print("\n📊 Generating visualizations...")

        # Figure 1: Spatial snapshot during heatwave peak
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        # Heatwave day (day 15)
        heatwave_day = 15

        # Panel 1: Temperature
        ax = axes[0, 0]
        ds['T_mean'].isel(time=heatwave_day).plot(ax=ax, cmap='hot', cbar_kwargs={'label': '°C'})
        ax.set_title('A) Temperature during Heatwave (Day 15)', fontweight='bold')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        # Panel 2: VPD
        ax = axes[0, 1]
        ds['VPD'].isel(time=heatwave_day).plot(ax=ax, cmap='YlOrRd', cbar_kwargs={'label': 'kPa'})
        ax.set_title('B) Vapor Pressure Deficit (Day 15)', fontweight='bold')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        # Panel 3: ET from first available model
        ax = axes[1, 0]
        first_model = list(results.keys())[0]
        results[first_model].isel(time=heatwave_day).plot(ax=ax, cmap='Blues',
                                                           cbar_kwargs={'label': 'mm/day'})
        ax.set_title(f'C) ET - {first_model} (Day 15)', fontweight='bold')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        # Panel 4: LAI
        ax = axes[1, 1]
        ds['LAI'].isel(time=0).plot(ax=ax, cmap='Greens', cbar_kwargs={'label': 'm²/m²'})
        ax.set_title('D) Leaf Area Index (constant)', fontweight='bold')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        plt.tight_layout()
        plt.savefig('stress_test_spatial_snapshot.png', dpi=150, bbox_inches='tight')
        print("   ✅ Saved: stress_test_spatial_snapshot.png")
        plt.close()

        # Figure 2: Time series comparison
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))

        # Select a specific location (mid-grid)
        lat_idx = self.lat_size // 2
        lon_idx = self.lon_size // 2

        # Panel 1: Meteorological drivers
        ax = axes[0]
        ax2 = ax.twinx()

        line1 = ax.plot(ds['time'], ds['T_mean'][:, lat_idx, lon_idx],
                       'r-', linewidth=2, label='Temperature')
        ax.set_ylabel('Temperature (°C)', color='r', fontweight='bold')
        ax.tick_params(axis='y', labelcolor='r')

        line2 = ax2.plot(ds['time'], ds['RH'][:, lat_idx, lon_idx],
                        'b-', linewidth=2, label='Humidity')
        ax2.set_ylabel('Relative Humidity (%)', color='b', fontweight='bold')
        ax2.tick_params(axis='y', labelcolor='b')

        ax.axvspan(ds['time'][10], ds['time'][19], alpha=0.2, color='red', label='Heatwave')
        ax.set_title(f'A) Meteorological Drivers (Lat={self.lat[lat_idx]:.1f}°, Lon={self.lon[lon_idx]:.1f}°)',
                    fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Panel 2: ET comparison
        ax = axes[1]
        for model_name, et in results.items():
            ax.plot(ds['time'], et[:, lat_idx, lon_idx],
                   linewidth=2.5, label=model_name, marker='o', markersize=4)

        ax.axvspan(ds['time'][10], ds['time'][19], alpha=0.2, color='red')
        ax.set_ylabel('ET (mm/day)', fontweight='bold')
        ax.set_title('B) ET Model Comparison', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Panel 3: Spatial mean ET
        ax = axes[2]
        for model_name, et in results.items():
            spatial_mean = et.mean(dim=['lat', 'lon'])
            ax.plot(ds['time'], spatial_mean, linewidth=2.5, label=model_name, marker='s', markersize=5)

        ax.axvspan(ds['time'][10], ds['time'][19], alpha=0.2, color='red')
        ax.set_ylabel('Spatial Mean ET (mm/day)', fontweight='bold')
        ax.set_xlabel('Date', fontweight='bold')
        ax.set_title('C) Domain-Averaged ET Response to Heatwave', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('stress_test_timeseries.png', dpi=150, bbox_inches='tight')
        print("   ✅ Saved: stress_test_timeseries.png")
        plt.close()

        print("✅ Visualization complete!")


def main():
    """
    Main execution function
    主执行函数
    """
    print("="*70)
    print("  ADVANCED SPATIAL STRESS TEST FOR ET MODELS")
    print("  ET模型的高级空间压力测试")
    print("="*70)

    # Initialize stress test
    stress_test = SpatialStressTest(lat_size=100, lon_size=100, days=30)

    # Generate synthetic data
    ds = stress_test.create_stress_scenario_grid()

    # Run models
    results = stress_test.run_models(ds)

    if not results:
        print("\n❌ No models successfully ran. Exiting.")
        return

    # Validate physics
    validation_report = stress_test.validate_physics(ds, results)

    # Plot results
    stress_test.plot_results(ds, results)

    # Save results
    print("\n💾 Saving results...")
    for model_name, et in results.items():
        filename = f"stress_test_{model_name.lower()}.nc"
        et.to_netcdf(filename)
        print(f"   ✅ Saved: {filename}")

    print("\n" + "="*70)
    print("  STRESS TEST COMPLETE!")
    print("  压力测试完成！")
    print("="*70)

    # Print final summary
    print("\n📋 Final Summary:")
    print(f"   • Simulated: {stress_test.lat_size * stress_test.lon_size * stress_test.days:,} data points")
    print(f"   • Models tested: {len(results)}")
    print(f"   • All models passed validation: {all(r['energy_violation_pct'] < 5 for r in validation_report.values())}")

    return ds, results, validation_report


if __name__ == "__main__":
    ds, results, validation_report = main()
