import requests
import pandas as pd
import numpy as np
from datetime import datetime
"""
milliseconds_to_minutes: Convertir milisegundos a minutos
"""
def milliseconds_to_minutes(milliseconds):
    """
    Convierte milisegundos a minutos.
    
    :param milliseconds: Tiempo en milisegundos.
    :return: Tiempo en minutos.
    """
    seconds = milliseconds / 1000  # Convertir milisegundos a segundos
    minutes = seconds / 60  # Convertir segundos a minutos
    return round(minutes)

"""
getMyDate: Obtener fecha a partir de un timestamp (ms)
"""
def getMyDate(timestamp_ms):
    return pd.to_datetime(timestamp_ms, unit='ms')
    
"""
checkArg: Revisar que se ingrese el núm correcto de argumentos
"""
def checkArg(arg1, arg2, arg3, arg4):
    # Contar cuántos argumentos no son None
    argumentos_proporcionados = sum(arg is not None for arg in [arg1, arg2, arg3, arg4])
    
    # Verificar si se ha proporcionado más de un argumento
    if argumentos_proporcionados > 1:
        raise ValueError("Debe proporcionar solo uno de los argumentos.")
    elif argumentos_proporcionados == 0:
        raise ValueError("Debe proporcionar al menos un argumento.")


class API:
    def __init__(self, urls,  header, parameters=None):
        self.header         = header      #Headers (estático)
        self.urls           = urls        #Lista con urls (dinámico)
        self.parameters     = parameters  #parametros (dinámico)
        self.myUrl          = urls if (type(urls) == str) else ""        #Url especifico que me interesa
        
        
    def doRequest(self, url=None):
        a0 = requests.get(self.myUrl, headers=self.header, params=self.parameters) if url is None else requests.get(url, headers=self.header, params=self.parameters)
        a1=  a0.json() 
        
        return a1

    def compressResults(self):
        a =  self.doRequest()
        a = pd.DataFrame(a)
        return a
    
    def findMyPagedResults(self, WIMU=True): #Para Wimu únicamente
        pageForm = "page" if (WIMU) else "Page"
        
        originalPage = self.parameters[pageForm]
        self.parameters[pageForm] = 1
        
        myPagedResults = []
        while True:
            myRequest =self.doRequest()
            
            if(len(myRequest)==0):
                break
            else:
                myPagedResults.append(myRequest)
                self.parameters[pageForm]+=1
                
        self.parameters[pageForm] = originalPage
    
        return myPagedResults