# PET-Lab: 全球潜在蒸散发公式“虚拟实验室” / A Tiny Virtual Lab for Potential Evapotranspiration (PET)

> 复刻并教学化实现 *Jensen–Haise / Hargreaves / Priestley–Taylor* 三种PET公式，提供多过程（PET/AET/Q）评估、Budyko分析、示例脚本与中英双语注释。This repo is a didactic re‑implementation of three classic PET formulas with a mini **multi‑process** evaluation pipeline and **Budyko** plots.

**Why this repo? / 为什么要做这个仓库？**  
原论文系统比较了不同气候区/下垫面下三种PET公式在水文模拟中的适用性，并用多信息（PET、AET、径流）进行联合判别。我们在此提供**轻量可运行**版本，用**随机合成数据**复刻核心思想，便于教学、代码重构与二次开发。The upstream paper tests PET formula choice worldwide with multi‑source checks. Here we give a lightweight, runnable version using **synthetic data** for pedagogy and rapid experiments.

> Cite / 引用：Pimentel et al. (2023) “Which Potential Evapotranspiration Formula to Use in Hydrological Modeling World‑Wide?”, *Water Resources Research*, 59, e2022WR033447.

---

## ✨ Features / 功能
- 三种PET公式：Jensen–Haise（Oudin改写）、Hargreaves、Priestley–Taylor（含简化净辐射估计）  
  Three PET formulas with clean Python implementations.
- 多过程评估：对 PET / AET / Q（径流）分别计算**相对误差RE**，并进行**联合最优**判别  
  Multi‑process evaluation with **Relative Error (RE)** and **consensus** selection.
- Budyko分析与绘图：内置Budyko曲线与能量/水分受限区可视化  
  Budyko plotting utilities.
- 出图**中英字体**兼容：自动尝试 *Noto Sans CJK SC / SimHei / Microsoft YaHei / DejaVu Sans*，并禁用负号乱码  
  Robust matplotlib font setup for **Chinese+English**.
- 完整示例脚本：`examples/run_quickstart.py` 一键生成合成流域、运行分析、保存图件与CSV  
  One‑click runnable example.
- 纯Python依赖（numpy / pandas / matplotlib）

> **说明 / Notes**：本仓库仅为**教学性复刻**，与原文的全球模型（WWH/HYPE）不同；所有输入均为**随机生成**的“类物理”合成数据，旨在演示**方法流程**。

---

## 📦 Install / 安装
```bash
pip install -e .
```

## ▶️ Quick Start / 快速上手
```bash
python examples/run_quickstart.py
```
脚本会：生成N=20个“流域”、T=730天日数据 → 计算三种PET → 随机合成“观测”PET/AET/Q → 评估并选择最优公式 → 生成图件与结果表。The script synthesizes catchments, computes PET, creates pseudo‑observations, evaluates, and plots.

输出（默认保存到 `outputs/`）：
- `map_best_formula.png`：按经纬度着色展示每个流域的“联合最优”PET公式
- `budyko_density.png`：Budyko空间密度图（按最优公式分色）
- `scores.csv`：每个流域在三变量上的RE与最优决策

---

## 🧪 Project Structure / 目录
```
petlab/
├─ src/petlab/
│  ├─ formulas.py        # 三种PET公式实现 + 天文学辐射工具
│  ├─ radiation.py       # FAO-56 辐射/日照几何辅助函数
│  ├─ metrics.py         # 相对误差等指标
│  ├─ budyko.py          # Budyko曲线函数与绘图
│  ├─ synthetic.py       # 合成数据生成器（流域/气象/“观测”）
│  ├─ plotting.py        # 字体和风格设置（中英兼容）
│  └─ analysis.py        # 多过程评估与“联合最优”选择
├─ examples/run_quickstart.py
├─ scripts/petlab_cli.py # CLI入口（可扩展）
├─ tests/test_formulas.py
└─ README.md, LICENSE, CITATION.cff, pyproject.toml
```

---

## 📊 Notes on Units / 计量单位说明
- 温度°C；降水/蒸散发：mm/day；辐射：MJ m⁻² day⁻¹。  
- 采用 FAO‑56 常用常数：λ≈2.45 MJ kg⁻¹；σ=4.903×10⁻⁹ MJ K⁻⁴ m⁻² day⁻¹ 等。

---

## 📝 Acknowledgement / 致谢
本仓库思路与指标设置参考下述论文（并非原始代码）：This code is inspired by the following paper (not the original codebase):

- Pimentel et al. (2023), Which Potential Evapotranspiration Formula to Use in Hydrological Modeling World‑Wide?, WRR, 59, e2022WR033447.

---

## ⚠️ Disclaimer / 免责声明
- 该实现为**教学演示**，不包含全球WWH/HYPE结构与数据；不构成对原论文数值结论的复刻。- This is a **teaching** re‑implementation with synthetic data; not a reproduction of global results.
