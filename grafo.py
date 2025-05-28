from db_conexion import crear_conexion, cerrar_conexion

class Grafo:
    def __init__(self):
        self.adyacencia = {} 

    def agregar_arista(self, origen, destino, distancia):
     
        if origen not in self.adyacencia:
            self.adyacencia[origen] = {}
        self.adyacencia[origen][destino] = distancia

    def cargar_desde_bd(self):
    
        # Datos cargados de la DB construyendo la lista de adyacencia

        self.adyacencia = {} 
        conexion = crear_conexion()
        if not conexion:
            print("No se pudo establecer conexión con la DB db_grafogt")
            return

        try:
            cursor = conexion.cursor()

            # municipios: {id: nombre}
            cursor.execute("SELECT idMunicipio, nombreMunicipio FROM tbl_verticesmunicipios")
            municipios = {id_: nombre for id_, nombre in cursor.fetchall()}


            # aristas (distancias)
            cursor.execute("SELECT idOrigen, idDestino, kmDistancia FROM tbl_aristadistancia")
            aristas = cursor.fetchall()

            # Construccion o visualizacion de nuestro grafo
            for id_origen, id_destino, distancia in aristas:
                origen_nombre = municipios.get(id_origen)
                destino_nombre = municipios.get(id_destino)

                if origen_nombre and destino_nombre:
                    self.agregar_arista(origen_nombre, destino_nombre, distancia)
                    self.agregar_arista(destino_nombre, origen_nombre, distancia)  

            print("Grafo cargado correctamente desde la DB db_grafogt")

        except Exception as e:
            print(f"Error al cargar el grafo: {e}")

        finally:
            cerrar_conexion(conexion)

    def mostrar_grafo(self):

        print("Lista de adyacencia del grafo:")
        for nodo, vecinos in self.adyacencia.items():
            conexiones = ', '.join([f"{v} ({d} km)" for v, d in vecinos.items()])
            print(f" {nodo} → {conexiones}")
