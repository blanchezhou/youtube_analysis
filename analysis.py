# ============================================================
#  YouTube Top 50 频道数据分析（2024 真实数据）
#  数据来源：Kaggle - rashminslnk/youtube-subscribers-data-2024
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")
plt.rcParams["font.family"] = ["Arial Unicode MS", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ─────────────────────────────────────────
# 第 1 步：读取数据
# ─────────────────────────────────────────
print("=" * 55)
print("第 1 步  读取数据")
print("=" * 55)

df = pd.read_csv("data/youtube_subscribers_data.csv")
df.columns = df.columns.str.strip()
print(f"数据规模：{df.shape[0]} 行 × {df.shape[1]} 列")
print(df.head(10).to_string())

# ─────────────────────────────────────────
# 第 2 步：数据探索
# ─────────────────────────────────────────
print("\n" + "=" * 55)
print("第 2 步  数据探索（EDA）")
print("=" * 55)
print("\n【字段类型】")
print(df.dtypes)
print("\n【订阅数统计摘要（单位：百万）】")
print(df["Subscribers (millions)"].describe().round(2))
print("\n【缺失值】")
print(df.isnull().sum())

# ─────────────────────────────────────────
# 第 3 步：数据清洗
# ─────────────────────────────────────────
print("\n" + "=" * 55)
print("第 3 步  数据清洗")
print("=" * 55)

# 合并细分类别，便于分析
df["Category_clean"] = df["Category"].replace({
    "Entertainment/Sports": "Entertainment",
    "Education/Entertainment": "Education",
})

# 简化国家字段（去掉注释和多国）
def clean_country(c):
    c = c.strip()
    if "United States" in c:  return "United States"
    if "Cyprus" in c:         return "Cyprus"
    if "Sweden" in c:         return "Sweden/Japan"
    return c

df["Country_clean"] = df["Country"].apply(clean_country)

# 将 Brand channel Yes/No → bool
df["is_brand"] = df["Brand channel"].str.strip() == "Yes"

print("清洗完成：新增 Category_clean / Country_clean / is_brand 三列")
print(f"缺失值总计：{df.isnull().sum().sum()}")

# ─────────────────────────────────────────
# 第 4 步：分析 & 可视化
# ─────────────────────────────────────────
print("\n" + "=" * 55)
print("第 4 步  数据分析 & 可视化")
print("=" * 55)

# 调色板
PAL = sns.color_palette("tab10")
sns.set_theme(style="whitegrid")

fig = plt.figure(figsize=(20, 22))
fig.suptitle("YouTube Top 50 Channels – Data Analysis 2024",
             fontsize=20, fontweight="bold", y=0.98)

# ── 图 1：Top 15 频道订阅数排行（水平条形）──────────
ax1 = fig.add_subplot(4, 2, (1, 2))   # 占一整行
top15 = df.nlargest(15, "Subscribers (millions)")
colors = [PAL[0] if b else PAL[1] for b in top15["is_brand"]]
bars = ax1.barh(top15["Name"][::-1], top15["Subscribers (millions)"][::-1],
                color=colors[::-1], edgecolor="white", height=0.7)
ax1.set_title("Top 15 Channels by Subscribers", fontsize=13, fontweight="bold")
ax1.set_xlabel("Subscribers (Millions)")
for bar, val in zip(bars, top15["Subscribers (millions)"][::-1]):
    ax1.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
             f"{val:.0f}M", va="center", fontsize=9)
brand_patch  = mpatches.Patch(color=PAL[0], label="Brand Channel")
creator_patch= mpatches.Patch(color=PAL[1], label="Creator Channel")
ax1.legend(handles=[brand_patch, creator_patch], loc="lower right")
ax1.set_xlim(0, top15["Subscribers (millions)"].max() * 1.15)

# ── 图 2：各类别频道数量 vs 平均订阅数（双轴柱状图）──
ax2 = fig.add_subplot(4, 2, 3)
cat = df.groupby("Category_clean").agg(
    Count=("Name", "count"),
    AvgSubs=("Subscribers (millions)", "mean")
).sort_values("Count", ascending=False)

x  = range(len(cat))
ax2.bar(x, cat["Count"], color=PAL[2], label="# Channels")
ax2b = ax2.twinx()
ax2b.plot(x, cat["AvgSubs"], "o-", color=PAL[3], linewidth=2, label="Avg Subs (M)")
ax2.set_xticks(list(x))
ax2.set_xticklabels(cat.index, rotation=35, ha="right", fontsize=8)
ax2.set_title("Category: Channel Count vs Avg Subscribers", fontsize=11, fontweight="bold")
ax2.set_ylabel("Number of Channels", color=PAL[2])
ax2b.set_ylabel("Avg Subscribers (M)", color=PAL[3])
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2b.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc="upper right")

# ── 图 3：国家分布（饼图，Top 5 + 其他）────────────
ax3 = fig.add_subplot(4, 2, 4)
country_counts = df["Country_clean"].value_counts()
top5 = country_counts.iloc[:5]
other = pd.Series({"Others": country_counts.iloc[5:].sum()})
pie_data = pd.concat([top5, other])
wedge_props = dict(width=0.55, edgecolor="white")
ax3.pie(pie_data.values, labels=pie_data.index, autopct="%1.0f%%",
        startangle=140, colors=sns.color_palette("Set2"),
        wedgeprops=wedge_props)
