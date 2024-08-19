from wimu import *
from graphs import *
import streamlit as st
from streamlit_extras.stoggle import stoggle
from streamlit_extras.colored_header import colored_header
from streamlit_extras.bottom_container import bottom
from streamlit_extras.echo_expander import echo_expander
from io import BytesIO


st.set_page_config(
    page_title="Sporting Football Club",
    page_icon="https://cdn.icon-icons.com/icons2/861/PNG/512/Soccer_icon-icons.com_67819.png",  # Cambia esto a la URL de tu imagen
)

#VARIABLES DE ESTADO:
#%%--------------------------------------------------------------
# Inicializar el estado de visibilidad
if 'show_widgets' not in st.session_state:
    st.session_state.show_widgets = False

if 'informAlreadyDone' not in st.session_state:
    st.session_state.informAlreadyDone = False

if 'informAlreadyDoneX1' not in st.session_state:
    st.session_state.informAlreadyDoneX1 = False

if 'opcionEq_seleccionadaLast' not in st.session_state:
    st.session_state.opcionEq_seleccionadaLast = ''

if 'show_OpsInform' not in st.session_state:
        st.session_state.show_OpsInform =False

if 'last_option' not in st.session_state:
    st.session_state.last_option = None
#%%--------------------------------------------------------------

# Definir las dos columnas
col1, col2 = st.columns(2)
with col2:
    # Título de la aplicación
    st.markdown('# WIMU Data')
with col1:
    url_imagen = 'https://upload.wikimedia.org/wikipedia/commons/8/89/Sporting_Football_Club_2019.png'
    st.image(url_imagen, caption='Sporting FC', width=140)

st.markdown('-----------------------')

st.markdown('## Clubes suscritos en la base de datos')
st.dataframe(wimuApp.Club)
st.markdown('## Equipos suscritos en la base de datos')
st.dataframe(wimuApp.teams)

# Crear un selectbox para los equipos
l=wimuApp.teams["Abreviatura"].to_list()
l=l.index("1aM")
opcionEq_seleccionada = st.selectbox('Selecciona un equipo:', wimuApp.teams, index=l)


st.markdown(f"## Jugadores - {opcionEq_seleccionada}")

wimuApp.getMyTeam(name=opcionEq_seleccionada)
wimuApp.getMyPlayers()

st.dataframe(wimuApp.players)

#Cargar listado de sesiones anterior:
#.............................................................................................................
on = st.toggle("Cargar listado de sesiones anterior")
if on:
    archivo_subido = st.file_uploader("Elige un archivo", type=["csv", "txt", "xlsx"])

    if archivo_subido is not None:
        wimuApp.session = pd.read_csv(archivo_subido)
        wimuApp.session["Participantes"] = wimuApp.session["Participantes"].apply(lambda val: val.split(","))
        wimuApp.session["Actividades de la sesión"] = wimuApp.session["Actividades de la sesión"].apply(lambda val: val.split(","))

        wimuApp.session.set_index("id", inplace=True)
        st.session_state.show_widgets = True
        st.session_state.opcionEq_seleccionadaLast = opcionEq_seleccionada
        
        csv = wimuApp.session.to_csv(index=False)

#Cargar listado de sesiones desde cero:
#.............................................................................................................
col1, col2 = st.columns(2)

with col2:
    yStart = st.checkbox("Solo sesiones desde inicio del año", value=True, disabled=on)
with col1:
    if st.button(f'Generar listado de sesiones para {opcionEq_seleccionada}', disabled= on):
        st.session_state.opcionEq_seleccionadaLast = opcionEq_seleccionada
        st.session_state.show_widgets = True
        with st.spinner('Cargando datos...'):
            wimuApp.getAllSessions(fromYearStart=yStart)

#Mostrar opciones tras cargar el listado de sesiones:
#.............................................................................................................
if st.session_state.show_widgets: #No se puede acceder a las demás opciones hasta haber ingresado
                                  #el listado de sesiones

    st.markdown(f"## Listado de sesiones - {st.session_state.opcionEq_seleccionadaLast}")
    st.dataframe(wimuApp.session)

    # Crear el radio button con las opciones
    selected_optionInf = st.radio(
        'Seleccione una opción de informe:',
        ["Generar informe para solo una sesión", "Generar informe completo (todas las sesiones)"]
    )

    # Actualizar el estado solo si la opción cambia
    if selected_optionInf != st.session_state.last_option:
        st.session_state.show_OpsInform = False
        st.session_state.last_option = selected_optionInf

    if st.button('Continuar'):
        st.session_state.show_OpsInform =True

