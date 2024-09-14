from API_FrameWork import *
hoy = pd.Timestamp(datetime.now())
#WIMU:

try: #Leer token del archivo:
    f = open("key.txt", "r")
    tokenWimu = f.read()
except:
    print("Error al leer archivo")


#tokenWimu = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2NjkxMmRlNmVlNGQ3ZTM1NTIzYmZmMDciLCJjbHViIjoiNjQwZWVjOWE4NTY2ZDQxMmMyZTdlZGUyIiwiY2VudGVyIjoiNjQwZWVkMTE4NTY2ZDQxMmMyZTgxZWRiIiwidXNlclR5cGUiOiJDRU5URVJfQURNSU4iLCJ1c2VyIjoiNjY5MTJkZTZlZTRkN2UzNTUyM2JmZjA3IiwiZXhwIjoxNzI2MzgyNDY5fQ.e58JVpTbjFVX-xiBaojevu5Z9cpXJ04TJ-tJbLHnEEs"

headersWimu = {
    "accept": "application/json",
    "Authorization": f"Bearer {tokenWimu}"
}

urlsWimu ={
      "url1":       "https://wimupro.wimucloud.com/apis/rest/login?username=gabrielSFC&password=gabrielSFC1234%2A", #Usuario
      "urlTeams":   "https://wimupro.wimucloud.com/apis/rest/teams",                                                #Equipos 
      "urlClub":    "https://wimupro.wimucloud.com/apis/rest/clubs"                                                 #Clubes
}


"""
filterSessionData: Función que nos permite filtar la información que no interesa de una determinada sesión.
inputs:
    -mySession: La sesión que hemos escogido
outputs:
    -La misma sesión ya filtrada con solo los datos que nos interesan.
"""
filterSessionData = lambda mySession:  {"id"                          :   mySession["id"] , 
                                        "Nombre"                      :   mySession["name"] , 
                                        "Creado"                      :   mySession["created"] ,
                                        "Duración (min)"              :   mySession["duration"] , 
                                        "Grupo"                       :   mySession["group"] ,
                                        "matchDay"                    :   mySession["matchDay"] , 
                                        "semanaCal"                   :   mySession['weekCalendar'] ,
                                        "Participantes"               :   mySession["members"] ,
                                        "Actividades de la sesión"    :   mySession['sessionTasks'] }


