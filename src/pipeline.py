from pathlib import Path
import json, re
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / 'data' / 'raw'
OUT = BASE / 'data' / 'cleaned'
OUT.mkdir(parents=True, exist_ok=True)

CROP_MAP = {
    'wheat':'Wheat','gehun':'Wheat','गेहूं':'Wheat','kanak':'Wheat',
    'rice':'Rice','paddy':'Rice','dhaan':'Rice','chawal':'Rice','धान':'Rice','चावल':'Rice',
    'cotton':'Cotton','kapas':'Cotton','narma':'Cotton','कपास':'Cotton',
    'mustard':'Mustard','sarson':'Mustard','sarso':'Mustard','सरसों':'Mustard',
    'maize':'Maize','corn':'Maize','makka':'Maize','makki':'Maize','मक्का':'Maize',
    'sugarcane':'Sugarcane','ganna':'Sugarcane','ganne':'Sugarcane','गन्ना':'Sugarcane',
    'basmati':'Basmati'
}

def clean_text(x):
    return str(x).strip() if pd.notna(x) else np.nan

def normalize_crop(x):
    if pd.isna(x): return np.nan
    s = str(x).strip()
    return CROP_MAP.get(s.lower(), CROP_MAP.get(s, s.title()))

def normalize_mandi_id(x):
    if pd.isna(x): return np.nan
    s = str(x).strip().upper()
    m = re.search(r'(?:MANDI[-_ ]*)?(\d{1,3})$', s)
    if not m: return np.nan
    n = int(m.group(1))
    return f'MANDI{n:03d}' if 1 <= n <= 999 else np.nan

def parse_number(x):
    if pd.isna(x) or str(x).strip() == '': return np.nan
    s = str(x).replace(',', '').replace('₹','').replace('Rs.','').replace('Rs','').replace('INR','').replace('/-','').strip()
    m = re.search(r'-?\d+(?:\.\d+)?', s)
    return float(m.group()) if m else np.nan

def parse_date(x):
    # Bundle convention: ISO/month-name and hyphen numeric dates are month-first;
    # slash/dot numeric dates are day-first. This avoids turning 01/05 into Jan 5
    # when transport data intends 1 May.
    s = pd.Series(x) if not isinstance(x, pd.Series) else x.copy()
    out = pd.Series(pd.NaT, index=s.index, dtype='datetime64[ns]')
    text = s.astype('string')
    slashdot = text.str.contains(r'[/\.]', regex=True, na=False) & ~text.str.contains(r'^[0-9]{4}[/\.]', regex=True, na=False)
    if slashdot.any(): out.loc[slashdot] = pd.to_datetime(text[slashdot], errors='coerce', format='mixed', dayfirst=True)
    if (~slashdot).any(): out.loc[~slashdot] = pd.to_datetime(text[~slashdot], errors='coerce', format='mixed', dayfirst=False)
    return out if isinstance(x, pd.Series) else out.iloc[0]

def normalize_quantity(row):
    raw = str(row.get('arrival_quantity',''))
    unit = row.get('unit', np.nan)
    # Recover unit embedded in quantity when the explicit unit is missing.
    if pd.isna(unit) or str(unit).strip() == '':
        low = raw.lower()
        if re.search(r'\bqtl\b|\bquintal', low): unit = 'Qtl'
        elif re.search(r'\bkg\b|\bkgs?\b|\bkilo', low): unit = 'KG'
        elif re.search(r'\bmt\b|\btonnes?\b|\btonne\b|\bt\b', low): unit = 'T'
    val = parse_number(row.get('arrival_quantity'))
    if pd.isna(val) or pd.isna(unit): return pd.Series([val, np.nan, 'UNKNOWN'])
    u = str(unit).strip().lower()
    if u in {'q','qtl','quintal','quintals'}: return pd.Series([val, val, 'QTL'])
    if u in {'kg','kgs','kilo'}: return pd.Series([val/100, val/100, 'QTL'])
    if u in {'t','mt','tonne','tonnes'}: return pd.Series([val*10, val*10, 'QTL'])
    return pd.Series([val, np.nan, 'UNKNOWN'])

