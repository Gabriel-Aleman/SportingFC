from tkinter import *
import tkinter.font as font
import requests

from googletrans import Translator
from datetime import datetime, timedelta, timezone

def obtener_hora_por_desplazamiento_segundos(desplazamiento_segundos):
    # Crear un objeto timezone con el desplazamiento horario dado en segundos
    zona_horaria = timezone(timedelta(seconds=desplazamiento_segundos))
    
    # Obtener la hora actual en UTC
    hora_utc = datetime.now(timezone.utc)
    
    # Convertir la hora UTC a la zona horaria dada
    hora_local = hora_utc.astimezone(zona_horaria)
       
    # Formatear la fecha y hora omitiendo los segundos
    fecha_hora_formateada = hora_local.strftime('%H:%M \n%m-%d')

    return fecha_hora_formateada

"""
getWeatherData: Obtener información del clima en determinada ciudad
    inputs:
        -city (str): Ciudad de la que deseo información (default: SJ-CR)
    outputs:
        -(dic): Datos que incluyen temperatura, temperaturas máxima y 
                minima registradas, viento (velocidad y ángulo), humedad
                descripción general del clima y país.
"""
def getWeatherData(city = "San José,SJ,CR"):
    api_key = "b162cb08d9dd5cde1df5ad708aab10fe"  
    url="http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": f"{city}",
        "appid": api_key,
        "units": "metric"
    }

    weather_data = requests.get(url, params=params)

    if weather_data.json()['cod'] == '404': #Revisar si API funciona
        print("ERROR 404, API clima")
        return None

    else:
        myWdata = weather_data.json()
        temp       = myWdata['main']['temp']
        maxtemp    = myWdata['main']['temp_max']
        mintemp    = myWdata['main']['temp_min']
        pressure  = myWdata["main"]["pressure"]
        hum        = myWdata['main']['humidity']
        wind       = [myWdata['wind']["speed"],myWdata['wind']["deg"]] #[Velocidad, Ángulo]
        country    = myWdata["sys"]["country"]
        
        timeZ      = obtener_hora_por_desplazamiento_segundos(myWdata["timezone"])
        weather    = myWdata['weather'][0]['main']

        return { 
                "temp"      : temp      ,     
                "maxtemp"   : maxtemp   ,
                "mintemp"   : mintemp   ,
                "wind"      : wind      ,
                "hum"       : hum       ,
                "weather"   :  weather  ,
                "country"   : country   ,
                "pressure"  : pressure,
                "city"      : city,
                "all"       : myWdata,
                "tz"        :timeZ
                }

#Testbench:
a=getWeatherData("Madrid")
a=a["tz"]
print(a)