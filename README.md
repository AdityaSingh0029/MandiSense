# \# MandiSense — Mandi-to-Market Supply Chain Optimizer

# 

# \## TransOrg AgentIQ Datathon 2026 — Track 3: AgriTech

# 

# MandiSense is a data-driven mandi intelligence and supply-chain analytics dashboard designed to convert messy agricultural market, weather, and transport data into actionable insights.

# 

# The solution cleans and integrates mandi arrivals, wholesale prices/MSP, weather sensor logs, transport logistics, and mandi master data into a unified analytical layer.

# 

# \---

# 

# \## Problem Statement

# 

# Agricultural supply-chain data is often fragmented and inconsistent.

# 

# The provided datasets contain:

# 

# \- Messy crop names across English, Hindi, and Punjabi

# \- Mixed quantity units such as KG, Quintals, and Tonnes

# \- Mixed distance units such as KM and Miles

# \- Mixed temperature units such as Celsius and Fahrenheit

# \- Mixed rainfall units such as mm and inches

# \- UTC and IST timestamps

# \- Missing mandi IDs and districts

# \- Invalid or negative transport durations

# \- Inconsistent vehicle registration formats

# \- Duplicate records

# 

# MandiSense addresses these data-quality issues before performing business analysis.

# 

# \---

# 

# \## Solution

# 

# The project follows a complete data-to-insight pipeline:

# 

# Raw Data

# ↓

# Data Cleaning \& Standardization

# ↓

# Unified Analytical Tables

# ↓

# Business Metrics

# ↓

# Interactive Dashboard

# ↓

# Natural-Language MandiSense Assistant

# 

# \---

# 

# \## Dataset Sources

# 

# The solution uses five provided datasets:

# 

# 1\. `track3\_mandi\_arrivals.csv`

# &#x20;  - Daily crop arrivals

# &#x20;  - Crop, variety, quantity, unit, mandi and farmer information

# 

# 2\. `track3\_price\_and\_msp.json`

# &#x20;  - Wholesale minimum/maximum/modal prices

# &#x20;  - MSP information

# 

# 3\. `track3\_weather\_sensors.xlsx`

# &#x20;  - Temperature

# &#x20;  - Rainfall

# &#x20;  - Humidity

# &#x20;  - Sensor timestamps

# 

# 4\. `track3\_transport\_logistics.csv`

# &#x20;  - Truck movement

# &#x20;  - Destination warehouse

# &#x20;  - Distance

# &#x20;  - Transit duration

# &#x20;  - Vehicle information

# 

# 5\. `track3\_mandi\_master.csv`

# &#x20;  - Mandi master information

# &#x20;  - District, state and mandi type

# 

# \---

# 

# \## Data Cleaning \& Engineering

# 

# \### Crop Standardization

# 

# Crop names are mapped to canonical categories such as:

# 

# \- Wheat

# \- Rice

# \- Cotton

# \- Mustard

# \- Maize

# \- Sugarcane

# \- Basmati

# 

# This handles variations such as English, Hindi and regional spellings.

# 

# \### Quantity Standardization

# 

# All arrival quantities are converted to Quintals.

# 

# Conversion rules:

# 

# \- 1 Quintal = 100 KG

# \- 1 Tonne = 10 Quintals

# 

# \### Distance Standardization

# 

# Transport distances are converted to KM.

# 

# \### Temperature Standardization

# 

# Temperature readings are converted to Celsius where Fahrenheit values are present.

# 

# \### Rainfall Standardization

# 

# Rainfall readings are converted to millimetres where inch-based readings are present.

# 

# \### Timestamp Standardization

# 

# Weather timestamps are normalized to India Standard Time (IST) where timezone information is available.

# 

# \### Transport Data Validation

# 

# Invalid negative transit durations are treated as unreliable and replaced with duration calculated from departure and arrival timestamps when a valid duration can be derived.

# 

# \### Duplicate Handling

# 

# Duplicate records are removed during the cleaning pipeline.

# 

# \---

# 

# \## Key Analytics

# 

# MandiSense provides:

# 

# \- Total crop arrivals in Quintals

# \- Crop-wise arrival distribution

# \- Top-performing mandis by arrivals

# \- Wholesale modal price vs MSP

# \- Price-below-MSP instances

# \- Average transit time by warehouse

# \- Operational transit delay indicators

# \- Rainfall vs arrival relationship

# \- Daily arrival trends

# \- Natural-language business queries

# 

# \---

# 

# \## Dashboard Modules

# 

# \### 1. Executive Dashboard

# 

# Provides a high-level view of:

# 

# \- Total arrivals

# \- Average modal price

# \- Below-MSP records

# \- Average transit time

# \- Daily arrivals trend

# \- Top mandis

# \- Crop distribution

# 

# \### 2. Price vs MSP

# 

# Helps identify crops and market conditions where wholesale modal prices fall below MSP.

# 

# \### 3. Weather Impact

# 

# Explores the relationship between rainfall and mandi arrivals.

# 

# \### 4. Transport

# 

# Analyzes average transit time across destination warehouses.

# 

# \### 5. Ask MandiSense

# 

# A natural-language business intelligence interface that converts common operational questions into relevant analytics and visualizations.

# 

# Example questions:

# 

# \- How much wheat arrived?

# \- Show top 5 mandis.

# \- Which crops are below MSP?

# \- What is the wheat price trend?

# \- Which warehouse has the highest transit time?

# \- What is the rainfall impact on arrivals?

# 

# \---

# 

# \## Technology Stack

# 

# \- Python

# \- Pandas

# \- NumPy

# \- OpenPyXL

# \- Streamlit

# \- Plotly

# \- Statsmodels

# 

# \---

# 

# \## Project Structure

# 

# ```text

# Track3\_MandiSense/

# │

# ├── agent/

# │

# ├── dashboard/

# │   └── app.py

# │

# ├── data/

# │   ├── raw/

# │   └── cleaned/

# │

# ├── notebooks/

# │

# ├── outputs/

# │

# ├── src/

# │   ├── pipeline.py

# │   └── analytics.py

# │

# ├── README.md

# └── requirements.txt

