import pyodbc
direccion_servidor = 'localhost'
nombre_bd = 'pubs'
nombre_usuario = 'sa'
password = 'auditoria'
try:
    #conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
     #                         direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD=' + password)

    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                              direccion_servidor+';UID='+nombre_usuario+';PWD=' + password)                              
    # OK! conexión exitosa
    print('Conectado')
    cursor = conexion.cursor()

    #for database in cursor.tables():
        #print(database)
    cursor.execute('SELECT name FROM master.sys.databases')
    bases = cursor.fetchall()
    #for base in bases:
        #print(base)
    print(bases)
    base = bases[4][0]
    print(base)
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                              direccion_servidor+';DATABASE='+base+';UID='+nombre_usuario+';PWD=' + password)
    # Crear Todos los procesdimientos
    
    tablas = conexion.cursor().tables()
    for tabla in tablas:
        print(tabla)

except Exception as e:
    # Atrapar error
    print("Ocurrió un error al conectar a SQL Server: ", e)