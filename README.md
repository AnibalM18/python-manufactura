# python-manufactura
# *Proyecto 1: Análisis de Producción por Turno* 
 
## Descripción 
Script en Python que lee datos de producción de una planta manufacturera, 
calcula métricas clave (producción total, tasa de calidad, paros) y genera 
un reporte automático desglosado por turno y por operador. 
 
## Herramientas utilizadas
- Python 3.13.13
- pandas 
 
## Cómo ejecutar 
```bash 
pip install pandas 
python analisis_produccion.py 
``` 
 
## Resultados esperados 
- Métricas globales: total producido, tasa de calidad, promedio de paros 
- Ranking de turnos por producción 
- Ranking de operadores por rendimiento 
- Archivo reporte_produccion.txt generado automáticamente 
 
## Conexión con manufactura 
Los KPIs calculados (tasa de calidad, tiempo de paro) son inputs directos 
para el cálculo de OEE (Overall Equipment Effectiveness)

