import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def boxDiag(df, columna, tittle):
    fig, ax = plt.subplots()
    # Generar el diagrama de caja
    box =ax.boxplot(x=df[columna], vert=False, patch_artist=True)
    # Colores personalizados
    # Colores de Seaborn
    colors = sns.color_palette("pastel", n_colors=3)  # Paleta 'pastel' con 3 colores

    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

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

def sesHist(df, column, tittle,  bins=10):
    # Crear la figura
    plt.figure(figsize=(10, 6))
    
    # Generar el histograma
    plt.hist(df[column], bins=bins, color='skyblue', edgecolor='black')
    
    # Título y etiquetas
    plt.title(f'Histograma: {tittle} - {column}', fontweight="bold")
    plt.xlabel(column)
    plt.ylabel('Frecuencia')
    
    # Retornar la figura actual    
    return plt.gcf()

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


def sesBoxAll(df,  tittle):
    # Crear una figura y un conjunto de subgráficas (una por columna)
    num_cols = len(df.select_dtypes(include='number').columns)
    # Crear la figura y los ejes
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))


    axs[0, 0].boxplot(df["Distancia m"])
    axs[0, 0].set_title("Distancia m", fontweight='bold')
    axs[0, 0].grid(axis="y")


    # Segundo gráfico
    axs[0, 1].boxplot(df["HSRAbsDistance"])
    axs[0, 1].set_title('HSRAbsDistance', fontweight='bold')
    axs[0, 1].grid(axis="y")


    # Tercer gráfico
    axs[1, 0].boxplot(df["highIntensityAccAbsCounter"])
    axs[1, 0].set_title('highIntensityAccAbsCounter', fontweight='bold')
    axs[1, 0].grid(axis="y")


    # Cuarto gráfico
    axs[1, 1].boxplot(df["highIntensityDecAbsCounter"])
    axs[1, 1].set_title('highIntensityDecAbsCounter', fontweight='bold')

    axs[1, 1].grid(axis="y")        # Primer gráfico

    fig.suptitle('Diagramas de caja (Sesión): '+tittle, fontsize=16, fontweight='bold')
    plt.tight_layout()

    return fig

def sesHisytAll(df,  tittle, bins=10):
    # Crear una figura y un conjunto de subgráficas (una por columna)
    num_cols = len(df.select_dtypes(include='number').columns)
    # Crear la figura y los ejes
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))


    axs[0, 0].hist(df["Distancia m"], binsbins=bins)
    axs[0, 0].set_title("Distancia m", fontweight='bold')
    axs[0, 0].grid(axis="y")


    # Segundo gráfico
    axs[0, 1].hist(df["HSRAbsDistance"], binsbins=bins)
    axs[0, 1].set_title('HSRAbsDistance', fontweight='bold')
    axs[0, 1].grid(axis="y")


    # Tercer gráfico
    axs[1, 0].hist(df["highIntensityAccAbsCounter"], binsbins=bins)
    axs[1, 0].set_title('highIntensityAccAbsCounter', fontweight='bold')
    axs[1, 0].grid(axis="y")


    # Cuarto gráfico
    axs[1, 1].hist(df["highIntensityDecAbsCounter"], binsbins=bins)
    axs[1, 1].set_title('highIntensityDecAbsCounter', fontweight='bold')

    axs[1, 1].grid(axis="y")        # Primer gráfico

    fig.suptitle('Diagramas de caja (Sesión): '+tittle, fontsize=16,  fontweight='bold')
    plt.tight_layout()

    return fig

def graficar_matriz_correlacion(df, s):
    # Calcular la matriz de correlación
    corr_matrix = df.corr()

    # Crear el heatmap
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)

    # Título del gráfico
    plt.title(f'Matriz de Correlación{s}')

    # Retornar la figura actual
    return plt.gcf()