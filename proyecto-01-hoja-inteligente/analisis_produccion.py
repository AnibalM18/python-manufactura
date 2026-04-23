# ============================================================
# ANÁLISIS DE PRODUCCIÓN POR TURNO
# Proyecto 1 — Python para Manufactura Inteligente
# Autor: Anibal Moreno
# ============================================================

import pandas as pd   # La librería estrella para datos tabulares
import os              # Para manejar rutas de archivos

# -------Lectura de datos-------
RUTA_DATOS= os.path.join('datos','produccion.csv') 

df = pd.read_csv(RUTA_DATOS, parse_dates=['fecha']) 

print("===VISTA PREVIA DE LOS DATOS===")
print(df.head(5))  # Muestra las primeras 5 filas
print()
print(f'Filas: {len(df)} | Columnas: {len(df.columns)}')
print(f'Columnas: {list(df.columns)}')

# ------ Exploración basica -------
print('=== TIPOS DE DATOS POR COLUMNA ===')
print(df.dtypes)
print()
print('=== ESTADÍSTICAS DESCRIPTIVAS ===')
print(df.describe())

# ------ Metricas globales -------
total_producido  = df['unidades_producidas'].sum() 
total_defectuoso = df['unidades_defectuosas'].sum() 
promedio_paro    = df['tiempo_paro_min'].mean() 
max_produccion   = df['unidades_producidas'].max() 
min_produccion   = df['unidades_producidas'].min()

 
# Calcular la tasa de calidad global 
tasa_calidad = (1 - total_defectuoso / total_producido) * 100 
 
print('=== MÉTRICAS GLOBALES ===') 
print(f'Total producido:      {total_producido:,} unidades') 
print(f'Total defectuoso:     {total_defectuoso:,} unidades') 
print(f'Tasa de calidad:      {tasa_calidad:.2f}%') 
print(f'Promedio de paros:    {promedio_paro:.1f} min/turno') 
print(f'Máxima producción:    {max_produccion} unidades') 
print(f'Mínima producción:    {min_produccion} unidades') 

# ------ Análisis por turno ------ 
metricas_turno = df.groupby('turno').agg( 
    produccion_promedio = ('unidades_producidas', 'mean'), 
    produccion_total    = ('unidades_producidas', 'sum'), 
    defectos_promedio   = ('unidades_defectuosas', 'mean'), 
    paro_promedio_min   = ('tiempo_paro_min', 'mean'), 
).round(1)    # Redondear a 1 decimal 

# Calcular la tasa de calidad por turno 
metricas_turno['tasa_calidad_%'] = ( 
    (1 - df.groupby('turno')['unidades_defectuosas'].sum() / 
         df.groupby('turno')['unidades_producidas'].sum()) * 100 
).round(2) 
 
print('=== MÉTRICAS POR TURNO ===') 
print(metricas_turno.to_string()) 

# ------ Análisis por operador ------ 
metricas_operador = df.groupby('operador').agg( 
    turnos_trabajados    = ('fecha', 'count'), 
    produccion_promedio  = ('unidades_producidas', 'mean'), 
    defectos_promedio    = ('unidades_defectuosas', 'mean'), 
).round(1) 
 
# Ranking de operadores por producción promedio 
metricas_operador = metricas_operador.sort_values( 
    'produccion_promedio', ascending=False 
) 
 
print('=== RANKING DE OPERADORES (por producción promedio) ===') 
print(metricas_operador.to_string()) 

# ------ Reporte final ------ 
turno_mejor = metricas_turno['produccion_promedio'].idxmax() 
turno_peor  = metricas_turno['produccion_promedio'].idxmin() 
operador_top = metricas_operador['produccion_promedio'].idxmax() 
 
reporte = f''' 
{'='*55} 
   REPORTE DE PRODUCCIÓN — SEMANA DEL 2024-01-02 
{'='*55} 
 
    RESUMEN GLOBAL 
    Total de unidades producidas : {total_producido:,} 
    Total de unidades defectuosas: {total_defectuoso:,} 
    Tasa de calidad global       : {tasa_calidad:.2f}% 
    Tiempo de paro promedio      : {promedio_paro:.1f} min/turno 
 
    ANÁLISIS DE TURNOS 
    Turno con mayor producción   : {turno_mejor} 
    Turno con menor producción   : {turno_peor} 
 
    OPERADORES 
    Operador con mayor rendimiento: {operador_top} 
 
    ACCIONES SUGERIDAS 
    - Revisar causas de paro en turno {turno_peor} 
    - Documentar prácticas del turno {turno_mejor} como best practice 
{'='*55} 
''' 
 
print(reporte) 
 
# Guardar el reporte en un archivo de texto 
with open('reporte_produccion.txt', 'w', encoding='utf-8') as f: 
    f.write(reporte) 
 
print('Reporte guardado como reporte_produccion.txt') 
