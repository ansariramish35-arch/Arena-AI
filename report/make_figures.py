"""Generate every figure used in the Summer Internship Report."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import daily_data as DD

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "axes.edgecolor": "#333333",
    "axes.linewidth": 0.8,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
})

NAVY = "#1f3864"
BLUE = "#2e75b6"
LBLUE = "#9dc3e6"
ORANGE = "#c55a11"
RED = "#c00000"
GREEN = "#548235"
GREY = "#7f7f7f"
GOLD = "#bf9000"

MONTHS = DD.MONTHS
DATA = DD.build()

def _mm(k):
    return [float(np.mean(DATA[k][DATA["month"] == m])) for m in MONTHS]

# ---- Monthly mean concentrations derived from the daily dataset -----------
PM25 = _mm("PM25")
PM10 = _mm("PM10")
NO2 = _mm("NO2")
SO2 = _mm("SO2")
CO = _mm("CO")
O3 = _mm("O3")
AQI = [int(round(v)) for v in _mm("AQI")]

SEASON = {"Winter (Nov-Feb)": [0, 1, 10, 11],
          "Summer (Mar-Jun)": [2, 3, 4, 5],
          "Monsoon (Jul-Sep)": [6, 7, 8],
          "Post-Monsoon (Oct)": [9]}


def monthly_days(key, months):
    """All daily values of `key` falling in the given month indices."""
    out = []
    for i in months:
        out.extend(DATA[key][DATA["month"] == MONTHS[i]])
    return np.array(out, dtype=float)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------- Figure 1.1
def fig_ecosystem():
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    layers = [
        (4.75, "APPLICATION LAYER", "Jupyter Notebook  |  Google Colab  |  VS Code", LBLUE),
        (3.40, "VISUALISATION LAYER", "Matplotlib  |  Seaborn  |  Plotly", "#f8cbad"),
        (2.05, "ANALYSIS LAYER", "Pandas  |  NumPy  |  SciPy", "#c6e0b4"),
        (0.70, "DATA LAYER", "CSV / Excel files  |  Public AQI records", "#d9d9d9"),
    ]
    for y, title, sub, col in layers:
        ax.add_patch(FancyBboxPatch((0.4, y), 9.2, 1.05,
                                    boxstyle="round,pad=0.02,rounding_size=0.12",
                                    facecolor=col, edgecolor=NAVY, linewidth=0.9))
        ax.text(1.0, y + 0.66, title, fontsize=7.5, fontweight="bold", color=NAVY)
        ax.text(1.0, y + 0.24, sub, fontsize=8, color="#222222")
        if y > 0.7:
            ax.add_patch(FancyArrowPatch((5.0, y + 1.10), (5.0, y + 1.30),
                                         arrowstyle="-|>", mutation_scale=9,
                                         color=NAVY, linewidth=1.0))
    ax.text(5.0, 5.85, "Python Data-Visualisation Stack", ha="center",
            fontsize=10, fontweight="bold", color=NAVY)
    save(fig, "fig_ecosystem.png")


# ---------------------------------------------------------------- Figure 1.2
def fig_pipeline():
    fig, ax = plt.subplots(figsize=(6.6, 2.6))
    ax.set_xlim(0, 12.2); ax.set_ylim(0, 4); ax.axis("off")
    steps = ["Problem\nDefinition", "Data\nCollection", "Data\nCleaning",
             "Exploratory\nAnalysis", "Visualisation", "Report"]
    w, gap = 1.70, 0.42
    x = 0.25
    for i, s in enumerate(steps):
        col = BLUE if i % 2 == 0 else NAVY
        ax.add_patch(FancyBboxPatch((x, 1.9), w, 1.15,
                                    boxstyle="round,pad=0.02,rounding_size=0.10",
                                    facecolor=col, edgecolor="none"))
        ax.text(x + w / 2, 2.47, s, ha="center", va="center",
                fontsize=5.9, color="white", fontweight="bold", linespacing=1.3)
        ax.text(x + w / 2, 3.35, str(i + 1), ha="center", va="center",
                fontsize=7, color=NAVY, fontweight="bold")
        if i < len(steps) - 1:
            ax.add_patch(FancyArrowPatch((x + w + 0.06, 2.47),
                                         (x + w + gap - 0.06, 2.47),
                                         arrowstyle="-|>", mutation_scale=9,
                                         color=GREY, linewidth=1.0))
        x += w + gap
    ax.text(6.0, 0.95, "Iterative refinement loops back to any earlier stage",
            ha="center", fontsize=7, style="italic", color=GREY)
    save(fig, "fig_pipeline.png")


# ---------------------------------------------------------------- Figure 3.1
def fig_aqi_scale():
    cats = ["Good\n(0-50)", "Satisfactory\n(51-100)", "Moderate\n(101-200)",
            "Poor\n(201-300)", "Very Poor\n(301-400)", "Severe\n(401-500)"]
    cols = ["#00b050", "#92d050", "#ffff00", "#ff7c00", "#ff0000", "#c00000"]
    fig, ax = plt.subplots(figsize=(6.2, 1.9))
    for i, (c, col) in enumerate(zip(cats, cols)):
        ax.barh(0, 1, left=i, color=col, edgecolor="white", height=0.55)
        ax.text(i + 0.5, 0, c, ha="center", va="center", fontsize=6.6,
                color="white" if i > 3 else "#1a1a1a", fontweight="bold",
                linespacing=1.3)
    ax.set_xlim(0, 6); ax.set_ylim(-0.6, 0.9); ax.axis("off")
    ax.text(3.0, 0.72, "CPCB National Air Quality Index (AQI) Categories",
            ha="center", fontsize=9, fontweight="bold", color=NAVY)
    save(fig, "fig_aqi_scale.png")


# ---------------------------------------------------------------- Figure 4.1
def fig_monthly_aqi():
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    x = np.arange(12)
    ax.plot(x, AQI, marker="o", color=NAVY, linewidth=1.6, markersize=4.5,
            label="Monthly mean AQI")
    ax.axhline(np.mean(AQI), color=RED, linestyle="--", linewidth=1.0,
               label=f"Annual mean = {np.mean(AQI):.0f}")
    ax.fill_between(x, AQI, np.mean(AQI), where=np.array(AQI) >= np.mean(AQI),
                    color=ORANGE, alpha=0.18)
    for xi, v in zip(x, AQI):
        ax.annotate(str(v), (xi, v), textcoords="offset points", xytext=(0, 13),
                    ha="center", fontsize=6.4, color=NAVY,
                    bbox=dict(boxstyle="round,pad=0.12", facecolor="white",
                              edgecolor="none", alpha=0.85))
    ax.set_xticks(x); ax.set_xticklabels(MONTHS)
    ax.set_ylabel("AQI (dimensionless)")
    ax.set_ylim(40, 400)
    ax.set_title("Monthly Variation of Air Quality Index in Lucknow")
    ax.legend(frameon=False, loc="upper center", ncol=2,
              bbox_to_anchor=(0.5, -0.13))
    ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    save(fig, "fig_monthly_aqi.png")


# ---------------------------------------------------------------- Figure 4.2
def fig_seasonal_bar():
    labels, vals = [], []
    for s, idx in SEASON.items():
        labels.append(s.replace(" (", "\n("))
        vals.append(np.mean([PM25[i] for i in idx]))
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    bars = ax.bar(labels, vals, color=[BLUE, ORANGE, GREEN, GOLD],
                  width=0.58, edgecolor=NAVY, linewidth=0.6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 3, f"{v:.0f}",
                ha="center", fontsize=8, fontweight="bold", color=NAVY)
    ax.set_ylabel("Mean PM$_{2.5}$ ($\\mu g/m^3$)")
    ax.set_title("Season-wise Mean PM$_{2.5}$ Concentration")
    ax.set_ylim(0, 175)
    ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    save(fig, "fig_seasonal_bar.png")


# ---------------------------------------------------------------- Figure 4.3
def fig_pie():
    # share of the total sub-index load contributed by each pollutant
    raw = {}
    for k in ["PM25", "PM10", "NO2", "SO2", "CO", "O3"]:
        raw[k] = float(np.mean([DD.sub_index(k, c) for c in DATA[k]]))
    order = ["PM25", "PM10", "NO2", "O3", "CO", "SO2"]
    tot = sum(raw[k] for k in order)
    vals = [raw[k] / tot * 100 for k in order]
    disp = {"PM25": "PM$_{2.5}$", "PM10": "PM$_{10}$", "NO2": "NO$_2$",
            "O3": "O$_3$", "CO": "CO", "SO2": "SO$_2$"}
    labels = [f"{disp[k]}\n{v:.0f}%" for k, v in zip(order, vals)]
    cols = [NAVY, BLUE, LBLUE, ORANGE, GOLD, GREY]
    fig, ax = plt.subplots(figsize=(4.6, 3.3))
    w, _ = ax.pie(vals, colors=cols, startangle=88,
                  wedgeprops=dict(width=0.42, edgecolor="white", linewidth=1.4))
    ax.legend(w, labels, loc="center left", bbox_to_anchor=(0.92, 0.5),
              frameon=False, fontsize=7.5)
    ax.text(0, 0, "Pollutant\nshare", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color=NAVY)
    ax.set_title("Contribution of Pollutants to Overall AQI Load", pad=12)
    save(fig, "fig_pie.png")


# ---------------------------------------------------------------- Figure 4.4
def fig_heatmap():
    names = ["PM$_{2.5}$", "PM$_{10}$", "NO$_2$", "SO$_2$", "CO", "O$_3$", "AQI"]
    data = np.vstack([DATA[k] for k in ["PM25", "PM10", "NO2", "SO2", "CO",
                                        "O3", "AQI"]]).astype(float)
    c = np.corrcoef(data)
    fig, ax = plt.subplots(figsize=(4.9, 4.0))
    im = ax.imshow(c, cmap="RdYlBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(names))); ax.set_xticklabels(names)
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names)
    for i in range(len(names)):
        for j in range(len(names)):
            ax.text(j, i, f"{c[i, j]:.2f}", ha="center", va="center",
                    fontsize=6.6,
                    color="white" if abs(c[i, j]) > 0.65 else "#1a1a1a")
    ax.set_title("Correlation Matrix of Pollutants and AQI")
    fig.colorbar(im, ax=ax, shrink=0.82, label="Pearson r")
    save(fig, "fig_heatmap.png")


# ---------------------------------------------------------------- Figure 4.5
def fig_boxplot():
    data, labels = [], []
    for s, idx in SEASON.items():
        data.append(monthly_days("PM25", idx))
        labels.append(s.split(" ")[0])
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    bp = ax.boxplot(data, tick_labels=labels, patch_artist=True, widths=0.5,
                    medianprops=dict(color=RED, linewidth=1.4),
                    flierprops=dict(marker="o", markersize=2.5,
                                    markerfacecolor=GREY, markeredgecolor=GREY))
    for patch, col in zip(bp["boxes"], [BLUE, ORANGE, GREEN, GOLD]):
        patch.set_facecolor(col); patch.set_alpha(0.65)
        patch.set_edgecolor(NAVY)
    ax.set_ylabel("Daily PM$_{2.5}$ ($\\mu g/m^3$)")
    ax.set_xlabel("Season")
    ax.set_title("Distribution of Daily PM$_{2.5}$ Values by Season")
    ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    save(fig, "fig_boxplot.png")


# ---------------------------------------------------------------- Figure 4.6
def fig_histogram():
    days = DATA["AQI"]
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    ax.hist(days, bins=22, color=LBLUE, edgecolor=NAVY, linewidth=0.7)
    ax.set_ylim(0, 56)
    for xv, lab, col in [(100, "Satisfactory", GREEN), (200, "Moderate", GOLD),
                         (300, "Poor", ORANGE), (400, "Very Poor", RED)]:
        ax.axvline(xv, color=col, linestyle="--", linewidth=1.0)
        ax.text(xv, 40.5, lab, fontsize=6.2, color=col, rotation=90,
                ha="center", va="bottom")
    ax.set_xlabel("Daily AQI")
    ax.set_ylabel("Number of days")
    ax.set_title("Frequency Distribution of Daily AQI Values", pad=18)
    ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    save(fig, "fig_histogram.png")


# ---------------------------------------------------------------- Figure 4.7
def fig_stacked():
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    x = np.arange(12)
    series = [("PM$_{2.5}$", PM25, NAVY), ("PM$_{10}$", PM10, BLUE),
              ("NO$_2$", NO2, LBLUE), ("O$_3$", O3, ORANGE),
              ("SO$_2$", SO2, GOLD), ("CO ($\\times$25)", [v * 25 for v in CO], GREY)]
    bottom = np.zeros(12)
    for name, vals, col in series:
        ax.bar(x, vals, bottom=bottom, color=col, label=name,
               width=0.68, edgecolor="white", linewidth=0.4)
        bottom += np.array(vals, dtype=float)
    ax.set_xticks(x); ax.set_xticklabels(MONTHS)
    ax.set_ylabel("Concentration ($\\mu g/m^3$)")
    ax.set_title("Month-wise Stacked Pollutant Concentration Profile")
    ax.legend(ncol=3, frameon=False, loc="upper center",
              bbox_to_anchor=(0.5, -0.16))
    ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    save(fig, "fig_stacked.png")


# ---------------------------------------------------------------- Figure 4.8
def fig_categories():
    days = DATA["AQI"]
    bins = [0, 50, 100, 200, 300, 400, 500]
    labels = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
    counts = [int(np.sum((days >= bins[i]) & (days < bins[i + 1])))
              for i in range(6)]
    cols = ["#00b050", "#92d050", "#ffff00", "#ff7c00", "#ff0000", "#c00000"]
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    bars = ax.bar(labels, counts, color=cols, edgecolor=NAVY, width=0.6,
                  linewidth=0.6)
    for b, c in zip(bars, counts):
        ax.text(b.get_x() + b.get_width() / 2, c + 2,
                f"{c}\n({c / sum(counts) * 100:.1f}%)", ha="center",
                fontsize=7, color=NAVY)
    ax.set_ylabel("Number of days")
    ax.set_title("Number of Days in Each AQI Category (Whole Year)")
    ax.set_ylim(0, max(counts) * 1.28)
    ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    save(fig, "fig_categories.png")


# ---------------------------------------------------------------- Figure 4.9
def fig_scatter():
    x = DATA["PM25"]
    y = DATA["AQI"]
    fig, ax = plt.subplots(figsize=(5.4, 3.1))
    ax.scatter(x, y, s=9, alpha=0.55, color=BLUE, edgecolor="none", zorder=3)
    m, c = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 50)
    r = np.corrcoef(x, y)[0, 1]
    ax.plot(xs, m * xs + c, color=RED, linewidth=1.3,
            label=f"Least-squares fit: AQI = {m:.2f} PM$_{{2.5}}$ {c:+.1f}\n"
                  f"Pearson r = {r:.2f},  $R^2$ = {r ** 2:.2f}")
    ax.set_ylim(0, 470)
    ax.set_xlabel("PM$_{2.5}$ ($\\mu g/m^3$)")
    ax.set_ylabel("AQI")
    ax.set_title("Relation between PM$_{2.5}$ and AQI")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.16))
    ax.grid(linestyle=":", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    save(fig, "fig_scatter.png")


# --------------------------------------------------------------- Figure 4.10
def fig_compare():
    delhi = [345, 288, 232, 205, 192, 168, 118, 104, 148, 245, 338, 372]
    kanpur = [326, 271, 216, 188, 178, 152, 105, 92, 128, 214, 318, 350]
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ax.plot(MONTHS, delhi, marker="s", markersize=3.6, color=RED,
            linewidth=1.4, label="Delhi")
    ax.plot(MONTHS, kanpur, marker="^", markersize=3.8, color=ORANGE,
            linewidth=1.4, label="Kanpur")
    ax.plot(MONTHS, AQI, marker="o", markersize=4, color=NAVY,
            linewidth=1.7, label="Lucknow")
    ax.set_ylabel("Monthly mean AQI")
    ax.set_title("Comparison of Lucknow with Delhi and Kanpur")
    ax.legend(frameon=False, ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, -0.14))
    ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    save(fig, "fig_compare.png")


# --------------------------------------------------------------- Figure 4.11
def fig_dayofweek():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    vals = [float(np.mean(DATA["AQI"][DATA["dow"] == i])) for i in range(7)]
    fig, ax = plt.subplots(figsize=(6.2, 2.7))
    bars = ax.bar(days, vals, color=[BLUE] * 5 + [LBLUE, GREEN],
                  edgecolor=NAVY, linewidth=0.6, width=0.58)
    ax.axhline(np.mean(vals), color=RED, linestyle="--", linewidth=1.0,
               label="Weekly mean")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 2.5, f"{v:.0f}",
                ha="center", fontsize=7.5, color=NAVY)
    ax.set_ylim(min(vals) - 30, max(vals) + 25)
    ax.set_ylabel("Mean AQI")
    ax.set_title("Day-of-Week Pattern of Air Quality")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    save(fig, "fig_dayofweek.png")


# --------------------------------------------------------------- Figure 4.12
def fig_month_pollutant_heat():
    names = ["PM$_{2.5}$", "PM$_{10}$", "NO$_2$", "SO$_2$", "O$_3$"]
    data = np.array([PM25, PM10, NO2, SO2, O3], dtype=float)
    norm = data / data.max(axis=1, keepdims=True)
    fig, ax = plt.subplots(figsize=(6.2, 2.6))
    im = ax.imshow(norm, cmap="YlOrRd", aspect="auto", vmin=0.05, vmax=1)
    ax.set_xticks(range(12)); ax.set_xticklabels(MONTHS)
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names)
    for i in range(len(names)):
        for j in range(12):
            ax.text(j, i, f"{data[i, j]:.0f}", ha="center", va="center",
                    fontsize=6, color="white" if norm[i, j] > 0.62 else "#1a1a1a")
    ax.set_title("Month-wise Pollutant Intensity Heat Map")
    fig.colorbar(im, ax=ax, shrink=0.85, label="Normalised intensity")
    save(fig, "fig_month_pollutant.png")


# ---------------------------------------------------------------- Figure 5.1
def fig_aqi_formula():
    fig, ax = plt.subplots(figsize=(6.0, 2.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.2); ax.axis("off")
    ax.text(5, 2.5, "Linear Interpolation used by the CPCB Sub-Index",
            ha="center", fontsize=9, fontweight="bold", color=NAVY)
    ax.add_patch(FancyBboxPatch((0.6, 0.75), 8.8, 1.15,
                                boxstyle="round,pad=0.03,rounding_size=0.12",
                                facecolor="#eef3fa", edgecolor=NAVY, linewidth=0.9))
    ax.text(5, 1.32,
            r"$I_p = \dfrac{I_{HI}-I_{LO}}{BP_{HI}-BP_{LO}}\,(C_p-BP_{LO}) + I_{LO}$",
            ha="center", va="center", fontsize=14, color=NAVY)
    ax.text(5, 0.35, "AQI = max($I_p$) over all pollutants p",
            ha="center", fontsize=8.5, style="italic", color="#333333")
    save(fig, "fig_aqi_formula.png")


# ---------------------------------------------------------------- Figure 5.2
def fig_chart_types():
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
    items = [("Line chart", "trend over time", 0.3, 3.35),
             ("Bar chart", "compare categories", 6.2, 3.35),
             ("Pie chart", "part-to-whole", 0.3, 0.55),
             ("Scatter plot", "relationship", 6.2, 0.55)]
    for title, sub, x, y in items:
        ax.add_patch(FancyBboxPatch((x, y), 5.5, 2.1,
                                    boxstyle="round,pad=0.02,rounding_size=0.10",
                                    facecolor="#f2f2f2", edgecolor=GREY, linewidth=0.8))
        ax.text(x + 0.35, y + 1.45, title, fontsize=9, fontweight="bold", color=NAVY)
        ax.text(x + 0.35, y + 0.78, "Used for " + sub, fontsize=8, color="#333333")
    save(fig, "fig_chart_types.png")


for fn in (fig_ecosystem, fig_pipeline, fig_aqi_scale, fig_monthly_aqi,
           fig_seasonal_bar, fig_pie, fig_heatmap, fig_boxplot, fig_histogram,
           fig_stacked, fig_categories, fig_scatter, fig_compare,
           fig_dayofweek, fig_month_pollutant_heat, fig_aqi_formula,
           fig_chart_types):
    fn()

print("\nAll figures generated in", OUT)
