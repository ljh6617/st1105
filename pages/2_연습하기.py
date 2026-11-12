import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


st.set_page_config(page_title="펭귄 데이터 탐험", page_icon="🐧", layout="wide")

st.markdown(
    """
    <style>
    .block-container {padding-top: 2.2rem; padding-bottom: 3rem;}
    [data-testid="stMetric"] {
        background: #f3f7fb;
        border: 1px solid #e5edf5;
        padding: 16px 18px;
        border-radius: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

SPECIES_KO = {
    "Adelie": "아델리",
    "Chinstrap": "턱끈",
    "Gentoo": "젠투",
}
SEX_KO = {"Female": "암컷", "Male": "수컷"}
MEASURE_LABELS = {
    "bill_length_mm": "부리 길이 (mm)",
    "bill_depth_mm": "부리 높이 (mm)",
    "flipper_length_mm": "날개 길이 (mm)",
    "body_mass_g": "몸무게 (g)",
}


@st.cache_data
def load_penguins():
    data = sns.load_dataset("penguins")
    data["species_ko"] = data["species"].map(SPECIES_KO)
    data["sex_ko"] = data["sex"].map(SEX_KO).astype("object").fillna("정보 없음")
    return data


st.title("🐧 펭귄 데이터 탐험")
st.caption("Palmer Penguins 데이터로 펭귄의 종과 신체 특징을 살펴보세요.")

try:
    penguins = load_penguins()
except Exception as error:
    st.error("펭귄 데이터를 불러오지 못했어요. 인터넷 연결을 확인한 뒤 페이지를 새로고침해 주세요.")
    st.caption(f"상세 정보: {error}")
    st.stop()

with st.sidebar:
    st.header("데이터 필터")
    selected_species_ko = st.multiselect(
        "펭귄 종",
        options=list(SPECIES_KO.values()),
        default=list(SPECIES_KO.values()),
    )
    selected_islands = st.multiselect(
        "관측 섬",
        options=sorted(penguins["island"].dropna().unique().tolist()),
        default=sorted(penguins["island"].dropna().unique().tolist()),
    )
    selected_sexes = st.multiselect(
        "성별",
        options=["암컷", "수컷", "정보 없음"],
        default=["암컷", "수컷", "정보 없음"],
    )

    bill_min = int(penguins["bill_length_mm"].min())
    bill_max = int(penguins["bill_length_mm"].max())
    bill_range = st.slider(
        "부리 길이 범위 (mm)",
        min_value=bill_min,
        max_value=bill_max,
        value=(bill_min, bill_max),
    )
    st.divider()
    st.caption("필터를 바꾸면 지표와 그래프가 함께 업데이트됩니다.")

filtered = penguins[
    penguins["species_ko"].isin(selected_species_ko)
    & penguins["island"].isin(selected_islands)
    & penguins["sex_ko"].isin(selected_sexes)
    & penguins["bill_length_mm"].between(*bill_range)
].copy()

if filtered.empty:
    st.info("선택한 조건에 맞는 펭귄이 없어요. 사이드바 필터를 넓혀 보세요.")
    st.stop()

metric_columns = st.columns(4)
body_mass_values = filtered["body_mass_g"].dropna()
metric_columns[0].metric("펭귄 수", f"{len(filtered):,}마리", f"전체 {len(penguins):,}마리 중")
metric_columns[1].metric(
    "평균 몸무게",
    f"{body_mass_values.mean():,.0f} g" if not body_mass_values.empty else "데이터 없음",
)
metric_columns[2].metric("평균 부리 길이", f"{filtered['bill_length_mm'].mean():.1f} mm")
metric_columns[3].metric("관측된 종", f"{filtered['species'].nunique()}종")

st.subheader("종별 신체 특징")
left, right = st.columns((1.6, 1))

with left:
    scatter_x = st.selectbox(
        "가로축",
        options=list(MEASURE_LABELS),
        format_func=lambda key: MEASURE_LABELS[key],
        index=0,
    )
    scatter_y = st.selectbox(
        "세로축",
        options=list(MEASURE_LABELS),
        format_func=lambda key: MEASURE_LABELS[key],
        index=1,
    )
    scatter_data = filtered.dropna(subset=[scatter_x, scatter_y])
    fig, ax = plt.subplots(figsize=(9, 5.2))
    if not scatter_data.empty:
        sns.scatterplot(
            data=scatter_data,
            x=scatter_x,
            y=scatter_y,
            hue="species_ko",
            hue_order=[name for name in SPECIES_KO.values() if name in selected_species_ko],
            style="sex_ko",
            palette="Set2",
            alpha=0.82,
            s=72,
            ax=ax,
        )
        ax.set_xlabel(MEASURE_LABELS[scatter_x])
        ax.set_ylabel(MEASURE_LABELS[scatter_y])
        ax.grid(axis="both", alpha=0.2)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(title="종 · 성별", frameon=False, bbox_to_anchor=(1.02, 1), loc="upper left")
    else:
        ax.text(0.5, 0.5, "선택한 조건에 표시할 데이터가 없습니다.", ha="center", va="center")
        ax.set_axis_off()
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with right:
    st.markdown("#### 종별 개체 수")
    counts = (
        filtered.groupby("species_ko", observed=True)
        .size()
        .reindex([name for name in SPECIES_KO.values() if name in selected_species_ko])
        .dropna()
        .rename("개체 수")
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(6, 5.2))
    sns.barplot(data=counts, x="species_ko", y="개체 수", hue="species_ko", palette="Set2", ax=ax)
    if ax.legend_ is not None:
        ax.legend_.remove()
    ax.set_xlabel("")
    ax.set_ylabel("개체 수")
    ax.grid(axis="y", alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for container in ax.containers:
        ax.bar_label(container, padding=3, fmt="%.0f")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

tab_body, tab_corr, tab_data = st.tabs(["몸무게 비교", "특징 간 상관관계", "데이터 보기"])

with tab_body:
    st.markdown("#### 종과 성별에 따른 몸무게")
    body_data = filtered.dropna(subset=["body_mass_g"])
    if body_data.empty:
        st.info("선택한 조건의 몸무게 데이터가 없어요.")
    else:
        fig, ax = plt.subplots(figsize=(10, 4.8))
        sns.boxplot(
            data=body_data,
            x="species_ko",
            y="body_mass_g",
            hue="sex_ko",
            order=[name for name in SPECIES_KO.values() if name in selected_species_ko],
            hue_order=[name for name in ["암컷", "수컷", "정보 없음"] if name in selected_sexes],
            palette="pastel",
            ax=ax,
        )
        ax.set_xlabel("펭귄 종")
        ax.set_ylabel("몸무게 (g)")
        ax.grid(axis="y", alpha=0.2)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(title="성별", frameon=False)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

with tab_corr:
    st.markdown("#### 신체 측정값 상관관계")
    numeric_data = filtered[list(MEASURE_LABELS)].dropna()
    if len(numeric_data) < 2:
        st.info("상관관계를 계산하기에 데이터가 부족해요.")
    else:
        corr = numeric_data.corr().rename(index=MEASURE_LABELS, columns=MEASURE_LABELS)
        fig, ax = plt.subplots(figsize=(8, 5.5))
        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="vlag",
            center=0,
            vmin=-1,
            vmax=1,
            square=True,
            linewidths=0.5,
            ax=ax,
        )
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.caption("상관계수는 두 측정값이 함께 변하는 정도를 나타내며, 인과관계를 뜻하지는 않습니다.")

with tab_data:
    st.markdown("#### 필터링된 펭귄 데이터")
    display_columns = {
        "species_ko": "종",
        "island": "관측 섬",
        "sex_ko": "성별",
        **MEASURE_LABELS,
    }
    display_data = filtered[list(display_columns)].rename(columns=display_columns)
    st.dataframe(display_data, use_container_width=True, hide_index=True)
    st.download_button(
        "필터된 데이터 CSV 다운로드",
        data=display_data.to_csv(index=False).encode("utf-8-sig"),
        file_name="penguins_filtered.csv",
        mime="text/csv",
    )

st.caption("데이터 출처: Palmer Penguins · 종별/성별 결측치는 각 그래프에서 필요한 경우 제외됩니다.")
