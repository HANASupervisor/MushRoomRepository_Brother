
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================
# STEP 1. 그래프 스타일 및 한글 폰트 설정
# ==============================================

plt.rcParams["font.family"] = "Malgun Gothic"  # Windows
plt.rcParams["axes.unicode_minus"] = False

sns.set_theme(
    style="whitegrid",
    context="notebook",
    font="Malgun Gothic",
    rc={
        "axes.unicode_minus": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.alpha": 0.2,
        "font.size": 11,
    }
)

# 색상 정의
BLUE = "#3777C8"
PURPLE = "#7864C8"
PALETTE = {
    "가뭄": "#E6A64B",
    "일반강수": "#5A9BD5",
    "강한폭우": "#7764B4"
}

os.makedirs("output", exist_ok=True)


# ==============================================
# STEP 2. 엑셀 데이터 불러오기
# ==============================================

correlation_data = pd.read_excel(
    "brother_data.xlsx",
    sheet_name="correlation",
    header=0
)

boxplot_data = pd.read_excel(
    "brother_data.xlsx",
    sheet_name="boxplot",
    header=0
)

# 분석에 필요한 컬럼만 선택하고 결측값 제거
correlation_data = correlation_data[
    ["버섯 발생", "3일 강수량(mm)"]
].copy()

for col in correlation_data.columns:
    correlation_data[col] = pd.to_numeric(
        correlation_data[col], errors="coerce"
    )

correlation_data = correlation_data.dropna()

boxplot_data = boxplot_data[
    ["강수강도", "3일 강수량(mm)"]
].copy()

boxplot_data["3일 강수량(mm)"] = pd.to_numeric(
    boxplot_data["3일 강수량(mm)"],
    errors="coerce"
)

boxplot_data = boxplot_data.dropna()

print("상관계수:")
print(correlation_data.corr())


# ==============================================
# STEP 3. 산점도 + 회귀선
# ==============================================

x_col = "3일 강수량(mm)"
y_col = "버섯 발생"

r = correlation_data[x_col].corr(
    correlation_data[y_col]
)

fig, ax = plt.subplots(figsize=(9, 6))

sns.regplot(
    data=correlation_data,
    x=x_col,
    y=y_col,
    ax=ax,
    ci=95,
    color=BLUE,
    scatter_kws={
        "s": 75,
        "alpha": 0.75,
        "edgecolor": "white",
    },
    line_kws={
        "color": "#D44D5C",
        "linewidth": 2.5
    }
)

ax.set_title(
    "강수량과 버섯 발생의 상관관계",
    fontsize=17,
    fontweight="bold",
    pad=20
)

ax.set_xlabel("3일 누적 강수량 (mm)", fontsize=12)
ax.set_ylabel("버섯 발생", fontsize=12)

ax.text(
    0.04, 0.95,
    f"Pearson r = {r:.3f}\nN = {len(correlation_data)}",
    transform=ax.transAxes,
    fontsize=12,
    fontweight="bold",
    va="top",
    bbox={
        "boxstyle": "round,pad=0.6",
        "facecolor": "white",
        "edgecolor": "#DDDDDD",
        "alpha": 0.95
    }
)

plt.tight_layout()
plt.savefig(
    "output/01_correlation_scatter.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# ==============================================
# STEP 4. 상관계수 히트맵
# ==============================================

corr_matrix = correlation_data.corr()

fig, ax = plt.subplots(figsize=(7, 5.5))

sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".3f",
    cmap="RdBu_r",
    vmin=-1,
    vmax=1,
    center=0,
    square=True,
    linewidths=2,
    linecolor="white",
    annot_kws={
        "size": 15,
        "weight": "bold"
    },
    cbar_kws={
        "label": "Pearson 상관계수",
        "shrink": 0.8
    },
    ax=ax
)

ax.set_title(
    "변수 간 Pearson 상관계수",
    fontsize=17,
    fontweight="bold",
    pad=20
)

ax.tick_params(axis="x", rotation=0, labelsize=11)
ax.tick_params(axis="y", rotation=0, labelsize=11)

plt.tight_layout()
plt.savefig(
    "output/02_correlation_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


# ==============================================
# STEP 5. 강수강도별 박스플롯
# ==============================================

order = ["가뭄", "일반강수", "강한폭우"]

# 실제 데이터에 존재하는 범주만 사용
order = [
    category for category in order
    if category in boxplot_data["강수강도"].unique()
]

fig, ax = plt.subplots(figsize=(9, 6))

sns.boxplot(
    data=boxplot_data,
    x="강수강도",
    y="3일 강수량(mm)",
    hue="강수강도",
    order=order,
    hue_order=order,
    palette=PALETTE,
    dodge=False,
    legend=False,
    width=0.5,
    linewidth=1.5,
    showfliers=False,
    ax=ax
)

# 박스플롯 위에 실제 개별 관측값 표시
sns.stripplot(
    data=boxplot_data,
    x="강수강도",
    y="3일 강수량(mm)",
    order=order,
    color="#333333",
    size=5,
    alpha=0.5,
    jitter=0.18,
    ax=ax
)

# 그룹별 표본 수 표시
counts = boxplot_data["강수강도"].value_counts()

for i, category in enumerate(order):
    ax.text(
        i, -0.12,
        f"n = {counts[category]}",
        transform=ax.get_xaxis_transform(),
        ha="center",
        va="top",
        fontsize=10,
        color="#666666"
    )

ax.set_title(
    "강수강도별 3일 누적 강수량 분포",
    fontsize=17,
    fontweight="bold",
    pad=20
)

ax.set_xlabel("강수강도", fontsize=12)
ax.set_ylabel("3일 누적 강수량 (mm)", fontsize=12)

ax.grid(axis="x", visible=False)

plt.subplots_adjust(bottom=0.17)

plt.savefig(
    "output/03_rainfall_boxplot.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
