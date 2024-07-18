#Importar librerias:
#%-------------------------------
import tkinter as tk
import ctypes

from data import *
from tkinter import messagebox
from time import strftime
from PIL import Image, ImageTk
#%-------------------------------

#VARIABLES:
lastLine = 100
image_path = "./src/im/"

misImagenes={"logo" :   image_path+"myIcon.ico",
              "cloud":  image_path+"sun.png",
              "search": image_path+"searchbar.jpeg",
              "search1":image_path+"bar.png",
              "button": image_path+"button.png",
              "loc":    image_path+"loc.png",
              "cuadro": image_path+"cuadro.png",
              "clk":    image_path+"clock.png"
              }
              


#FUNCIONES:

"""
update_label_T:   Actualizar el estado del calendario y reloj de forma 
                periodica
"""
def update_label_T():
    current_time = strftime("Hora: %H: %M: %S\nFecha: %d-%m-%Y ")
    clock_label.configure(text=current_time)
    clock_label.after(80, update_label_T)
    clock_label.place(x=0, y=500)

"""
get_entry_text_City: Obtener la ciudad ingresada por el usuario
"""
def get_entry_text_City():

    c = getWeatherData(textfield.get())

    if c!= None:
        label_Temperatura.config(text        =f"•Temperatura: {c["temp"]}°C")
        label_TemperaturaM.config(text=f"•Temp máx y min: {c["maxtemp"]}°C / {c["mintemp"]}°C")
        label_humedad.config(text       =f"•Humedad: {c["hum"]}%")
        label_viento.config(text   =f"•Viento: {c["wind"][0]} m/s {c["wind"][1]}°")
        label_ubicacion.config(text= f"{c["city"]}-{c["country"]}")
        label_presion.config(text= f"•Presión: {c["pressure"]} hPa")
        label_clk.config(text=c["tz"])
    else:
        messagebox.showerror("Error", f"No se han encontrado datos para la ubicación {textfield.get()}.")   



def begin(root):
    pass

#Main del programa:
if __name__ == "__main__":
    #Initi:
    #------------------------------------------------------------------------------------
    root = tk.Tk()
    root.config(bg="white")
    root.geometry("930x585")  # Ancho x Alto
    root.title("Sporting FC")
    root.resizable(False, False)

    myappid = 'mycompany.myproduct.subproduct.version' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    root.iconbitmap(misImagenes["logo"]) #Logo
    
    global c
    c = getWeatherData()
    #------------------------------------------------------------------------------------

    #Reloj
    clock_label = tk.Label(
        root, bg="#347aeb", fg="white", font=("System", 25, "bold"), relief="flat", width=60
    )

    # Barra de exploración:
    image = Image.open(misImagenes["search1"])
    image = image.resize((820, 70))
    photo = ImageTk.PhotoImage(image)

    bar = tk.Label(root, image=photo, bg="white", fg="white")
    bar.place(x=0, y=20)
  
    entry_var = tk.StringVar()
    entry_var.set("'Ingrese una ubicación'")  # Establecer texto predeterminado

    textfield=tk.Entry(root, justify="center", width=35, font=("calibri", 23),  border=0, fg="black",  textvariable=entry_var)
    textfield.place(x=150, y=35)

    #Imagen de fondo:
    image = Image.open(misImagenes["cloud"])
    image = image.resize((300,300))
    back  = ImageTk.PhotoImage(image)

    bar = tk.Label(root, image=back, bg="white")
    bar.place(x=100, y=150)

    #Boton de busqueda 
    b = Image.open(misImagenes["button"])
    b = b.resize((60, 60))  # Redimensionar la imagen si es necesario
    b = ImageTk.PhotoImage(b)

    botonBusq = tk.Button(root, image=b, bg="white", padx=30, command=get_entry_text_City)
    botonBusq.place(x=812, y=24)

    # Vincular la tecla Enter a la función de búsqueda
    root.bind('<Return>', lambda event: get_entry_text_City())

    #Parametros
    box = Image.open(misImagenes["cuadro"])
    box = box.resize((480, 350))
    box = ImageTk.PhotoImage(box)

    myBox = tk.Label(root, image=box, bg="white")
    myBox.place(x=425, y=115)

    label_Temperatura   = tk.Label(text=f"•Temperatura: {c["temp"]}°C",fg="black", bg="white", font=("Arial", 20))
    label_Temperatura.place(x=450, y=200)

    label_TemperaturaM  = tk.Label(text=f"•Temp máx y min: {c["maxtemp"]}°C / {c["mintemp"]}°C",fg="black", bg="white", font=("Arial", 20))
    label_TemperaturaM.place(x=450, y=240)

    label_humedad       = tk.Label(text=f"•Humedad: {c["hum"]}%",fg="black", bg="white", font=("Arial", 20))
    label_humedad.place(x=450, y=280)

    label_viento        = tk.Label(text=f"•Viento: {c["wind"][0]} m/s {c["wind"][1]}°",fg="black", bg="white", font=("Arial", 20))
    label_viento.place(x=450, y=320)

    label_presion        = tk.Label(text=f"•Presión: {c["pressure"]} hPa",fg="black", bg="white", font=("Arial", 20))
    label_presion.place(x=450, y=360)

    loc = Image.open(misImagenes["loc"])
    loc = loc.resize((60, 65))
    loc = ImageTk.PhotoImage(loc)

    #Ubicación:
    myLoc = tk.Label(root, image=loc, bg="white")
    myLoc.place(x=0, y=120)

    label_ubicacion     = tk.Label(text="San José-CR",fg="red", bg="white", font=("Arial", 15, "bold"))
    label_ubicacion.place(x=55, y=140)

    #Zona horaria:
    clk = Image.open(misImagenes["clk"])
    clk = clk.resize((40, 40))
    clk = ImageTk.PhotoImage(clk)

    myClk = tk.Label(root, image=clk, bg="white")
    myClk.place(x=20, y=200)

    label_clk     = tk.Label(text=f"{c["tz"]}",fg="black", bg="white", font=("console", 12, "bold"))
    label_clk.place(x=65, y=200)

    update_label_T() #Actualizar reloj 

    # Iniciar el bucle principal de la aplicación
    root.mainloop()
