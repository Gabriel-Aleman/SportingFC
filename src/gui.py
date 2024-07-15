import tkinter as tk

# Función para manejar el evento del botón
def on_button_click():
    label.config(text="¡Botón presionado!")

# Crear la ventana principal
root = tk.Tk()
root.title("Sporting FC")

# Crear una etiqueta
label = tk.Label(root, text="Hola, mundo!")
label.pack(pady=20)

# Crear un botón
button = tk.Button(root, text="Presióname", command=on_button_click)
button.pack(pady=10)


root.iconbitmap('C:/Users/gabri/OneDrive/Escritorio/SportingFC/src/im/myIcon.ico')

# Iniciar el bucle principal de la aplicación
root.mainloop()
