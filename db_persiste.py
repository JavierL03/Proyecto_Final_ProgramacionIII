#Archivo para la creacion de la persistencia solicitada del proyecto 
from db_conexion import crear_conexion, cerrar_conexion

def insertar_municipio(nombre):
    conexion = crear_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO tbl_verticesmunicipios (nombreMunicipio) VALUES (%s)", (nombre,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error insertando municipio: {e}")
        return False
    finally:
        cerrar_conexion(conexion)

def insertar_conexion(id_origen, id_destino, distancia):
    conexion = crear_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO tbl_aristadistancia (idOrigen, idDestino, kmDistancia)
            VALUES (%s, %s, %s)
        """, (id_origen, id_destino, distancia))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error insertando conexión: {e}")
        return False
    finally:
        cerrar_conexion(conexion)

def conexion_existe(id_origen, id_destino):
    conexion = crear_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 1 FROM tbl_aristadistancia
            WHERE idOrigen = %s AND idDestino = %s
                OR (idOrigen = %s AND idDestino = %s) 
            LIMIT 1
        """, (id_origen, id_destino, id_destino, id_origen))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error verificando conexión existente: {e}")
        return False
    finally:
        cerrar_conexion(conexion)


def actualizar_distancia(id_origen, id_destino, nueva_distancia):
    conexion = crear_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE tbl_aristadistancia
            SET kmDistancia = %s
            WHERE idOrigen = %s AND idDestino = %s
        """, (nueva_distancia, id_origen, id_destino))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error actualizando distancia: {e}")
        return False
    finally:
        cerrar_conexion(conexion)

def obtener_municipios():
    conexion = crear_conexion()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT idMunicipio, nombreMunicipio FROM tbl_verticesmunicipios")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error obteniendo municipios: {e}")
        return []
    finally:
        cerrar_conexion(conexion)


def eliminar_municipio(id_municipio):
    conexion = crear_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM tbl_aristadistancia WHERE idOrigen = %s OR idDestino = %s", (id_municipio, id_municipio))
        cursor.execute("DELETE FROM tbl_verticesmunicipios WHERE idMunicipio = %s", (id_municipio,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error eliminando municipio: {e}")
        return False
    finally:
        cerrar_conexion(conexion)

def eliminar_conexion(id_origen, id_destino):
    conexion = crear_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM tbl_aristadistancia WHERE idOrigen = %s AND idDestino = %s", (id_origen, id_destino))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error eliminando conexión: {e}")
        return False
    finally:
        cerrar_conexion(conexion)

        
def vaciar_tablas():
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM tbl_aristadistancia")
        cursor.execute("DELETE FROM tbl_verticesmunicipios")
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error vaciando tablas: {e}")
        return False
    finally:
        cerrar_conexion(conexion)

def obtener_conexiones():
   
    conexion = crear_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT idOrigen, idDestino, kmDistancia FROM tbl_aristadistancia")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error obteniendo conexiones: {e}")
        return []
    finally:
        cerrar_conexion(conexion)
