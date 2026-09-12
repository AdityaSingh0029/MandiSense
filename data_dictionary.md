\# MandiSense Data Dictionary



\## 1. Mandi Arrivals



File: `track3\_mandi\_arrivals.csv`



| Column | Description | Final/Standardized Form |

|---|---|---|

| arrival\_id | Unique identifier for an arrival record | ID |

| date | Date of crop arrival | Standardized date |

| mandi\_id | Mandi identifier | Standardized as MANDI### |

| crop\_name | Crop name | Standardized crop category |

| variety | Crop variety | Text |

| arrival\_quantity | Raw crop arrival quantity | Converted to Quintals |

| unit | Original quantity unit | KG / Quintal / Tonne |

| farmer\_count | Number of farmers associated with arrival | Numeric |



\### Quantity Conversion



\- 1 Quintal = 100 KG

\- 1 Tonne = 10 Quintals

\- Final analytical quantity: `arrival\_quantity\_qtl`



\---



\## 2. Price \& MSP



File: `track3\_price\_and\_msp.json`



| Column | Description | Final/Standardized Form |

|---|---|---|

| record\_id | Unique price record identifier | ID |

| date | Price observation date | Standardized date |

| mandi\_id | Mandi identifier | Standardized mandi ID |

| district | District associated with price record | Text |

| crop\_name | Crop name | Standardized crop category |

| min\_price | Minimum wholesale price | Numeric |

| max\_price | Maximum wholesale price | Numeric |

| modal\_price | Modal wholesale price | Numeric |

| msp | Minimum Support Price | Numeric |



\### Key Metric



A price-crash instance is counted when:



`modal\_price < msp`



\---



\## 3. Weather Sensors



File: `track3\_weather\_sensors.xlsx`



Sheet: `sensor\_logs`



| Column | Description | Final/Standardized Form |

|---|---|---|

| sensor\_id | Weather sensor identifier | Text |

| timestamp | Sensor observation timestamp | Standardized to IST where applicable |

| temperature | Recorded temperature | Converted to Celsius |

| temp\_unit | Original temperature unit | Standardized |

| rainfall | Recorded rainfall | Converted to mm |

| rain\_unit | Original rainfall unit | Standardized |

| humidity\_percent | Relative humidity | Percentage |



\### Weather Conversion



Fahrenheit temperature values are converted to Celsius.



Rainfall recorded in inches is converted to millimetres.



Daily weather observations are aggregated into:



`weather\_daily.csv`



\---



\## 4. Transport \& Logistics



File: `track3\_transport\_logistics.csv`



| Column | Description | Final/Standardized Form |

|---|---|---|

| trip\_id | Unique transport trip identifier | ID |

| mandi\_id | Origin mandi | Standardized mandi ID |

| destination\_warehouse | Destination warehouse | Text |

| departure\_time | Truck departure timestamp | Standardized datetime |

| arrival\_time | Truck arrival timestamp | Standardized datetime |

| transit\_hours | Reported transit duration | Validated / recalculated when possible |

| distance | Transport distance | Converted to KM |

| distance\_unit | Original distance unit | KM / Miles |

| vehicle\_no | Vehicle registration number | Standardized text |

| driver\_id | Driver identifier | Text |



\### Transport Validation



Negative transit durations are treated as invalid.



Where valid departure and arrival timestamps are available, transit duration can be recalculated from the timestamps.



\---



\## 5. Mandi Master



File: `track3\_mandi\_master.csv`



| Column | Description | Final/Standardized Form |

|---|---|---|

| mandi\_id | Mandi identifier | Standardized as MANDI### |

| mandi\_name | Mandi name | Text |

| district | District name | Text |

| state | State name | Text |

| mandi\_type | Type/category of mandi | Text |

| total\_area\_acres | Total area associated with mandi | Numeric |



\---



\# Standardization Rules



\## Crop Names



Messy English, Hindi and regional crop names are mapped into canonical crop categories.



Examples:



\- Wheat / Gehun / गेहूं / Kanak → Wheat

\- Rice / Paddy / Dhaan / Chawal / धान / चावल → Rice

\- Cotton / Kapas / Narma / कपास → Cotton

\- Mustard / Sarson / Sarso / सरसों → Mustard

\- Maize / Corn / Makka / Makki / मक्का → Maize

\- Sugarcane / Ganna / Ganne / गन्ना → Sugarcane

\- Basmati → Basmati



\## Mandi IDs



Mandi identifiers are normalized into a consistent:



`MANDI###`



format.



\## Units



All analytical quantities are standardized before aggregation.



\- Quantity → Quintals

\- Distance → KM

\- Temperature → Celsius

\- Rainfall → Millimetres



\## Dates \& Time



Dates and timestamps are parsed into standardized formats.



Weather timestamps containing explicit UTC information are converted to IST.



\---



\# Main Analytical Outputs



The cleaned data supports the following metrics:



\- Total arrivals in Quintals

\- Crop-wise arrivals

\- Top mandis by arrival volume

\- Modal wholesale price vs MSP

\- Price-below-MSP instances

\- Average transit time by warehouse

\- Transit delay indicators

\- Rainfall vs arrival relationship

\- Daily arrival trends



\---



\# Data Quality



The cleaning pipeline produces cleaned datasets and a quality report.



Quality checks include:



\- Duplicate detection/removal

\- Missing-value handling

\- Unit standardization

\- Crop-name normalization

\- Mandi-ID normalization

\- Invalid transit-time handling

\- Timestamp normalization

\- Numeric field conversion



Quality report:



`data/cleaned/data\_quality\_report.json`

