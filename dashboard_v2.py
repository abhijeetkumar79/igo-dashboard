import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IGO Market Intelligence 2026", layout="wide")

# ---------- LOAD ALL DATA ----------
fare_2026 = pd.read_csv("igo_fare_benchmark_2026.csv")
rapido_2025 = pd.read_csv("rapido_city_summary_2025.csv")
score = pd.read_csv("igo_city_opportunity_score_v3.csv")

# ---------- HEADER ----------
st.title("🚀 IGO Market Intelligence Dashboard")
st.caption("Rapido actual data (July 2025) + 2026 public estimates + City Opportunity Score")

# ---------- SIDEBAR ----------
st.sidebar.header("Filters")
selected_cities = st.sidebar.multiselect(
    "Select Cities",
    options=sorted(score["city"].unique()),
    default=sorted(score["city"].unique())
)
selected_platforms = st.sidebar.multiselect(
    "Select Platforms",
    options=sorted(fare_2026["platform"].unique()),
    default=sorted(fare_2026["platform"].unique())
)

fare_f = fare_2026[fare_2026["city"].isin(selected_cities) & fare_2026["platform"].isin(selected_platforms)]
score_f = score[score["city"].isin(selected_cities)]
rapido_f = rapido_2025[rapido_2025["Pickup_Location"].isin(selected_cities)]

# ---------- TABS ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏆 City Ranking", "📊 Rapido 2025 (Actual)", "💰 2026 Fare Estimates",
    "📈 2025 vs 2026 Comparison", "📋 Raw Data"
])

# ============ TAB 1: CITY RANKING ============
with tab1:
    st.subheader("City Opportunity Score (Higher = Better Focus)")
    fig = px.bar(
        score_f.sort_values("opportunity_score", ascending=True),
        x="opportunity_score", y="city", orientation="h",
        color="opportunity_score", color_continuous_scale="Blues",
        text="opportunity_score"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Top City", score_f.iloc[0]["city"],
                f"Score: {score_f.iloc[0]['opportunity_score']}")
    col2.metric("Verified Demand",
                ", ".join(score_f[score_f["has_verified"]]["city"].tolist()) or "None")
    col3.metric("Cities Analyzed", len(score_f))

# ============ TAB 2: RAPIDO 2025 ACTUAL DATA ============
with tab2:
    st.subheader("Rapido Actual Performance (July 2025 — 30,000 bookings)")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Bookings", f"{rapido_f['total_bookings'].sum():,}")
    col2.metric("Completed", f"{rapido_f['completed'].sum():,}")
    col3.metric("Cancelled", f"{rapido_f['cancelled'].sum():,}")
    col4.metric("Incomplete", f"{rapido_f['incomplete'].sum():,}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Completion Rate by City")
        fig_comp = px.bar(
            rapido_f.sort_values("completion_pct"),
            x="Pickup_Location", y="completion_pct",
            color="completion_pct", color_continuous_scale="RdYlGn",
            text="completion_pct"
        )
        fig_comp.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_comp.update_layout(height=400, showlegend=False,
                                yaxis_range=[78, 85])
        st.plotly_chart(fig_comp, use_container_width=True)

    with col2:
        st.subheader("Cancellation % by City")
        rapido_f["cancel_pct"] = (rapido_f["cancelled"] / rapido_f["total_bookings"] * 100).round(2)
        fig_cancel = px.bar(
            rapido_f.sort_values("cancel_pct", ascending=False),
            x="Pickup_Location", y="cancel_pct",
            color="cancel_pct", color_continuous_scale="Reds",
            text="cancel_pct"
        )
        fig_cancel.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig_cancel.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_cancel, use_container_width=True)

    st.markdown("---")

    st.subheader("Per-km Rate by City (Rapido Actual)")
    fig_pk = px.bar(
        rapido_f, x="Pickup_Location", y="mean_per_km",
        color="mean_per_km", color_continuous_scale="Blues",
        text="mean_per_km"
    )
    fig_pk.update_traces(texttemplate="₹%{text:.2f}", textposition="outside")
    fig_pk.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_pk, use_container_width=True)

    st.subheader("Operational Efficiency (TAT)")
    tat_df = rapido_f[["Pickup_Location", "avg_v_tat", "avg_c_tat"]].copy()
    tat_df.columns = ["City", "Vehicle TAT (min)", "Customer TAT (min)"]
    st.dataframe(tat_df, use_container_width=True)

# ============ TAB 3: 2026 FARE ESTIMATES ============
with tab3:
    st.subheader("2026 Public Fare Estimates (₹/km)")
    pivot = fare_f.pivot_table(
        index="city", columns="platform",
        values="per_km_rate_inr", aggfunc="mean"
    ).round(2)
    st.dataframe(pivot, use_container_width=True)

    fig_2026 = px.bar(
        fare_f.dropna(subset=["per_km_rate_inr"]),
        x="city", y="per_km_rate_inr", color="platform",
        barmode="group", title="2026 Estimated Per-km Rate by Platform"
    )
    fig_2026.update_layout(height=450)
    st.plotly_chart(fig_2026, use_container_width=True)

    st.caption("⚠️ These are public estimates (2026 guides), not actual platform rates. "
               "Use as benchmark only.")

# ============ TAB 4: 2025 vs 2026 COMPARISON ============
with tab4:
    st.subheader("Rapido 2025 Actual vs 2026 Public Estimates")

    # Map Rapido city names to score city names
    rapido_map = {"Bengaluru": "Bengaluru", "Chennai": "Chennai",
                  "Delhi": "Delhi NCR", "Hyderabad": "Hyderabad", "Pune": "Pune"}
    rapido_f["city"] = rapido_f["Pickup_Location"].map(rapido_map)

    # Rapido bike 2025 per-km
    rapido_compare = rapido_f[["city", "mean_per_km"]].copy()
    rapido_compare.columns = ["city", "Rapido 2025 (actual)"]

    # 2026 Rapido estimate
    r26 = fare_2026[fare_2026["platform"] == "Rapido"].groupby("city")["per_km_rate_inr"].mean().reset_index()
    r26.columns = ["city", "Rapido 2026 (estimate)"]

    comparison = rapido_compare.merge(r26, on="city", how="inner")
    comparison["change_%"] = ((comparison["Rapido 2026 (estimate)"]
                                - comparison["Rapido 2025 (actual)"])
                               / comparison["Rapido 2025 (actual)"] * 100).round(1)

    st.dataframe(comparison.round(2), use_container_width=True)

    fig_compare = px.bar(
        comparison.melt(id_vars="city", value_vars=["Rapido 2025 (actual)", "Rapido 2026 (estimate)"]),
        x="city", y="value", color="variable", barmode="group",
        title="Per-km Rate: 2025 Actual vs 2026 Estimate"
    )
    fig_compare.update_layout(height=450, yaxis_title="₹/km")
    st.plotly_chart(fig_compare, use_container_width=True)

    st.info("💡 Key insight: If 2026 estimates are close to 2025 actuals, market is stable. "
            "Large gaps may indicate data quality issues or real market shifts.")

# ============ TAB 5: RAW DATA ============
with tab5:
    st.subheader("Rapido 2025 City Summary")
    st.dataframe(rapido_f, use_container_width=True)
    st.subheader("2026 Fare Benchmark")
    st.dataframe(fare_f, use_container_width=True)
    st.subheader("Opportunity Score")
    st.dataframe(score_f, use_container_width=True)