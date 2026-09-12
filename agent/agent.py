import os
import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# PROJECT PATH
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_DIR = os.path.join(BASE_DIR, "data", "cleaned")


# -----------------------------
# LOAD CLEANED DATA
# -----------------------------
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

    return arrivals, prices, transport, weather, master


arrivals, prices, transport, weather, master = load_data()


# -----------------------------
# HELPER
# -----------------------------
def text(q):
    return q.lower().strip()


# -----------------------------
# AI AGENT
# -----------------------------
def ask_mandi_agent(question):

    q = text(question)

    # ==========================================
    # 1. TOTAL ARRIVALS BY CROP
    # ==========================================
    if (
        "total arrivals" in q
        or "arrivals by crop" in q
        or "crop type" in q
    ):

        df = (
            arrivals
            .groupby("crop_name")["arrival_quantity_qtl"]
            .sum()
            .reset_index()
            .sort_values(
                "arrival_quantity_qtl",
                ascending=False
            )
        )

        fig = px.bar(
            df,
            x="crop_name",
            y="arrival_quantity_qtl",
            title="Total Crop Arrivals"
        )

        top = df.iloc[0]

        answer = (
            f"The highest arrival volume is for "
            f"**{top['crop_name']}**, with approximately "
            f"**{top['arrival_quantity_qtl']:,.0f} Quintals**."
        )

        return fig, answer


    # ==========================================
    # 2. TOP 5 MANDIS
    # ==========================================
    if "top 5 mandi" in q or "top mandi" in q:

        df = (
            arrivals
            .groupby("mandi_id")["arrival_quantity_qtl"]
            .sum()
            .reset_index()
            .sort_values(
                "arrival_quantity_qtl",
                ascending=False
            )
            .head(5)
        )

        fig = px.bar(
            df,
            x="mandi_id",
            y="arrival_quantity_qtl",
            title="Top 5 Mandis by Arrival Volume"
        )

        answer = (
            "These are the **Top 5 mandis** contributing "
            "the highest arrival volume."
        )

        return fig, answer


    # ==========================================
    # 3. WHEAT TREND
    # ==========================================
    if "wheat" in q and (
        "trend" in q or "arrival" in q
    ):

        df = arrivals[
            arrivals["crop_name"].astype(str).str.lower()
            == "wheat"
        ].copy()

        if df.empty:
            return None, "No Wheat data found."

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        df = (
            df.groupby("date")["arrival_quantity_qtl"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            df,
            x="date",
            y="arrival_quantity_qtl",
            title="Wheat Arrival Trend"
        )

        answer = (
            "This chart shows the daily Wheat arrival "
            "trend across the mandis."
        )

        return fig, answer


    # ==========================================
    # 4. BELOW MSP / PRICE CRASH
    # ==========================================
    if (
        "below msp" in q
        or "price crash" in q
        or "below msp" in q
    ):

        df = prices.copy()

        df["modal_price"] = pd.to_numeric(
            df["modal_price"],
            errors="coerce"
        )

        df["msp"] = pd.to_numeric(
            df["msp"],
            errors="coerce"
        )

        df = df.dropna(
            subset=["modal_price", "msp"]
        )

        df["below_msp"] = (
            df["modal_price"] < df["msp"]
        )

        crash = (
            df[df["below_msp"]]
            .groupby("crop_name")
            .size()
            .reset_index(name="instances")
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

        total = int(
            df["below_msp"].sum()
        )

        answer = (
            f"Total records where the modal price "
            f"was below MSP: **{total:,}**."
        )

        return fig, answer


    # ==========================================
    # 5. TRANSPORT / DELAY
    # ==========================================
    if (
        "delay" in q
        or "transit" in q
        or "warehouse" in q
    ):

        df = transport.copy()

        df["transit_hours"] = pd.to_numeric(
            df["transit_hours"],
            errors="coerce"
        )

        df = df.dropna(
            subset=["transit_hours"]
        )

        result = (
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
            result,
            x="destination_warehouse",
            y="transit_hours",
            title="Average Transit Time by Warehouse"
        )

        worst = result.iloc[0]

        answer = (
            f"**{worst['destination_warehouse']}** "
            f"has the highest average transit time at "
            f"approximately **{worst['transit_hours']:.2f} hours**."
        )

        return fig, answer


    # ==========================================
    # 6. WEATHER / RAINFALL
    # ==========================================
    if (
        "rainfall" in q
        or "weather impact" in q
        or "weather" in q
    ):

        arr = arrivals.copy()

        arr["date"] = pd.to_datetime(
            arr["date"],
            errors="coerce"
        )

        daily_arrivals = (
            arr.groupby("date")["arrival_quantity_qtl"]
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

        if merged.empty:
            return None, "Weather and arrival data could not be matched."

        correlation = merged[
            "rainfall_mm"
        ].corr(
            merged["arrival_quantity_qtl"]
        )

        fig = px.scatter(
            merged,
            x="rainfall_mm",
            y="arrival_quantity_qtl",
            title="Rainfall vs Crop Arrivals",
            trendline="ols"
        )

        answer = (
            f"The correlation between rainfall and "
            f"daily crop arrivals is approximately "
            f"**{correlation:.2f}**."
        )

        return fig, answer


    # ==========================================
    # 7. UNKNOWN QUESTION
    # ==========================================
    return None, """
I couldn't understand that question yet.

Try one of these:

• Show total arrivals by crop type
• Top 5 mandis by arrival volume
• Show Wheat arrival trend
• Which crops are below MSP?
• Which warehouse has highest transit delay?
• Show rainfall impact on arrivals
"""


# =================================================
# STREAMLIT UI
# =================================================

st.set_page_config(
    page_title="MandiSense AI",
    page_icon="🌾",
    layout="wide"
)


st.title("🌾 MandiSense AI Agent")

st.write(
    "Ask questions about mandi arrivals, prices, MSP, "
    "weather and transportation."
)


# -----------------------------
# EXAMPLE QUESTIONS
# -----------------------------

st.markdown("### 💡 Try asking")

examples = [
    "Show total arrivals by crop type",
    "Top 5 mandis by arrival volume",
    "Show Wheat arrival trend",
    "Which crops are below MSP?",
    "Which warehouse has highest transit delay?",
    "Show rainfall impact on arrivals"
]

cols = st.columns(3)

for i, example in enumerate(examples):

    with cols[i % 3]:

        if st.button(
            example,
            key=f"example_{i}"
        ):

            st.session_state["question"] = example


# -----------------------------
# QUESTION BOX
# -----------------------------

question = st.text_input(
    "🤖 Ask MandiSense",
    value=st.session_state.get(
        "question",
        ""
    ),
    placeholder="Example: Which crops are below MSP?"
)


# -----------------------------
# RUN AGENT
# -----------------------------

if question:

    with st.spinner("Analyzing mandi data..."):

        fig, answer = ask_mandi_agent(
            question
        )

    if fig is not None:

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("### 📌 Business Insight")

    st.markdown(answer)