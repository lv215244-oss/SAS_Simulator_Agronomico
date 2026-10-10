# SAS — Simulador Agronómico Sombrerete

Software experimental/profesional de simulación agronómica orientado a Sombrerete, Zacatecas.

## Alcance

SAS reproduce la arquitectura conceptual de un simulador de sistemas de cultivo: **clima + suelo + cultivo + manejo**, con paso de tiempo diario, balance hídrico simplificado por capas, desarrollo fenológico, acumulación de biomasa, estrés hídrico/térmico/nutricional y conversión a rendimiento.

Cultivos incluidos:
- Frijol negro
- Frijol pinto
- Maíz
- Calabaza
- Trigo
- Cebada

## Importante

SAS es un modelo propio y **no es APSIM ni pretende ser matemáticamente idéntico a APSIM**. Un simulador profesional requiere calibración con observaciones locales y validación independiente. La aplicación incluye controles para no confundir una simulación con un dato observado.

## Rendimientos objetivo para temporal

Los límites son deliberadamente conservadores para el ambiente de referencia de Sombrerete y pueden modificarse por ambiente/cultivar durante la calibración:

- Frijol negro: 2,000 kg/ha
- Frijol pinto: 2,000 kg/ha
- Calabaza: 900 kg/ha
- Trigo: 4,500 kg/ha
- Cebada: 4,500 kg/ha
- Maíz: 7,500 kg/ha (ajustable según híbrido y régimen hídrico)

Estos valores son **techos de validación del modelo**, no afirmaciones de que cada parcela alcance esos rendimientos.

## Datos climáticos

La aplicación acepta CSV diario con:
`date,rain_mm,tmax_c,tmin_c,rad_mj_m2`

Para uso profesional se recomienda alimentar el modelo con registros de estaciones CONAGUA/SMN o una fuente meteorológica trazable. CONAGUA publica información histórica de estaciones convencionales, incluida precipitación y temperaturas.

## Instalación

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Diseño

- `app.py`: interfaz Streamlit.
- `sas/model.py`: motor diario.
- `sas/parameters.py`: parámetros de cultivos y suelo.
- `sas/weather.py`: carga/validación de clima.
- `sas/validation.py`: métricas RMSE, R² y NSE.
- `tests/`: pruebas automáticas.
- `data/example_weather.csv`: clima sintético únicamente para probar el programa; **no usar como clima real**.

## Siguiente nivel de validación

1. Recopilar 5–10 campañas de parcelas de Sombrerete.
2. Separar calibración y validación por campaña.
3. Ajustar parámetros genéticos/eco-fisiológicos con datos observados.
4. Evaluar RMSE, R², sesgo y NSE para rendimiento y fenología.
5. Validar por separado temporal y riego.
6. No calibrar los parámetros para alcanzar un rendimiento deseado.
