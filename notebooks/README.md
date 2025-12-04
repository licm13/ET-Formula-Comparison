# 📚 Educational Jupyter Notebooks / 教学向 Jupyter Notebooks

欢迎！这个目录包含三个循序渐进的教学笔记本，专为**大一新生**设计，从零开始学习蒸散发（ET）计算。

Welcome! This directory contains three progressive educational notebooks designed for **freshmen**, learning evapotranspiration (ET) calculations from scratch.

---

## 🎯 学习路径 / Learning Path

### 📘 Notebook 1: 地球是如何"出汗"的？
**Earth's Sweating: Temperature-based ET Fundamentals**

**文件 / File:** `01_Earth_Sweating_Temperature_ET.ipynb`

**难度 / Difficulty:** ⭐ Beginner

**学习目标 / Learning Objectives:**
- 理解蒸散发的物理本质（Clausius-Clapeyron关系）
- 掌握最简单的温度法公式（Hargreaves）
- 学会使用 `pet_comparison` 库
- 通过可视化理解温度与ET的关系

**关键内容 / Key Contents:**
- 🔬 饱和水汽压的物理直觉
- 📐 Hargreaves公式的逐步实现
- 🌡️ 控制变量实验：温度、昼夜温差的影响
- 🌏 真实应用：模拟一年的ET变化

**适合人群 / Suitable for:**
完全没有背景知识的初学者，只需要高中物理基础。

Complete beginners with only high school physics background.

---

### 📗 Notebook 2: 能量的博弈
**Energy Balance: Penman-Monteith Equation**

**文件 / File:** `02_Energy_Balance_Penman_Monteith.ipynb`

**难度 / Difficulty:** ⭐⭐ Intermediate

**学习目标 / Learning Objectives:**
- 理解能量平衡原理
- 掌握"阻力网络"类比（电路类比）
- 使用世界标准的彭曼-蒙蒂斯方程
- 探索风速、湿度、辐射的综合影响

**关键内容 / Key Contents:**
- 🔌 电路类比：水汽传输如同电流
- ⚡ PM方程的拆解：辐射项 vs. 空气动力学项
- 🧪 三个实验：风速、湿度、辐射的独立影响
- 🔥 综合实验：热浪场景下的多变量响应

**适合人群 / Suitable for:**
完成Notebook 1的学习者，或具有基本物理化学知识的学生。

Learners who completed Notebook 1, or students with basic physics/chemistry knowledge.

---

### 📙 Notebook 3: 气候变化的悖论
**Climate Paradox: CO2 Effects on Stomatal Conductance**

**文件 / File:** `03_Climate_Paradox_CO2_Effects.ipynb`

**难度 / Difficulty:** ⭐⭐⭐ Advanced

**学习目标 / Learning Objectives:**
- 理解蒸发悖论的科学前沿问题
- 掌握植物气孔响应的生物物理机制
- 使用CO2感知的先进ET模型
- 预测2020-2100年的ET变化

**关键内容 / Key Contents:**
- 🌿 CO2的双重效应：温室效应 vs. 气孔效应
- 📐 气孔导度模型（$g_s \propto 1/\sqrt{CO_2}$）
- 🌍 IPCC情景模拟（RCP2.6, RCP4.5, RCP8.5）
- 🔥 温度vs.CO2的"拉锯战"

**适合人群 / Suitable for:**
完成前两个Notebook，或对气候变化感兴趣的高年级学生。

Learners who completed Notebooks 1-2, or advanced students interested in climate change.

---

## 🚀 快速开始 / Quick Start

### 安装依赖 / Install Dependencies

```bash
# 进入项目根目录 / Navigate to project root
cd PET-Formula-Comparison

# 安装项目（开发模式）/ Install project (development mode)
pip install -e .

# 安装Jupyter / Install Jupyter
pip install jupyter matplotlib pandas xarray
```

### 启动Notebook / Launch Notebook

```bash
# 进入notebooks目录 / Navigate to notebooks directory
cd notebooks

# 启动Jupyter / Launch Jupyter
jupyter notebook
```

然后在浏览器中依次打开三个笔记本。

Then open the three notebooks sequentially in your browser.

---

## 📊 学习顺序建议 / Recommended Learning Sequence

1. **第1-2周 / Weeks 1-2:**
   - 完成 Notebook 1
   - 理解温度与蒸发的关系
   - 动手实现第一个ET公式

2. **第3-4周 / Weeks 3-4:**
   - 完成 Notebook 2
   - 掌握能量平衡概念
   - 学会分析多因子影响

3. **第5-6周 / Weeks 5-6:**
   - 完成 Notebook 3
   - 探索前沿科学问题
   - 思考气候变化的复杂性

4. **第7周+ / Week 7+:**
   - 尝试运行 `examples/advanced_stress_test_spatial.py`
   - 阅读项目文档深入理解
   - 探索其他ET模型

---

