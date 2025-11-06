# PET Formula Comparison: An Integrated Scientific Framework

**潜在蒸散发公式对比：整合科学框架**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A comprehensive, production-ready framework for comparing Potential Evapotranspiration (PET) formulas, integrating methods from six landmark scientific papers into a unified library.

一个全面的、可用于生产的潜在蒸散发(PET)公式对比框架，将六篇标志性科学论文的方法整合到统一的库中。

---

## 🎯 Project Overview / 项目概述

This framework unifies **20+ PET formulas** spanning classic methods, temperature-based approaches, radiation-based models, and advanced vegetation/CO2-aware algorithms. It is designed for:

本框架统一了 **20+ PET 公式**，涵盖经典方法、基于温度的方法、基于辐射的模型以及高级植被/CO2感知算法。设计用于：

- **Systematic formula comparison** under identical forcing conditions / 相同强迫条件下的系统公式对比
- **Climate change impact assessment** with CO2 sensitivity / 具有CO2敏感性的气候变化影响评估
- **Vegetation-atmosphere interaction studies** / 植被-大气相互作用研究
- **High-impact publication** targeting Nature Water, Nature Climate Change, WRR, etc. / 针对Nature Water、Nature Climate Change、WRR等的高影响力发表

---

## 📚 Integrated Scientific Papers / 整合的科学论文

This framework consolidates methodologies from:

本框架整合了以下方法：

### 1. **Liu et al. (2023)** - *Journal of Hydrology*
**"A physically-based potential evapotranspiration model for global water availability projections"**

- **EP_Veg**: Vegetation-aware PM with Medlyn stomatal conductance / 植被感知PM与Medlyn气孔导度
- **Budyko framework**: Runoff estimation / Budyko框架：径流估算
- **g1 parameter**: Climate-dependent optimal conductance / 气候依赖的最优导度

### 2. **Pimentel et al. (2023)** - *Water Resources Research*
**"Which Potential Evapotranspiration Formula to Use in Hydrological Modeling World-Wide?"**

- **Jensen-Haise**: Minimal-data temperature method / 最少数据的温度法
- **Hargreaves**: Temperature range-based approach / 基于温度范围的方法
- **Multi-process evaluation**: PET, AET, Runoff comparison / 多过程评估

### 3. **Yang et al. (2019)** - *Nature Climate Change*
**"Hydrologic implications of vegetation response to elevated CO2 in climate projections"**

- **PM-CO2**: Linear CO2-stomatal resistance relationship / 线性CO2-气孔阻力关系
- **Attribution analysis**: Component-wise sensitivity / 逐分量敏感性分析
- **Budyko runoff**: CO2 impact on water balance / CO2对水平衡的影响

### 4. **Xiong & Yang (2025)** - *Scientific Data*
**"PDSI_CMIP6: an ensemble CMIP6-projected self-calibrated palmer drought severity index dataset"**

- **Oudin**: Temperature-radiation PET / 温度-辐射PET
- **Yang-Roderick**: Alternative radiation-based formula / 替代基于辐射的公式
- **PDSI framework**: Drought index calculation / PDSI框架：干旱指数计算

### 5. **Wang et al. (2025)** - *Current Climate Change Reports*
**"Three Paradoxes Related to Potential Evapotranspiration in a Warming Climate"**

- **PM-RC-Jarvis**: Multiplicative stomatal response / 乘法气孔响应
- **Aridity Index**: P/PET temporal trends / P/PET时间趋势
- **Paradox analysis**: Formula disagreement in climate change / 气候变化中的公式分歧

### 6. **Yin & Porporato (2023)** - *Geophysical Research Letters*
**"Global distribution of climatic aridity"**

- **Dryness Index**: PET/P theoretical distributions / PET/P理论分布
- **Power-law tails**: Aridity distribution analysis / 幂律尾：干旱分布分析

---

## 🧪 Implemented PET Formulas / 实现的PET公式

### Classic Methods / 经典方法

