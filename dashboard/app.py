import os
import pandas as pd
import streamlit as st
import plotly.express as px


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

    # Convert numeric columns safely
    arrivals["arrival_quantity_qtl"] = pd.to_numeric(
        arrivals["arrival_quantity_qtl"],
        errors="coerce"
    )

    prices["modal_price"] = pd.to_numeric(
        prices["modal_price"],
        errors="coerce"
    )

    prices["msp"] = pd.to_numeric(
        prices["msp"],
        errors="coerce"
    )

    transport["transit_hours"] = pd.to_numeric(
        transport["transit_hours"],
        errors="coerce"
    )

    weather["rainfall_mm"] = pd.to_numeric(
        weather["rainfall_mm"],
        errors="coerce"
    )

    return arrivals, prices, transport, weather, master


arrivals, prices, transport, weather, master = load_data()


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MandiSense",
    page_icon="🌾",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🌾 MandiSense")

st.subheader(
    "Mandi-to-Market Supply Chain Intelligence"
)

st.write(
    "From messy agricultural data to actionable insights "
    "across arrivals, prices, weather and transportation."
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎛️ MandiSense")

page = st.sidebar.radio(
    "Select Module",
    [
        "📊 Executive Dashboard",
        "💰 Price vs MSP",
        "🌧️ Weather Impact",
        "🚚 Transport",
        "🤖 Ask MandiSense"
    ]
)


# =========================================================
# EXECUTIVE DASHBOARD
# =========================================================

if page == "📊 Executive Dashboard":

    st.header("📊 Executive Dashboard")

    # -----------------------------
    # FILTERS
    # -----------------------------

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
        "Select Crop",
        ["All"] + crops
    )

    selected_mandi = st.sidebar.selectbox(
        "Select Mandi",
        ["All"] + mandis
    )

    df = arrivals.copy()

    if selected_crop != "All":

        df = df[
            df["crop_name"] == selected_crop
        ]

    if selected_mandi != "All":

        df = df[
            df["mandi_id"] == selected_mandi
        ]

    # -----------------------------
    # KPIs
    # -----------------------------

    total_arrivals = df[
        "arrival_quantity_qtl"
    ].sum()

    avg_modal = prices[
        "modal_price"
    ].mean()

    valid_prices = prices.dropna(
        subset=["modal_price", "msp"]
    )

    below_msp = (
        valid_prices["modal_price"]
        < valid_prices["msp"]
    ).sum()

    avg_transit = transport[
        "transit_hours"
    ].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🌾 Total Arrivals",
        f"{total_arrivals:,.0f} Qtl"
    )

    col2.metric(
        "💰 Avg Modal Price",
        f"₹{avg_modal:,.0f}"
    )

    col3.metric(
        "⚠️ Below MSP",
        f"{below_msp:,}"
    )

    col4.metric(
        "🚚 Avg Transit",
        f"{avg_transit:.1f} hrs"
    )

    st.divider()

    # -----------------------------
    # ARRIVAL TREND
    # -----------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    daily_arrivals = (
        df.groupby("date")[
            "arrival_quantity_qtl"
        ]
        .sum()
        .reset_index()
    )

    fig = px.line(
        daily_arrivals,
        x="date",
        y="arrival_quantity_qtl",
        title="Daily Crop Arrival Trend"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Arrival Quantity (Qtl)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------
    # TOP MANDIS
    # -----------------------------

    top_mandis = (
        df.groupby("mandi_id")[
            "arrival_quantity_qtl"
        ]
        .sum()
        .reset_index()
        .sort_values(
            "arrival_quantity_qtl",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_mandis,
        x="mandi_id",
        y="arrival_quantity_qtl",
        title="Top 10 Mandis by Arrival Volume"
    )

    fig.update_layout(
        xaxis_title="Mandi",
        yaxis_title="Arrival Quantity (Qtl)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------
    # CROP DISTRIBUTION
    # -----------------------------

    crop_volume = (
        df.groupby("crop_name")[
            "arrival_quantity_qtl"
        ]
        .sum()
        .reset_index()
        .sort_values(
            "arrival_quantity_qtl",
            ascending=False
        )
    )

    fig = px.bar(
        crop_volume,
        x="crop_name",
        y="arrival_quantity_qtl",
        title="Crop-wise Arrival Distribution"
    )

    fig.update_layout(
        xaxis_title="Crop",
        yaxis_title="Arrival Quantity (Qtl)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# PRICE VS MSP
# =========================================================

elif page == "💰 Price vs MSP":

    st.header("💰 Price vs MSP Analysis")

    df = prices.copy()

    df = df.dropna(
        subset=[
            "modal_price",
            "msp"
        ]
    )

    df["status"] = df.apply(
        lambda row:
        "Below MSP"
        if row["modal_price"] < row["msp"]
        else "At / Above MSP",
        axis=1
    )

    # -----------------------------
    # PRICE COMPARISON
    # -----------------------------

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
        y=[
            "modal_price",
            "msp"
        ],
        barmode="group",
        title="Average Modal Price vs MSP"
    )

    fig.update_layout(
        xaxis_title="Crop",
        yaxis_title="Price"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------
    # PRICE CRASH
    # -----------------------------

    crash = (
        df[
            df["status"] == "Below MSP"
        ]
        .groupby("crop_name")
        .size()
        .reset_index(
            name="instances"
        )
        .sort_values(
            "instances",
            ascending=False
        )
    )

    fig = px.bar(
        crash,
        x="crop_name",
        y="instances",
        title="Price Crash Instances by Crop"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        f"Total records below MSP: {len(df[df['status'] == 'Below MSP']):,}"
    )


# =========================================================
# WEATHER IMPACT
# =========================================================

elif page == "🌧️ Weather Impact":

    st.header("🌧️ Weather Impact on Mandi Arrivals")

    arr = arrivals.copy()

    arr["date"] = pd.to_datetime(
        arr["date"],
        errors="coerce"
    )

    daily_arrivals = (
        arr.groupby("date")[
            "arrival_quantity_qtl"
        ]
        .sum()
        .reset_index()
    )

    w = weather.copy()

    w["date"] = pd.to_datetime(
        w["date"],
        errors="coerce"
    )

    merged = daily_arrivals.merge(
        w,
        on="date",
        how="inner"
    )

    merged = merged.dropna(
        subset=[
            "rainfall_mm",
            "arrival_quantity_qtl"
        ]
    )

    if len(merged) > 1:

        correlation = merged[
            "rainfall_mm"
        ].corr(
            merged["arrival_quantity_qtl"]
        )

        st.metric(
            "Rainfall ↔ Arrival Correlation",
            f"{correlation:.2f}"
        )

        fig = px.scatter(
            merged,
            x="rainfall_mm",
            y="arrival_quantity_qtl",
            trendline="ols",
            title="Rainfall vs Crop Arrivals"
        )

        fig.update_layout(
            xaxis_title="Rainfall (mm)",
            yaxis_title="Daily Arrivals (Qtl)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.info(
            "Each dot represents an observed day. "
            "The trend line shows the overall relationship "
            "between rainfall and arrival volume."
        )

    else:

        st.warning(
            "Not enough matched weather and arrival records."
        )


# =========================================================
# TRANSPORT
# =========================================================

elif page == "🚚 Transport":

    st.header("🚚 Transport & Logistics")

    df = transport.copy()

    df = df.dropna(
        subset=["transit_hours"]
    )

    warehouse = (
        df.groupby(
            "destination_warehouse"
        )["transit_hours"]
        .mean()
        .reset_index()
        .sort_values(
            "transit_hours",
            ascending=False
        )
    )

    fig = px.bar(
        warehouse,
        x="destination_warehouse",
        y="transit_hours",
        title="Average Transit Time by Warehouse"
    )

    fig.update_layout(
        xaxis_title="Destination Warehouse",
        yaxis_title="Average Transit Hours"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if not warehouse.empty:

        worst = warehouse.iloc[0]

        st.warning(
            f"Highest average transit time: "
            f"{worst['destination_warehouse']} "
            f"({worst['transit_hours']:.2f} hours)"
        )


# =========================================================
# ASK MANDISENSE AI
# =========================================================

elif page == "🤖 Ask MandiSense":

    st.header("🤖 Ask MandiSense")

    st.write(
        "Ask a natural-language question about the "
        "agricultural supply chain."
    )

    st.markdown("### 💡 Try these questions")

    examples = [
        "Show total arrivals by crop type",
        "Top 5 mandis by arrival volume",
        "Show Wheat arrival trend",
        "Which crops are below MSP?",
        "Which warehouse has highest transit delay?",
        "Show rainfall impact on arrivals"
    ]

    for example in examples:

        st.caption(
            "• " + example
        )

    question = st.text_input(
        "Ask your question",
        placeholder="Example: Which crops are below MSP?"
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
                    ascending=False
                )
            )

            fig = px.bar(
                result,
                x="crop_name",
                y="arrival_quantity_qtl",
                title="Total Crop Arrivals"
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
                    ascending=False
                )
                .head(5)
            )

            fig = px.bar(
                result,
                x="mandi_id",
                y="arrival_quantity_qtl",
                title="Top 5 Mandis by Arrival Volume"
            )

            answer = (
                "These are the **Top 5 mandis** "
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
                errors="coerce"
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
                title="Wheat Arrival Trend"
            )

            answer = (
                "The chart shows the daily Wheat "
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
                    "msp"
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
                    ascending=False
                )
            )

            fig = px.bar(
                crop_crash,
                x="crop_name",
                y="instances",
                title="Price Crash Instances by Crop"
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
                    ascending=False
                )
            )

            fig = px.bar(
                result,
                x="destination_warehouse",
                y="transit_hours",
                title="Average Transit Time"
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
                errors="coerce"
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
                errors="coerce"
            )

            merged = daily.merge(
                w,
                on="date",
                how="inner"
            )

            merged = merged.dropna(
                subset=[
                    "rainfall_mm",
                    "arrival_quantity_qtl"
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
                title="Rainfall vs Crop Arrivals"
            )

            answer = (
                f"🌧️ Rainfall and daily arrivals have "
                f"a correlation of **{correlation:.2f}**."
            )

            return fig, answer


        # ---------------------------------------------
        # UNKNOWN QUESTION
        # ---------------------------------------------

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

            fig, answer = ask_agent(
                question
            )

        if fig is not None:

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.markdown(
            "### 📌 Business Insight"
        )

        st.markdown(
            answer
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "MandiSense | TransOrg AgentIQ Datathon 2026 | "
    "Mandi-to-Market Supply Chain Optimizer"
)