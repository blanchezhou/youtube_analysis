# 📺 YouTube Top 50 Channels — Data Analysis 2024

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas)
![Data Source](https://img.shields.io/badge/Data-Kaggle-20BEFF?logo=kaggle)
![License](https://img.shields.io/badge/license-MIT-green)

An exploratory data analysis (EDA) of the **top 50 most-subscribed YouTube channels in 2024**, examining subscriber distribution across categories, countries, languages, and channel types (brand vs. independent creator).

---

## 📊 Analysis Report

![YouTube Analysis](output/youtube_analysis.png)

---

## 🎯 Questions Explored

| Question | Method |
|----------|--------|
| Which channel has the most subscribers? | Top 15 ranked horizontal bar chart |
| Which category has the most channels? Highest avg subscribers? | Dual-axis bar + line chart |
| Where do these channels come from? | Donut chart by country |
| What languages dominate? | Horizontal bar chart |
| Do brand channels outperform independent creators? | Box plot + strip plot overlay |
| How does India compare to the United States? | Scatter plot comparison |

---

## 📂 Project Structure

```
youtube_analysis/
├── data/
│   └── youtube_subscribers_data.csv   # Raw dataset (from Kaggle)
├── output/
│   ├── youtube_analysis.png           # 7-panel visualisation report
│   └── category_summary.csv          # Aggregated summary table
├── analysis.py                        # Main analysis script (fully commented)
├── requirements.txt
└── README.md
```

---

## 🔧 Dataset Fields

| Field | Description |
|-------|-------------|
| `Name` | Channel name |
| `Brand channel` | Whether the channel belongs to a company/brand (Yes/No) |
| `Subscribers (millions)` | Subscriber count in millions |
| `Primary language` | Main language of content |
| `Category` | Content category |
| `Country` | Channel's country of origin |

Data source: [Kaggle — YouTube Subscribers Data 2024](https://www.kaggle.com/datasets/rashminslnk/youtube-subscribers-data-2024)

---

## 🚀 Getting Started

```bash
git clone https://github.com/your-username/youtube_analysis.git
cd youtube_analysis
pip install -r requirements.txt
python analysis.py
```

---

## 📈 Key Findings

- 👑 **MrBeast** leads with **335M subscribers** — roughly 55M ahead of second-place T-Series
- 🇮🇳 **India** dominates with **17 channels** in the Top 50, followed by the US (13)
- 🎭 **Entertainment** is the largest category (21 channels) with the highest average subscribers (99.8M)
- 🏢 Brand channels (91.7M avg) and independent creators (90.0M avg) are nearly equal — individual creators hold their own against large organisations
- 🗣 **English** is the most common language (21 channels), with **Hindi** a strong second (15 channels)
- 🎵 Despite having fewer channels, **Sports** channels average the highest subscribers per channel (105M)

---

## 🛠 Tech Stack

- **pandas** — data loading, cleaning, and aggregation
- **matplotlib** — multi-panel layout, dual-axis charts
- **seaborn** — box plots, strip plots, statistical visualisation

---

## 📝 Analysis Pipeline

1. **Load** — `pd.read_csv()` with dtype inspection
2. **Explore** — `.dtypes`, `.describe()`, `.value_counts()`
3. **Clean** — normalise categories and countries; encode boolean flag for brand channels
4. **Aggregate** — `groupby()` across multiple dimensions
5. **Visualise** — 7 charts covering rankings, distributions, and comparisons
6. **Summarise** — export insights and CSV summary table

---

## 📜 License

MIT © 2024
