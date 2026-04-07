# 📺 YouTube Top 50 Channels — Data Analysis 2024

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas)
![Data Source](https://img.shields.io/badge/Data-Kaggle-20BEFF?logo=kaggle)
![License](https://img.shields.io/badge/license-MIT-green)

> 使用 Python 与 pandas 对 **2024 年 YouTube 订阅数 Top 50 频道**进行完整的数据分析，从国家分布、语言、类别、品牌 vs 创作者等多维度探索全球最大 YouTube 频道的规律。

---

## 📊 分析报告预览

![YouTube Analysis](output/youtube_analysis.png)

---

## 🎯 核心问题

| 问题 | 分析方法 |
|------|----------|
| 谁是订阅数第一的频道？ | Top 15 水平条形排行图 |
| 哪个类别频道最多？订阅最高？ | 双轴柱线图 |
| 这些频道来自哪些国家？ | 环形饼图 |
| 哪种语言的频道最多？ | 水平条形图 |
| 品牌频道 vs 个人创作者，谁更强？ | 箱线图 + 散点叠加 |
| 印度 vs 美国频道实力对比？ | 散点对比图 |

---

## 📂 项目结构

```
youtube_analysis/
├── data/
│   └── youtube_subscribers_data.csv   # 原始数据（Kaggle）
├── output/
│   ├── youtube_analysis.png           # 7 合 1 可视化报告
│   └── category_summary.csv          # 分类汇总表
├── analysis.py                        # 主分析脚本（含完整注释）
├── requirements.txt
└── README.md
```

---

## 🔧 数据集字段

| 字段 | 说明 |
|------|------|
| `Name` | 频道名称 |
| `Brand channel` | 是否为品牌/机构频道（Yes/No）|
| `Subscribers (millions)` | 订阅数（单位：百万）|
| `Primary language` | 主要语言 |
| `Category` | 内容类别 |
| `Country` | 频道所属国家 |

数据来源：[Kaggle - YouTube Subscribers Data 2024](https://www.kaggle.com/datasets/rashminslnk/youtube-subscribers-data-2024)

---

## 🚀 快速开始

```bash
git clone https://github.com/你的用户名/youtube_analysis.git
cd youtube_analysis
pip install -r requirements.txt
python analysis.py
```

---

## 📈 关键发现

- 👑 **MrBeast** 以 **335M** 订阅数雄居第一，比第二名 T-Series 多出约 20%
- 🇮🇳 **印度**以 17 个频道占据最多，**英语**是最主流的语言（21 个频道）
- 🎭 **娱乐类**频道数量最多（21 个），平均订阅数 99.8M 也最高
- 🏢 品牌频道（91.7M）与个人创作者（90.0M）均值几乎持平——个人影响力不输大机构
- 🎵 **音乐类**总订阅 1424M，其中印度频道贡献了大部分

---

## 🛠 技术栈

- **pandas** — 数据读取、清洗、分组聚合
- **matplotlib** — 多子图布局、双轴图
- **seaborn** — 箱线图、散点叠加

---

## 📝 分析步骤

1. **读取数据** `pd.read_csv()`
2. **数据探索** `.dtypes` `.describe()` `.value_counts()`
3. **数据清洗** 标准化类别、国家字段；布尔化品牌字段
4. **聚合分析** `groupby()` 多维度交叉统计
5. **可视化** 7 张图表，双轴/箱线/散点全覆盖
6. **洞察总结** 输出关键业务结论

---

## 📜 License

MIT © 2024