#.............................................................................................................
    if st.session_state.show_OpsInform:
        #INFORME DE 1 SOLA SESIÓN:
        #.............................................................................................................
        if selected_optionInf=="Generar informe para solo una sesión":
            opcionEq_seleccionadaSes = st.selectbox('Selecciona una sesión:', wimuApp.session, index=0)
            if st.button(f"Generar informe para {opcionEq_seleccionadaSes}"):
                with st.spinner('Cargando datos...'):
                    wimuApp.getInform(nameSes=opcionEq_seleccionadaSes, onlyOneSes=True)
                st.session_state.informAlreadyDoneX1 = True
            
            if st.session_state.informAlreadyDoneX1:
                st.markdown(f" ## Informe de la sesión - {opcionEq_seleccionadaSes}")
                st.dataframe(wimuApp.inform)
                colored_header(
                    label="Opciones de gráficos:",
                    description="Aquí podrá encontrar diferentes tipos de gráficos que se pueden realizar a partir de la información presente.",
                    color_name="violet-70",
                )
   
                st.markdown("### Gráfico para resultados")
                show_graphSesDis        = st.checkbox("Distancia")
                show_graphSesHSR        = st.checkbox("HSRAbsDistance")
                show_graphSesAccCoun    = st.checkbox("highIntensityAccAbsCounter")
                show_graphSesDesCoun    = st.checkbox("highIntensityDecAbsCounter")
                show_graphSesComp       = st.checkbox("Generar gráfico con todos los resultados")

                # Mostrar el gráfico si el checkbox está seleccionado
                if show_graphSesDis:
                    st.pyplot( sesGraph(wimuApp.inform, "Distancia m", opcionEq_seleccionadaSes))
                if show_graphSesHSR:
                    st.pyplot( sesGraph(wimuApp.inform, "HSRAbsDistance", opcionEq_seleccionadaSes, "g"))
                if show_graphSesAccCoun:
                    st.pyplot( sesGraph(wimuApp.inform, "highIntensityAccAbsCounter", opcionEq_seleccionadaSes, "b"))
                if show_graphSesDesCoun:
                    st.pyplot( sesGraph(wimuApp.inform, "highIntensityDecAbsCounter", opcionEq_seleccionadaSes, "m"))
                if show_graphSesComp:
                    st.pyplot( sesGraphAll(wimuApp.inform, opcionEq_seleccionadaSes))

                st.markdown("-------------------------------------------------------------------------------")
                show_graphHist          = st.checkbox("Histograma de los datos")
                if show_graphHist:
                    with st.expander("Histogramas"):
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
                            st.pyplot( sesHist(wimuApp.inform,"Distancia m", opcionEq_seleccionadaSes, misBins))
                        if show_graphSesHSRHist:
                            st.pyplot( sesHist(wimuApp.inform,"HSRAbsDistance", opcionEq_seleccionadaSes, misBins))
                        if show_graphSesAccCounHist:
                            st.pyplot( sesHist(wimuApp.inform,"highIntensityAccAbsCounter", opcionEq_seleccionadaSes, misBins))
                        if show_graphSesDesCounHist:
                            st.pyplot( sesHist(wimuApp.inform,"highIntensityDecAbsCounter", opcionEq_seleccionadaSes, misBins))
                st.markdown("-------------------------------------------------------------------------------")
                show_graphBox           = st.checkbox("Diagrama de caja los datos")
                if show_graphBox:
                    with st.expander("Diagramas de caja"):

                        show_graphSesDisBox        = st.checkbox("Box-Plot: Distancia")
                        show_graphSesHSRBox        = st.checkbox("Box-Plot: HSRAbsDistance")
                        show_graphSesAccCounBox    = st.checkbox("Box-Plot: highIntensityAccAbsCounter")
                        show_graphSesDesCounBox    = st.checkbox("Box-Plot: highIntensityDecAbsCounter")
                        show_graphSesCompBox       = st.checkbox("Box-Plot: Generar gráfico con todos los resultados")
                    
                        if show_graphSesDisBox:
                            st.pyplot( boxDiag(wimuApp.inform,"Distancia m", opcionEq_seleccionadaSes))
                        if show_graphSesHSRBox:
                            st.pyplot( boxDiag(wimuApp.inform,"HSRAbsDistance", opcionEq_seleccionadaSes))
                        if show_graphSesAccCounBox:
                            st.pyplot( boxDiag(wimuApp.inform,"highIntensityAccAbsCounter", opcionEq_seleccionadaSes))
                        if show_graphSesDesCounBox:
                            st.pyplot( boxDiag(wimuApp.inform,"highIntensityDecAbsCounter", opcionEq_seleccionadaSes))
                        if show_graphSesCompBox:
                            st.pyplot(sesBoxAll(wimuApp.inform,  opcionEq_seleccionadaSes))




        #Informe oara todas las sesiones sesión:
        #---------------------------------------------------------------------------------------------------------------------------
        else:
            col1, col2 = st.columns(2)
            #Inicializado en 01/01/(año actual) - Hoy:
            with col1:

                start_date = st.date_input(
                    "Selecciona la fecha de inicio:",
                    value=datetime(datetime.now().year, 1, 1), 
                    max_value=datetime.now().date()
                )
            with col2:
                end_date = st.date_input(
                    "Selecciona la fecha de fin:",
                    value=datetime.now(), 
                    max_value=datetime.now().date() 
                )
            
            st.write(f"Rango de fechas seleccionado: Desde {start_date} hasta {end_date}")
            # Convertir fechas a strings para la consulta
            start_date = start_date.strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')


            if st.button(f'Generar informe completo: {start_date} - {end_date}'):
                progress_bar = st.progress(0)
                status_text = st.empty()
                info_text = st.empty()
                for i in wimuApp.getAllInforms(endDate=end_date, beginDate= start_date):
                    progress_bar.progress(i)
                    status_text.text(f"Progreso: {round(i*100)}%")
                    info_text.info("Esto puede tomar un momento...")
                st.success("¡Proceso completado!")
                st.markdown(f"## Informe de sesiones - {st.session_state.opcionEq_seleccionadaLast}")
                st.session_state.informAlreadyDone = True

            if  st.session_state.informAlreadyDone: #Ya se generó el informe
                #Guardar resultados importantes:
                #.............................................................................................
                informe_Jug         = wimuApp.getAllInformsByXData("Jugador")
                informe_JugZ, informe_JugZProm = wimuApp.getZScores("Jugador")
                informe_JugEst      = wimuApp.getStatistics("Jugador")

                informe_Ses         = wimuApp.getAllInformsByXData("Sesión")
                informe_SesZ, informe_SesZProm = wimuApp.getZScores("Sesión")
                informe_SesEst      = wimuApp.getStatistics("Sesión")
                #.............................................................................................

                opcionCompInform=st.radio("¿Cómo desea visualizar los datos?", options=["Visualizar por sesión", "Visualizar por jugador"])
                st.markdown("-----------------------------------------------")
                
                dataFInf  =st.checkbox("Ver informe completo")
                estdFInf  =st.checkbox("Ver estadísticas del informe")
                zScoreInf =st.checkbox("Ver tabla de z score del informe")

                if opcionCompInform == "Visualizar por sesión":
                    if dataFInf:
                        st.markdown(informe_Ses.to_html(), unsafe_allow_html=True)
                    if estdFInf:
                        st.markdown(informe_SesEst.to_html(), unsafe_allow_html=True)
                    if zScoreInf:
                        st.markdown(informe_SesZ.to_html(), unsafe_allow_html=True)
                        st.dataframe(informe_SesZProm)
                else:
                    if dataFInf:
                        st.markdown(informe_Jug.to_html(), unsafe_allow_html=True)
                    if estdFInf:
                        st.markdown(informe_JugEst.to_html(), unsafe_allow_html=True)
                    if zScoreInf:
                        st.markdown(informe_JugZ.to_html(), unsafe_allow_html=True)
                        st.dataframe(informe_JugZProm)

                # DESCARGAR INFORME COMPLETO:
                def create_excel_file():
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

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
                    label="Descargar archivo Excel ⬇️",
                    data=excel_data,
                    file_name=f'informeCompleto_{datetime.now()}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )