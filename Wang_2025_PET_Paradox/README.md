
# PET Paradoxes Reproduction (教学演示复刻)

> Reproduces the **core formulas** and **qualitative figures** from the review paper *"Three Paradoxes Related to Potential Evapotranspiration in a Warming Climate"* **using synthetic (randomized) data for teaching/demo**.  
> 该仓库基于合成（随机）数据，**教学演示性地**复刻论文中的关键公式与定性图形，不用于科学结论复刻。

## What is included / 本仓库包含
- **PET formulations / 潜在蒸散（PET）公式**  
  - PM-RC (FAO-56 Penman–Monteith reference crop)  
  - PM-RC + CO₂ stomatal response (Yang et al. 2019-style)  
  - PM-RC + multi-factor stomatal responses (Jarvis-type, with Sg, Ta, VPD, CO₂)
- **Indices / 指标**  
  - Aridity Index (AI = P / PET, 年平均尺度)  
  - A toy “PDSI-like” drought metric for demonstration (教学版、近似方法)
- **Synthetic data generator / 合成气候数据生成器**：1950–2100 月尺度，包含 Ta、VPD、风速、短波辐射、净辐射、CO₂、降水等
- **Plotting utilities with CN/EN fonts / 中英文字体绘图工具**：自动寻找 Noto/SourceHan/SimHei/Microsoft YaHei 等字体，避免中文乱码或负号显示问题

> ⚠️ **Disclaimer**：这是一套**教学演示**代码，用合成数据复刻文中**方法**与**逻辑**，不等价于论文图表的科学结果复刻。请勿据此作政策或工程结论。  
> 本仓库中的公式、参数与符号，均参考论文与相关文献公开描述；如需真实再现论文曲线，请替换为相应的CMIP/观测数据并完成偏差订正流程。

## Install / 安装
```bash
git clone <your-fork-url>
cd pet_paradoxes_replication
python -m venv .venv && source .venv/bin/activate    # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

## Quickstart / 快速开始
1) 生成合成数据：
```bash
python scripts/generate_synthetic.py
```
2) 计算并绘图（复刻示意图 Fig.2/3 的“趋势形态”）：
```bash
python scripts/reproduce_figures.py
```
输出图片在 `figures/`。

## Repo Layout / 目录结构
```
pet_paradoxes_replication/
├── src/paradoxes_pet/            # Core library / 核心库
│   ├── __init__.py
│   ├── data.py                   # synthetic data / 合成数据
│   ├── pet.py                    # PET formulas / PET 公式
│   ├── indices.py                # AI & toy-PDSI / 干旱指标
│   └── plotting.py               # font + plotting helpers / 字体+绘图
├── scripts/
│   ├── generate_synthetic.py     # make synthetic CSV / 生成CSV
│   └── reproduce_figures.py      # compute & plot / 计算与出图
├── data/                         # synthetic outputs / 合成输出
├── figures/                      # saved figures / 图片输出
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── README.md
```

## Methods (brief) / 方法简述
主要依据论文中的公式与描述：
- **ETrc (PM-RC)**：FAO-56 Penman–Monteith 参考作物公式
- **ETrc–Yang**：在 PM-RC 基础上，**线性**考虑 CO₂ 对气孔（rs）的影响
- **ETrc–Jarvis**：在 PM-RC 基础上，采用 **Jarvis 型**乘法权重，考虑 Sg、Ta、VPD、CO₂ 等环境因子对气孔的影响

**Aridity Index**：年尺度 AI = P / PET。  
**Drought (toy PDSI-like)**：基于(P - PET) 归一化并平滑的教学版指标，仅作定性演示。

> 参照文献：Wang et al., 2025, *Current Climate Change Reports* （“三大悖论”评述）。

## Font notes / 字体说明
- 自动尝试优先使用：`Noto Sans CJK SC` / `Source Han Sans SC` / `Microsoft YaHei` / `SimHei`。
- 处理 `axes.unicode_minus=False` 防止中文环境下负号显示为方块。

## Replacing with real data / 更换真实数据
- 将真实的月尺度 **P、Ta、VPD、WS2、Sg、Rn\*, CO₂** 等数据替换到 `data/` 中，或修改 `scripts/generate_synthetic.py` 以读取您的数据源。
- 如果要复现实证结果，请在 PET 计算前进行**偏差订正**（如文中所述的均值订正流程）。

## License
MIT

---

本仓库用于**教学与科研方法演示**，欢迎在此基础上拓展、连接您的真实数据、或纳入更多 PET 公式与干旱指标。
