import pandas as pd
from sas.model import simulate

def weather():
    d=pd.date_range('2026-06-15',periods=160)
    return pd.DataFrame({'date':d,'rain_mm':[3]*160,'tmax_c':[28]*160,'tmin_c':[12]*160,'rad_mj_m2':[22]*160})

def test_bean_cap():
    s,_=simulate(weather(),'Frijol negro','Franco','Temporal','2026-06-15')
    assert s['yield_kg_ha'] <= 2000

def test_squash_cap():
    s,_=simulate(weather(),'Calabaza','Franco','Temporal','2026-06-15')
    assert s['yield_kg_ha'] <= 900

def test_wheat_cap():
    s,_=simulate(weather(),'Trigo','Franco','Temporal','2026-06-15')
    assert s['yield_kg_ha'] <= 4500
