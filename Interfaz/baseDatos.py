import pyodbc
from tkinter import messagebox

class BaseDatos:
    def __init__(self):
        self.direccion_servidor = 'localhost'
        self.nombre_usuario = 'sa'
        self.password = 'auditoria'
        self.conexion = None
        self.cursor = None
        self.baseActual = None

    # Se emite un error si no se ha establecido la conexión
    def checkConexion(self):
        if self.conexion == None:
            raise NameError('No se ha establecido aún una conexión')

    # Se realiza una conexion sin una base
    def conectarSinBase(self):
        try:
            # Establecer conexión
            self.conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};' +
                                            'SERVER=' + self.direccion_servidor +
                                            ';UID=' + self.nombre_usuario +
                                            ';PWD=' + self.password)
            print('Conexión exitosa!')            
            # Cursor de la conexión
            self.cursor = self.conexion.cursor()
        except Exception as e:
            # Atrapar error
            print("Ocurrió un error al conectar a SQL Server: ", e)

    # Se configura la base actual
    def setBaseDatos(self, nombreBaseDatos: str):
        self.baseActual = nombreBaseDatos
    
    # Se conecta a la base actual
    def conectarConBase(self, base: str = None):
        if base != None:
            self.setBaseDatos(base)
        if self.baseActual == None:
            raise NameError('No se indicó una base de datos. Usar setBaseDatos(nombreBaseDatos: str)')
        try:
            self.conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};' +
                                            'SERVER=' + self.direccion_servidor +
                                            ';DATABASE=' + self.baseActual +
                                            ';UID=' + self.nombre_usuario +
                                            ';PWD=' + self.password)            
            messagebox.showinfo(message=f'Conexión a la base {self.baseActual} exitosa!', title='Conexión exitosa')

            # Cursor de la conexión
            self.cursor = self.conexion.cursor()
        except Exception as e:
            # Atrapar error
            messagebox.showerror(message=f'Ocurrió un error al conectar a la base {self.baseActual}', title='Error en la conexión')
            print(f"Ocurrió un error al conectar a la base {self.baseActual}", e)

    # Devuelve una lista de strings con los nombres de las bases existentes
    def getBasesExistentes(self):
        self.checkConexion()
        self.cursor.execute('SELECT name FROM master.sys.databases')
        tuplas = self.cursor.fetchall()
        return [tupla[0] for tupla in tuplas]

    # Ejecuta un script de un archivo indicado
    def ejecutarScript(self, fileName: str):
        directory = '../SQL_scripts/'
        with open(directory + fileName, 'r') as f:
            query = f.read()
            self.cursor.execute(query)

    # Borra los 4 Stored Procedures existentes
    def borrarStoredProcedures(self):
        self.ejecutarScript('DROP_EXISTING_SP.sql')
        print('Stored Procedures eliminados')

    # Crea los 4 Stored Procedures para la auditoria
    def crearStoredProcedures(self):
        self.ejecutarScript('SP_RELACIONES_DESHABILITADAS.sql')
        self.ejecutarScript('SP_POSIBLES_RELACIONES.sql')
        self.ejecutarScript('SP_TRIGGERS_DESHABILITADOS.sql')
        self.ejecutarScript('SP_CHEQUEO_AUTOMÁTICO.sql')
        print('Stored Procedures creados (4)')
    
    # Ejecutar Stored Procedures
    def execStoredProcedure(self, nombreSP: str):
        query = 'EXEC ' + nombreSP
        rows = self.cursor.execute(query).fetchall()
        return [list(row) for row in rows]

    def execRelacionesDeshabilitadas(self):
        return self.execStoredProcedure('RelacionesDeshabilitadas')
    
    def execPosiblesRelaciones(self):
        return self.execStoredProcedure('PosiblesRelaciones')

    def execTriggersDeshabilitados(self):
        return self.execStoredProcedure('TriggersDeshabilitados')

    def execChequeoAutomatico(self):
        return self.execStoredProcedure('ChequeoAutomatico')