class myTeamAPIWimu(API):
    def __init__(self, header, urls, index=0):
        super().__init__(urls, header)
        self.Club              = None   #Mi club
        self.teams             = None   #Lista de equipos
        self.myTeam            = None   #Mi equipo
        self.players           = None   #Lista con los jugadores del equipo
        self.mySession         = None   #Sesión particular de mi elección
        self.session           = None   #Lista con todas las sesiones
        self.inform            = None   #Informe de mi sesión
        self.compInform        = None   #Informe de todas las sesiones
        self.compInformByXData = None   #Informe de todas las sesiones (ordenado Jugador-> Sesión) o (ordenado Sesión-> Jugador)
        self.stadistics        = None   #Estadísticas de mi informe completo
        
        #IDLE:
        self.getTeams() #Obtener la lista de equipos
        self.getClubs() #Obtener la lista de clubes

        if index==0:  #Predeterminado, escoger 1aM como mi equipo
            self.getMyTeam(id="640eed118566d412c2e81edb") 
            self.getMyPlayers()
    
    """
    getClubs: Método para obtener la lista de clubes matriculados.
    """
    def getClubs(self):
        self.Club = self.doRequest(self.urls["urlClub"])
    
        self.Club = [(i["id"], i["name"]) for i in self.Club]
        
        self.Club = pd.DataFrame(self.Club, columns=["id", "Nombre"])
        self.Club.set_index('id', inplace=True)

    """     
    getTeams: Método para obtener una lista de todos los equipos matriculados asociados.
    """
    def getTeams(self):
        self.teams = self.doRequest(self.urls["urlTeams"])
        
        self.teams = [(i["id"], i["name"], i["abbreviation"])  for i in self.teams]
        
        self.teams = pd.DataFrame(self.teams, columns=["id", "Nombre", "Abreviatura"])
        self.teams.set_index('id', inplace=True)
    
    """
    getMyTeam: Método para escoger el equipo del que me interesa obtener los resultados basado en 
    el criterio de mi escogencia.
    inputs:
        -index: Indice númeral del equipo que me interesa.
        -name Nombre del equipo que me interesa.
        -abv: Abreviatura del equipo que me interesa.
        -id: Id del equipo que me interesa.
    """
    def getMyTeam(self, index=None, name=None, abv=None, id=None):

        if (index is not None):
            self.myTeam = self.teams.iloc[index]
            self.myTeam = self.myTeam.name 
            
        elif (name is not None):
            self.myTeam = self.teams.query(f"Nombre == '{name}'")
            self.myTeam = self.myTeam.iloc[0].name
            
        elif (abv is not None):
            self.myTeam = self.teams.query(f"Abreviatura == '{abv}'")
            self.myTeam = self.myTeam.iloc[0].name
                        
        elif (id is not None):
            self.myTeam = self.teams.loc[id]
            self.myTeam = self.myTeam.name 
        
        self.urls["urlPlayers"] = f"https://wimupro.wimucloud.com/apis/rest/players?team={self.myTeam}&page=1&limit=200&sort=name%2Casc"
        

    """
    getMyPlayers: Método para obtener el listado con los jugadores del equipo que escogí.
    """
    def getMyPlayers(self):
        self.players  = self.doRequest(self.urls["urlPlayers"])
        
        self.players  = [(i["id"], i["name"], i["lastName"], i["height"], i["weight"], i["position"], i["maxSpeed"], i["maxAcc"], i["maxHR"]) for i in self.players]
        self.players  = pd.DataFrame(self.players, columns=["id", "Nombre", "Apellido", "Altura (m)", "Peso","Posición", "máx Vel", "máx Ac", "máx HR"])
        self.players.set_index('id', inplace=True)

        
    """
    getAllSessions: M´étodo para btener un listado con todas las sesiones registradas.
    inputs:
        -limit: Límite de datos por página
        -sort: Criterio de ordenación (ascendente o descentendte)
        -onlyColective: Si se desean solo resultados de las sesiones colectivas
        -fromYearStart: Si se desean solo las sesiones desde comienzos de este año.
        -playersAsName: Si se desea ver los jugadores según su nombre en lugar de según si id.
    """
    def getAllSessions(self, limit=200, sort=True, onlyColective=True, fromYearStart=True, playersAsName=True):
        #Se puede ordenar las sesiones empezando por la última (predeterminado) o la primera
        sortType = "end,desc" if sort else "start,asc"
        self.myUrl = self.urls["session"] = "https://wimupro.wimucloud.com/apis/rest/sessions"
        
        self.parameters ={
            "team": self.myTeam,
            "informTypes": "intervalsindoor",
            "page": 1,
            "limit": limit,
            "sort": sortType
        }
        self.session = self.findMyPagedResults() #Crear una lista con todas las sesiones
        
        myTemporalList=[]
        
        for element in self.session: #Cada elemento es un diccionario
            myTemporalResult = [filterSessionData(i) for i in element]
            myTemporalResult = pd.DataFrame(myTemporalResult)
            
            myTemporalList.append(myTemporalResult)

        self.session  = pd.concat(myTemporalList)
        
        self.session.set_index('id', inplace=True)
        self.session["Duración (min)"] = self.session["Duración (min)"].apply(milliseconds_to_minutes) #Obtener duración de la sesión en minutos
        self.session["Creado"]=self.session["Creado"].apply(getMyDate)                                 #Obtener fecha de la sesión
        
        # Eliminar filas con índices duplicados, conservando solo la primera ocurrencia
        self.session = self.session[~self.session.index.duplicated(keep='first')]
        
        if onlyColective: #Solo sesiones grupales
            self.session = self.session.query('Grupo == "Collective"')
            self.session.drop(['Grupo'], axis=1, inplace=True)
            
        if fromYearStart: #Solo a partir del primer día del año
            # Obtener el primer día del año actual
            primer_dia_ano = pd.Timestamp(year=pd.Timestamp.now().year, month=1, day=1)
            
            # Filtrar el DataFrame
            self.session = self.session[self.session['Creado'] >= primer_dia_ano]
            
        if playersAsName: #Mostrar la lista de asistentes como nombres en lugar del id del atleta.
            a=self.session["Participantes"].tolist()
            temArr=[]

            for i in a:
                try:
                    tempVar=self.players.loc[i]
                except KeyError:
                    pass
                    temArr0=[]
                    
                    for j in i:
                        try:
                            tempVar0=self.players.loc[j]
                        except KeyError:
                            temArr0.append(f"{j} Not Found in players")
                        else:
                            b=tempVar0["Nombre"]+" "+tempVar0["Apellido"]
                            temArr0.append(b)
                    temArr.append(temArr0)
                else:
                    b=tempVar["Nombre"]+" "+tempVar["Apellido"]
                    temArr.append(b.tolist())

            self.session["Participantes"] = temArr
        
        #Evitar que 2 o más sesiones tengan el mismo nombre
        conteo = self.session['Nombre'].value_counts()
        duplicados = conteo[conteo > 1].index

        for valor in duplicados:
            mask = self.session['Nombre'] == valor
            counts = self.session[mask].groupby('Nombre').cumcount() + 1
            self.session.loc[mask, 'Nombre'] = self.session.loc[mask, 'Nombre'] + ' _ ' + counts.astype(str)


    def getAllSessions_V2(self, type=None):
        if type == "fromYearStart":
            myDate = pd.Timestamp(datetime(hoy.year, 1, 1))
        elif type == "fromMonthAgo":
            myDate = hoy - pd.DateOffset(months=1)
        else:
            myDate = None

        #Se puede ordenar las sesiones empezando por la última (predeterminado) o la primera
        sortType = "end,desc" 
        self.myUrl = "https://wimupro.wimucloud.com/apis/rest/sessions"

        self.parameters ={
            "team": "640eed118566d412c2e81edb",
            "informTypes": "intervalsindoor",
            "page": 1,
            "limit": 200,
            "sort": sortType
        }
        
        self.session = self.findMyPagedResultsCompress(myDate)
            
        self.session = self.session [["id","name", "created", "duration", "group", "matchDay", "weekCalendar", "members", "sessionTasks"]]
        self.session.columns      = ["id", "Nombre" , "Creado", "Duración (min)", "Grupo" , "matchDay" , "semanaCal" ,"Participantes" , "Actividades de la sesión"]
    
        self.session.set_index('id', inplace=True)
        self.session["Duración (min)"] = self.session["Duración (min)"].apply(milliseconds_to_minutes) #Obtener duración de la sesión en minutos

        #Solo sesiones colectivas
        self.session = self.session.query('Grupo == "Collective"')
        self.session.drop(['Grupo'], axis=1, inplace=True)


       #ATLETAS POR NOMBRE EN LUGAR DE ID:
       #--------------------------------------------------------------
        a=self.session["Participantes"].tolist()
        temArr=[]
        for i in a:
            try:
                tempVar=self.players.loc[i]
            except KeyError:
                pass
                temArr0=[]
                
                for j in i:
                    try:
                        tempVar0=self.players.loc[j]
                    except KeyError:
                        temArr0.append(f"{j} Not Found in players")
                    else:
                        b=tempVar0["Nombre"]+" "+tempVar0["Apellido"]
                        temArr0.append(b)
                temArr.append(temArr0)
            else:
                b=tempVar["Nombre"]+" "+tempVar["Apellido"]
                temArr.append(b.tolist())
        self.session["Participantes"] = temArr
       #--------------------------------------------------------------
    
        #Evitar que 2 o más sesiones tengan el mismo nombre
        conteo = self.session['Nombre'].value_counts()
        duplicados = conteo[conteo > 1].index

        for valor in duplicados:
            mask = self.session['Nombre'] == valor
            counts = self.session[mask].groupby('Nombre').cumcount() + 1
            self.session.loc[mask, 'Nombre'] = self.session.loc[mask, 'Nombre'] + ' _ ' + counts.astype(str)

        if not(myDate):
            myDate =  self.session["Creado"].iloc[-1]
            
        return myDate
    """
    getSessionAssistants: Método para obtener un listado de los jugadores que asistieron a determinada sesión.
    -input:
        -filter: Si el dato ya está filtrado o no
    """
    def getSessionAssistants(self, filter=True):
        a= "Miembros" if filter else "members"
        return self.players.loc[self.mySession[a]]
    
    """
    getMySession: Selecionar una sesión especifica
    -input:
        -index: Indice de la sesión (de 0 a n)
        -name: Nombre de la sesión.
        -id:   Id de la sesión
    """
    def getMySession(self, index=None, name=None, id=None):        
        if(index is not None):
            self.mySession = self.session.iloc[index]
        
        elif(name is not None):
            self.mySession = self.session.query('Nombre == @name').iloc[0]
            
        elif(id is not None):
            self.mySession = self.session.loc[id]

    """
    getLastSession: Método para usar únicamente la última sesión.
    """
    def getLastSession(self):
        self.myUrl = self.urls["urlLastSession"] =f"https://wimupro.wimucloud.com/apis/rest/lastsession?team={self.myTeam}&informTypes=intervalsindoor"
        lastSession = self.doRequest()[0]
        lastSession = filterSessionData(lastSession)
        lastSession =pd.Series(lastSession)
        self.mySession = lastSession
            
            
    """
    getInform: Generar el informe completo de una sesión con los resultados que nos interesan.
    inputs: 
        -sort: Criterio de ordenación (ascendente o descendente)
        -sessionId: Id de la sesión de la que queremos el reporte.
        -nameSes: Nombre de la sesión de la que queremos el reporte.
        -onlyOneSes: Variable booleana que determina si es solo 1 sesión
    output: 
        -self.inform: Informe de la sesión correspondiente.
    """
    def getInform(self,sort=True, sessionId=None, nameSes=None, onlyOneSes=False):

        self.mySession = self.session.loc[sessionId] if (sessionId is not None) else self.session.query('Nombre == @nameSes').iloc[0] if (nameSes is not None) else None

        self.myUrl=self.urls["urlInform"] ="https://wimupro.wimucloud.com/apis/rest/informs"
        
        sortType = "end,desc" if sort else "start,asc"
        
        print("Descargando SESIÓN:",self.mySession["Nombre"])
        
        self.parameters = {
            "task": "Drills",
            "session": self.mySession.name,
            "informTypes": "intervalsindoor",
            "page": 1,
            "limit": 200,
            "team": self.myTeam,
            "sort": sortType
        }

        self.inform= self.doRequest()
        data =                                   [(j["id"],self.mySession["Nombre"], j["created"]    , j["username"], j["duration"]   , j["distance"]["distance"],j["distance"]["HSRAbsDistance"],j["accelerations"]["highIntensityAccAbsCounter"],j["accelerations"]["highIntensityDecAbsCounter"]) for j in self.inform]
        self.inform = pd.DataFrame(data, columns=['id'    , "Sesión",'Creado (fecha)', "Jugador"  , "Duración (min)", "Distancia m",            "HSRAbsDistance",               "highIntensityAccAbsCounter"                    ,"highIntensityDecAbsCounter"])
        

        self.inform["Duración (min)"] = self.inform["Duración (min)"].apply(milliseconds_to_minutes) 
        self.inform["Creado (fecha)"] =	self.inform["Creado (fecha)"].apply(getMyDate)
        if onlyOneSes:
            self.inform.drop(columns=["Sesión"], inplace=True)
        return self.inform
        
    """
    getAllInforms: Obtener un listado que integre todas las sesiones.
    inputs: 
        -myRange: Indicarle si queremos solo las "n" últimas sesiones en el informe completo.
        -beginDate: Fecha a partir de la cual quiero los datos
        -endDate: Fecha a partir de la cual ya no quiero los datos.
        -sessionList: Ingresar las sesiones de forma personalizada
    """
    def getAllInforms(self, myRange=None, beginDate=None, endDate=None, sessionList=None):
        if sessionList is not None:
            self.session = sessionList
            
        if (beginDate is not None and endDate is not None):
            mySessions = self.session.query("Creado >= @beginDate and Creado <= @endDate").index

        elif myRange is not None:
            mySessions = self.session.index[0: myRange]
        
        else:
            mySessions = self.session.index

        myTempArray = []

        j=0
        for i in mySessions:
            j+=1
            a= self.getInform(sessionId=i)
            myTempArray.append(a)
            yield (j / len(mySessions)) #Devolver el porcentaje de avance

        print("¡DESCARGA DE TODAS LAS SESIONES FINALIZADA!")
        self.compInform = pd.concat(myTempArray)
        self.compInform.reset_index(drop=True, inplace=True)

        self.listaJugadores = np.sort(pd.unique(self.compInform["Jugador"])) #Lista de Jugadores en el informe
        self.listaSesiones  = pd.unique(self.compInform["Sesión"])           #Lista de sesiones en el informe
        #Tenga presente que las sesiónes por defecto ya vienen ordenadas por fecha

    """
   getAllInformsByXData: Obtener el informe de sesión 
   inputs:
        -data: Define si quiero organizar mi informe completo por sesión o jugador.
    outputs:
        -self.compInformByXData: Tabla con información ordenada por sesión o jugador
    """
    def getAllInformsByXData(self, data): #Sesión o Jugador
        if (data == "Sesión"):      #Ordenar por fecha
            dataX = "Jugador" 
            self.compInformByXData = self.compInform.sort_values(by=["Creado (fecha)", "Duración (min)"], ascending=[False, True])

        elif (data == "Jugador"):   #Ordenar por jugador (en ordén alfabetico)
            dataX = "Sesión" 
            self.compInformByXData = self.compInform.sort_values(by=[data, "Creado (fecha)"])

        # Definir el MultiIndex único que quieres aplicar a todas las filas
        self.compInformByXData.set_index([data, dataX], inplace=True)
        self.compInformByXData.drop(columns=["id"], inplace=True)
        self.data = data #Guardar tipo de ordenamiento
        return self.compInformByXData

    """
    getStatistics: Método para obtener las estadisticas de mi informe completo.
    outputs:
        -self.stadistics: Tabla con las estadísticas por sesión o jugador.
    """
    def getStatistics(self):

        lista = self.listaJugadores if (self.data=="Jugador") else self.listaSesiones if(self.data=="Sesión") else None
        
        self.stadistics=[]
        for i in lista:
            tempVal=self.compInformByXData.loc[i][["Distancia m", "HSRAbsDistance", "highIntensityAccAbsCounter", "highIntensityDecAbsCounter" ]].describe() 
            tempVal.index=["Núm de datos","Promedio", "Desviación estandar", 'min', '25%', '50%', '75%', 'max']
            self.stadistics.append(tempVal)
        
        self.stadistics  = pd.concat( self.stadistics)

        index = [elemento for elemento in lista for _ in range(8)]
        Nuevoindice =[(index[i],  self.stadistics.index[i]) for i in range(len( self.stadistics))]
        multi_index = pd.MultiIndex.from_tuples(Nuevoindice , names=[self.data,"Estadísticas"])
        self.stadistics.index = multi_index

        return self.stadistics

    """
    getZScores: Método para obtener el parametro z del informe completo
    -inputs:
        -data: Define si quiero organizar mi tabla con z score  por sesión o jugador.

    -outputs:
        -c : Z score x sesión o jugador
        -cP: Z score promedio por sesión o jugador
    """
    def getZScores(self):
        lista = self.listaJugadores if (self.data=="Jugador") else self.listaSesiones if(self.data=="Sesión") else None
        c=self.compInformByXData.copy()
        c.drop(columns=["Duración (min)", "Creado (fecha)"], inplace=True)
        c.columns = [i+ "- Z score" for i in c.columns]

        templist=[]
        templiswimuApp=[]

        for element in lista:                                   #Iterar sobre cada sesión o jugador
            m = c.loc[element]
            m = (m - m.mean()) / m.std()                       #Calcula z score

            m["Sesión"]=[element]*len(m)
            m.set_index(["Sesión"], append=True, inplace=True)
            m=m.swaplevel(0, 1)
            m['Z score Average'] = m.mean(axis=1)              #Promedio de los z scores x línea
            templiswimuApp.append(m['Z score Average'].mean()) #Promedio x sesión
            templist.append(m)


        # Concatenar las nuevas columnas con el DataFrame original
        c = pd.concat(templist)
        c["Creado (fecha)"] = self.compInformByXData["Creado (fecha)"].to_list()
        columnas = ['Creado (fecha)'] + [col for col in c.columns if col != 'Creado (fecha)']
        c = c[columnas]
                                        
        cP = pd.DataFrame(templiswimuApp, columns=["Promedios Z score"])                 #cP:Matriz con el promedio de los z score
        cP.index = lista

        return c, cP


    """
    loadInform: metodo para cargar un informe de un archivo
    -inputs:
        -fileName: Nombre del archivo de donde quiero sacar mi información
    """
    def loadInform(self, fileName= "miInformeCompleto.csv"):
        self.compInform=pd.read_csv(fileName)

        if np.array_equal(self.compInform.columns,['id', 'Sesión', 'Creado (fecha)', 'Jugador', 'Duración (min)','Distancia m', 'HSRAbsDistance', 'highIntensityAccAbsCounter','highIntensityDecAbsCounter']):
            self.listaJugadores = sorted(pd.unique(self.compInform["Jugador"]))
            self.listaSesiones  = pd.unique(self.compInform["Sesión"]) #Tenga presente que las sesiónes por defecto ya vienen ordenadas por fecha
            return True
        else:
            return False
        
    def loadSesList(self, fileName= "miListadoDeSesiones.csv"):

        self.session = pd.read_csv(fileName)

        # Revisar si sigue el formato es adecuado
        if np.array_equal(self.session.columns, ["id",'Nombre', 'Creado', 'Duración (min)', 'matchDay', 'semanaCal', 'Participantes', 'Actividades de la sesión']):

            self.session["Participantes"] = self.session["Participantes"].apply(lambda val: val.split(","))                       #PARTICIPANTES -> LIST
            self.session["Actividades de la sesión"] = self.session["Actividades de la sesión"].apply(lambda val: val.split(",")) #ACTIVIDADES -> LIST

            self.session.set_index("id", inplace=True)
            return True
        else: 
            return False

