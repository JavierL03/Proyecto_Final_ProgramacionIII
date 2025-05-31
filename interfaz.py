import json                              #  pra R/W JSON
import os
import matplotlib.pyplot as plt          #   dibujar grafo
import networkx as nx                    #   manipulacion de grafos 
from tkinter.filedialog import askopenfilename, asksaveasfilename  # Abrir dialogo para abrir y guardar JSON
import tkinter as tk # Realizar interfaz grafica
from tkinter import ttk, messagebox # Popup de mensajes, confirmaciones, advertencias 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from grafo import Grafo # importar clase Grafo de mi archivo grafo.py
from algoritmoGrafo import algBFS, algDFS # importar mis funciones BFS y DFS de mi archivo AlgoritmoGrafo.py

from db_persiste import ( # importar funciones de persistencia de los datos del archivo db_persiste.py
    conexion_existe,
    insertar_municipio,
    insertar_conexion,
    actualizar_distancia,
    obtener_municipios,
    vaciar_tablas,
    obtener_conexiones,
    eliminar_municipio as eliminar_municipio_db,
    eliminar_conexion as eliminar_conexion_db    
)


# inicio de interfaz grafica. 
class InterfazGrafo:
    def __init__(self, root):
        self.root = root
        self.root.title("GrafoGT APP")

        #mi Icono
        #self.root.iconbitmap("C:/Users/JESDA_PC/OneDrive - Universidad Mariano Gálvez/Escritorio/UMG-7/Progra III/EndProyect/icono/iconoWindow.ico")

        base = os.path.dirname(__file__)
        icon_path = os.path.join(base, "icono", "iconoWindow.ico")
        self.root.iconbitmap(icon_path)

        self.root.rowconfigure(0, weight=0)  # panel controles
        self.root.rowconfigure(1, weight=1)  # lienzo grafico
        self.root.rowconfigure(2, weight=0)  # editor rapido
        self.root.columnconfigure(0, weight=1)

        self.grafo = Grafo()
        self.G = nx.Graph()
        self.pos = {}

        self._crear_componentes()
        self._crear_editor_rapido()

    def _crear_componentes(self):
        panel = ttk.Frame(self.root)
        panel.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        for col in range(9): #Agregar mas columnas para los botones y labels de opciones 
            panel.columnconfigure(col, weight=1)

        # Cargar / Importar / Exportar
        ttk.Button(panel, text="Cargar Grafo",  command=self.cargar_grafo)  .grid(row=0, column=0, padx=5)
        ttk.Button(panel, text="Importar Grafo", command=self.importar_grafo).grid(row=0, column=1, padx=5)
        ttk.Button(panel, text="Exportar Grafo", command=self.exportar_grafo).grid(row=0, column=2, padx=5)

        # Parte alta Comienzo de Municipio
        ttk.Label(panel, text="Comienzo:").grid(row=0, column=4, padx=5, sticky="e")
        self.combo_origen = ttk.Combobox(panel, state="readonly")
        self.combo_origen.grid(row=0, column=5, padx=5, sticky="ew")

        # Botón BFS
        self.btn_bfs = ttk.Button(panel, text="Ejecutar BFS", command=self.ejecutar_bfs)
        self.btn_bfs.grid(row=0, column=6, padx=5)

        # Botón DFS
        self.btn_dfs = ttk.Button(panel, text="Ejecutar DFS", command=self.ejecutar_dfs)
        self.btn_dfs.grid(row=0, column=7, padx=5)

        # Boton de Reinicio de algoritmos
        self.btn_reiniciar = ttk.Button(panel, text="Reiniciar Recorrido", command=self.reiniciar_grafo)
        self.btn_reiniciar.grid(row=0, column=8, padx=5)

        # lienzo grafico
        self.figura, self.ax = plt.subplots(figsize=(5,4))
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.root)
        widget = self.canvas.get_tk_widget()
        widget.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    # Parte Baja ara el editor rapido y sus funciones o botones 
    def _crear_editor_rapido(self):
        editor = ttk.LabelFrame(self.root, text="Editor Rápido")
        editor.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        # columnas responsivas
        for c in range(5):
            editor.columnconfigure(c, weight=1)

        # fila 0: nuevo municipio
        ttk.Label(editor, text="Nuevo Municipio:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.entry_municipio = ttk.Entry(editor)
        self.entry_municipio.grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(editor, text="Agregar", command=self.agregar_municipio).grid(row=0, column=2, padx=5)

        # fila 1: origen + eliminar municipio
        ttk.Label(editor, text="Origen:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.combo_origen_con = ttk.Combobox(editor, state="readonly")
        self.combo_origen_con.grid(row=1, column=1, padx=5, sticky="ew")
        ttk.Button(editor, text="Eliminar Municipio", command=self.eliminar_municipio).grid(row=1, column=2, padx=5)

        # fila 2: destino + eliminar conexion
        ttk.Label(editor, text="Destino:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        self.combo_destino_con = ttk.Combobox(editor, state="readonly")
        self.combo_destino_con.grid(row=2, column=1, padx=5, sticky="ew")
        ttk.Button(editor, text="Eliminar Conexión", command=self.eliminar_conexion).grid(row=2, column=2, padx=5)

        # limpiar distancia al cambiar selección
        self.combo_origen_con.bind("<<ComboboxSelected>>",
            lambda e: self.entry_distancia.delete(0, tk.END))
        self.combo_destino_con.bind("<<ComboboxSelected>>",
            lambda e: self.entry_distancia.delete(0, tk.END))

        # fila 3: distancia + actualizar
        ttk.Label(editor, text="Distancia (km):").grid(row=3, column=0, padx=5, sticky="e")
        self.entry_distancia = ttk.Entry(editor)
        self.entry_distancia.grid(row=3, column=1, padx=5, sticky="ew")
        ttk.Button(editor, text="Actualizar", command=self.editar_distancia).grid(row=3, column=2, padx=5)
        ttk.Button(editor, text="Agregar Conexión", command=self.agregar_conexion).grid(row=3, column=3, padx=5)

        self.actualizar_comboboxes()

    # Limpia de comboboxs luego de una acción
    def actualizar_comboboxes(self):
        datos = obtener_municipios()
        nombres = [nombre for _, nombre in datos]
        self.municipio_map = {nombre: id_ for id_, nombre in datos}

        self.combo_origen_con['values'] = nombres
        self.combo_destino_con['values'] = nombres
        self.combo_origen['values'] = nombres


    def agregar_municipio(self):
        nombre = self.entry_municipio.get().strip()
        if not nombre:
            messagebox.showwarning("Campos vacíos", "Debes ingresar un nombre de municipio.")
            return
        
        #Comparación para evitar duplicado haciendo que el nombre ingresado se vuelva minuscula 
        existentes = [n.lower() for _, n in obtener_municipios()]
        if nombre.lower() in existentes:
            messagebox.showwarning(
                "Duplicado", f"El municipio '{nombre}' ya existe."
            )
            return

        if insertar_municipio(nombre):
            messagebox.showinfo("Éxito", f"Municipio '{nombre}' agregado.")
            self.entry_municipio.delete(0, tk.END)
            self.cargar_grafo()
            self.actualizar_comboboxes()
        else:
            messagebox.showerror("Error", "No se pudo insertar el municipio.")

    def agregar_conexion(self):
        origen = self.combo_origen_con.get()
        destino = self.combo_destino_con.get()
        try:
            distancia = float(self.entry_distancia.get())
        except ValueError:
            messagebox.showwarning("Valor inválido", "La distancia debe ser un número.")
            return
        if origen and destino and origen != destino:
            id_o = self.municipio_map[origen]
            id_d = self.municipio_map[destino]
            if conexion_existe(id_o, id_d):
                messagebox.showwarning("Conexión existente",
                    "Esta conexión ya existe. Usa 'Actualizar'.")
                return
            if insertar_conexion(id_o, id_d, distancia) and insertar_conexion(id_d, id_o, distancia):
                messagebox.showinfo("Éxito", "Conexión agregada.")
                self.entry_distancia.delete(0, tk.END)
                self.combo_origen_con.set('')
                self.combo_destino_con.set('')
                self.cargar_grafo()
            else:
                messagebox.showerror("Error", "No se pudo insertar la conexión.")
        else:
            messagebox.showwarning("Datos faltantes", "Selecciona municipios distintos.")

    def editar_distancia(self):
        origen = self.combo_origen_con.get()
        destino = self.combo_destino_con.get()
        try:
            distancia = float(self.entry_distancia.get())
        except ValueError:
            messagebox.showwarning("Valor inválido", "La distancia debe ser un número.")
            return
        if origen and destino and origen != destino:
            id_o = self.municipio_map[origen]
            id_d = self.municipio_map[destino]
            success = (actualizar_distancia(id_o, id_d, distancia)
                       and actualizar_distancia(id_d, id_o, distancia))
            if success:
                messagebox.showinfo("Distancia actualizada",
                    f"Distancia entre '{origen}' y '{destino}' actualizada a {distancia:.2f} km")
                self.entry_distancia.delete(0, tk.END)
                self.combo_origen_con.set('')
                self.combo_destino_con.set('')
                self.cargar_grafo()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la distancia.")
        else:
            messagebox.showwarning("Datos faltantes", "Selecciona municipios distintos.")

    def eliminar_municipio(self):
        nombre = self.combo_origen_con.get()
        if not nombre:
            messagebox.showwarning("Selecciona un municipio", "Selecciona un municipio a eliminar.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}'?"):
            return
        id_m = self.municipio_map[nombre]
        if eliminar_municipio_db(id_m):
            messagebox.showinfo("Éxito", "Municipio y sus conexiones eliminados.")
            self.combo_origen_con.set('')
            self.combo_destino_con.set('')
            self.combo_origen.set('')
            self.cargar_grafo()
            self.actualizar_comboboxes()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el municipio.")

    def eliminar_conexion(self):
        origen = self.combo_origen_con.get()
        destino = self.combo_destino_con.get()
        if not origen or not destino or origen == destino:
            messagebox.showwarning("Datos inválidos","Selecciona origen y destino diferentes.")
            return
        if not messagebox.askyesno("Confirmar",
                f"¿Eliminar conexión entre '{origen}' y '{destino}'?"):
            return
        id_o = self.municipio_map[origen]
        id_d = self.municipio_map[destino]
        if eliminar_conexion_db(id_o, id_d) and eliminar_conexion_db(id_d, id_o):
            messagebox.showinfo("Éxito","Conexión eliminada.")
            self.combo_origen_con.set('')
            self.combo_destino_con.set('')
            self.cargar_grafo()
        else:
            messagebox.showerror("Error","No se pudo eliminar la conexión.")

    def reiniciar_grafo(self):
        self.dibujar_grafo()
        messagebox.showinfo("Reiniciado","El grafo se ha reiniciado.")
        self.combo_origen.set('')
        self.combo_origen_con.set('')
        self.combo_destino_con.set('')
        self.entry_distancia.delete(0, tk.END)

    def cargar_grafo(self):
        self.grafo.cargar_desde_bd()
        self.dibujar_grafo()
        nodos = list(self.grafo.adyacencia.keys())
        self.combo_origen['values'] = nodos
        if nodos:
            self.combo_origen.current(0)

    def dibujar_grafo(self):
        self.G.clear()
        self.ax.clear()
        for o, vecinos in self.grafo.adyacencia.items():
            for d, p in vecinos.items():
                self.G.add_edge(o, d, weight=p)
        self.pos = nx.spring_layout(self.G, seed=42)
        nx.draw(self.G, self.pos, ax=self.ax,
                with_labels=True, node_color='lightblue',
                node_size=1500, font_size=8)
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, self.pos,
                                     edge_labels=labels, ax=self.ax)
        self.ax.set_title("Grafo de Municipios de Guatemala")
        self.canvas.draw()

    def ejecutar_bfs(self):
        origen = self.combo_origen.get()
        if not origen:
            messagebox.showwarning("Atención","Selecciona un nodo de origen.")
            return
        recorrido = algBFS(self.grafo.adyacencia, origen)
        self.animar_recorrido(recorrido, "BFS")

    def ejecutar_dfs(self):
        origen = self.combo_origen.get()
        if not origen:
            messagebox.showwarning("Atención","Selecciona un nodo de origen.")
            return
        recorrido = algDFS(self.grafo.adyacencia, origen)
        self.animar_recorrido(recorrido, "DFS")

    def animar_recorrido(self, recorrido, tipo):
        self.ax.clear()
        self.G.clear()
        for o, vecinos in self.grafo.adyacencia.items():
            for d, p in vecinos.items():
                self.G.add_edge(o, d, weight=p)
        self.pos = nx.spring_layout(self.G, seed=42)
        labels = nx.get_edge_attributes(self.G, 'weight')

        def paso(i):
            self.ax.clear()
            nodes = list(self.G.nodes)
            colors = ['lightblue']*len(nodes)
            for j in range(i+1):
                colors[nodes.index(recorrido[j])] = 'orange'
            nx.draw(self.G, self.pos, ax=self.ax,
                    with_labels=True, node_color=colors,
                    node_size=1500, font_size=8)
            nx.draw_networkx_edge_labels(self.G, self.pos,
                edge_labels=labels, ax=self.ax)
            self.ax.set_title(f"{tipo} paso {i+1}/{len(recorrido)}")
            self.canvas.draw()
            if i+1 < len(recorrido):
                self.root.after(800, lambda: paso(i+1))
            else:
                messagebox.showinfo(f"{tipo} terminado",
                    f"Orden: {', '.join(recorrido)}")

        paso(0)


    def importar_grafo(self):
        # 1) Selección de archivo
        path = askopenfilename(filetypes=[("JSON","*.json")])
        if not path:
            return

        # 2) Leer y parsear JSON
        try:
            with open(path, 'r', encoding='utf8') as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el JSON:\n{e}")
            return

        # 3) Preguntar modo: sobrescribir o añadir
        opcion = messagebox.askyesnocancel(
            "Importar Grafo",
            "¿Deseas SOBRESCRIBIR toda la DB?\n"
            "Sí = BORRAR TODO y cargar desde el JSON.\n"
            "No = AÑADIR sólo nuevos municipios/conexiones.\n"
            "Cancelar = Salir."
        )
        if opcion is None:
            return
        if opcion:  
            if not vaciar_tablas():
                messagebox.showerror("Error","No se pudo vaciar la base de datos.")
                return

        # 4) Insertar municipios
        existentes = {nombre for _, nombre in obtener_municipios()}
        for nombre in data.get("municipios", []):
            if opcion or nombre not in existentes:
                insertar_municipio(nombre)

        # 5) Reconstruir mapa nombre→id
        mapping = {nombre: id_ for id_, nombre in obtener_municipios()}

        # 6) Insertar conexiones
        for c in data.get("conexiones", []):
            o, d, dist = c["origen"], c["destino"], c["distancia"]
            id_o, id_d = mapping.get(o), mapping.get(d)
            if id_o is None or id_d is None:
                continue
            if not opcion and conexion_existe(id_o, id_d):
                continue
            insertar_conexion(id_o, id_d, dist)
            insertar_conexion(id_d, id_o, dist)

        # 7) Refrescar UI
        self.cargar_grafo()
        self.actualizar_comboboxes()
        messagebox.showinfo("Importar","Grafo importado correctamente.")

    def exportar_grafo(self):
        # 1) Diálogo de guardar
        path = asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON","*.json")]
        )
        if not path:
            return

        # 2) Leer data desde BD
        municipios = obtener_municipios()      # [(id, nombre), …]
        conexiones = obtener_conexiones()      # [(o_id, d_id, km), …]

        # 3) Preparar payload sin IDs en JSON
        payload = {
            "municipios": [nombre for _, nombre in municipios],
            "conexiones": []
        }
        # Construir mapa id→nombre
        id_a_nombre = {id_: nombre for id_, nombre in municipios}

        for o_id, d_id, km in conexiones:
            # km puede venir como Decimal, así que lo pasamos a float
            distancia = float(km)
            payload["conexiones"].append({
                "origen":  id_a_nombre.get(o_id),
                "destino": id_a_nombre.get(d_id),
                "distancia": distancia
            })

        # 4) Volcar a archivo
        try:
            with open(path, 'w', encoding='utf8') as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Exportar", f"Grafo exportado a:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{e}")



if __name__ == '__main__':
    root = tk.Tk()
    app = InterfazGrafo(root)
    root.mainloop()
