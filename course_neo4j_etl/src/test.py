import pandas as pd
import csv

# Abrir el archivo CSV
with open('archivo.csv', newline='') as csvfile:

    # Cargar el archivo CSV original
    df = pd.read_csv('D:\Universidad\Semestre 11\Aplicación de IA Generativa\trabajo final\source_code_final\data\courses.csv')

    # Crear un DataFrame de partners únicos
    partners_df = pd.DataFrame(df['partner'].unique(), columns=['partner'])
    partners_df['partner_id'] = partners_df.index + 1

    # Crear un DataFrame de habilidades únicas
    # Asumiendo que las habilidades están en una columna separada por comas
    df['habilidades'] = df['habilidades'].str.replace(r'[{}]', '')  # Eliminar llaves si existen
    habilidades = df['habilidades'].str.split(',', expand=True).stack().str.strip().unique()
    habilidades_df = pd.DataFrame(habilidades, columns=['habilidad'])
    habilidades_df['habilidad_id'] = habilidades_df.index + 1

    # Reemplazar el nombre del partner con su ID en el DataFrame original
    df = df.merge(partners_df, how='left', on='partner')

    # Crear un DataFrame para los cursos con el partner_id
    cursos_df = df[['curso', 'partner_id']].copy()

    # Crear un DataFrame para las habilidades por curso
    cursos_habilidades = df[['curso', 'habilidades']].copy()
    cursos_habilidades = cursos_habilidades.set_index('curso')['habilidades'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).reset_index(name='habilidad')
    cursos_habilidades = cursos_habilidades.merge(habilidades_df, how='left', on='habilidad')
    cursos_habilidades = cursos_habilidades[['curso', 'habilidad_id']]

    # Guardar los DataFrames en archivos CSV separados
    partners_df.to_csv('partners.csv', index=False)
    habilidades_df.to_csv('habilidades.csv', index=False)
    cursos_df.to_csv('cursos.csv', index=False)
    cursos_habilidades.to_csv('cursos_habilidades.csv', index=False)

    print("Archivos CSV generados exitosamente.")