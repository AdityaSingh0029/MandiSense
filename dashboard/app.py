import os
import pandas as pd
import streamlit as st
import plotly.express as px


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MandiSense | Supply Chain Intelligence",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #f7f9f7;
    }

    [data-testid="stSidebar"] {
        background: #102a1b;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero {
        padding: 28px 32px;
        border-radius: 20px;
        background: linear-gradient(135deg, #123d24, #236b3b);
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }

    .hero h1 {
        font-size: 42px;
        margin: 0;
        font-weight: 800;
    }

    .hero p {
        font-size: 17px;
        margin-top: 8px;
        opacity: 0.92;
    }

    .hero-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        background: rgba(255,255,255,0.15);
        font-size: 13px;
        margin-top: 12px;
    }

    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #e5ebe6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        min-height: 125px;
    }

    .kpi-label {
        color: #66736a !important;
        font-size: 14px;
        font-weight: 600;
    }

    .kpi-value {
        color: #123d24 !important;
        font-size: 28px;
        font-weight: 800;
        margin-top: 8px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #123d24 !important;
        margin-top: 12px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #6b756e !important;
        margin-bottom: 18px;
    }

    /* =====================================================
       INSIGHT BOX - FIXED TEXT COLOR
       ===================================================== */

    .insight {
        padding: 16px 18px;
        border-radius: 14px;
        background: #edf7ef;
        border-left: 5px solid #2f7d46;
        margin: 12px 0;
        color: #1b4332 !important;
        font-size: 15px;
        line-height: 1.6;
    }

    .insight b {
        color: #123d24 !important;
    }

    .insight strong {
        color: #123d24 !important;
    }

    .agent-box {
        padding: 22px;
        border-radius: 18px;
        background: white;
        border: 1px solid #dfe8e1;
        box-shadow: 0 5px 18px rgba(0,0,0,0.05);
        color: #1b4332 !important;
    }

    .agent-box h3 {
        color: #123d24 !important;
    }

    .agent-box p {
        color: #4f6357 !important;
    }

    .footer {
        text-align: center;
        color: #718078 !important;
        padding: 24px 0 10px 0;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_DIR = os.path.join(BASE_DIR, "data", "cleaned")


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    arrivals = pd.read_csv(
        os.path.join(CLEAN_DIR, "arrivals_clean.csv")
    )

    prices = pd.read_csv(
        os.path.join(CLEAN_DIR, "prices_clean.csv")
    )

    transport = pd.read_csv(
        os.path.join(CLEAN_DIR, "transport_clean.csv")
    )

    weather = pd.read_csv(
        os.path.join(CLEAN_DIR, "weather_daily.csv")
    )

    master = pd.read_csv(
        os.path.join(CLEAN_DIR, "mandi_master_clean.csv")
    )

    arrivals["arrival_quantity_qtl"] = pd.to_numeric(
        arrivals["arrival_quantity_qtl"],
        errors="coerce",
    )

    prices["modal_price"] = pd.to_numeric(
        prices["modal_price"],
        errors="coerce",
    )

    prices["msp"] = pd.to_numeric(
        prices["msp"],
        errors="coerce",
    )

    transport["transit_hours"] = pd.to_numeric(
        transport["transit_hours"],
        errors="coerce",
    )

    weather["rainfall_mm"] = pd.to_numeric(
        weather["rainfall_mm"],
        errors="coerce",
    )

    return arrivals, prices, transport, weather, master


arrivals, prices, transport, weather, master = load_data()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>🌾 MandiSense</h1>
        <p>Mandi-to-Market Supply Chain Intelligence</p>
        <div class="hero-badge">
            TransOrg AgentIQ Datathon 2026 • Track 3 AgriTech
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 🌾 MandiSense")
st.sidebar.caption("Supply Chain Intelligence Platform")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "📊 Executive Dashboard",
        "💰 Price vs MSP",
        "🌧️ Weather Impact",
        "🚚 Transport",
        "🤖 Ask MandiSense",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("From messy data → actionable decisions")


# =========================================================
# HELPER
# =========================================================

def section(title, subtitle=""):

    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True,
    )

    if subtitle:

        st.markdown(
            f'<div class="section-subtitle">{subtitle}</div>',
            unsafe_allow_html=True,
        )