def normalize_vehicle(x):
    if pd.isna(x) or str(x).strip()=='': return np.nan
    s = re.sub(r'[^A-Za-z0-9]', '', str(x).upper())
    m = re.match(r'^([A-Z]{2})(\d{1,2})([A-Z]{1,3})(\d{4})$', s)
    if m: return f'{m.group(1)}-{int(m.group(2)):02d}-{m.group(3)}-{m.group(4)}'
    return s

def clean_arrivals():
    df = pd.read_csv(RAW/'track3_mandi_arrivals.csv')
    raw_rows=len(df); dup=df.duplicated().sum()
    df=df.drop_duplicates().copy()
    df['arrival_id']=df['arrival_id'].astype('string').str.strip()
    df['date']=parse_date(df['date'])
    df['mandi_id']=df['mandi_id'].map(normalize_mandi_id)
    df['crop_name_raw']=df['crop_name']
    df['crop_name']=df['crop_name'].map(normalize_crop)
    q=df.apply(normalize_quantity,axis=1); q.columns=['quantity_raw_numeric','arrival_quantity_qtl','unit_clean']; df=q.join(df)
    df['farmer_count']=pd.to_numeric(df['farmer_count'],errors='coerce')
    df['data_quality_flag']=np.where(df['arrival_quantity_qtl'].isna(),'MISSING_OR_UNKNOWN_UNIT','OK')
    df.to_csv(OUT/'arrivals_clean.csv',index=False)
    return {'dataset':'arrivals','raw_rows':raw_rows,'clean_rows':len(df),'duplicates_removed':int(dup),'quality_flags':df.data_quality_flag.value_counts().to_dict()}

def clean_master():
    df=pd.read_csv(RAW/'track3_mandi_master.csv').drop_duplicates().copy()
    df['mandi_id']=df['mandi_id'].map(normalize_mandi_id)
    for c in ['mandi_name','district','state','mandi_type']:
        df[c]=df[c].astype('string').str.strip()
    df['district']=df['district'].str.title()
    df['total_area_acres']=pd.to_numeric(df['total_area_acres'],errors='coerce')
    df.to_csv(OUT/'mandi_master_clean.csv',index=False)
    return {'dataset':'master','raw_rows':60,'clean_rows':len(df)}

def clean_prices():
    data=json.load(open(RAW/'track3_price_and_msp.json',encoding='utf-8'))
    df=pd.DataFrame(data)
    raw_rows=len(df)
    df['date']=parse_date(df['date'])
    df['mandi_id']=df['mandi_id'].map(normalize_mandi_id)
    df['district']=df['district'].replace('',np.nan).astype('string').str.strip().str.title()
    df['crop_name_raw']=df['crop_name']; df['crop_name']=df['crop_name'].map(normalize_crop)
    for c in ['min_price','max_price','modal_price','msp']: df[c]=df[c].map(parse_number)
    df['price_vs_msp_pct']=np.where(df['msp'].gt(0),(df['modal_price']-df['msp'])/df['msp']*100,np.nan)
    df['below_msp']=df['modal_price'].notna() & df['msp'].notna() & (df['modal_price']<df['msp'])
    df.to_csv(OUT/'prices_clean.csv',index=False)
    return {'dataset':'prices','raw_rows':raw_rows,'clean_rows':len(df),'missing_mandi_after_normalization':int(df.mandi_id.isna().sum())}

def clean_transport():
    df=pd.read_csv(RAW/'track3_transport_logistics.csv')
    raw_rows=len(df); dup=df.duplicated().sum(); df=df.drop_duplicates().copy()
    df['mandi_id']=df['mandi_id'].map(normalize_mandi_id)
    df['departure_time']=parse_date(df['departure_time'])
    df['arrival_time']=parse_date(df['arrival_time'])
    df['transit_hours_raw']=pd.to_numeric(df['transit_hours'],errors='coerce')
    computed=(df['arrival_time']-df['departure_time']).dt.total_seconds()/3600
    df['transit_hours_clean']=df['transit_hours_raw'].where(df['transit_hours_raw'].ge(0),np.nan)
    computed_valid=computed.where(computed.ge(0) & computed.le(72))
    df['transit_hours_clean']=df['transit_hours_clean'].fillna(computed_valid)
    df['transit_time_source']=np.where(df['transit_hours_raw'].ge(0),'reported',np.where(computed_valid.notna(),'computed','invalid'))
    df['distance']=pd.to_numeric(df['distance'],errors='coerce')
    du=df['distance_unit'].astype('string').str.lower().fillna('')
    df['distance_km']=np.where(du.eq('miles'),df['distance']*1.60934, np.where(du.eq('km'),df['distance'],np.nan))
    df['vehicle_no']=df['vehicle_no'].map(normalize_vehicle)
    df.to_csv(OUT/'transport_clean.csv',index=False)
    return {'dataset':'transport','raw_rows':raw_rows,'clean_rows':len(df),'duplicates_removed':int(dup),'negative_reported_transit':int(df.transit_hours_raw.lt(0).sum())}

