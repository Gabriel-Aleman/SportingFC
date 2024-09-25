from wimu import *
from graphs import *
import streamlit as st
from io import BytesIO

from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container
from streamlit_navigation_bar import st_navbar
from streamlit_extras.let_it_rain import rain


def loadAllMyData():
    global tablaSemaforo, tablaSemaforo_styled, md_ser, md_dic, md_table,informe_Jug, informe_JugZ, informe_JugZProm, informe_JugEst,informe_Ses, informe_SesEst,informe_SesZ, informe_SesZProm
    informe_Jug, informe_JugZ, informe_JugZProm, informe_JugEst, informe_Ses, informe_SesEst, informe_SesZ, informe_SesZProm = genInformResults()
    
    #Generar tablas de M-Day
    try:
        md_table, md_dic, md_ser            = getMdayZscore()
        tablaSemaforo, tablaSemaforo_styled = getMDAYTable()
    except:       
        return False
    else: 
        return True 

        
def graficos_Jugador():
    show_graphSesDis        = st.checkbox("Distancia")
    show_graphSesHSR        = st.checkbox("HSRAbsDistance")
    show_graphSesAccCoun    = st.checkbox("highIntensityAccAbsCounter")
    show_graphSesDesCoun    = st.checkbox("highIntensityDecAbsCounter")
    show_graphSesComp       = st.checkbox("Generar gráfico con todos los resultados")

    # Mostrar el gráfico si el checkbox está seleccionado
    if show_graphSesDis:
        st.pyplot( playGraph(wimuApp.inform, "Distancia m", st.session_state.opcionSes_seleccionadaLast))
    if show_graphSesHSR:
        st.pyplot( playGraph(wimuApp.inform, "HSRAbsDistance", st.session_state.opcionSes_seleccionadaLast, "g"))
    if show_graphSesAccCoun:
        st.pyplot( playGraph(wimuApp.inform, "highIntensityAccAbsCounter", st.session_state.opcionSes_seleccionadaLast, "b"))
    if show_graphSesDesCoun:
        st.pyplot( playGraph(wimuApp.inform, "highIntensityDecAbsCounter", st.session_state.opcionSes_seleccionadaLast, "m"))
    if show_graphSesComp:
        st.pyplot( playGraphAll(wimuApp.inform, st.session_state.opcionSes_seleccionadaLast))

def graficos_Sesion():
    show_graphSesDis        = st.checkbox("Distancia")
    show_graphSesHSR        = st.checkbox("HSRAbsDistance")
    show_graphSesAccCoun    = st.checkbox("highIntensityAccAbsCounter")
    show_graphSesDesCoun    = st.checkbox("highIntensityDecAbsCounter")
    show_graphSesComp       = st.checkbox("Generar gráfico con todos los resultados")

    # Mostrar el gráfico si el checkbox está seleccionado
    if show_graphSesDis:
        st.pyplot( sesGraph(wimuApp.inform, "Distancia m", st.session_state.opcionSes_seleccionadaLast))
    if show_graphSesHSR:
        st.pyplot( sesGraph(wimuApp.inform, "HSRAbsDistance", st.session_state.opcionSes_seleccionadaLast, "g"))
    if show_graphSesAccCoun:
        st.pyplot( sesGraph(wimuApp.inform, "highIntensityAccAbsCounter", st.session_state.opcionSes_seleccionadaLast, "b"))
    if show_graphSesDesCoun:
        st.pyplot( sesGraph(wimuApp.inform, "highIntensityDecAbsCounter", st.session_state.opcionSes_seleccionadaLast, "m"))
    if show_graphSesComp:
        st.pyplot( sesGraphAll(wimuApp.inform, st.session_state.opcionSes_seleccionadaLast))

