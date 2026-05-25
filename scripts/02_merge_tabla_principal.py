import pandas as pd
import os

print("Iniciando Fase 2: Ensamblaje del Dataset Maestro (Corrección de Orden Cronológico)...")

# 1. Cargar los datasets necesarios
pit_stops_medias = pd.read_csv('data/pit_stops_medias.csv')
races = pd.read_csv('data/races.csv')
constructor_results = pd.read_csv('data/constructor_results.csv')
constructor_standings = pd.read_csv('data/constructor_standings.csv')
constructors = pd.read_csv('data/constructors.csv')

# 2. Filtrar carreras (2011 - 2024) e incluir 'round' para el ordenamiento
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

# 5. CORRECCIÓN: Ordenar cronológicamente por año y número de ronda del calendario, 
# y finalmente por posición en el campeonato
df_maestro.sort_values(by=['year', 'round', 'championship_standing'], ascending=[True, True, True], inplace=True)

# 6. Selección y orden final de las columnas (Omitimos 'round' para respetar tu lista de variables)
columnas_finales = [
    'year', 'race_name', 'constructor_name', 
    'mean_pit_stop', 'race_points', 'season_points', 'championship_standing'
]
df_maestro = df_maestro[columnas_finales]

# 7. Guardar el dataset resultante
ruta_salida = os.path.join('data', 'dataset_maestro_f1.csv')
df_maestro.to_csv(ruta_salida, index=False)

print(f"\n¡Ensamblaje completado con éxito! Dataset maestro guardado en: {ruta_salida}")
print("\nPrimeras 5 filas del dataset final (Validación de orden cronológico):")
print(df_maestro.head())