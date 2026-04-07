# ============================================================
#  YouTube Top 50 Channels — Exploratory Data Analysis (2024)
#  Data Source: Kaggle — rashminslnk/youtube-subscribers-data-2024
#  Tools: Python · pandas · matplotlib · seaborn
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")
plt.rcParams["font.family"] = ["DejaVu Sans", "Liberation Sans", "Arial"]

# ─────────────────────────────────────────
# Step 1: Load Data
# ─────────────────────────────────────────
print("=" * 55)
print("Step 1  Load Data")
print("=" * 55)

df = pd.read_csv("data/youtube_subscribers_data.csv")
df.columns = df.columns.str.strip()
print(f"Dataset shape: {df.shape[0]} rows x {df.shape[1]} columns\n")
print(df.head(10).to_string())

# ─────────────────────────────────────────
# Step 2: Exploratory Data Analysis (EDA)
# ─────────────────────────────────────────
print("\n" + "=" * 55)
print("Step 2  Exploratory Data Analysis (EDA)")
print("=" * 55)

print("\n[Data Types]")
print(df.dtypes)

print("\n[Subscriber Count Summary — in Millions]")
print(df["Subscribers (millions)"].describe().round(2))

print("\n[Missing Values]")
print(df.isnull().sum())

print("\n[Category Distribution]")
print(df["Category"].value_counts())

print("\n[Country Distribution]")
print(df["Country"].value_counts())

# ─────────────────────────────────────────
# Step 3: Data Cleaning
# ─────────────────────────────────────────
print("\n" + "=" * 55)
print("Step 3  Data Cleaning")
print("=" * 55)

# Merge granular sub-categories for cleaner grouping
df["Category_clean"] = df["Category"].replace({
    "Entertainment/Sports": "Entertainment",
    "Education/Entertainment": "Education",
})

# Normalise country field (remove footnotes and multi-country entries)
def clean_country(c):
    c = c.strip()
    if "United States" in c: return "United States"
    if "Cyprus"       in c: return "Cyprus"
    if "Sweden"       in c: return "Sweden/Japan"
    return c

df["Country_clean"] = df["Country"].apply(clean_country)

# Convert Brand channel Yes/No to boolean
df["is_brand"] = df["Brand channel"].str.strip() == "Yes"
df["Type"]     = df["is_brand"].map({True: "Brand Channel", False: "Creator Channel"})

print("Cleaning complete. New columns added: Category_clean, Country_clean, is_brand, Type")
print(f"Total missing values after cleaning: {df.isnull().sum().sum()}")

# ─────────────────────────────────────────
# Step 4: Analysis & Visualisation
# ─────────────────────────────────────────
print("\n" + "=" * 55)
print("Step 4  Analysis & Visualisation")
print("=" * 55)

PAL = sns.color_palette("tab10")
sns.set_theme(style="whitegrid")

fig = plt.figure(figsize=(20, 22))
fig.suptitle("YouTube Top 50 Channels — Data Analysis 2024",
             fontsize=20, fontweight="bold", y=0.98)

# ── Chart 1: Top 15 Channels by Subscribers (horizontal bar) ──
ax1 = fig.add_subplot(4, 2, (1, 2))
top15  = df.nlargest(15, "Subscribers (millions)")
colors = [PAL[0] if b else PAL[1] for b in top15["is_brand"]]
bars   = ax1.barh(top15["Name"][::-1], top15["Subscribers (millions)"][::-1],
                  color=colors[::-1], edgecolor="white", height=0.7)
ax1.set_title("Top 15 Channels by Subscribers", fontsize=13, fontweight="bold")
ax1.set_xlabel("Subscribers (Millions)")
for bar, val in zip(bars, top15["Subscribers (millions)"][::-1]):
    ax1.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
             f"{val:.0f}M", va="center", fontsize=9)
ax1.legend(handles=[
    mpatches.Patch(color=PAL[0], label="Brand Channel"),
    mpatches.Patch(color=PAL[1], label="Creator Channel"),
], loc="lower right")
ax1.set_xlim(0, top15["Subscribers (millions)"].max() * 1.15)

# ── Chart 2: Category — Channel Count vs Avg Subscribers (dual axis) ──
ax2 = fig.add_subplot(4, 2, 3)
cat = df.groupby("Category_clean").agg(
    Count  =("Name",                   "count"),
    AvgSubs=("Subscribers (millions)", "mean"),
).sort_values("Count", ascending=False)
x = range(len(cat))
ax2.bar(x, cat["Count"], color=PAL[2], label="# Channels")
ax2b = ax2.twinx()
ax2b.plot(x, cat["AvgSubs"], "o-", color=PAL[3], linewidth=2, label="Avg Subs (M)")
ax2.set_xticks(list(x))
ax2.set_xticklabels(cat.index, rotation=35, ha="right", fontsize=8)
ax2.set_title("Category: Channel Count vs Avg Subscribers", fontsize=11, fontweight="bold")
ax2.set_ylabel("Number of Channels", color=PAL[2])
ax2b.set_ylabel("Avg Subscribers (M)",  color=PAL[3])
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2b.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc="upper right")

