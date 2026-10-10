import numpy as np
import pandas as pd
from parameters import CROPS, SOILS

def temp_factor(t, p):
    if t <= p['base_temp'] or t >= p['max_temp']: return 0.0
    if t <= p['opt_temp']: return (t-p['base_temp'])/(p['opt_temp']-p['base_temp'])
    return (p['max_temp']-t)/(p['max_temp']-p['opt_temp'])

def simulate(weather, crop_name, soil_name='Franco', regime='Temporal', sowing_date=None,
             initial_water_frac=0.65, n_fertilizer=40, irrigation_mm=0,
             plant_density=1.0, residue=0.0):
    p=CROPS[crop_name]; s=SOILS[soil_name]
    w=weather.copy(); w['date']=pd.to_datetime(w['date'])
    if sowing_date is not None:
        sd=pd.Timestamp(sowing_date); w=w[w['date']>=sd].copy()
    w=w.head(p['season_days']).copy()
    if w.empty: raise ValueError('No hay datos climáticos después de la fecha de siembra.')
    aw=s['theta_wp']+(s['theta_fc']-s['theta_wp'])*initial_water_frac
    root_depth=p['root_depth']; water_mm=max(0,(aw-s['theta_wp'])*root_depth*1000)
    water_capacity=(s['theta_fc']-s['theta_wp'])*root_depth*1000
    n_supply=max(0,s['om']*18*root_depth + n_fertilizer*0.70)
    biomass=0.0; cum_gdd=0.0; maturity=False; rows=[]; stress_w=[]; stress_t=[]; stress_n=[]
    for _,d in w.iterrows():
        tmean=(d.tmax_c+d.tmin_c)/2
        tf=temp_factor(tmean,p)
        gdd=max(0,tmean-p['base_temp'])
        cum_gdd+=gdd
        pet=max(0,0.16*(d.rad_mj_m2)*(1+0.03*(tmean-20)))
        et0=max(0.1,pet)
        et_req=et0*p['kc']
        rain=float(d.rain_mm)
        if regime=='Riego': rain += irrigation_mm/max(1,p['season_days'])
        infil=rain*(0.88+0.04*residue)
        runoff=max(0,rain-infil)
        water_mm=min(water_capacity,water_mm+infil)
        sw=min(1.0, water_mm/max(1,et_req*1.5))
        uptake=min(water_mm,et_req*sw)
        water_mm=max(0,water_mm-uptake)
        nw=min(1.0,n_supply/max(1,p['n_demand']))
        stress_w.append(sw); stress_t.append(tf); stress_n.append(nw)
        daily_growth=0.035*d.rad_mj_m2*tf*sw*nw
        biomass += max(0,daily_growth)
        n_supply=max(0,n_supply-0.35*daily_growth)
        rows.append(dict(date=d.date,rain_mm=rain,tmean=tmean,et_req=et_req,water_mm=water_mm,
                         water_factor=sw,temp_factor=tf,n_factor=nw,biomass_kg_ha=biomass,
                         gdd=cum_gdd,runoff_mm=runoff))
    out=pd.DataFrame(rows)
    if len(out)==0: raise ValueError('Simulación vacía.')
    mean_w=float(np.mean(stress_w)); mean_t=float(np.mean(stress_t)); mean_n=float(np.mean(stress_n))
    duration=len(out)/p['season_days']
    # Potencial dinámico; el techo se aplica al final para impedir rendimientos físicamente incoherentes con el ambiente objetivo.
    potential=p['cap_riego'] if regime=='Riego' else p['cap_temporal']
    raw=potential*(0.18+0.82*(mean_w**0.9))*(0.75+0.25*mean_t)*(0.70+0.30*mean_n)*min(1,duration)
    # Penalización adicional por lluvia insuficiente en etapas críticas aproximada mediante disponibilidad estacional.
    rain_total=float(out.rain_mm.sum())
    if regime=='Temporal':
        rain_factor=np.clip(rain_total/450,0.35,1.0)
        raw*=0.72+0.28*rain_factor
    yield_kg=float(np.clip(raw,0,potential))
    maturity = cum_gdd >= 0.92*p['season_days']*(p['opt_temp']-p['base_temp'])
    summary={'crop':crop_name,'soil':soil_name,'regime':regime,'days':len(out),'rain_total_mm':rain_total,
             'yield_kg_ha':yield_kg,'yield_t_ha':yield_kg/1000,'mean_water_factor':mean_w,
             'mean_temperature_factor':mean_t,'mean_n_factor':mean_n,'biomass_kg_ha':float(out.biomass_kg_ha.iloc[-1]),
             'maturity_reached':maturity,'gdd':cum_gdd,'cap_kg_ha':potential}
    return summary,out
