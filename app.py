import streamlit as st
import pandas as pd, numpy as np
import plotly.express as px
from model import simulate
from parameters import CROPS, SOILS
from weather import validate_weather

st.set_page_config(page_title='SAS — Simulador Agronómico Sombrerete', layout='wide')
st.title('SAS — Simulador Agronómico Sombrerete')
st.caption('Motor de simulación diario para clima + suelo + cultivo + manejo | Modelo propio calibrable')

with st.sidebar:
    st.header('1. Clima')
    f=st.file_uploader('Cargar clima CSV', type=['csv'])
    st.caption('Columnas: date,rain_mm,tmax_c,tmin_c,rad_mj_m2')
    st.header('2. Suelo')
    soil=st.selectbox('Textura',list(SOILS))
    water=st.slider('Agua inicial disponible',0.1,1.0,0.65,0.05)
    st.header('3. Cultivo')
    crop=st.selectbox('Cultivo',list(CROPS))
    st.header('4. Manejo')
    regime=st.selectbox('Régimen',['Temporal','Riego'])
    sow=st.date_input('Fecha de siembra',value=pd.Timestamp('2026-06-15'))
    n=st.number_input('N aplicado (kg N/ha)',0.0,300.0,40.0,5.0)
    irr=st.number_input('Riego total (mm)',0.0,800.0,0.0,10.0)
    residue=st.slider('Cobertura/residuo superficial',0.0,1.0,0.2,0.05)

if f:
    try: weather=validate_weather(pd.read_csv(f))
    except Exception as e: st.error(str(e)); st.stop()
else:
    dates=pd.date_range('2026-06-15',periods=160,freq='D'); rng=np.random.default_rng(42)
    rain=np.where(rng.random(160)<0.28,rng.gamma(2.0,7.0,160),0)
    tmean=19+7*np.sin(np.linspace(0,2*np.pi,160))+rng.normal(0,2,160)
    weather=pd.DataFrame({'date':dates,'rain_mm':rain,'tmax_c':tmean+8,'tmin_c':tmean-8,'rad_mj_m2':20+3*np.sin(np.linspace(0,2*np.pi,160))})
    st.info('Se está usando un clima sintético de demostración. Para uso profesional carga datos diarios de una estación trazable.')

summary, daily=simulate(weather,crop,soil,regime,sow,water,n,irr,1.0,residue)

c1,c2,c3,c4=st.columns(4)
c1.metric('Rendimiento',f"{summary['yield_kg_ha']:,.0f} kg/ha")
c2.metric('Lluvia',f"{summary['rain_total_mm']:.0f} mm")
c3.metric('Biomasa',f"{summary['biomass_kg_ha']:,.0f} kg/ha")
c4.metric('Techo del escenario',f"{summary['cap_kg_ha']:,.0f} kg/ha")

st.subheader('Diagnóstico de la simulación')
st.write({k:v for k,v in summary.items() if k not in ['crop','soil','regime']})

fig=px.line(daily,x='date',y=['water_factor','temp_factor','n_factor'],labels={'value':'Factor 0–1','variable':'Factor'})
st.plotly_chart(fig,use_container_width=True)
fig2=px.line(daily,x='date',y=['biomass_kg_ha','water_mm'],labels={'value':'Valor','variable':'Variable'})
st.plotly_chart(fig2,use_container_width=True)

st.subheader('Resultados diarios')
st.dataframe(daily,use_container_width=True)

st.warning('Validación: los techos de rendimiento son restricciones del escenario, no sustituyen la calibración con datos observados. Un resultado de simulación debe contrastarse con parcelas independientes.')