| Formula | Abbreviation | Data Requirements | Key Reference |
|---------|--------------|-------------------|---------------|
| Penman-Monteith | PM | T, RH, WS, Rn | Allen et al. (1998) FAO-56 |
| Priestley-Taylor | PT | T, Rn | Priestley & Taylor (1972) |
| PT-JPL | PT-JPL | T, Rn, LAI, SM | Fisher et al. (2008) |
| PML (Leuning) | PML | T, RH, WS, Rn, LAI | Zhang et al. (2016) |

### Temperature-Based Methods / 基于温度的方法

| Formula | Abbreviation | Data Requirements | Key Reference |
|---------|--------------|-------------------|---------------|
| Jensen-Haise | JH | T, DOY, Lat | Pimentel et al. (2023) |
| Hargreaves | HG | T_mean, T_max, T_min, DOY, Lat | Hargreaves & Samani (1985) |
| Oudin | Oudin | T, Ra | Xiong & Yang (2025) |

### Radiation-Based Methods / 基于辐射的方法

| Formula | Abbreviation | Data Requirements | Key Reference |
|---------|--------------|-------------------|---------------|
| Yang-Roderick | YR | T, Rn | Yang & Roderick (2019) |

### CO2-Aware Methods / CO2感知方法

| Formula | Abbreviation | Data Requirements | Key Reference |
|---------|--------------|-------------------|---------------|
| PM-CO2 | PM-CO2 | T, RH, WS, Rn, CO2 | Yang et al. (2019) |
| PM-CO2-LAI | PM-CO2-LAI | T, RH, WS, Rn, CO2, LAI | Central library |

### Vegetation-Aware Methods / 植被感知方法

| Formula | Abbreviation | Data Requirements | Key Reference |
|---------|--------------|-------------------|---------------|
| EP_Veg (Liu) | EP_Veg | T, Rn, WS, VPD, LAI, CO2 | Liu et al. (2023) |
| PM-Jarvis (Wang) | PM-Jarvis | T, Rn, WS, VPD, Sg, CO2 | Wang et al. (2025) |

### Complementary Relationship / 互补关系

| Formula | Abbreviation | Data Requirements | Key Reference |
|---------|--------------|-------------------|---------------|
| Bouchet | CR-Bouchet | T, RH, Rn | Bouchet (1963) |
| Advection-Aridity | CR-AA | T, RH, WS, Rn | Brutsaert & Stricker (1979) |
| Granger-Gray | CR-GG | T, RH, Rn | Granger & Gray (1989) |

**Legend / 图例:**
- T: Temperature / 温度
- RH: Relative Humidity / 相对湿度
- WS: Wind Speed / 风速
- Rn: Net Radiation / 净辐射
- LAI: Leaf Area Index / 叶面积指数
- VPD: Vapor Pressure Deficit / 水汽压差
- Sg: Solar radiation / 太阳辐射
- CO2: CO2 concentration / CO2浓度
- DOY: Day of Year / 日序
- Lat: Latitude / 纬度
- Ra: Extraterrestrial radiation / 天文辐射
- SM: Soil Moisture / 土壤湿度

---

## 🚀 Installation / 安装

### Prerequisites / 先决条件

- Python 3.8 or higher / Python 3.8或更高版本
- NumPy, Pandas, Matplotlib

### Install from GitHub / 从GitHub安装

```bash
# Clone the repository / 克隆仓库
git clone https://github.com/licm13/PET-Formula-Comparison.git
cd PET-Formula-Comparison

# Install dependencies / 安装依赖
pip install -r requirements.txt

# Install in development mode / 以开发模式安装
pip install -e .
```

---

## 💡 Quick Start / 快速开始

### Example 1: Basic Formula Comparison / 基本公式对比