def graficos_box():

    show_graphSesDisBox        = st.checkbox("Box-Plot: Distancia")
    show_graphSesHSRBox        = st.checkbox("Box-Plot: HSRAbsDistance")
    show_graphSesAccCounBox    = st.checkbox("Box-Plot: highIntensityAccAbsCounter")
    show_graphSesDesCounBox    = st.checkbox("Box-Plot: highIntensityDecAbsCounter")
    show_graphSesCompBox       = st.checkbox("Box-Plot: Generar gráfico con todos los resultados")

    if show_graphSesDisBox:
        st.pyplot( boxDiag(wimuApp.inform,"Distancia m", st.session_state.opcionSes_seleccionadaLast))
    if show_graphSesHSRBox:
        st.pyplot( boxDiag(wimuApp.inform,"HSRAbsDistance", st.session_state.opcionSes_seleccionadaLast))
    if show_graphSesAccCounBox:
        st.pyplot( boxDiag(wimuApp.inform,"highIntensityAccAbsCounter", st.session_state.opcionSes_seleccionadaLast))
    if show_graphSesDesCounBox:
        st.pyplot( boxDiag(wimuApp.inform,"highIntensityDecAbsCounter", st.session_state.opcionSes_seleccionadaLast))
    if show_graphSesCompBox:
        st.pyplot(sesBoxAll(wimuApp.inform,  st.session_state.opcionSes_seleccionadaLast))

def grafico_Hist():

    col1, col2 = st.columns(2)
    with col1:
        show_graphSesDisHist        = st.checkbox("Histograma: Distancia")
        show_graphSesHSRHist        = st.checkbox("Histograma: HSRAbsDistance")
        show_graphSesAccCounHist    = st.checkbox("Histograma: highIntensityAccAbsCounter")
        show_graphSesDesCounHist    = st.checkbox("Histograma: highIntensityDecAbsCounter")
        show_graphSesCompHist       = st.checkbox("Histograma: Generar gráfico con todos los resultados")
    
    with col2:
        misBins = st.number_input('Ingresa él número de bins', value=10, step=1, format='%d')

    if show_graphSesDisHist:
        st.pyplot( sesHist(wimuApp.inform,"Distancia m", st.session_state.opcionSes_seleccionadaLast, misBins))
    if show_graphSesHSRHist:
        st.pyplot( sesHist(wimuApp.inform,"HSRAbsDistance", st.session_state.opcionSes_seleccionadaLast, misBins))
    if show_graphSesAccCounHist:
        st.pyplot( sesHist(wimuApp.inform,"highIntensityAccAbsCounter", st.session_state.opcionSes_seleccionadaLast, misBins))
    if show_graphSesDesCounHist:
        st.pyplot( sesHist(wimuApp.inform,"highIntensityDecAbsCounter", st.session_state.opcionSes_seleccionadaLast, misBins))
    if show_graphSesCompHist:
        st.pyplot(sesHisytAll(wimuApp.inform,  st.session_state.opcionSes_seleccionadaLast, misBins))

#%% ESTADO DE INICIO:

st.set_page_config(
    page_title="SFC Data-App",
    page_icon="https://cdn.icon-icons.com/icons2/861/PNG/512/Soccer_icon-icons.com_67819.png", 
    layout="wide",
)

# Sidebar
st.sidebar.title("Sporting Football Club")
with st.sidebar:
    url_imagen = 'https://upload.wikimedia.org/wikipedia/commons/8/89/Sporting_Football_Club_2019.png'
    st.image(url_imagen, caption='Sporting FC', width=140)

    with st.expander("📧 Contactos"):
        st.subheader("Datos del desarrollador") 
        st.text("Nombre: Gabriel Alemán Ruiz")
        st.text("Correo Electrónico: gabrieldejesusalemanruiz@gmail.com")
        st.text("Núm de teléfono: (+506) 8546-5843")

    with st.expander("🔗 links"):
        st.link_button("Página principal",url="https://www.sporting.cr/")
        st.link_button("WIMU (API Service)",url="https://wimupro.wimucloud.com/commons/restapi/")
        st.link_button("WIMU",url="https://wimupro.wimucloud.com/")


    if st.button ("Push me"):
        rain(
            emoji="⚽",
            font_size=54,
            falling_speed=4,
            animation_length=[5,""],
        )
        

#VARIABLES DE ESTADO
#--------------------------------------------------------------
if 'informAlreadyDone' not in st.session_state:
    st.session_state.informAlreadyDone = False

