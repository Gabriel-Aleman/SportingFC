import matplotlib.pyplot as plt
import seaborn as sns

def barZ(df, dfProm, ses=None, jugador=None):
    df = df.loc[ses] if  (ses is not None) else  df.loc[jugador] if  (jugador is not None) else None
    dfProm = dfProm.loc[ses]["Promedios Z score"] if  (ses is not None) else  dfProm.loc[jugador]["Promedios Z score"] if  (jugador is not None) else None
    tit =  ses if  (ses is not None) else  jugador if  (jugador is not None) else None
    valores = df["Z score Average"].to_list()
    ids = df.index


    limite_positivo = 1.5
    limite_negativo =-1.5
    fig, ax = plt.subplots()

    upper, lower= False, False
    # Dibujar las barras
    for i in range(len(valores)):
        valor = valores[i]
        i = ids[i]
        if valor > limite_positivo:
            upper =True
            # Parte dentro del límite positivo
            ax.bar(i, limite_positivo, color='#e9e9e9', edgecolor='black')
            # Parte fuera del límite positivo
            ax.bar(i, valor - limite_positivo, bottom=limite_positivo, color='#bc5566', edgecolor='black')
        elif valor < limite_negativo:
            lower = True
            # Parte fuera del límite negativo
            ax.bar(i, valor-limite_negativo, bottom=limite_negativo, color='#55a5bc', edgecolor='black')
            # Parte dentro del límite negativo
            ax.bar(i, limite_negativo, color='#e9e9e9', edgecolor='black')
        else:
            # Parte dentro del rango
            ax.bar(i, valor, color='#e9e9e9', edgecolor='black')

    # Agregar líneas para los límites
    if upper:
        ax.axhline(limite_positivo, color='black', linewidth=3, linestyle=':')
    if lower:
        ax.axhline(limite_negativo, color='black', linewidth=3, linestyle=':')
    
    ax.axhline(y=dfProm, color='b', linestyle='--', label=f'Promedio z score {tit}')
    

    # Ajustar etiquetas y mostrar el gráfico

    ax.grid(axis="y")
    ax.set_title(f"Z scores: {tit}", fontweight='bold')
    #ax.set_xticklabels(ids, rotation=90)
    ax.legend(loc=(0,0.25))
    return fig

def boxDiag(df, columna, tittle):
    fig, ax = plt.subplots()
    # Colores de Seaborn
    palette = sns.color_palette("Set3")  # Paleta 'pastel' con 3 colores

    sns.boxplot(x=df[columna], palette=palette, width=0.6, linewidth=1.5)

    # Título y etiquetas
    ax.set_title(f'Diagrama de Caja: {tittle} - {columna}', fontweight="bold")
    ax.grid(axis="x")
    ax.set_ylabel("Distribución")
    
    # Retornar la figura actual
    return fig

def sesGraph(df, column, tittle, myColor="r"):
    a= df.index if(df.index.dtype != 'int64') else df["Jugador"]

    a =[i[:9]+"." for i in a]

    fig, ax = plt.subplots()
    ax.bar(a, df[column], color=myColor)
    ax.grid(axis="y")
    ax.tick_params(axis='x', rotation=80) #90 grados para que las etiquetas estén horizontales
    ax.set_title(f'Resultados ({column}): '+tittle, fontweight='bold')
    return fig

def playGraph(df, column, tittle, myColor="r"):
    a= df["Creado (fecha)"]

    fig, ax = plt.subplots()
    ax.plot(a, df[column], color=myColor, linestyle="--", marker='o')
    ax.set_xticks(a)
    ax.set_xticklabels(df.index)
    ax.grid(axis="y")
    ax.tick_params(axis='x', rotation=90) #90 grados para que las etiquetas estén horizontales
    ax.set_title(f'Resultados ({column}): '+tittle, fontweight='bold')
    return fig

