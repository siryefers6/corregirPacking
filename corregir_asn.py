import pandas as pd
import os
import time
import openpyxl

while True:
    try:
        carpeta_corregir = '../../Downloads/corregir'
        if not os.path.exists(carpeta_corregir):
            os.makedirs(carpeta_corregir)
        nombres_archivos = os.listdir('../../Downloads/corregir')
        if len(nombres_archivos) == 2:
            if nombres_archivos[0] == 'Posiciones.xlsx':
                archivo_a_corregir = nombres_archivos[0]
                archivo_corrector = nombres_archivos[1]
            elif nombres_archivos[1] == 'Posiciones.xlsx':
                archivo_a_corregir = nombres_archivos[1]
                archivo_corrector = nombres_archivos[0]
            else:
                archivo_a_corregir = nombres_archivos[0]
                archivo_corrector = nombres_archivos[1]
        if archivo_corrector and archivo_a_corregir:
            df1 = pd.read_excel(f'../../Downloads/corregir/{archivo_a_corregir}')
            df2 = pd.read_excel(f'../../Downloads/corregir/{archivo_corrector}')
            df1 = df1.sort_values(by='Pos')
            df1['Material'] = df1['Pos'].map(df2.set_index('Pos')['Material'])
            df1.to_excel(f'../../Downloads/{archivo_a_corregir}', index=False)
            os.remove(f'../../Downloads/corregir/{archivo_a_corregir}')
            os.remove(f'../../Downloads/corregir/{archivo_corrector}')
    except:
        continue
    time.sleep(2)
#Convertir archivo.py a .exe sin consola
#pyinstaller --onefile --noconsole --paths=C:\Users\sirye\Documents\Corregir_ASN\venv\Scripts corregir_asn.py