if 'sesListAlreadyDone' not in st.session_state:
    st.session_state.sesListAlreadyDone = False

if 'onLast' not in st.session_state:
    st.session_state.onLast = [False, False]

if 'onCurrent' not in st.session_state:
    st.session_state.onCurrent = [False, False]

if 'informAlreadyDoneX1' not in st.session_state:
    st.session_state.informAlreadyDoneX1 = False

if 'opcionEq_seleccionadaLast' not in st.session_state:
    st.session_state.opcionEq_seleccionadaLast = ''

if 'opcionSes_seleccionadaLast' not in st.session_state:
    st.session_state.opcionSes_seleccionadaLast = ''

if  'myDateRes' not in st.session_state:
    st.session_state.myDateRes = ""

if 'last_option' not in st.session_state:
    st.session_state.last_option = None
#%%--------------------------------------------------------------

# INICIO:-
#%%--------------------------------------------------------------

image_path = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTD-ViQjMELIoVlV44DnXliYZoV2knLJ218zQ&s"
# Redondear bordes de la imagen usando HTML y CSS
html_code = f"""
<style>
img {{
    border-radius: 15px;
}}
</style>
<img src="{image_path}" width="100">
"""

# Título de la aplicación
col1, col2 = st.columns([1,7])

with col2:
    st.title("SFC: Data - APP")
with col1:
    st.markdown(html_code, unsafe_allow_html=True)
    
st.markdown('-----------------------')

col1, col2 = st.columns(2)
with col1:
    colored_header(label="Clubes en la base de datos", description="", color_name="violet-70", )
    with st.expander("Clubes"):
        st.dataframe(wimuApp.Club)

with col2:
    colored_header(label="Equipos en la base de datos", description="", color_name="violet-70", )
    with st.expander("Equipos"):
        st.dataframe(wimuApp.teams)

# Crear un selectbox para los equipos
l=wimuApp.teams["Abreviatura"].to_list()
l=l.index("1aM")
opcionEq_seleccionada = st.selectbox('Selecciona un equipo:', wimuApp.teams, index=l) #Predeterminado 1era división masculina


st.markdown(f"## Jugadores - {opcionEq_seleccionada}")
wimuApp.getMyTeam(name=opcionEq_seleccionada) #Seleccionar equipo
wimuApp.getMyPlayers()                       

with st.expander("Jugadores"):
    st.dataframe(wimuApp.players)
#%%--------------------------------------------------------------


#Cargar datos anteriores o desde cero:
#.............................................................................................................
onSes =  st.toggle("🔄 Cargar listado de sesiones de archivo", key="Cargar listado")

if onSes: #Sí quiero cargar datos anteriores:
    with st.expander("Cargar listado de sesiones"):
        archivoListSes = st.file_uploader("Elige un archivo", type=["csv"], key="list")

        if archivoListSes is not None:
            archivoFormatoCorrecto = wimuApp.loadSesList(archivoListSes)

            if archivoFormatoCorrecto:
                st.session_state.sesListAlreadyDone =True
                st.session_state.opcionEq_seleccionadaLast = opcionEq_seleccionada
                st.session_state.myDateRes  = pd.to_datetime(wimuApp.session["Creado"].iloc[-1])
            else:
                st.error('El archivo subido no sigue el formato adecuado', icon="🚨")


else:
    #Cargar listado de sesiones desde cero:
    #.............................................................................................................
    col1, col2 = st.columns(2)

    with col2:
        myDateSelect = st.radio("Tipo de sesiones", ["Sesiones del último mes", "Solo sesiones desde inicio del año", "Todas las sesiones"])
        if myDateSelect == "Sesiones del último mes": 
            NewType = "fromMonthAgo"

        elif myDateSelect == "Solo sesiones desde inicio del año":
            NewType = "fromYearStart"

        else:
            NewType = None

    with col1:
        # ESTILO BOTÓN:
        
        # Create buttons with st.button
        with stylable_container(
            "bses",
            css_styles="""
            button {
                    background-color: #a82f51;
                    color: white;
            }""",
        ):
            bSesList = st.button(f'📝 Generar listado de sesiones para\n {opcionEq_seleccionada} - ({myDateSelect})', disabled= onSes)

        if bSesList:
            st.session_state.opcionEq_seleccionadaLast = opcionEq_seleccionada
            with st.spinner('Cargando datos...'):
                st.session_state.myDateRes  = pd.to_datetime(wimuApp.getAllSessions_V2(type=NewType), format="%m/%d/%Y")
            st.session_state.sesListAlreadyDone = True