#---------------------------------------------------------------------------------------------------------------
"""
genInformResults: Función que permite obtener a partir del informe completo, el informe por jugador o sesión, los z score y estadísticas.
"""
def genInformResults():
    global informe_Jug, informe_JugZ, informe_JugZProm, informe_JugEst, informe_Ses, informe_SesEst, informe_SesZ, informe_SesZProm
    informe_Ses         = wimuApp.getAllInformsByXData("Sesión")
    informe_SesZ, informe_SesZProm = wimuApp.getZScores()
    informe_SesEst      = wimuApp.getStatistics()

    informe_Jug         = wimuApp.getAllInformsByXData("Jugador")
    informe_JugZ, informe_JugZProm = wimuApp.getZScores()
    informe_JugEst      = wimuApp.getStatistics()
    return informe_Jug, informe_JugZ, informe_JugZProm, informe_JugEst, informe_Ses, informe_SesEst, informe_SesZ, informe_SesZProm


# Las siguientes funciones, solo pueden ser empleadas luego de haber seguido los siguientes pasos: 
#   1-Crear una instancia del objeto que debe estar llamada "wimuApp" (de ningún otro modo servirá)
#   2-Se debe generar el litstado de sesiones
#   3-Se debe generar el informe completo
#   4-Se debe generar el informe completo ordenado por sesión
#   5-Se debe generar la tabla de z-score para la tabla x sesión