ax3.set_title("Channel Distribution by Country", fontsize=11, fontweight="bold")

# ── 图 4：语言分布（水平条形）──────────────────────
ax4 = fig.add_subplot(4, 2, 5)
lang = df["Primary language"].value_counts()
ax4.barh(lang.index[::-1], lang.values[::-1], color=PAL[4])
ax4.set_title("Channels by Primary Language", fontsize=11, fontweight="bold")
ax4.set_xlabel("Number of Channels")
for i, v in enumerate(lang.values[::-1]):
    ax4.text(v + 0.1, i, str(v), va="center", fontsize=9)

# ── 图 5：品牌 vs 创作者订阅数分布（箱线图）─────────
ax5 = fig.add_subplot(4, 2, 6)
df["Type"] = df["is_brand"].map({True: "Brand Channel", False: "Creator Channel"})
sns.boxplot(data=df, x="Type", y="Subscribers (millions)", ax=ax5,
            palette={"Brand Channel": PAL[0], "Creator Channel": PAL[1]},
            width=0.5)
# 叠加散点，看单个数据
sns.stripplot(data=df, x="Type", y="Subscribers (millions)", ax=ax5,
              color="black", alpha=0.5, size=5, jitter=True)
ax5.set_title("Brand vs Creator: Subscriber Distribution", fontsize=11, fontweight="bold")
ax5.set_xlabel("")
ax5.set_ylabel("Subscribers (Millions)")

# ── 图 6：各类别订阅数总量（堆叠含品牌标注）─────────
ax6 = fig.add_subplot(4, 2, 7)
cat_type = df.groupby(["Category_clean", "Type"])["Subscribers (millions)"].sum().unstack(fill_value=0)
cat_type_sorted = cat_type.loc[cat_type.sum(axis=1).sort_values(ascending=True).index]
cat_type_sorted.plot(kind="barh", ax=ax6, stacked=True,
                     color=[PAL[0], PAL[1]], edgecolor="white")
ax6.set_title("Total Subscribers by Category (Brand vs Creator)", fontsize=11, fontweight="bold")
ax6.set_xlabel("Total Subscribers (Millions)")
ax6.set_ylabel("")

# ── 图 7：印度 vs 美国 频道对比散点图──────────────
ax7 = fig.add_subplot(4, 2, 8)
for country, color, marker in [("India", PAL[5], "o"), ("United States", PAL[6], "^")]:
    sub = df[df["Country_clean"] == country]
    ax7.scatter(range(len(sub)), sub["Subscribers (millions)"].sort_values(ascending=False),
                label=country, color=color, s=80, marker=marker, alpha=0.8)
ax7.set_title("India vs United States – Individual Channel Subs", fontsize=11, fontweight="bold")
ax7.set_xlabel("Channel Rank (within country)")
ax7.set_ylabel("Subscribers (Millions)")
ax7.legend()

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("output/youtube_analysis.png", dpi=150, bbox_inches="tight")
print("可视化已保存 → output/youtube_analysis.png")

# ─────────────────────────────────────────
# 第 5 步：关键洞察汇总
# ─────────────────────────────────────────
print("\n" + "=" * 55)
print("第 5 步  关键业务洞察")
print("=" * 55)

top1 = df.loc[df["Subscribers (millions)"].idxmax()]
brand_avg   = df[df["is_brand"]]["Subscribers (millions)"].mean()
creator_avg = df[~df["is_brand"]]["Subscribers (millions)"].mean()
top_country = df["Country_clean"].value_counts().idxmax()
top_lang    = df["Primary language"].value_counts().idxmax()
music_avg   = df[df["Category_clean"] == "Music"]["Subscribers (millions)"].mean()
ent_avg     = df[df["Category_clean"] == "Entertainment"]["Subscribers (millions)"].mean()

print(f"\n👑 订阅数第一   : {top1['Name']} ({top1['Subscribers (millions)']:.0f}M)")
print(f"🏢 品牌频道均值 : {brand_avg:.1f}M  vs  创作者均值: {creator_avg:.1f}M")
print(f"   品牌是创作者的 {brand_avg/creator_avg:.1f}x")
print(f"🌍 最多频道国家 : {top_country} ({df['Country_clean'].value_counts().max()} 个频道)")
print(f"🗣  最常用语言   : {top_lang} ({df['Primary language'].value_counts().max()} 个频道)")
print(f"🎵 音乐类均值   : {music_avg:.1f}M  vs  娱乐类均值: {ent_avg:.1f}M")

# 导出汇总表
summary = df.groupby("Category_clean").agg(
    频道数=("Name", "count"),
    总订阅数_M=("Subscribers (millions)", "sum"),
    平均订阅数_M=("Subscribers (millions)", "mean"),
    品牌频道数=("is_brand", "sum"),
).round(1).sort_values("总订阅数_M", ascending=False)
summary.to_csv("output/category_summary.csv", encoding="utf-8-sig")
print("\n分类汇总已导出 → output/category_summary.csv")
print(summary.to_string())