if st.session_state.onLast[0] != onSes: #Si hubo un cambio en la opción de cargar
    print(st.session_state.onLast)
    st.session_state.sesListAlreadyDone =False
    st.session_state.show_OpsInform =False
    st.session_state.informAlreadyDone = False
    st.session_state.opcionEq_seleccionadaLast = ""
    st.session_state.onLast[0] = onSes

#Mostrar opciones tras cargar el listado de sesiones:
#.............................................................................................................
if st.session_state.sesListAlreadyDone: #No se puede acceder a las demás opciones hasta haber ingresado
                                  #el listado de sesiones y/u informe (por archivo).

    # Crear el radio button con las opciones
    st.markdown(f"## Listado de sesiones - {st.session_state.opcionEq_seleccionadaLast}")
    st.dataframe(wimuApp.session.reset_index(drop=True).set_index("Nombre"))

    selected_optionInf = st.radio(
        'Seleccione una opción de informe:',
        ["Generar informe completo (varias sesiones)","Generar informe para solo una sesión"]
    )

    # Actualizar el estado solo si la opción cambia
    if selected_optionInf != st.session_state.last_option:
        st.session_state.show_OpsInform = False
        st.session_state.informAlreadyDone = False
        st.session_state.last_option = selected_optionInf

    if st.button('Continuar'):
        st.session_state.show_OpsInform =True