#FUNCIONES DE COLOREADO:
#%%
def color_unico(val):
    return 'background-color: #d6fdff; color: red'


# Función para aplicar el estilo a la tabla de semaforo:
def colorear_celdas(val):
    abs_val = abs(val)
    if abs_val < 0.5:
        color = 'background-color: green; color: white;'
    elif abs_val>= 0.5 and abs_val < 1:
        color = 'background-color: yellow; color: black;'
    elif abs_val>= 1 and abs_val < 1.5:
        color = 'background-color: orange; color: white;'
    elif abs_val>= 1.5:
        color = 'background-color: red; color: white;'
    else:
        color = 'background-color: grey; color: white;'
    return color

# Las siguientes funciones, solo pueden ser empleadas luego de haber seguido los siguientes pasos: 
#   1-Crear una instancia del objeto que debe estar llamada "wimuApp" (de ningún otro modo servirá)
#   2-Se debe generar el litstado de sesiones
#   3-Se debe generar el informe completo
#   4-Se debe generar el informe completo ordenado por sesión
#   5-Se debe generar la tabla de z-score para la tabla x sesión


"""
getMdayZscore: Función para obtener el promedio de z score para cada jugador por tipo de match day
-outputs:
    -md_table:      Tabla con el promedio de z core por jugador (líneas) en cada tipo de match day (columnas)
    -md_dic: Diccionario que contiene en cada value, una lista con las sesiones correspondientes a cada sesión.
"""
def getMdayZscore():
    global md_table, md_dic, md_ser
    md=['MD', '-1 MD', '-2 MD', '-3 MD', '-4 MD', '-5 MD', '>-5 MD', '+1 MD', '+- MD', '+2 MD', 'No MD']

    md_dic ={}
    for i in md:                        # Obtener md_dic
        md_dic[i] = wimuApp.session.query('matchDay == @i')["Nombre"].tolist()

    j_md = []
    for n in wimuApp.listaJugadores:    #Para cada jugador...
        j=informe_JugZ.loc[n]
        j_md_dic={}
        for i in md:                  #Para cada mathc day....
            j_md_dic[i]=np.intersect1d(j.index, md_dic[i])      #Array con la intersección de elementos de sesiones contenidos en el md n
            j_md_dic[i]=j.loc[j_md_dic[i]]
            j_md_dic[i] = j_md_dic[i]["Z score Average"].mean() #Calcular promedio de md para jugador
        
        j_md.append(j_md_dic)

    md_table=pd.DataFrame(j_md, index=wimuApp.listaJugadores)
    md_table.index.name ="Jugadores"

    md_ser=pd.Series(md_dic)
    md_ser.name ="Sesiones acumuladas por MD"
    return md_table, md_dic, md_ser

