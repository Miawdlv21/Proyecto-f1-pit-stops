import pandas as pd
import numpy as np
import os

# 1. Cargar los datasets desde la carpeta 'data' (Formato CSV puro)
pit_stops = pd.read_csv('data/pit_stops.csv')
results = pd.read_csv('data/results.csv')

# 2. Limpieza de la columna de tiempo (duration)
def limpiar_duracion(valor):
    try:
        # Intenta convertir a número directamente
        return float(valor)
    except ValueError:
        # Si tiene formato de minutos:segundos (ej. "1:25.400")
        partes = str(valor).split(':')
        if len(partes) == 2:
            minutos = float(partes[0])
            segundos = float(partes[1])
            return (minutos * 60) + segundos
        else:
            return np.nan

# Aplicamos la función
pit_stops['duration_seg'] = pit_stops['duration'].apply(limpiar_duracion)

# 3. Preparar la tabla puente (results)
results_subset = results[['raceId', 'driverId', 'constructorId']]

# 4. Cruce de datos (Merge)
pit_stops_merged = pd.merge(pit_stops, results_subset, on=['raceId', 'driverId'], how='inner')

# 5. Agrupación y cálculo de la media
pit_stops_mean = pit_stops_merged.groupby(['raceId', 'constructorId'])['duration_seg'].mean().reset_index()
pit_stops_mean.rename(columns={'duration_seg': 'mean_pit_stop'}, inplace=True)
pit_stops_mean['mean_pit_stop'] = pit_stops_mean['mean_pit_stop'].round(3)

# 6. GUARDAR EL RESULTADO
ruta_salida = os.path.join('data', 'pit_stops_medias.csv')
pit_stops_mean.to_csv(ruta_salida, index=False)

print(f"¡Proceso completado con éxito! Dataset guardado en: {ruta_salida}")
print(pit_stops_mean.head())