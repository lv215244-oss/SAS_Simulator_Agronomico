# Arquitectura científica de SAS

## Flujo diario

1. Clima: lluvia, Tmax, Tmin y radiación.
2. Suelo: almacén de agua disponible, infiltración, escorrentía y extracción.
3. Cultivo: grados-día, respuesta térmica, crecimiento de biomasa y demanda de N.
4. Manejo: fecha de siembra, régimen hídrico, N, riego y cobertura.
5. Rendimiento: potencial específico del cultivo × factores de agua × temperatura × N × duración × condición de temporal.

## Validación

El motor debe evolucionar hacia calibración independiente con observaciones de Sombrerete. Las métricas objetivo son RMSE, R², NSE y sesgo. La validación debe hacerse con campañas/sitios no utilizados para calibración.

## Control de plausibilidad

Los límites de temporal son una barrera de seguridad agronómica para impedir predicciones manifiestamente incompatibles con el alcance regional definido por el proyecto. No deben usarse como sustituto de datos de rendimiento observados.
