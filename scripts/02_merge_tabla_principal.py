import pandas as pd
import numpy as np
import os

print("Iniciando Fase 2: Ensamblaje Maestro con Normalización de Circuitos (Delta)...")

# 1. Cargar los datasets necesarios
pit_stops_medias = pd.read_csv('data/pit_stops_medias.csv')
races = pd.read_csv('data/races.csv')
constructor_results = pd.read_csv('data/constructor_results.csv')
constructor_standings = pd.read_csv('data/constructor_standings.csv')
constructors = pd.read_csv('data/constructors.csv')

# MODIFICACIÓN CRÍTICA: Calcular el benchmark por carrera para obtener el Delta Relativo
# 'transform' calcula la media de la carrera y la expande para que coincida con el tamaño del grupo original
pit_stops_medias['race_baseline'] = pit_stops_medias.groupby('raceId')['mean_pit_stop'].transform('mean')
pit_stops_medias['delta_pit_stop'] = (pit_stops_medias['mean_pit_stop'] - pit_stops_medias['race_baseline']).round(3)

# 2. Filtrar carreras (2011 - 2024) e incluir 'round' para el ordenamiento cronológico
races_filtradas = races[(races['year'] >= 2011) & (races['year'] <= 2024)][['raceId', 'year', 'round', 'name']]
races_filtradas.rename(columns={'name': 'race_name'}, inplace=True)

# 3. Preparar tabla de constructores
constructors_subset = constructors[['constructorId', 'name']].rename(columns={'name': 'constructor_name'})

# 4. Ensamblaje progresivo (Merges)
df_maestro = pd.merge(pit_stops_medias, races_filtradas, on='raceId', how='inner')

df_maestro = pd.merge(df_maestro, constructor_results[['raceId', 'constructorId', 'points']], 
                      on=['raceId', 'constructorId'], how='left')
df_maestro.rename(columns={'points': 'race_points'}, inplace=True)

df_maestro = pd.merge(df_maestro, constructor_standings[['raceId', 'constructorId', 'points', 'position']], 
                      on=['raceId', 'constructorId'], how='left')
df_maestro.rename(columns={'points': 'season_points', 'position': 'championship_standing'}, inplace=True)

df_maestro = pd.merge(df_maestro, constructors_subset, on='constructorId', how='left')

# 5. Creación de la variable objetivo (Target) basada en el nuevo objetivo: Top 5
df_maestro['target_top5'] = np.where(df_maestro['championship_standing'] <= 5, 1, 0)

# 6. Ordenar por el flujo real del campeonato mundial
df_maestro.sort_values(by=['year', 'round', 'championship_standing'], ascending=[True, True, True], inplace=True)

# 7. Selección y orden final de las columnas estratégicas
columnas_finales = [
    'year', 'race_name', 'constructor_name', 
    'total_stops', 'mean_pit_stop', 'delta_pit_stop',
    'race_points', 'season_points', 'championship_standing', 'target_top5'
]
df_maestro = df_maestro[columnas_finales]

# 8. Guardar el dataset final de la verdad
ruta_salida = os.path.join('data', 'dataset_maestro_f1.csv')
df_maestro.to_csv(ruta_salida, index=False)

print(f"\n¡Pipeline ETL finalizado con éxito! Dataset maestro guardado en: {ruta_salida}")
print("\nMuestra del dataset final con la nueva variable Delta:")
print(df_maestro[['race_name', 'constructor_name', 'mean_pit_stop', 'delta_pit_stop', 'target_top5']].head(10))