#.............................................................................................................
    if st.session_state.show_OpsInform:
        #INFORME DE 1 SOLA SESIÓN:
        #.............................................................................................................
        if selected_optionInf=="📝 Generar informe para solo una sesión":
            opcionTip_seleccionada = st.selectbox('Selecciona una sesión:', wimuApp.session, index=0)
            if st.button(f"Generar informe para {opcionTip_seleccionada}"):
                with st.spinner('Cargando datos...'):
                    wimuApp.getInform(nameSes=opcionTip_seleccionada, onlyOneSes=True)
                    wimuApp.inform.sort_values(by="Jugador", inplace=True)

                st.session_state.opcion_Ses = opcionEq_seleccionada
                st.session_state.opcionSes_seleccionadaLast = opcionTip_seleccionada
                st.session_state.informAlreadyDoneX1 = True
            
            if st.session_state.informAlreadyDoneX1:
                st.markdown(f" ## Informe de la sesión - {st.session_state.opcionSes_seleccionadaLast}")
                tablas, graficos = st.tabs(["Tablas", "Gráficos"])

                with tablas:
                    st.markdown("### Resultados")
                    with st.expander("Resultados"):
                        st.dataframe(wimuApp.inform.reset_index(drop=True))

                    st.markdown("### Estadísticas")
                    with st.expander("Estadísticas"):
                        est=wimuApp.inform.describe().drop(columns=["Creado (fecha)", "Duración (min)"])
                        est.index=["Núm de datos","Promedio", "Desviación estandar", 'min', '25%', '50%', '75%', 'max']
                        st.dataframe(est)

                    st.markdown("### Matriz de correlación")
                    with st.expander("Matriz de correlación"):
                        st.pyplot(graficar_matriz_correlacion(wimuApp.inform[['Distancia m', 'HSRAbsDistance', 'highIntensityAccAbsCounter','highIntensityDecAbsCounter']], st.session_state.opcionSes_seleccionadaLast))

                with graficos:
                
                    with st.expander("Gráfico de resultados"):
                        graficos_Sesion()
                    with st.expander("Histograma de resultados"):
                        grafico_Hist()
                    with st.expander("Diagrama de caja de resultados"):                    
                        graficos_box()


        #Informe oara todas las sesiones sesión:
        #---------------------------------------------------------------------------------------------------------------------------
        else:

            onInf =  st.toggle("🔄 Cargar informe completo de archivo", key="Cargar informe")

                
            if onInf: #Sí quiero cargar datos anteriores:
                with st.expander("Cargar informe"):
                    archivoInf = st.file_uploader("Elige un archivo", type=["csv"], key="inf")
                    if archivoInf is not None:
                        archivoFormatoCorrecto = wimuApp.loadInform(archivoInf)

                        if archivoFormatoCorrecto:
                            st.session_state.informAlreadyDone = True
                            #.................................................................................................................................................
                            st.session_state.semStatus = loadAllMyData()
                            #.................................................................................................................................................
                        else:
                            st.error('El archivo subido no sigue el formato adecuado', icon="🚨")


            else:
                col1, col2 = st.columns(2)
                #Inicializado en 01/01/(año actual) - Hoy:
                with col1:

                    start_date = st.date_input(
                        "Selecciona la fecha de inicio:",
                        min_value=st.session_state.myDateRes ,
                        value=st.session_state.myDateRes , 
                        max_value=datetime.now().date()
                    )
                with col2:
                    end_date = st.date_input(
                        "Selecciona la fecha de fin:",
                        min_value=st.session_state.myDateRes ,
                        value=datetime.now(), 
                        max_value=datetime.now() 
                    )
                
                st.write(f"Rango de fechas seleccionado: Desde {start_date} hasta {end_date}")
                # Convertir a '2024-09-19 23:59:59'
                end_date = end_date + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

                # Create buttons with st.button
                with stylable_container(
                    "bInf",
                    css_styles="""
                    button {
                            background-color: #a82f51;
                            color: white;
                    }""",
                ): 
                    bCompInfo = st.button(f'📝 Generar informe completo: {start_date} / {end_date}')
                    
                if bCompInfo:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    info_text = st.empty()
                    for i in wimuApp.getAllInforms_V2(endDate=end_date, beginDate= start_date):
                        progress_bar.progress(i)
                        status_text.text(f"Progreso: {round(i*100)}%")
                        info_text.info("Esto puede tomar un momento...")
                    #.................................................................................................................................................
                    st.session_state.semStatus = loadAllMyData()
                    #.................................................................................................................................................
                    
                    st.success("¡Proceso completado!")
                    st.session_state.informAlreadyDone = True

  
            if st.session_state.onLast[1] != onInf: #Si hubo un cambio en la opción de cargar
                st.session_state.informAlreadyDone = False
                st.session_state.onLast[1] = onInf
            #.................................................................................................................................................
            if  st.session_state.informAlreadyDone: #Ya se generó el informe       
                st.markdown(f"## Informe de sesiones - {st.session_state.opcionEq_seleccionadaLast}")
                semaforo, delta, std, tablas, graficos = st.tabs(["🚦Semaforo", "𝚫 Delta", "📊 Estadísticas MD", "🗂 Tablas completas", "📒 Sesión / Jugador Específico"])
                
                with delta:
                    with st.expander("Varios jugadores"):
                        input_ses = st.selectbox("Seleccione una sesión:", wimuApp.listaSesiones, key="many")
                        l=wimuApp.getDeltaSes(input_ses)
                        col1, col2, col3, col4 = st.columns(4)
                        for i in l:
                            st.markdown(f"### -Jugador: {i["Delta"].name}")
                            with stylable_container(
                            key="container_with_border1",
                            css_styles="""
                                {
                                    border: 5px solid #ff4700;
                                    border-radius: 0.5rem;
                                    padding: calc(1em - 1px)
                                }
                                """,
                            ):
                                col1, col2, col3, col4 = st.columns(4)
                                col1.metric("Distancia m",                  i["Resultado"]["Distancia m"]                  ,i["Delta"]["Distancia m"]                  )
                                col2.metric("HSRAbsDistance",               i["Resultado"]["HSRAbsDistance"]               ,i["Delta"]["HSRAbsDistance"]               )
                                col3.metric("highIntensityAccAbsCounter",   i["Resultado"]["highIntensityAccAbsCounter"]   ,i["Delta"]["highIntensityAccAbsCounter"]   )
                                col4.metric("highIntensityDecAbsCounter",   i["Resultado"]["highIntensityDecAbsCounter"]   ,i["Delta"]["highIntensityDecAbsCounter"]   )
                            
                    with st.expander("1 jugador"):
                        input_ses = st.selectbox("Seleccione una sesión:", wimuApp.listaSesiones, key="only")
                        input_jug = st.selectbox("Seleccione un jugador:", sorted(wimuApp.compInform.query('Sesión == @input_ses')["Jugador"].to_list()))
                        delta, resXJugXSes, _, _ =wimuApp.getDeltaPlaySes(input_ses, input_jug)

                        with stylable_container(
                        key="container_with_border1",
                        css_styles="""
                            {
                                border: 5px solid #ff4700;
                                border-radius: 0.5rem;
                                padding: calc(1em - 1px)
                            }
                            """,
                        ):

                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("Distancia m",                  resXJugXSes["Distancia m"]                  ,delta["Distancia m"]                  )
                            col2.metric("HSRAbsDistance",               resXJugXSes["HSRAbsDistance"]               ,delta["HSRAbsDistance"]               )
                            col3.metric("highIntensityAccAbsCounter",   resXJugXSes["highIntensityAccAbsCounter"]   ,delta["highIntensityAccAbsCounter"]   )
                            col4.metric("highIntensityDecAbsCounter",   resXJugXSes["highIntensityDecAbsCounter"]   ,delta["highIntensityDecAbsCounter"]   )




                with semaforo:
                    if st.session_state.semStatus:
                        if st.checkbox("Semaforo completo"):
                            st.write(tablaSemaforo_styled)
                        if st.checkbox("Semaforo individual"):
                            opcionTip_seleccionada = st.selectbox("Seleccione una sesión para el semaforo", wimuApp.listaSesiones)
                            datos, seleccion, concat, seleccion_styled, concat_styled = SemIndv(opcionTip_seleccionada)
                            st.write(concat_styled)
                    else:
                        st.error('Error generando semaforo', icon="🚨")
                with std:
                    my_md = st.selectbox('Selecciona un MD:', md)
                    st.markdown(f"### {my_md}")
                    st.dataframe(wimuApp.getMDStad(my_md))

                with tablas:
                    col1, col2 = st. columns(2)
                    with col2:
                        opcionCompInform=st.radio("### ¿Cómo desea visualizar los datos?", options=["Visualizar por sesión", "Visualizar por jugador"], key="321")               
                    
                    with col1:
                        dataFInf   = st.checkbox("Ver informe completo")
                        estdFInf   = st.checkbox("Ver estadísticas del informe")
                        zScoreInf  = st.checkbox("Tabla de Z-Scores")
                        zScoreProm = st.checkbox("Tabla de Z-Scores promedio")
                        sesType = st.checkbox("Ver tipos de sesión")

                        if opcionCompInform == "Visualizar por sesión":
                            ops=[informe_Ses, informe_SesEst, informe_SesZ, informe_SesZProm]
                        else:
                            ops=[informe_Jug, informe_JugEst, informe_JugZ, informe_JugZProm]
                        
                        if dataFInf:
                            st.markdown("### Informe completo")
                            st.write(ops[0].to_html(), unsafe_allow_html=True)
                        if estdFInf:
                            st.markdown("### Estadísticas")
                            st.write(ops[1].to_html(), unsafe_allow_html=True)
                        if zScoreInf:
                            st.markdown("### Z-Scores")
                            st.write(ops[2].to_html(), unsafe_allow_html=True)
                        if zScoreProm:
                            st.markdown("### Z-Scores: Promedio")
                            st.dataframe(ops[3])
                        if sesType:
                            st.write(md_ser)

                with graficos:
                    opcionCompInform=st.radio("Datos a seleccionar", options=["Sesión", "Jugador"], key="123")               
                
                    if opcionCompInform == "Sesión":
                        st.session_state.opcionSes_seleccionadaLast = st.selectbox("Seleccione una sesión", wimuApp.listaSesiones)
                        opsGPR=[True, informe_SesEst, informe_SesZ, informe_SesZProm, informe_Ses]
                    else: #VISUALIZAR por jugador
                        st.session_state.opcionSes_seleccionadaLast = st.selectbox("Seleccione una sesión", wimuApp.listaJugadores)
                        opsGPR=[False, informe_JugEst, informe_JugZ, informe_JugZProm, informe_Jug]
                    
                    
                    wimuApp.inform = opsGPR[4].loc[st.session_state.opcionSes_seleccionadaLast]
                    if opsGPR[0]:
                        wimuApp.inform.sort_index(inplace=True)
                    else:
                        wimuApp.inform.sort_values(by="Creado (fecha)")

                    with st.expander(f"Tabla: {st.session_state.opcionSes_seleccionadaLast}"):
                        resu=st.checkbox("Tabla de resultados")
                        estd=st.checkbox("Tabla de estadísticas")
                        if resu:
                            st.markdown(f"### Resultados: {st.session_state.opcionSes_seleccionadaLast}")
                            st.write(wimuApp.inform )
                        if estd:
                            st.markdown(f"### Estadísticas: {st.session_state.opcionSes_seleccionadaLast}")
                            st.write(opsGPR[1].loc[st.session_state.opcionSes_seleccionadaLast])
                            
                    with st.expander("Grafico de resultados"):
                        if opsGPR[0]:
                            graficos_Sesion()
                        else:
                            graficos_Jugador()
                    with st.expander("Histograma"):
                        grafico_Hist()
                    with st.expander("Diagrama de caja"):
                        graficos_box()
                    with st.expander("z-Score"):
                        st.pyplot(barZ(opsGPR[2], opsGPR[3],ses=st.session_state.opcionSes_seleccionadaLast))


                   
                st.markdown("-----------------------------------------------")

                #DESCARGAR DATOS
                with st.expander ("Descargar archivos 📁"):
                                                            
                    # DESCARGAR INFORME COMPLETO:
                    def create_excel_file():
                        buffer = BytesIO()
                        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                            tablaSemaforo_styled.to_excel(writer, sheet_name='SEMAFORO')
                            md_table.to_excel(writer, sheet_name='Z SCORE x MD')

                            informe_Jug.to_excel(writer, sheet_name='JUGADORES')
                            informe_JugEst.to_excel(writer, sheet_name='JUGADORES (Estadisticas)')
                            # Z: Score
                            s= "JUGADORES (z- Score)"
                            informe_JugZ.to_excel(writer, sheet_name=s, startrow=0, startcol=0)

                            # Guardar el segundo DataFrame en la misma hoja pero en una posición diferente
                            informe_JugZProm.to_excel(writer, sheet_name=s, startrow=0, startcol=len(informe_JugZ.columns) + 4)

                            #-----------------------------------------------------------------------------------------------------------------------------------------------
                            
                            informe_Ses.to_excel(writer, sheet_name='SESIONES')
                            informe_SesEst.to_excel(writer, sheet_name='SESIONES (Estadisticas)')

                            s= "SESIONES (z- Score)"
                            informe_SesZ.to_excel(writer, sheet_name=s, startrow=0, startcol=0)

                            # Guardar el segundo DataFrame en la misma hoja pero en una posición diferente
                            informe_SesZProm.to_excel(writer, sheet_name=s, startrow=0, startcol=len(informe_SesZ.columns) + 4)

                        buffer.seek(0)
                        return buffer.getvalue()
                    
                    excel_data = create_excel_file()
                    st.download_button(
                        label="⬇️ Descargar archivo Excel",
                        data=excel_data,
                        file_name=f'informeCompleto_{datetime.now()}.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )

                    st.download_button(
                        label="⬇️ Descargar  informe",
                        data=wimuApp.compInform.to_csv(),
                        file_name=f'informe_{datetime.now()}.xlsx',
                        mime="text/csv"

                    )