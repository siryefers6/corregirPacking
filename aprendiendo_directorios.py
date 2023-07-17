import os
archivo = os.path.exists('../Posiciones.xlsx')# mismo nivel
# archivo = os.path.exists('../Posiciones.xlsx')# Un nivel superior 
# archivo = os.path.exists('../miExtension/Posiciones.xlsx')# Un nivel superior dentro de una carpeta
# archivo = os.path.exists('../../Posiciones.xlsx')# dos niveles superiores
# archivo = os.path.exists('../../comandos_herramientas_linux/Posiciones.xlsx')# dos niveles superiores dentro de una carpeta

if archivo:
    print('archivo existe')
else:
    print('archivo no existe')