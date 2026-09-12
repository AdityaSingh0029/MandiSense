\# MandiSense — Data Cleaning Proof



\## Raw vs Cleaned Dataset Summary



| Dataset | Raw Rows | Cleaned Rows | Main Cleaning Action |

|---|---:|---:|---|

| Mandi Arrivals | 25,750 | 25,000 | Duplicate removal, crop/unit/date standardization |

| Mandi Master | 60 | 57 | Duplicate removal and ID standardization |

| Price \& MSP | 12,000 | 12,000 | Price parsing, crop/date/mandi standardization |

| Transport Logistics | 10,400 | 10,000 | Duplicate removal, distance conversion, transit validation |

| Weather Sensors | 15,000 | 15,000 | Unit conversion, timestamp normalization, daily aggregation |



\---



\## 1. Mandi Arrivals



\### Raw Data Issues



\- 25,750 raw records

\- 750 duplicate records

\- 484 missing arrival IDs

\- 3,735 missing variety values

\- 5,143 missing unit values

\- 3,899 missing farmer-count values

\- 36 crop-name variants

\- 342 raw mandi-ID variants



\### Cleaning Performed



\- Removed duplicate records.

\- Standardized crop names.

\- Standardized mandi IDs.

\- Parsed and standardized dates.

\- Recovered units embedded in quantity values where possible.

\- Converted KG and Tonnes into Quintals.

\- Created standardized analytical field:



`arrival\_quantity\_qtl`



\### Result



\*\*25,750 → 25,000 records\*\*



\---



\## 2. Mandi Master



\### Raw Data Issues



\- 60 raw records

\- 3 duplicate records

\- Missing district values

\- Missing state values

\- Missing mandi-type values

\- Missing area values

\- Inconsistent mandi identifiers



\### Cleaning Performed



\- Removed duplicate records.

\- Standardized mandi IDs.

\- Preserved available master attributes.

\- Standardized field types.



\### Result



\*\*60 → 57 records\*\*



\---



\## 3. Price \& MSP



\### Raw Data Issues



\- 12,000 price records

\- 1,235 records with missing mandi IDs

\- 773 records with missing/blank district information

\- 36 crop-name variants

\- Price fields stored as strings/mixed formats



\### Cleaning Performed



\- Parsed minimum, maximum and modal prices into numeric values.

\- Parsed MSP into numeric values.

\- Standardized crop names.

\- Standardized dates.

\- Standardized mandi identifiers where available.

\- Preserved records with missing mandi IDs instead of dropping them unnecessarily.



\### Result



\*\*12,000 → 12,000 records\*\*



\---



\## 4. Transport Logistics



\### Raw Data Issues



\- 10,400 raw records

\- 400 duplicate records

\- 563 negative/reported invalid transit-duration records

\- 1,053 missing arrival timestamps

\- 518 missing transit-hour values

\- 1,032 missing distance units

\- 1,622 missing vehicle numbers

\- 1,551 missing driver IDs



\### Cleaning Performed



\- Removed duplicate records.

\- Converted Miles to KM.

\- Standardized vehicle registration numbers.

\- Validated transit duration.

\- Treated negative transit durations as invalid.

\- Recalculated transit duration from departure and arrival timestamps when valid timestamps were available.

\- Preserved records where reliable recovery was not possible.



\### Result



\*\*10,400 → 10,000 records\*\*



\---



\## 5. Weather Sensors



\### Raw Data Issues



\- 15,000 raw sensor records

\- 1,555 missing timestamps

\- 2,263 missing temperature units

\- 791 missing rainfall/unit information

\- 1,500 missing humidity values

\- Mixed Celsius and Fahrenheit temperature units

\- Mixed mm and inch rainfall units

\- Mixed UTC and IST timestamps

\- Unknown sensor identifiers



\### Cleaning Performed



\- Standardized timestamps.

\- Converted explicit UTC timestamps to IST.

\- Converted Fahrenheit temperatures to Celsius.

\- Converted rainfall inches to millimetres.

\- Parsed numeric sensor measurements.

\- Aggregated observations into daily weather data.



\### Result



\*\*15,000 sensor records → daily weather analytical table\*\*



Daily output:



`data/cleaned/weather\_daily.csv`



\---



\# Standardization Examples



\## Crop Names



```text

Gehun / Wheat / गेहूं → Wheat

Dhaan / Paddy / Rice / धान → Rice

Kapas / Cotton / कपास → Cotton

Sarson / Mustard / सरसों → Mustard

Makka / Maize / मक्का → Maize

Ganna / Sugarcane / गन्ना → Sugarcane

