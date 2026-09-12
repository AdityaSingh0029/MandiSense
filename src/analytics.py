from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parents[1]; D=BASE/'data'/'cleaned'

def build_metrics():
    a=pd.read_csv(D/'arrivals_enriched.csv'); p=pd.read_csv(D/'prices_enriched.csv'); t=pd.read_csv(D/'transport_clean.csv')
    metrics={
      'total_arrivals_qtl': float(a.arrival_quantity_qtl.sum()),
      'avg_modal_price': float(p.modal_price.mean()),
      'price_crash_instances': int((p.modal_price.lt(p.msp) & p.modal_price.notna() & p.msp.notna()).sum()),
      'avg_transit_hours': float(t.transit_hours_clean.mean()),
      'transit_delay_rate_pct': float((t.transit_hours_clean.gt(8).mean()*100)),
    }
    return metrics

if __name__=='__main__': print(build_metrics())