## 🎓 教学使用建议 / Teaching Recommendations

### 适用课程 / Suitable Courses
- 🌍 地球系统科学导论 / Introduction to Earth System Science
- 💧 水文学基础 / Fundamentals of Hydrology
- 🌱 生态气象学 / Ecoclimatology
- 🖥️ 科学计算入门 / Introduction to Scientific Computing

### 课堂活动 / Classroom Activities

**Activity 1: "谁的ET最高?" / "Who Has the Highest ET?"**
- 让学生输入自己家乡的气象数据
- 比较不同地区的ET
- 讨论气候差异的原因

**Activity 2: "设计一个灌溉系统" / "Design an Irrigation System"**
- 基于ET计算每日灌溉需求
- 考虑季节变化
- 讨论节水策略

**Activity 3: "2100年的地球" / "Earth in 2100"**
- 使用Notebook 3预测未来ET
- 讨论不同减排情景
- 撰写气候政策建议书

---

## 🛠️ 技术要求 / Technical Requirements

### 必需 / Required
- Python 3.9+
- NumPy
- Matplotlib
- pandas
- Jupyter Notebook

### 可选（用于高级功能）/ Optional (for advanced features)
- xarray（空间数据分析）
- dask（并行计算）
- seaborn（更美观的可视化）

---

## 📖 参考资料 / References

### 教科书 / Textbooks
1. Allen et al. (1998). *FAO Irrigation and Drainage Paper 56*
   - 标准参考书，介绍PM方程 / Standard reference for PM equation

2. Brutsaert, W. (2005). *Hydrology: An Introduction*
   - 全面的水文学教材 / Comprehensive hydrology textbook

### 论文 / Papers
1. Hargreaves & Samani (1985). *Applied Engineering in Agriculture*
   - 温度法的经典论文 / Classic paper on temperature methods

2. Yang et al. (2019). *Nature Climate Change*
   - CO2效应的前沿研究 / Cutting-edge research on CO2 effects

3. Priestley & Taylor (1972). *Monthly Weather Review*
   - PT系数的原始论文 / Original paper on PT coefficient

### 在线资源 / Online Resources
- [FAO Irrigation Portal](http://www.fao.org/land-water/databases-and-software/eto-calculator/en/)
- [IPCC Climate Change Reports](https://www.ipcc.ch/)
- [NASA Earth Observatory](https://earthobservatory.nasa.gov/)

---

## 💬 常见问题 / FAQ

### Q1: 我没有编程基础，能学习这些Notebook吗？
**A:** 可以！Notebook 1 从零开始，包含详细的代码解释。只要跟着代码一步步运行，就能理解。

### Q2: 为什么有些公式用中文，有些用英文？
**A:** 这是双语教学设计。关键概念同时提供中英文，帮助国际交流和文献阅读。

### Q3: 可以用自己的真实数据吗？
**A:** 当然！只需把气象数据替换成你自己的，公式会自动计算。确保单位正确（°C, %, m/s等）。

### Q4: Notebook里的图表保存在哪里？
**A:** 默认显示在Notebook中。如果要保存，可以在代码中添加 `plt.savefig('filename.png')`。

### Q5: 运行Notebook时遇到错误怎么办？
**A:** 检查步骤：
1. 是否安装了所有依赖？（`pip install -e .`）
2. 是否按顺序运行了所有单元格？
3. 检查 `examples/` 目录中的示例代码是否能运行

---

## 🤝 贡献与反馈 / Contribution and Feedback

### 发现问题？ / Found an Issue?
请在项目GitHub页面提交Issue，描述：
- 哪个Notebook
- 哪个代码单元格
- 错误信息截图

Please submit an Issue on the project GitHub page, describing:
- Which Notebook
- Which code cell
- Screenshot of error message

### 有改进建议？ / Have Suggestions?
欢迎提交Pull Request，添加：
- 新的可视化示例
- 更多实际应用案例
- 其他语言的翻译

Welcome to submit Pull Requests, adding:
- New visualization examples
- More real-world case studies
- Translations in other languages

---

## 🌟 致谢 / Acknowledgments

这些教学Notebooks基于以下开源项目和科学研究：

These educational Notebooks are based on the following open-source projects and scientific research:

- **FAO-56 Penman-Monteith** (Allen et al., 1998)
- **Hargreaves Method** (Hargreaves & Samani, 1985)
- **PM-CO2 Model** (Yang et al., 2019; Milly & Dunne, 2016)
- **PET Comparison Framework** (本项目 / This project)

特别感谢全球水文学和气候科学社区的贡献！

Special thanks to the global hydrology and climate science community!

---

## 📜 许可证 / License

这些教学材料与主项目使用相同的许可证。自由使用、修改和分享，但请保留原作者信息。

These teaching materials use the same license as the main project. Feel free to use, modify, and share, but please retain attribution.

---

**Happy Learning! / 学习愉快！** 🎓🌍💧
