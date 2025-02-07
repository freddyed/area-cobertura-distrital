# Para hallar % de cobertura el area debe estar en km2 lo que hace
# necesario un sistema de referencia lineal, tipo 'EPSG:32718'

""" Mantener las geometrías en un sistema de referencia de coordenadas geográficas 
(como WGS 84, con EPSG:4326) puede producir cálculos de área incorrectos debido 
a la naturaleza de estas proyecciones. Las coordenadas geográficas usan grados de 
latitud y longitud, que no representan distancias uniformes en la superficie de la Tierra. 
Esto significa que las distancias y áreas medidas en estos sistemas pueden ser distorsionadas, 
especialmente en regiones alejadas del ecuador.

Para realizar cálculos precisos de área y distancia, es necesario re-proyectar las geometrías 
a un sistema de referencia de coordenadas proyectadas. Estos sistemas utilizan unidades lineales 
como metros, lo que permite obtener medidas más precisas. """

import geopandas as gpd
import pandas as pd
import os

# Lista de empresas, tecnologías y tipos de cobertura
empresas = ['bitel', 'claro', 'entel', 'movistar']  # Lista de nombres de empresas
tecnologias = ['2g', '3g', '4g', '5g']  # Lista de tecnologías
#tecnologias = ['2g']  # Lista de tecnologías
tipos_cobertura = ['cobertura_adicional', 'cobertura_garantizada']  # Lista de tipos de cobertura
#tipos_cobertura = ['cobertura_garantizada']  # Lista de tipos de cobertura

# Directorio base

base_dir = 'C:/Users/fhuillca/Desktop/Mapas inter-disueltos/'
ruta_shp_dis = 'C:/Users/fhuillca/Documents/DPRC/Análisis Regulatorio/Checa tu señal/GEO OSIPTEL/info empresas/z-distritos/DISTRITOS.shp'
dis = gpd.read_file(ruta_shp_dis)
dis_km2 = dis.to_crs('EPSG:32718')
# DataFrame acumulativo para todas las combinaciones
df_final = dis[['UBIGEO', 'DEPARTAMEN', 'PROVINCIA', 'DISTRITO']].copy()

for tecnologia in tecnologias:
    print(f'------------------------------')
    print(f'Procesando: {tecnologia}')
    print(f'------------------------------')
    for tipo_cobertura in tipos_cobertura:
        print(f'Procesando: {tipo_cobertura}')
        print(f'------------------------------')

        ruta_shp = os.path.join(base_dir, f"{tecnologia}-{tipo_cobertura}.shp")

        if not os.path.exists(ruta_shp):
            print(f'Archivo no encontrado: {ruta_shp}.')
            print(f'Saltando...')
            print(f'------------------------------')
            continue  # Salta al siguiente tipo de cobertura

        data = gpd.read_file(ruta_shp)
        data_km2 = data.to_crs('EPSG:32718')

        
        print(f'------------------------------------------------------------')
        print('Realizando intersección...')
        resultado_interseccion = gpd.overlay(dis_km2, data_km2, how='intersection')
        print(' --> Intersección concluida')
        print(f'------------------------------------------------------------')
        print('Disolviendo valores únicos a nivel distrital')

        # Obtener valores únicos de departamento, provincia y distrito
        valores_unicos = resultado_interseccion.dissolve(by=['DEPARTAMEN', 'PROVINCIA', 'DISTRITO']).reset_index()
        valores_unicos[f'area_km2-{tecnologia}-{tipo_cobertura}'] = round(valores_unicos['geometry'].area / 1e6, 4)
        print(valores_unicos.columns)
        print(valores_unicos)

        # Crear un DataFrame para guardar en Excel
        datos_para_excel = valores_unicos[['UBIGEO', 'DEPARTAMEN', 'PROVINCIA', 'DISTRITO', f'area_km2-{tecnologia}-{tipo_cobertura}']]

        # Merge con el DataFrame acumulativo
        df_final = df_final.merge(datos_para_excel, on=['DEPARTAMEN', 'PROVINCIA', 'DISTRITO'], how='left')

        # Renombrar UBIGEO_x a UBIGEO y eliminar UBIGEO_y si aparece
        df_final.rename(columns={'UBIGEO_x': 'UBIGEO'}, inplace=True)
        df_final.drop(columns=['UBIGEO_y'], errors='ignore', inplace=True)


        # Rellenar valores NaN con 0
        df_final[f'area_km2-{tecnologia}-{tipo_cobertura}'].fillna(0, inplace=True)

        # Guardar el DataFrame en un archivo Excel
        output_excel1 = os.path.join(base_dir, f'area_km2-{tecnologia}-{tipo_cobertura}')
        df_final.to_excel(output_excel1, index=False)
        print(f'Archivo Excel guardado en: {output_excel1}')

        """ for index, valor_unico in valores_unicos.iterrows():
            ubigeo = valor_unico['UBIGEO']
            departamento = valor_unico['DEPARTAMEN']
            provincia = valor_unico['PROVINCIA']
            distrito = valor_unico['DISTRITO']
            area = valor_unico[f'area_km2-{tecnologia}-{tipo_cobertura}'] """

# Guardar el DataFrame final en un solo archivo Excel
output_excel = os.path.join(base_dir, "area-cubierta-total.xlsx")
df_final.to_excel(output_excel, index=False)

print(f'Archivo Excel consolidado guardado en: {output_excel}')