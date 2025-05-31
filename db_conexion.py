import pymysql #libreria utilizada para la conexion a la DB llamada db_grafogt

def crear_conexion():
  
    #Nuestra conexión hacia la DB de MariaDB usando la libreria pymysql

    try:
        conexion = pymysql.connect(
            host='localhost',
            port=3307, #puerto utilizado modificado del default de MariaDB  
            user='root', #El user 
            password='1234',#El password 
            database='db_grafogt', #Nuestra base de datos llamada db_grafogt contiene dos tablas 
            charset='utf8mb4'
        )
        print(f"Se ha establecido la conexion a la DB db_grafogt")
        return conexion
    except pymysql.MySQLError as e:
        print(f"Error en la conexion a la DB: {e}")
        return None

def cerrar_conexion(conexion):
    if conexion:
        conexion.close()
        print("Conexión Finalizada")