def sesHist(df, column, tittle,  bins=10):
    # Crear la figura
    plt.figure(figsize=(10, 6))
    
    # Generar el histograma
    plt.hist(df[column], bins=bins, color='skyblue', edgecolor='black')
    
    # Título y etiquetas
    plt.title(f'Histograma: {tittle} - {column}', fontweight="bold")
    plt.xlabel(column)
    plt.ylabel('Frecuencia')
    
    plt.grid(axis="x")
    # Retornar la figura actual    
    return plt.gcf()


def playGraphAll(df,  tittle):
    a= df["Creado (fecha)"]
    # Crear la figura y los ejes
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    ang = 100
    # Primer gráfico
    axs[0, 0].plot(a,df["Distancia m"], color="r", marker='o')
    axs[0, 0].set_title("Distancia m", fontweight='bold')
    axs[0, 0].tick_params(axis='x', labelrotation=ang)
    axs[0, 0].set_xticks(a)
    axs[0, 0].set_xticklabels(df.index)
    axs[0, 0].grid(axis="y")


    # Segundo gráfico
    axs[0, 1].plot(a,df["HSRAbsDistance"], color='g', marker='o')
    axs[0, 1].set_title('HSRAbsDistance', fontweight='bold')
    axs[0, 1].tick_params(axis='x', labelrotation=ang)
    axs[0, 1].set_xticks(a)
    axs[0, 1].set_xticklabels(df.index)
    axs[0, 1].grid(axis="y")


    # Tercer gráfico
    axs[1, 0].plot(a,df["highIntensityAccAbsCounter"], color='b', marker='o')
    axs[1, 0].set_title('highIntensityAccAbsCounter', fontweight='bold')
    axs[1, 0].tick_params(axis='x', labelrotation=ang)
    axs[1, 0].set_xticks(a)
    axs[1, 0].set_xticklabels(df.index)
    axs[1, 0].grid(axis="y")


    # Cuarto gráfico
    axs[1, 1].plot(a,df["highIntensityDecAbsCounter"], color='m', marker='o')
    axs[1, 1].set_title('highIntensityDecAbsCounter', fontweight='bold')
    axs[1, 1].tick_params(axis='x', labelrotation=ang)
    axs[1, 1].set_xticks(a)
    axs[1, 1].set_xticklabels(df.index)
    axs[1, 1].grid(axis="y")

    # Añadir título global a toda la figura
    fig.suptitle('Resultados (jugador): '+tittle, fontsize=16, fontweight='bold' )

    # Ajustar el espaciado entre subgráficas
    plt.tight_layout()

    return fig

def sesGraphAll(df,  tittle):
    a= df.index if(df.index.dtype != 'int64') else df["Jugador"]
    a =[i[:9]+"." for i in a]
    
    # Crear la figura y los ejes
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    ang = 60
    # Primer gráfico
    axs[0, 0].bar(a,df["Distancia m"], color='r')
    axs[0, 0].set_title("Distancia m", fontweight='bold')
    axs[0, 0].tick_params(axis='x', labelrotation=ang)
    axs[0, 0].grid(axis="y")


    # Segundo gráfico
    axs[0, 1].bar(a,df["HSRAbsDistance"], color='g')
    axs[0, 1].set_title('HSRAbsDistance', fontweight='bold')
    axs[0, 1].tick_params(axis='x', labelrotation=ang)
    axs[0, 1].grid(axis="y")


    # Tercer gráfico
    axs[1, 0].bar(a,df["highIntensityAccAbsCounter"], color='b')
    axs[1, 0].set_title('highIntensityAccAbsCounter', fontweight='bold')
    axs[1, 0].tick_params(axis='x', labelrotation=ang)
    axs[1, 0].grid(axis="y")


    # Cuarto gráfico
    axs[1, 1].bar(a,df["highIntensityDecAbsCounter"], color='m')
    axs[1, 1].set_title('highIntensityDecAbsCounter', fontweight='bold')
    axs[1, 1].tick_params(axis='x', labelrotation=ang)
    axs[1, 1].grid(axis="y")

    # Añadir título global a toda la figura
    fig.suptitle('Resultados (Sesión): '+tittle, fontsize=16, fontweight='bold' )

    # Ajustar el espaciado entre subgráficas
    plt.tight_layout()

    return fig


