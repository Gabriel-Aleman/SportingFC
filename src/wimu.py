from API_FrameWork import *

#WIMU:
tokenWimu = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2NjkxMmRlNmVlNGQ3ZTM1NTIzYmZmMDciLCJjbHViIjoiNjQwZWVjOWE4NTY2ZDQxMmMyZTdlZGUyIiwiY2VudGVyIjoiNjQwZWVkMTE4NTY2ZDQxMmMyZTgxZWRiIiwidXNlclR5cGUiOiJDRU5URVJfQURNSU4iLCJ1c2VyIjoiNjY5MTJkZTZlZTRkN2UzNTUyM2JmZjA3IiwiZXhwIjoxNzI0MzA0NDc3fQ.CL7qRvY0GjfW9eDUpjxNALuh0mBtkL1-J5vD_rB0f78"
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
                                        "semanaCal"                   : mySession['weekCalendar'] ,
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

        #checkArg(index, name, abv, id) #Revisar que se haya ingresado la cantidad correcta de argumentos
        
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
        print("Id del equipo escogido:",self.myTeam)
        

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


    """
    getSessionAssistants: Método para obtener un listado de los jugadores que asistieron a determinada sesión.
    """
    def getSessionAssistants(self, filter=True):
        a= "Miembros" if filter else "members"
        return self.players.loc[self.mySession[a]]
    
    """
    getMySession: Obtener selecionar una sesión especifica
    -input:
        -index: Indice de la sesión (de 0 a n)
        -name: Nombre de la sesión.
        -id:   Id de la sesión
    """
    def getMySession(self, index=None, name=None, id=None):
        #checkArg(index, name, id) #Revisar que se haya ingresado la cantidad correcta de argumentos
        
        if(index is not None):
            self.mySession = self.session.iloc[index]
        
        elif(name is not None):
            self.mySession = self.session.query('Nombre == @name').iloc[0]
            
        elif(id is not None):
            self.mySession = self.session.loc[id]

    """
    getLastSession: Método para usar únicamente la última sesión.
    inputs:
        -s: Variable boooleana que determina si quiero definirlo como mi sesión
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
    """
    def getAllInforms(self, myRange=None, beginDate=None, endDate=None):
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
            #self.progress = (i + 1) / len(mySessions)
            yield (j / len(mySessions))
        print("¡DESCARGA DE TODAS LAS SESIONES FINALIZADA!")
        self.compInform = pd.concat(myTempArray)
        self.compInform.reset_index(drop=True, inplace=True)

        self.listaJugadores = np.sort(pd.unique(self.compInform["Jugador"]))
        self.listaSesiones  = pd.unique(self.compInform["Sesión"]) #Tenga presente que las sesiónes por defecto ya vienen ordenadas por fecha

    """
   getAllInformsByXData: Obtener el informe de sesión 
   inputs:
        -data: Define si quiero organizar mi informe completo por sesión o jugador.
    """
    def getAllInformsByXData(self, data): #Sesión o Jugador
        
        if (data == "Sesión"):      #Ordenar por fecha 
            b = self.compInform.sort_values(by="Creado (fecha)", ascending=False)
        elif (data == "Jugador"):   #Ordenar por jugador (en ordén alfabetico)
            b=self.compInform.sort_values(by=data)
            
        dataX = "Jugador" if (data == "Sesión") else "Sesión" if(data == "Jugador") else None

        # Definir el MultiIndex único que quieres aplicar a todas las filas
        b.set_index([data, dataX], inplace=True)
        b.drop(columns=["id"], inplace=True)
        self.compInformByXData = b
                    
        return self.compInformByXData

    """
    getStatistics: Método para obtener las estadisticas de mi informe completo.
    inputs:
        -data: Define si quiero organizar mi informe completo por sesión o jugador.
    """
    def getStatistics(self, data=None):
        lista = self.listaJugadores if (data=="Jugador") else self.listaSesiones if(data=="Sesión") else None
        
        df = [self.compInformByXData.loc[i][["Distancia m", "HSRAbsDistance", "highIntensityAccAbsCounter", "highIntensityDecAbsCounter" ]].describe() for i in lista]
        df  = pd.concat(df)

        index = [elemento for elemento in lista for _ in range(8)]
        Nuevoindice =[(index[i], df.index[i]) for i in range(len(df))]
        multi_index = pd.MultiIndex.from_tuples(Nuevoindice , names=[data,"Estadísticas"])
        df.index = multi_index
        self.stadistics = df


        return self.stadistics

    """
    getZScores: Método para obtener el parametro z del informe completo
    """
    def getZScores(self, data=None):
        lista = self.listaJugadores if (data=="Jugador") else self.listaSesiones if(data=="Sesión") else None

        c= self.compInformByXData.drop(columns=["Duración (min)", "Creado (fecha)"]).copy()
        c.columns = [i+ "- Z score" for i in c.columns]

        templist=[]
        templist1=[]

        for element in lista:
            m = c.loc[element]
            m = (m - m.mean()) / m.std()

            m["Sesión"]=[element]*len(m)
            m.set_index(["Sesión"], append=True, inplace=True)
            m=m.swaplevel(0, 1)
            m['Z score Average'] = m.mean(axis=1)
            templist1.append(m['Z score Average'].mean())
            templist.append(m)


        # Concatenar las nuevas columnas con el DataFrame original
        c = pd.concat(templist)                                             
        c = pd.concat([ self.compInformByXData["Creado (fecha)"], c], axis=1)   #c: Matriz con los z scores
        cP = pd.DataFrame(templist1, columns=["Promedios Z score"])                 #cP:Matriz con el promedio de los z score
        cP.index = lista

        return c, cP

    def getMatCorr():
        pass
    
    def saveInform(self):
        nombre_archivo = f'InformeGuardado_{self.myTeam}.csv'

        # Guardar el DataFrame en un archivo CSV con la fecha en el nombre
        self.compInform.to_csv(nombre_archivo, index=False)
        print("INFORME GUARDADO EXITOSAMENTE")

    def loadInform(self, fileName):
        self.compInform = pd.read_csv(fileName)
        self.myTeam ="InformeGuardado_640eed118566d412c2e81edb.csv"
        self.myTeam=self.myTeam.split("_",1)
        self.myTeam=self.myTeam[1][:-4]
        self.urls["urlPlayers"] = f"https://wimupro.wimucloud.com/apis/rest/players?team={self.myTeam}&page=1&limit=200&sort=name%2Casc"
        print("Id del equipo escogido:",self.myTeam)
        print("INFORME CARGADO EXITOSAMENTE")

wimuApp= myTeamAPIWimu(header=headersWimu, urls=urlsWimu)

