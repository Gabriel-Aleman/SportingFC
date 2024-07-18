import pandas as pd
import numpy as np
import matplotlib as plt
import os

documentos = "./src/dataFiles"
misArchivos = {"VALD"   : "forcedecks-test-export",
               "WIMU"   : "Masculina vs Heredia.xls",
               "GESDEP" : documentos}


# Obtener la lista de archivos y subdirectorios en el directorio especificado
contenido_directorio = os.listdir(documentos)
print(contenido_directorio)

for archivo in contenido_directorio:
    cntrStr = misArchivos["VALD"]

    if cntrStr in archivo:
        fecha = archivo[len(cntrStr):][1:-4].replace("_","/")
        misArchivos["VALD"]=archivo


# Lee el archivo CSV en un DataFrame de Pandas
df = pd.read_csv(f"{documentos}/{misArchivos["VALD"]}")

# Muestra las primeras filas del DataFrame para verificar que se haya cargado correctamente
print(df.head())