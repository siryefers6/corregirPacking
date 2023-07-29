import pandas as pd
import os
import time
import re
import PyPDF2
import shutil

def obtener_codigo(line):
  patron = r"\D\D\D.............{1,100}"
  codigo = re.findall(patron, line)
  codigo_limpio = codigo[0].strip()
  lista_cadenas = codigo_limpio.split(' ')
  codigo_prisa = lista_cadenas.pop(-1)
  lista_cadenas = ' '.join(lista_cadenas)
  codigo_completo = codigo_prisa + ' ' + lista_cadenas
  return codigo_completo

def leer_codigos_pdf(pdf_name):
    guia_1 = f'../../Downloads/corregir/{pdf_name}'

    pdf_reader = PyPDF2.PdfReader(guia_1)
    page = pdf_reader.pages[0]
    text = page.extract_text()
    lines = text.split('\n')

    inicio_items = lines.index('VentaCódigo Detalle PRECIO UNITARIO TOTALDEBE') + 1
    for index, line in enumerate(lines):
        if 'Res. 23  de 2006' in line:
            fin_items = index
            break
    if not fin_items:
        fin_items = 'No existe esta cadena'

    lines = lines[inicio_items:fin_items]
    df_3 = pd.DataFrame(data=lines)
    df_3[1] = df_3[0].apply(obtener_codigo)
    df_3 = df_3[1]
    lista_codigos = df_3.values.tolist()
    return lista_codigos

while True:
    try:
        carpeta_corregir = '../../Downloads/corregir'
        if not os.path.exists(carpeta_corregir):
            os.makedirs(carpeta_corregir)
        nombre_archivo_pdf = os.listdir('../../Downloads/corregir')[0]
        lista_codigos = leer_codigos_pdf(nombre_archivo_pdf)
        nombres_archivos = os.listdir('../../Downloads/corregir')
        nombres_archivos = nombres_archivos[1:]
        if len(nombres_archivos) == 2:
            numero_archivo1 = re.findall(r'\d{1,3}', nombres_archivos[0])
            numero_archivo1 = 0 if not numero_archivo1 else int(numero_archivo1[0])
            numero_archivo2 = re.findall(r'\d{1,3}', nombres_archivos[1])
            numero_archivo2 = 0 if not numero_archivo2 else int(numero_archivo2[0])
            if numero_archivo1 < numero_archivo2:
                archivo_a_corregir = nombres_archivos[0]
                archivo_corrector = nombres_archivos[1]
            elif numero_archivo1 > numero_archivo2:
                archivo_a_corregir = nombres_archivos[1]
                archivo_corrector = nombres_archivos[0]
        if archivo_corrector and archivo_a_corregir:
            df1 = pd.read_excel(f'../../Downloads/corregir/{archivo_a_corregir}')
            df2 = pd.read_excel(f'../../Downloads/corregir/{archivo_corrector}')
            df1 = df1.sort_values(by='Pos')
            df1_sin_duplicados = df1.drop_duplicates(subset='Pos')
            indices_diferentes = []
            codigos_a_corregir = []
            codigos_sap = []
            for idx, (valor_df1, valor_df2) in enumerate(zip(df1_sin_duplicados['Material'], df2['Material'])):
                if valor_df1 != valor_df2:
                    indices_diferentes.append(idx)
                    codigos_a_corregir.append(lista_codigos[idx])
                    codigos_sap.append(valor_df2)
            df_codigos = pd.DataFrame(data=codigos_a_corregir)
            df_codigos['Codigos SAP'] = codigos_sap
            df_codigos.to_csv('../../Pictures/codigos_a_corregir.csv', mode='a', header=False, index=False)
            df1['Material'] = df1['Pos'].map(df2.set_index('Pos')['Material'])
            df1.to_excel(f'../../Downloads/{archivo_a_corregir}', index=False)
            shutil.copy(f'../../Downloads/corregir/{nombre_archivo_pdf}', f'../../Downloads')
            os.remove(f'../../Downloads/corregir/{archivo_a_corregir}')
            os.remove(f'../../Downloads/corregir/{archivo_corrector}')
            os.remove(f'../../Downloads/corregir/{nombre_archivo_pdf}')
            df = pd.read_csv('../../Pictures/codigos_a_corregir.csv', header=None)
            df_sin_duplicados = df.drop_duplicates(subset=0)
            df_sin_duplicados.to_csv('../../Pictures/codigos_a_corregir.csv', index=False, header=False)
    except:
        time.sleep(1)
        continue
    time.sleep(1)
#Convertir archivo.py a .exe sin consola
#pyinstaller --onefile --noconsole --paths=C:\Users\sirye\Documents\Corregir_ASN\venv\Scripts corregir_asn.py