```python
import pandas as pd
import numpy as np
from pet_comparison.analysis import PETComparison

# Prepare forcing data / 准备强迫数据
dates = pd.date_range('2020-01-01', periods=365, freq='D')
forcing_data = pd.DataFrame({
    'temperature': 20 + 10 * np.sin(2 * np.pi * np.arange(365) / 365),
    'relative_humidity': 60 + 10 * np.cos(2 * np.pi * np.arange(365) / 365),
    'wind_speed': 2.5 + 0.5 * np.random.randn(365),
    'net_radiation': 15 + 5 * np.sin(2 * np.pi * np.arange(365) / 365),
    'lai': 3.0 + 1.0 * np.sin(2 * np.pi * np.arange(365) / 365),
    'co2': 400.0,  # ppm
    'doy': np.arange(1, 366),
    'latitude': 45.0,
}, index=dates)

# Initialize comparison framework / 初始化对比框架
comparison = PETComparison(forcing_data)

# Run all formulas / 运行所有公式
results = comparison.run_all()

# Get results as DataFrame / 获取结果为DataFrame
results_df = comparison.get_results_dataframe()
print(results_df.head())

# Compute statistics / 计算统计
stats = comparison.compute_statistics()
print("\nStatistics across all formulas:")
print(stats)

# Compute correlations / 计算相关性
correlations = comparison.compute_correlations()
print("\nFormula correlations:")
print(correlations)
```

### Example 2: CO2 Sensitivity Analysis / CO2敏感性分析

```python
from pet_comparison.formulas import pm_co2_aware, penman_monteith_veg

# Test different CO2 levels / 测试不同CO2水平
co2_levels = [280, 380, 550, 900]  # ppm

for co2 in co2_levels:
    pet_co2 = pm_co2_aware(
        temperature=20.0,
        relative_humidity=60.0,
        wind_speed=2.5,
        net_radiation=15.0,
        co2=co2
    )

    pet_veg = penman_monteith_veg(
        temperature=20.0,
        net_radiation=15.0,
        wind_speed=2.5,
        vpd=1.5,
        lai=3.0,
        co2_ppm=co2,
        temperature_mean=18.0,
        moisture_index=1.0
    )

    print(f"CO2 = {co2:4d} ppm: PM-CO2 = {pet_co2:.2f}, EP_Veg = {pet_veg:.2f} mm/day")
```

### Example 3: Vegetation Response / 植被响应

```python
from pet_comparison.formulas import penman_monteith_veg, estimate_g1, estimate_Aww

# Estimate climate-dependent parameters / 估算气候依赖参数
temperature_mean = 15.0  # Mean temperature above 0°C / 0°C以上的平均温度
moisture_index = 1.2     # P/PET ratio / P/PET比率

g1 = estimate_g1(temperature_mean, moisture_index)
Aww = estimate_Aww(co2_ppm=400.0, species="tree")

print(f"Estimated g1 = {g1:.3f} kPa^0.5")
print(f"Estimated Aww = {Aww:.2f} μmol m⁻² s⁻¹")

# Run EP_Veg with estimated parameters / 使用估算参数运行EP_Veg
pet = penman_monteith_veg(
    temperature=20.0,
    net_radiation=15.0,
    wind_speed=2.5,
    vpd=1.5,
    lai=3.0,
    co2_ppm=400.0,
    g1=g1,
    Aww=Aww,
    pressure=101.3
)

print(f"EP_Veg PET = {pet:.2f} mm/day")
```

---

## 📊 Framework Features / 框架特性

### 1. Unified Comparison Framework / 统一对比框架

- **Identical forcing**: All formulas use the same input data / 所有公式使用相同输入数据
- **Automatic handling**: Missing data handled gracefully / 优雅处理缺失数据
- **Statistical analysis**: Built-in statistics and correlations / 内置统计和相关性分析
- **Bilingual support**: English/Chinese documentation / 英文/中文文档

### 2. Scientific Rigor / 科学严谨性

- **Peer-reviewed sources**: All formulas from published papers / 所有公式来自已发表论文
- **Physically-based**: Clear parameter interpretations / 清晰的参数解释
- **Validated**: Cross-checked against original implementations / 与原始实现交叉验证
- **Documented**: Comprehensive docstrings and references / 全面的文档字符串和参考文献

### 3. Flexibility / 灵活性