#---------------------------------------------------------------------------------------------------------------
"""
getMDAYTable: Función que busca el tipo de MD que fue cada sesión y genera una tabla con los resultados de z score por sesión según el MD
-outputs:
    -tablaSemaforo: Resultados de Z - score por sesión según el MD para todos los jugadores
"""
def getMDAYTable():
    global tablaSemaforo, tablaSemaforo_styled
    tempList  = []
    matchType = ["Tipo de MatchDay"]
    for n in wimuApp.listaSesiones: #Buscar el tipo de MD que fue cada sesión y obtener los resultados por sesión
        for llave, array in md_dic.items():  
            if n in array:
                llave_con_n = llave
                break  # Deja de buscar una vez que se encuentra el elemento
        matchType.append(llave_con_n)
        df=informe_SesZ.loc[n][["Z score Average"]].copy().sort_index()

        miM=md_table.loc[df.index][llave_con_n] #Obtener el promedio para el tipo de Mathc day
        df=pd.concat([df,miM], axis=1)

        # Añadir una nueva columna basada en la comparación

        df[n] = df["Z score Average"]-df[llave_con_n] #(PROMEDIO Z SCORE SESIÓN - Z SCORE TIPO DE MD)
        df=df[[n]]
        tempList.append(df)

    #Formmatear la tabla "tablaSemaforo":
    #-------------------------------------------------------------------------------------
    ## Combinar los DataFrames
    tablaSemaforo = pd.concat(tempList, axis=1).sort_index().reset_index().round(1) #CONCATENAR RESULTADOS
    ## Convertir la lista en un DataFrame
    nueva_fila_df = pd.DataFrame([matchType], columns=tablaSemaforo.columns)

    ## Concatenar la nueva fila al inicio del DataFrame
    tablaSemaforo = pd.concat([nueva_fila_df, tablaSemaforo], ignore_index=True)
    ## Extraer la primera fila
    first_row = tablaSemaforo.iloc[0]

    ## Eliminar la primera fila ya que ahora está en el MultiIndex
    tablaSemaforo= tablaSemaforo.set_index("Jugador")
    tablaSemaforo.columns = pd.MultiIndex.from_tuples(list(zip(tablaSemaforo.columns, first_row[1:])))
    ## Eliminar la primera línea usando el índice real
    tablaSemaforo = tablaSemaforo.drop(tablaSemaforo.index[0])

    tablaSemaforo_styled = tablaSemaforo.style.format('{:.1f}').map(colorear_celdas)
    
    return tablaSemaforo, tablaSemaforo_styled


def SemIndv(sessionValue):       

    seleccion=tablaSemaforo[sessionValue].copy()
    md=seleccion.columns[0]

    datos = seleccion[md]
    seleccion.columns=[sessionValue+" ("+md+")"] #Solo la sesión
    concat = pd.concat([seleccion, md_table], axis=1)   #La sesión y los match day

    seleccion_styled = seleccion.style.map(colorear_celdas)
    concat_styled = concat.style.map(colorear_celdas, subset=[concat.columns[0]])
    concat_styled = concat_styled.map(color_unico, subset=[md])
    return datos, seleccion, concat, seleccion_styled, concat_styled




wimuApp= myTeamAPIWimu(header=headersWimu, urls=urlsWimu) #Crear objeto con la clase