def kpi(label, value):

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# EXECUTIVE DASHBOARD
# =========================================================

if page == "📊 Executive Dashboard":

    section(
        "Executive Dashboard",
        "A high-level view of mandi arrivals, market prices and logistics performance.",
    )

    crops = sorted(
        arrivals["crop_name"]
        .dropna()
        .astype(str)
        .unique()
    )

    mandis = sorted(
        arrivals["mandi_id"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_crop = st.sidebar.selectbox(
        "🌾 Crop",
        ["All"] + crops,
    )

    selected_mandi = st.sidebar.selectbox(
        "📍 Mandi",
        ["All"] + mandis,
    )

    df = arrivals.copy()

    if selected_crop != "All":
        df = df[df["crop_name"] == selected_crop]

    if selected_mandi != "All":
        df = df[df["mandi_id"] == selected_mandi]

    total_arrivals = df["arrival_quantity_qtl"].sum()

    avg_modal = prices["modal_price"].mean()

    valid_prices = prices.dropna(
        subset=["modal_price", "msp"]
    )

    below_msp = (
        valid_prices["modal_price"]
        < valid_prices["msp"]
    ).sum()

    avg_transit = transport["transit_hours"].mean()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi(
            "🌾 Total Arrivals",
            f"{total_arrivals:,.0f} Qtl",
        )

    with c2:
        kpi(
            "💰 Avg Modal Price",
            f"₹{avg_modal:,.0f}",
        )

    with c3:
        kpi(
            "⚠️ Below MSP",
            f"{below_msp:,}",
        )

    with c4:
        kpi(
            "🚚 Avg Transit",
            f"{avg_transit:.1f} hrs",
        )

    st.write("")

    st.markdown(
        """
        <div class="insight">
            <b>Decision Snapshot:</b>
            Use the dashboard to identify market pressure,
            arrival concentration and logistics bottlenecks.
        </div>
        """,
        unsafe_allow_html=True,
    )

    section(
        "Arrival Trend",
        "Daily agricultural arrival volume across the selected filters.",
    )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    )

    daily_arrivals = (
        df.groupby("date")["arrival_quantity_qtl"]
        .sum()
        .reset_index()
    )

    fig = px.area(
        daily_arrivals,
        x="date",
        y="arrival_quantity_qtl",
        title="Daily Crop Arrival Trend",
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode="x unified",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    c1, c2 = st.columns(2)

    with c1:

        section(
            "Top Mandis",
            "Mandis ranked by total arrival volume.",
        )

        top_mandis = (
            df.groupby("mandi_id")["arrival_quantity_qtl"]
            .sum()
            .reset_index()
            .sort_values(
                "arrival_quantity_qtl",
                ascending=False,
            )
            .head(10)
        )

        fig = px.bar(
            top_mandis,
            x="arrival_quantity_qtl",
            y="mandi_id",
            orientation="h",
            title="Top 10 Mandis",
        )

        fig.update_layout(
            height=430,
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with c2:

        section(
            "Crop Distribution",
            "Arrival volume by crop category.",
        )

        crop_volume = (
            df.groupby("crop_name")["arrival_quantity_qtl"]
            .sum()
            .reset_index()
            .sort_values(
                "arrival_quantity_qtl",
                ascending=False,
            )
        )

        fig = px.bar(
            crop_volume,
            x="crop_name",
            y="arrival_quantity_qtl",
            title="Crop-wise Arrival Distribution",
        )

        fig.update_layout(
            height=430,
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )


# =========================================================
# PRICE VS MSP
# =========================================================

elif page == "💰 Price vs MSP":

    section(
        "Price vs MSP",
        "Identify crops where wholesale modal prices are below Minimum Support Price.",
    )

    df = prices.dropna(
        subset=["modal_price", "msp"]
    ).copy()

    df["status"] = df.apply(
        lambda row:
        "Below MSP"
        if row["modal_price"] < row["msp"]
        else "At / Above MSP",
        axis=1,
    )

    below_count = (
        df["status"] == "Below MSP"
    ).sum()

    above_count = (
        df["status"] == "At / Above MSP"
    ).sum()

    c1, c2 = st.columns(2)

    with c1:
        kpi(
            "⚠️ Records Below MSP",
            f"{below_count:,}",
        )

    with c2:
        kpi(
            "✅ At / Above MSP",
            f"{above_count:,}",
        )

    st.write("")

    crop_price = (
        df.groupby("crop_name")[
            ["modal_price", "msp"]
        ]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        crop_price,
        x="crop_name",
        y=["modal_price", "msp"],
        barmode="group",
        title="Average Modal Price vs MSP",
        labels={
            "value": "Price",
            "crop_name": "Crop",
        },
    )

    fig.update_layout(
        height=470,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    section(
        "Price Pressure",
        "Number of observations where modal wholesale price is below MSP.",
    )

    crash = (
        df[df["status"] == "Below MSP"]
        .groupby("crop_name")
        .size()
        .reset_index(name="instances")
        .sort_values(
            "instances",
            ascending=False,
        )
    )

    fig = px.bar(
        crash,
        x="crop_name",
        y="instances",
        title="Below-MSP Instances by Crop",
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.markdown(
        f"""
        <div class="insight">
            <b>Market Signal:</b>
            {below_count:,} price observations have a modal price
            below MSP.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# WEATHER IMPACT
# =========================================================

elif page == "🌧️ Weather Impact":

    section(
        "Weather Impact",
        "Explore the relationship between rainfall and daily mandi arrival volume.",
    )

    arr = arrivals.copy()

    arr["date"] = pd.to_datetime(
        arr["date"],
        errors="coerce",
    )

    daily_arrivals = (
        arr.groupby("date")["arrival_quantity_qtl"]
        .sum()
        .reset_index()
    )

    w = weather.copy()

    w["date"] = pd.to_datetime(
        w["date"],
        errors="coerce",
    )

    merged = daily_arrivals.merge(
        w,
        on="date",
        how="inner",
    )

    merged = merged.dropna(
        subset=[
            "rainfall_mm",
            "arrival_quantity_qtl",
        ]
    )

    if len(merged) > 1:

        correlation = merged[
            "rainfall_mm"
        ].corr(
            merged["arrival_quantity_qtl"]
        )

        kpi(
            "🌧️ Rainfall ↔ Arrival Correlation",
            f"{correlation:.2f}",
        )

        st.write("")

        fig = px.scatter(
            merged,
            x="rainfall_mm",
            y="arrival_quantity_qtl",
            trendline="ols",
            title="Rainfall vs Crop Arrivals",
            labels={
                "rainfall_mm": "Rainfall (mm)",
                "arrival_quantity_qtl": "Daily Arrivals (Qtl)",
            },
        )

        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        st.markdown(
            """
            <div class="insight">
                <b>How to read this:</b>
                Each point represents an observed day.
                The trend line shows the overall linear relationship
                between rainfall and arrival volume.
                Correlation indicates association, not causation.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.warning(
            "Not enough matched weather and arrival records."
        )


# =========================================================
# TRANSPORT
# =========================================================

elif page == "🚚 Transport":

    section(
        "Transport & Logistics",
        "Compare average transit performance across destination warehouses.",
    )

    df = transport.dropna(
        subset=["transit_hours"]
    ).copy()

    warehouse = (
        df.groupby(
            "destination_warehouse"
        )["transit_hours"]
        .mean()
        .reset_index()
        .sort_values(
            "transit_hours",
            ascending=False,
        )
    )

    if not warehouse.empty:

        worst = warehouse.iloc[0]

        c1, c2 = st.columns(2)

        with c1:
            kpi(
                "🚚 Average Transit",
                f"{df['transit_hours'].mean():.1f} hrs",
            )

        with c2:
            kpi(
                "⚠️ Highest Avg Transit",
                f"{worst['transit_hours']:.1f} hrs",
            )

        st.write("")

        fig = px.bar(
            warehouse,
            x="destination_warehouse",
            y="transit_hours",
            title="Average Transit Time by Warehouse",
        )

        fig.update_layout(
            height=470,
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        st.markdown(
            f"""
            <div class="insight">
                <b>Operational Bottleneck:</b>
                {worst['destination_warehouse']} has the highest
                average transit time at
                {worst['transit_hours']:.2f} hours.
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# ASK MANDISENSE
# =========================================================

elif page == "🤖 Ask MandiSense":

    section(
        "Ask MandiSense",
        "Ask a business question and MandiSense will select the relevant analytical view.",
    )

    st.markdown(
        """
        <div class="agent-box">
            <h3>🤖 MandiSense Intelligence Assistant</h3>
            <p>
                Query the mandi, market, weather and logistics data
                using natural language.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown("### 💡 Example questions")

    examples = [
        "Show total arrivals by crop type",
        "Top 5 mandis by arrival volume",
        "Show Wheat arrival trend",
        "Which crops are below MSP?",
        "Which warehouse has highest transit delay?",
        "Show rainfall impact on arrivals",
    ]

    ex1, ex2, ex3 = st.columns(3)

    for i, example in enumerate(examples):

        with [ex1, ex2, ex3][i % 3]:
            st.info(example)

    question = st.text_input(
        "Ask your question",
        placeholder="Example: Which crops are below MSP?",
    )


    # =====================================================
    # AGENT FUNCTION
    # =====================================================

    def ask_agent(q):

        q = q.lower().strip()


        # ---------------------------------------------
        # TOTAL ARRIVALS
        # ---------------------------------------------

        if (
            "total arrivals" in q
            or "arrivals by crop" in q
            or "crop type" in q
        ):

            result = (
                arrivals
                .groupby("crop_name")[
                    "arrival_quantity_qtl"
                ]
                .sum()
                .reset_index()
                .sort_values(
                    "arrival_quantity_qtl",
                    ascending=False,
                )
            )

            fig = px.bar(
                result,
                x="crop_name",
                y="arrival_quantity_qtl",
                title="Total Crop Arrivals",
            )

            top = result.iloc[0]

            answer = (
                f"🌾 **{top['crop_name']}** has the highest "
                f"arrival volume with approximately "
                f"**{top['arrival_quantity_qtl']:,.0f} Qtl**."
            )

            return fig, answer


        # ---------------------------------------------
        # TOP MANDIS
        # ---------------------------------------------

        if (
            "top 5 mandi" in q
            or "top mandi" in q
        ):

            result = (
                arrivals
                .groupby("mandi_id")[
                    "arrival_quantity_qtl"
                ]
                .sum()
                .reset_index()
                .sort_values(
                    "arrival_quantity_qtl",
                    ascending=False,
                )
                .head(5)
            )

            fig = px.bar(
                result,
                x="mandi_id",
                y="arrival_quantity_qtl",
                title="Top 5 Mandis by Arrival Volume",
            )

            answer = (
                "📍 These are the **Top 5 mandis** "
                "by total agricultural arrival volume."
            )

            return fig, answer


        # ---------------------------------------------
        # WHEAT
        # ---------------------------------------------

        if (
            "wheat" in q
            and (
                "trend" in q
                or "arrival" in q
            )
        ):

            result = arrivals[
                arrivals["crop_name"]
                .astype(str)
                .str.lower()
                == "wheat"
            ].copy()

            if result.empty:
                return None, "No Wheat data found."

            result["date"] = pd.to_datetime(
                result["date"],
                errors="coerce",
            )

            result = (
                result.groupby("date")[
                    "arrival_quantity_qtl"
                ]
                .sum()
                .reset_index()
            )

            fig = px.line(
                result,
                x="date",
                y="arrival_quantity_qtl",
                title="Wheat Arrival Trend",
            )

            answer = (
                "🌾 The chart shows the daily Wheat "
                "arrival trend across the mandis."
            )

            return fig, answer


        # ---------------------------------------------
        # MSP
        # ---------------------------------------------

        if (
            "below msp" in q
            or "price crash" in q
        ):

            result = prices.dropna(
                subset=[
                    "modal_price",
                    "msp",
                ]
            ).copy()

            result = result[
                result["modal_price"]
                < result["msp"]
            ]

            crop_crash = (
                result
                .groupby("crop_name")
                .size()
                .reset_index(
                    name="instances"
                )
                .sort_values(
                    "instances",
                    ascending=False,
                )
            )

            fig = px.bar(
                crop_crash,
                x="crop_name",
                y="instances",
                title="Price Crash Instances by Crop",
            )

            answer = (
                f"⚠️ **{len(result):,}** records have "
                "a modal price below MSP."
            )

            return fig, answer


        # ---------------------------------------------
        # TRANSPORT
        # ---------------------------------------------

        if (
            "delay" in q
            or "transit" in q
            or "warehouse" in q
        ):

            result = transport.dropna(
                subset=["transit_hours"]
            ).copy()

            result = (
                result
                .groupby(
                    "destination_warehouse"
                )["transit_hours"]
                .mean()
                .reset_index()
                .sort_values(
                    "transit_hours",
                    ascending=False,
                )
            )

            if result.empty:
                return None, "No transport data found."

            fig = px.bar(
                result,
                x="destination_warehouse",
                y="transit_hours",
                title="Average Transit Time",
            )

            worst = result.iloc[0]

            answer = (
                f"🚚 **{worst['destination_warehouse']}** "
                f"has the highest average transit time "
                f"at **{worst['transit_hours']:.2f} hours**."
            )

            return fig, answer


        # ---------------------------------------------
        # WEATHER
        # ---------------------------------------------

        if (
            "rainfall" in q
            or "weather" in q
        ):

            arr = arrivals.copy()

            arr["date"] = pd.to_datetime(
                arr["date"],
                errors="coerce",
            )

            daily = (
                arr.groupby("date")[
                    "arrival_quantity_qtl"
                ]
                .sum()
                .reset_index()
            )

            w = weather.copy()

            w["date"] = pd.to_datetime(
                w["date"],
                errors="coerce",
            )

            merged = daily.merge(
                w,
                on="date",
                how="inner",
            )

            merged = merged.dropna(
                subset=[
                    "rainfall_mm",
                    "arrival_quantity_qtl",
                ]
            )

            if len(merged) < 2:

                return None, (
                    "Not enough weather data "
                    "to calculate the relationship."
                )

            correlation = merged[
                "rainfall_mm"
            ].corr(
                merged["arrival_quantity_qtl"]
            )

            fig = px.scatter(
                merged,
                x="rainfall_mm",
                y="arrival_quantity_qtl",
                trendline="ols",
                title="Rainfall vs Crop Arrivals",
            )

            answer = (
                f"🌧️ Rainfall and daily arrivals have "
                f"a correlation of **{correlation:.2f}**."
            )

            return fig, answer


        return None, (
            "I couldn't understand that question yet. "
            "Please try one of the example questions."
        )


    # =====================================================
    # RUN AGENT
    # =====================================================

    if question:

        with st.spinner(
            "🔎 Analyzing mandi data..."
        ):

            fig, answer = ask_agent(question)

        if fig is not None:

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        st.markdown("### 📌 Business Insight")

        st.markdown(answer)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🌾 <b>MandiSense</b> · TransOrg AgentIQ Datathon 2026 ·
        Mandi-to-Market Supply Chain Optimizer
    </div>
    """,
    unsafe_allow_html=True,
)