- **Modular design**: Use individual formulas or full framework / 使用单个公式或完整框架
- **Extensible**: Easy to add new formulas / 易于添加新公式
- **Optional dependencies**: Only require what you use / 只需要您使用的内容
- **Multiple scales**: Daily to monthly timesteps / 从日到月的时间步长

### 4. Analysis Tools / 分析工具

- **Visualization**: Time series, box plots, correlation matrices / 时间序列、箱线图、相关矩阵
- **Statistics**: Mean, std, CV, pairwise differences / 均值、标准差、变异系数、成对差异
- **Sensitivity**: CO2, LAI, temperature, moisture / CO2、LAI、温度、湿度
- **Partitioning**: Transpiration vs. evaporation / 蒸腾vs.蒸发

---

## 📖 Documentation / 文档

### Input Data Requirements / 输入数据要求

**Minimum Required / 最低要求:**
- `temperature`: Air temperature (°C) / 气温
- `relative_humidity`: Relative humidity (%) / 相对湿度
- `wind_speed`: Wind speed at 2m (m s⁻¹) / 风速
- `net_radiation`: Net radiation (MJ m⁻² day⁻¹) / 净辐射

**Optional (Enables Advanced Formulas) / 可选（启用高级公式）:**
- `lai`: Leaf Area Index (m² m⁻²) / 叶面积指数
- `co2`: CO2 concentration (ppm) / CO2浓度
- `vpd`: Vapor pressure deficit (kPa) / 水汽压差
- `solar_radiation`: Solar radiation (W m⁻²) / 太阳辐射
- `doy`: Day of year (1-365) / 日序
- `latitude`: Latitude (degrees) / 纬度
- `temperature_max`: Maximum temperature (°C) / 最高温度
- `temperature_min`: Minimum temperature (°C) / 最低温度
- `soil_moisture`: Soil moisture (0-1) / 土壤湿度
- `pressure`: Atmospheric pressure (kPa) / 大气压力

### Formula Selection Guide / 公式选择指南

| Research Goal / 研究目标 | Recommended Formula / 推荐公式 | Rationale / 理由 |
|--------------------------|--------------------------------|------------------|
| FAO standard reference ET | PM | Most validated, operational standard / 最经验证的标准 |
| Data-limited regions / 数据有限地区 | Jensen-Haise, Hargreaves, Oudin | Minimal data requirements / 最少数据要求 |
| Remote sensing / 遥感 | PT-JPL, PML | Uses satellite LAI/NDVI / 使用卫星LAI/NDVI |
| Climate change / 气候变化 | PM-CO2, EP_Veg, PM-Jarvis | CO2 & vegetation effects / CO2和植被效应 |
| Vegetation dynamics / 植被动态 | EP_Veg, PML | Explicit stomatal models / 显式气孔模型 |
| Water balance / 水平衡 | Yang-Roderick, Budyko | Energy-limited approach / 能量限制方法 |
| Drought indices / 干旱指数 | Oudin, PM-CO2 (for PDSI) | Suitable for PDSI calculation / 适合PDSI计算 |

---

## 🔬 Scientific Background / 科学背景

### CO2 Effects on Stomatal Conductance / CO2对气孔导度的影响

Elevated CO2 reduces stomatal conductance through:

CO2升高通过以下方式降低气孔导度：

1. **Direct effect**: Lower stomatal aperture at higher [CO2] / 更高[CO2]下气孔开度降低
2. **Optimization**: Maintaining carbon gain while reducing water loss / 在减少水分损失的同时保持碳获取
3. **Non-linear response**: ~√(380/CO2) scaling (Yang et al. 2019) / ~√(380/CO2)缩放

**Formulas accounting for CO2:**
- PM-CO2 (Yang): Linear rs-CO2 relationship / 线性rs-CO2关系
- EP_Veg (Liu): Medlyn optimal stomatal model / Medlyn最优气孔模型
- PM-Jarvis (Wang): Multiplicative CO2 factor / 乘法CO2因子

### Vegetation-Atmosphere Coupling / 植被-大气耦合

