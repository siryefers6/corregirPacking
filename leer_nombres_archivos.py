import os
import pandas as pd

# Crea una lista con todos los archivos de una carpeta
nombres_archivos = os.listdir('../../Downloads/corregir')
print(nombres_archivos)
if nombres_archivos[0] == 'Posiciones.xlsx':
    archivo_a_corregir = nombres_archivos[0]
    archivo_corrector = nombres_archivos[1]
elif nombres_archivos[1] == 'Posiciones.xlsx':
    archivo_a_corregir = nombres_archivos[1]
    archivo_corrector = nombres_archivos[0]
else:
    archivo_a_corregir = nombres_archivos[0]
    archivo_corrector = nombres_archivos[1]