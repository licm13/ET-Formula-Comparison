# di-global-aridity — Recreating the global dryness index distribution

**目标 / Goal**  
本仓库以可复现实验（使用**随机合成数据**占位）复刻并讲解 Yin & Porporato (2023, GRL) 提出的**干燥度指数（DI）分布**理论与图示流程，包含：
- 理论推导公式的可计算实现（`p_DI(DI) = D0 / DI^2 * exp(-D0/DI)`；`p_HI(HI) = (1/H0) * exp(-HI/H0)`）。  
- 面向全球栅格的权重直方图（面积权重 ~ cos(纬度)）。  
- 演示 DI 经验分布与理论分布的拟合、-2 幂率尾特征，以及（模拟的）未来增暖情景下 D0 变化与“变干区域”比例。  
- 自定义中英文字体设置（Matplotlib），以避免中文显示为方框的问题。

> 论文参考 / Reference: Yin, J., & Porporato, A. (2023). *Global distribution of climatic aridity*. **Geophysical Research Letters**, 50, e2023GL105228.  
> 本仓库仅做方法复刻与教学用途；若使用真实数据，请按论文引用的数据源下载并替换示例数据。

---

## 快速开始 / Quick Start

```bash
# 1) (可选) 创建虚拟环境 / optional venv
# python -m venv .venv && source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate                            # Windows PowerShell

# 2) 安装依赖 / install
pip install -r requirements.txt

# 3) 运行示例 / run examples
python examples/example_synthetic_global.py
python examples/example_validate_power_law_tail.py
python examples/example_esms_projection_mock.py
```

生成的图保存在 `figures/`。

---

## 仓库结构 / Repository layout

```
di-global-aridity/
  ├─ src/di_global/
  │   ├─ theory.py          # 公式与分布
  │   ├─ compute.py         # 计算 DI、权重直方图、栅格权重
  │   ├─ datasets.py        # 随机合成数据/接口
  │   ├─ plots.py           # 画图与字体设置（中英文）
  │   └─ utils_fonts.py     # 字体与 Matplotlib rcParams
  ├─ examples/
  │   ├─ example_synthetic_global.py
  │   ├─ example_validate_power_law_tail.py
  │   └─ example_esms_projection_mock.py
  ├─ figures/               # 输出图像
  ├─ tests/
  │   └─ test_theory.py     # 简单单元测试
  ├─ README.md
  ├─ requirements.txt
  ├─ pyproject.toml
  └─ LICENSE
```

---

## 主要实现 / Main implementation

- **DI 理论分布 / Theory**  
  - `p_DI(di, D0) = D0 / di**2 * exp(-D0/di)`  
  - `p_HI(hi, H0) = (1/H0) * exp(-hi/H0)` where `H0 = 1/D0`  
- **面积权重直方图 / Area-weighted hist**：格点权重 `w ~ cos(lat)`；并自动丢弃海洋/冰盖在此示例中，可以通过掩膜控制。  
- **尾部 -2 幂律 / Power-law tail**：对数坐标下验证经验分布尾部与 `~ DI^-2` 的一致性。  
- **未来情景（模拟）/ Future scenario (mock)**：构造 “历史期 vs 未来期 (ssp585-like)” 的 P、PET 相对变化，计算 `ΔD0/D0` 与“变干区域比例”。

> **重要说明 / Important**：为**复刻流程**而非复刻数值结果，仓库默认用**合成随机数据**（对真实全球格网进行抽样模拟）；真实重现需下载 CRU/GPCC/GPCP/Global AI PET/CMIP6 等数据，并按论文设定计算 PET（Penman–Monteith）与 DI。

---

## 字体与中文 / Fonts and Chinese labels

- 采用 Matplotlib，未显式设置颜色（遵循“不要指定颜色”约束）。  
- 设置 `rcParams` 以支持中文：优先 `DejaVu Sans`，回退 `Noto Sans CJK SC / SimHei / Microsoft YaHei`。  
- 关闭负号问题：`axes.unicode_minus=False`。

---

## 数据与版权 / Data & License

- 本仓库内仅含**合成数据**。真实数据请遵循其各自许可与引用要求。  
- 代码使用 MIT 协议。

---

## 引用 / Citation

若在研究或教学中使用了此仓库，请引用：

- Yin, J., & Porporato, A. (2023). Global distribution of climatic aridity. *Geophysical Research Letters*, 50, e2023GL105228.