**EP_Veg (Liu et al. 2023):**
- Uses Medlyn et al. (2011) optimal stomatal conductance / 使用Medlyn最优气孔导度
- Scales from leaf to canopy via LAI / 通过LAI从叶片缩放到冠层
- Accounts for photosynthesis potential (Aww) / 考虑光合潜力

**PM-Jarvis (Wang et al. 2025):**
- Multiplicative stomatal response: f(Sg) × f(Ta) × f(VPD) × f(CO2)
- Classic Jarvis (1976) empirical approach / 经典Jarvis经验方法
- Demonstrates "paradoxes" in climate projections / 展示气候预测中的"悖论"

### Temperature-Based Simplifications / 基于温度的简化

When radiation data is unavailable:

当辐射数据不可用时：

- **Jensen-Haise**: PET ∝ Ra × (T + 5) / 100
- **Hargreaves**: PET ∝ Ra × (T + 17.8) × √(Tmax - Tmin)
- **Oudin**: PET ∝ Ra × (T + 5) / (100 × λ)

These formulas are calibrated for specific climates and may require regional adjustment.

这些公式针对特定气候进行校准，可能需要区域调整。

---

## 📁 Repository Structure / 仓库结构

```
PET-Formula-Comparison/
├── pet_comparison/              # Central library / 中央库
│   ├── formulas/               # All PET formula implementations / 所有PET公式实现
│   │   ├── temperature_based.py       # Jensen-Haise, Hargreaves, Oudin
│   │   ├── radiation_based.py         # Yang-Roderick
│   │   ├── penman_monteith.py         # Classic PM
│   │   ├── penman_monteith_veg.py     # EP_Veg (Liu 2023)
│   │   ├── penman_monteith_jarvis.py  # PM-Jarvis (Wang 2025)
│   │   ├── priestley_taylor.py        # PT, PT-JPL
│   │   ├── penman_monteith_leuning.py # PML
│   │   ├── co2_aware.py               # PM-CO2
│   │   └── complementary_relationship.py  # CR models
│   ├── analysis/               # Comparison and analysis tools / 对比和分析工具
│   │   ├── comparison.py       # PETComparison framework
│   │   └── visualization.py    # Plotting utilities
│   └── utils/                  # Utility functions / 实用函数
│       ├── constants.py        # Physical constants
│       └── meteorology.py      # Meteorological calculations
│
├── Liu_2023_PET/              # EP_Veg paper replica / EP_Veg论文复现
├── Pimentel_2023_WRR/         # Temperature-based methods / 基于温度的方法
├── Yang_2018_NCC/             # PM-CO2 paper replica / PM-CO2论文复现
├── Xiong_PDSI_025/            # PDSI and Oudin / PDSI和Oudin
├── Wang_2025_PET_Paradox/     # PM-Jarvis and paradoxes / PM-Jarvis和悖论
├── Yin_GRL_2025/              # Aridity distributions / 干旱分布
│
├── examples/                   # Example scripts / 示例脚本
│   ├── basic_comparison.py    # Basic usage example
│   └── co2_sensitivity.py     # CO2 analysis example
│
├── tests/                      # Unit tests / 单元测试
├── docs/                       # Documentation / 文档
├── README.md                   # This file / 本文件
├── requirements.txt            # Dependencies / 依赖
└── setup.py                    # Installation script / 安装脚本
```

---

## 🤝 Contributing / 贡献

Contributions are welcome! Areas of interest:

欢迎贡献！感兴趣的领域：

- **New formulas**: Add formulas from recent papers / 添加最新论文的公式
- **Analysis methods**: Budyko, attribution, uncertainty / Budyko、归因、不确定性
- **Case studies**: Real-world applications / 实际应用案例
- **Performance**: Vectorization, parallelization / 矢量化、并行化
- **Documentation**: Tutorials, examples / 教程、示例

**How to contribute:**
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

---

## 📚 Key References / 主要参考文献

### Integrated Papers / 整合的论文

1. **Liu, B., et al. (2023).** A physically-based potential evapotranspiration model for global water availability projections. *Journal of Hydrology*, 616, 128781.

