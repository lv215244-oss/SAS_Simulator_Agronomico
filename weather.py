import pandas as pd
import numpy as np

REQUIRED=['date','rain_mm','tmax_c','tmin_c','rad_mj_m2']

def validate_weather(df):
    missing=[c for c in REQUIRED if c not in df.columns]
    if missing: raise ValueError(f'Faltan columnas: {missing}')
    x=df.copy(); x['date']=pd.to_datetime(x['date'], errors='coerce')
    for c in REQUIRED[1:]: x[c]=pd.to_numeric(x[c], errors='coerce')
    if x[REQUIRED].isna().any().any(): raise ValueError('Hay fechas o datos climáticos no numéricos/ausentes.')
    if (x['tmax_c'] < x['tmin_c']).any(): raise ValueError('Existe Tmax < Tmin.')
    if (x[['rain_mm','rad_mj_m2']] < 0).any().any(): raise ValueError('Lluvia o radiación negativa.')
    return x.sort_values('date').reset_index(drop=True)
