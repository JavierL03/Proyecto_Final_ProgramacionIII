#principal.py para inicializar la ejecucion del proyecto final progra III

from tkinter import Tk #Libreria tkinter para interfaz grafica importando su clase Tk 
from interfaz import InterfazGrafo #importo mi clase InterfazGrafo de mi archivo interfaz.py

if __name__ == '__main__':
    root = Tk()
    app = InterfazGrafo(root)
    root.mainloop()