def clean_weather():
    df=pd.read_excel(RAW/'track3_weather_sensors.xlsx',sheet_name='sensor_logs')
    df['timestamp_raw']=df['timestamp']
    # Parse timezone-bearing strings and naive dates. Normalize all to IST-naive for daily aggregation.
    raw_ts=df['timestamp'].astype('string')
    is_utc=raw_ts.str.contains(r'\bUTC\b',case=False,regex=True,na=False)
    base_ts=raw_ts.str.replace(r'\s+(?:IST|UTC)\s*$', '', regex=True)
    parsed=pd.to_datetime(base_ts,errors='coerce',format='mixed',dayfirst=False)
    df['timestamp_ist']=parsed
    if is_utc.any():
        utc_vals=parsed[is_utc]
        df.loc[is_utc,'timestamp_ist']=utc_vals.dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
    # Explicit IST and timezone-less values are treated as IST local clock time.
    df['date']=df['timestamp_ist'].dt.date
    temp=pd.to_numeric(df['temperature'],errors='coerce')
    tu=df['temp_unit'].astype('string').str.lower().fillna('')
    df['temperature_c']=np.where(tu.isin(['f','°f','fahrenheit']), (temp-32)*5/9, np.where(tu.isin(['c','°c','celsius']),temp,np.nan))
    rain=pd.to_numeric(df['rainfall'],errors='coerce'); ru=df['rain_unit'].astype('string').str.lower().fillna('')
    df['rainfall_mm']=np.where(ru.isin(['in','inch','inches']),rain*25.4,np.where(ru.isin(['mm','millimeters']),rain,np.nan))
    df['humidity_percent']=pd.to_numeric(df['humidity_percent'],errors='coerce')
    df.to_csv(OUT/'weather_clean.csv',index=False)
    daily=df.groupby('date',dropna=True).agg(rainfall_mm=('rainfall_mm','sum'),avg_temperature_c=('temperature_c','mean'),avg_humidity=('humidity_percent','mean'),sensor_count=('sensor_id','nunique')).reset_index()
    daily.to_csv(OUT/'weather_daily.csv',index=False)
    return {'dataset':'weather','raw_rows':len(pd.read_excel(RAW/'track3_weather_sensors.xlsx',sheet_name='sensor_logs')),'clean_rows':len(df),'daily_rows':len(daily)}

def build_joined():
    a=pd.read_csv(OUT/'arrivals_clean.csv',parse_dates=['date'])
    m=pd.read_csv(OUT/'mandi_master_clean.csv')
    p=pd.read_csv(OUT/'prices_clean.csv',parse_dates=['date'])
    t=pd.read_csv(OUT/'transport_clean.csv',parse_dates=['departure_time','arrival_time'])
    w=pd.read_csv(OUT/'weather_daily.csv',parse_dates=['date'])
    a=a.merge(m[['mandi_id','mandi_name','district','state','mandi_type']],on='mandi_id',how='left',suffixes=('','_master'))
    # Price join is date + mandi + crop when mandi is available; retain unmatched records for transparency.
    p=p.merge(m[['mandi_id','mandi_name','district','state']],on='mandi_id',how='left',suffixes=('','_master'))
    a.to_csv(OUT/'arrivals_enriched.csv',index=False)
    p.to_csv(OUT/'prices_enriched.csv',index=False)
    t.to_csv(OUT/'transport_clean.csv',index=False)
    return len(a),len(p)

def main():
    reports=[clean_arrivals(),clean_master(),clean_prices(),clean_transport(),clean_weather()]
    build_joined()
    pd.DataFrame(reports).to_json(OUT/'data_quality_report.json',orient='records',indent=2)
    print(json.dumps(reports,indent=2))

if __name__=='__main__': main()