def sesBoxAll(df,  tittle, type=""):
    # Crear la figura y los ejes
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))


    sns.boxplot(x=df["Distancia m"], ax=axs[0, 0], color="#4287f5", linecolor="#2b2b2b", linewidth=.75)
    axs[0, 0].set_title("Distancia m", fontweight='bold')
    axs[0, 0].grid(axis="y")
    axs[0, 0].set_xlabel("Distribución")


    # Segundo gráfico
    sns.boxplot(x=df["HSRAbsDistance"], ax=axs[0, 1], color="#4287f5", linecolor="#2b2b2b", linewidth=.75)
    axs[0, 1].set_title('HSRAbsDistance', fontweight='bold')
    axs[0, 1].grid(axis="y")
    axs[0, 1].set_xlabel("Distribución")


    # Tercer gráfico
    sns.boxplot(x=df["highIntensityAccAbsCounter"], ax=axs[1, 0], color="#4287f5", linecolor="#2b2b2b", linewidth=.75)
    axs[1, 0].set_title('highIntensityAccAbsCounter', fontweight='bold')
    axs[1, 0].grid(axis="y")
    axs[1, 0].set_xlabel("Distribución")


    # Cuarto gráfico
    sns.boxplot(x=df["highIntensityDecAbsCounter"], ax=axs[1, 1], color="#4287f5", linecolor="#2b2b2b", linewidth=.75)

    axs[1, 1].set_title('highIntensityDecAbsCounter', fontweight='bold')
    axs[1, 1].grid(axis="y")        
    axs[1, 1].set_xlabel("Distribución")


    fig.suptitle('Diagramas de caja: '+tittle, fontsize=16, fontweight='bold')
    plt.tight_layout()

    return fig

def sesHisytAll(df,  tittle, bins=10):
    # Crear la figura y los ejes
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))


    axs[0, 0].hist(df["Distancia m"], bins=bins)
    axs[0, 0].set_title("Distancia m", fontweight='bold')
    axs[0, 0].grid(axis="y")


    # Segundo gráfico
    axs[0, 1].hist(df["HSRAbsDistance"], bins=bins)
    axs[0, 1].set_title('HSRAbsDistance', fontweight='bold')
    axs[0, 1].grid(axis="y")


    # Tercer gráfico
    axs[1, 0].hist(df["highIntensityAccAbsCounter"], bins=bins)
    axs[1, 0].set_title('highIntensityAccAbsCounter', fontweight='bold')
    axs[1, 0].grid(axis="y")


    # Cuarto gráfico
    axs[1, 1].hist(df["highIntensityDecAbsCounter"], bins=bins)
    axs[1, 1].set_title('highIntensityDecAbsCounter', fontweight='bold')

    axs[1, 1].grid(axis="y")        # Primer gráfico

    fig.suptitle('Diagramas de caja: '+tittle, fontsize=16,  fontweight='bold')
    plt.tight_layout()
#TODO: SESION O JUGADOR SEGÚN GRÁFICO
    return fig

def graficar_matriz_correlacion(df, title):
    plt.figure(figsize=(8, 6))  # Ancho=8 pulgadas, Alto=6 pulgadas
    # Crear la matriz de correlación
    matriz_correlacion = df.corr()

    # Crear un mapa de calor con colores
    sns.heatmap(matriz_correlacion, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, linewidths=0.5)

    # Añadir un título
    plt.title(f'Matriz de Correlación {title}')

    plt.xticks( rotation=30, ha='right')
    return plt.gcf()