# ── Chart 3: Country Distribution (donut chart) ──
ax3 = fig.add_subplot(4, 2, 4)
country_counts = df["Country_clean"].value_counts()
top5  = country_counts.iloc[:5]
other = pd.Series({"Others": country_counts.iloc[5:].sum()})
pie_data = pd.concat([top5, other])
ax3.pie(pie_data.values, labels=pie_data.index, autopct="%1.0f%%",
        startangle=140, colors=sns.color_palette("Set2"),
        wedgeprops=dict(width=0.55, edgecolor="white"))
ax3.set_title("Channel Distribution by Country", fontsize=11, fontweight="bold")

# ── Chart 4: Channels by Primary Language (horizontal bar) ──
ax4 = fig.add_subplot(4, 2, 5)
lang = df["Primary language"].value_counts()
ax4.barh(lang.index[::-1], lang.values[::-1], color=PAL[4])
ax4.set_title("Channels by Primary Language", fontsize=11, fontweight="bold")
ax4.set_xlabel("Number of Channels")
for i, v in enumerate(lang.values[::-1]):
    ax4.text(v + 0.1, i, str(v), va="center", fontsize=9)

# ── Chart 5: Brand vs Creator Subscriber Distribution (box + strip) ──
ax5 = fig.add_subplot(4, 2, 6)
sns.boxplot(data=df, x="Type", y="Subscribers (millions)", ax=ax5,
            palette={"Brand Channel": PAL[0], "Creator Channel": PAL[1]}, width=0.5)
sns.stripplot(data=df, x="Type", y="Subscribers (millions)", ax=ax5,
              color="black", alpha=0.5, size=5, jitter=True)
ax5.set_title("Brand vs Creator: Subscriber Distribution", fontsize=11, fontweight="bold")
ax5.set_xlabel("")
ax5.set_ylabel("Subscribers (Millions)")

# ── Chart 6: Total Subscribers by Category, stacked by Type ──
ax6 = fig.add_subplot(4, 2, 7)
cat_type = df.groupby(["Category_clean", "Type"])["Subscribers (millions)"].sum().unstack(fill_value=0)
cat_type.loc[cat_type.sum(axis=1).sort_values().index].plot(
    kind="barh", ax=ax6, stacked=True,
    color=[PAL[0], PAL[1]], edgecolor="white")
ax6.set_title("Total Subscribers by Category (Brand vs Creator)", fontsize=11, fontweight="bold")
ax6.set_xlabel("Total Subscribers (Millions)")
ax6.set_ylabel("")

# ── Chart 7: India vs United States — individual channel scatter ──
ax7 = fig.add_subplot(4, 2, 8)
for country, color, marker in [("India", PAL[5], "o"), ("United States", PAL[6], "^")]:
    sub = df[df["Country_clean"] == country]
    ax7.scatter(range(len(sub)),
                sub["Subscribers (millions)"].sort_values(ascending=False).values,
                label=country, color=color, s=80, marker=marker, alpha=0.8)
ax7.set_title("India vs United States — Per-Channel Subscribers", fontsize=11, fontweight="bold")
ax7.set_xlabel("Channel Rank (within country)")
ax7.set_ylabel("Subscribers (Millions)")
ax7.legend()

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("output/youtube_analysis.png", dpi=150, bbox_inches="tight")
print("Chart saved → output/youtube_analysis.png")

# ─────────────────────────────────────────
# Step 5: Key Insights
# ─────────────────────────────────────────
print("\n" + "=" * 55)
print("Step 5  Key Insights")
print("=" * 55)

top1        = df.loc[df["Subscribers (millions)"].idxmax()]
brand_avg   = df[df["is_brand"]]["Subscribers (millions)"].mean()
creator_avg = df[~df["is_brand"]]["Subscribers (millions)"].mean()
top_country = df["Country_clean"].value_counts().idxmax()
top_lang    = df["Primary language"].value_counts().idxmax()
music_avg   = df[df["Category_clean"] == "Music"]["Subscribers (millions)"].mean()
ent_avg     = df[df["Category_clean"] == "Entertainment"]["Subscribers (millions)"].mean()

print(f"\n👑 #1 Channel       : {top1['Name']} ({top1['Subscribers (millions)']:.0f}M subscribers)")
print(f"🏢 Brand avg        : {brand_avg:.1f}M  |  Creator avg: {creator_avg:.1f}M")
print(f"   Brand-to-Creator ratio: {brand_avg/creator_avg:.2f}x")
print(f"🌍 Most channels    : {top_country} ({df['Country_clean'].value_counts().max()} channels)")
print(f"🗣  Top language     : {top_lang} ({df['Primary language'].value_counts().max()} channels)")
print(f"🎵 Music avg        : {music_avg:.1f}M  |  Entertainment avg: {ent_avg:.1f}M")

# Export summary table
summary = df.groupby("Category_clean").agg(
    channel_count   =("Name",                   "count"),
    total_subs_M    =("Subscribers (millions)", "sum"),
    avg_subs_M      =("Subscribers (millions)", "mean"),
    brand_channels  =("is_brand",              "sum"),
).round(1).sort_values("total_subs_M", ascending=False)

summary.to_csv("output/category_summary.csv")
print("\nSummary table exported → output/category_summary.csv")
print(summary.to_string())