2. **Pimentel, R., et al. (2023).** Which Potential Evapotranspiration Formula to Use in Hydrological Modeling World-Wide? *Water Resources Research*, 59(3), e2022WR033447.

3. **Yang, Y., et al. (2019).** Hydrologic implications of vegetation response to elevated CO2 in climate projections. *Nature Climate Change*, 9(1), 44-48.

4. **Xiong, J., & Yang, Y. (2025).** PDSI_CMIP6: an ensemble CMIP6-projected self-calibrated palmer drought severity index dataset. *Scientific Data* (in press).

5. **Wang, K., et al. (2025).** Three Paradoxes Related to Potential Evapotranspiration in a Warming Climate. *Current Climate Change Reports* (in press).

6. **Yin, J., & Porporato, A. (2023).** Global distribution of climatic aridity. *Geophysical Research Letters*, 50(17), e2023GL104623.

### Foundational Papers / 基础论文

7. **Allen, R. G., et al. (1998).** Crop evapotranspiration - Guidelines for computing crop water requirements. *FAO Irrigation and Drainage Paper 56*.

8. **Priestley, C. H. B., & Taylor, R. J. (1972).** On the assessment of surface heat flux and evaporation using large-scale parameters. *Monthly Weather Review*, 100(2), 81-92.

9. **Medlyn, B. E., et al. (2011).** Reconciling the optimal and empirical approaches to modelling stomatal conductance. *Global Change Biology*, 17(6), 2134-2144.

10. **Jarvis, P. G. (1976).** The interpretation of the variations in leaf water potential and stomatal conductance found in canopies in the field. *Philosophical Transactions of the Royal Society B*, 273(927), 593-610.

---

## 📄 License / 许可证

This project is licensed under the MIT License - see the LICENSE file for details.

本项目采用MIT许可证 - 详情见LICENSE文件。

---

## 👥 Authors / 作者

- **licm13** - Framework development and paper integration / 框架开发和论文整合

---

## 🎓 Citation / 引用

If you use this framework in your research, please cite:

如果您在研究中使用此框架，请引用：

```bibtex
@software{pet_comparison_2025,
  author = {licm13},
  title = {PET Formula Comparison: An Integrated Scientific Framework},
  year = {2025},
  url = {https://github.com/licm13/PET-Formula-Comparison},
  note = {Integrates methods from Liu (2023), Pimentel (2023), Yang (2019), Xiong (2025), Wang (2025), and Yin (2023)}
}
```

Please also cite the original papers for specific formulas you use.

请同时引用您使用的特定公式的原始论文。

---

## 🔮 Future Directions / 未来方向

- **Budyko framework integration**: Runoff estimation and water balance / Budyko框架整合：径流估算和水平衡
- **PDSI calculation**: Drought index computation / PDSI计算：干旱指数计算
- **Attribution analysis**: Decompose PET changes / 归因分析：分解PET变化
- **Ensemble methods**: Multi-model PET estimates / 集合方法：多模型PET估算
- **Uncertainty quantification**: Formula disagreement analysis / 不确定性量化：公式分歧分析
- **Machine learning**: Hybrid physical-ML models / 机器学习：混合物理-机器学习模型
- **Remote sensing integration**: MODIS, Landsat, Sentinel / 遥感整合

---

## 📞 Support / 支持

For questions, issues, or suggestions:

对于问题、问题或建议：

- **Issues**: [GitHub Issues](https://github.com/licm13/PET-Formula-Comparison/issues)
- **Discussions**: [GitHub Discussions](https://github.com/licm13/PET-Formula-Comparison/discussions)
- **Email**: [Contact author]

---

## ⚠️ Disclaimer / 免责声明

This framework is designed for **research purposes**. For operational applications:

此框架设计用于**研究目的**。对于业务应用：

- Validate against local observations / 针对本地观测验证
- Consider site-specific calibration / 考虑站点特定校准
- Understand formula assumptions and limitations / 理解公式假设和限制
- Review original papers for context / 查阅原始论文以了解背景

---

**Last Updated**: 2025-11-06
**Version**: 1.0.0 (Integrated Framework Release)
