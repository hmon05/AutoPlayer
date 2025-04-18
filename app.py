import tkinter as tk
from tkinter import ttk
import json
import win32api
import win32con
import threading
import time
from modules import threads
ancho, alto = 400 , 700

class App:
    def __init__(self, master):
        self.master = master
        master.title("BOT de Clics")
        
        ancho_pantalla = root.winfo_screenwidth()
        alto_pantalla = root.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        master.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        from modules.window_manager import WindowManager
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.tab_seleccion = ttk.Frame(self.notebook)
        self.tab_mapeo = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_seleccion, text="Selección de Programa")
        self.notebook.add(self.tab_mapeo, text="Mapeo de Clics")
        
        #Tab Mapeo
        self.canvas = tk.Canvas(self.tab_mapeo, bg="white", width=ancho, height=alto)
        
        self.crear_tab_mapeo()  # Llama a crear_tab_mapeo aquí
    
        self.selected_window = None
        self.mapping_active = False
        self.clicks = []
    
        self.window_manager = WindowManager()  # Crea una instancia de WindowManager
        
        self.combobox_ventanas = ttk.Combobox(self.tab_seleccion, width=34, font=('Comfortaa', 10), state="readonly", justify="center")
        self.combobox_ventanas.pack(pady=5)
        self.cargar_ventanas()
        
        self.btn_seleccionar_ventana = tk.Button(self.tab_seleccion, text="Seleccionar Ventana", command=self.seleccionar_ventana)
        self.btn_seleccionar_ventana.pack(pady=10)

    def cargar_ventanas(self):
        self.window_manager.cargar_ventanas(self.combobox_ventanas)

    

    def crear_tab_mapeo(self):
        self.btn_iniciar = tk.Button(self.tab_mapeo, text="Iniciar Mapeo", command=lambda: threads.iniciar_mapeo_ventana(self))
        self.btn_iniciar.pack(pady=10, side=tk.TOP)

        self.btn_detener = tk.Button(self.tab_mapeo, text="Detener Mapeo", command=lambda: threads.detener_mapeo_ventana(self))
        self.btn_detener.pack(side=tk.TOP)  # Align to the top
        
        self.btn_guardar = tk.Button(self.tab_mapeo, text="Guardar Clics", command=self.guardar_clics_ventana)
        self.btn_guardar.pack(side=tk.TOP)  # Align to the top

        self.canvas.pack(pady=1)
        self.text_datos = tk.Text(self.tab_mapeo, height=10, width=50)
        self.text_datos.pack(pady=1)
        
    def inicializar_mapeo(self):
        self.clicks = []
        self.limpiar_canvas()
        self.dibujar_grid()

    def dibujar_grid(self):
        for i in range(0, alto, 20):  # Dibuja líneas verticales cada 20 píxeles
            self.canvas.create_line(i, 0, i, ancho, fill="lightgray")
        for i in range(0, ancho, 20):  # Dibuja líneas horizontales cada 20 píxeles
            self.canvas.create_line(0, i, alto, i, fill="lightgray")

    def limpiar_canvas(self):
        self.canvas.delete("all")  # Elimina todos los elementos del Canvas
        
    def seleccionar_ventana(self):
        self.selected_window = self.window_manager.select_window(self.combobox_ventanas)
        if self.selected_window:
            self.notebook.select(self.tab_mapeo)  # Cambia a la pestaña de mapeo
            self.notebook.tab(self.tab_seleccion, state="disabled")
            self.inicializar_mapeo()

            # Guardar las dimensiones de la ventana mapeada y de la region
            self.window_width = self.selected_window.width
            self.window_height = self.selected_window.height
            self.window_left = self.selected_window.left
            self.window_top = self.selected_window.top

            self.region_left = 380
            self.region_top = 40
            self.region_width = 1168 - 380
            self.region_height = 840 - 40
    
    def registrar_clic(self, x, y):
        try:
            # Coordenadas relativas a la ventana completa
            relative_x_full = x - self.window_left
            relative_y_full = y - self.window_top
            
            # Verificar si el clic está dentro de la región
            if not (self.region_left <= relative_x_full <= self.region_left + self.region_width and
                    self.region_top <= relative_y_full <= self.region_top + self.region_height):
                return  # Ignorar el clic

            # Coordenadas relativas a la región
            relative_x_region = relative_x_full - self.region_left
            relative_y_region = relative_y_full - self.region_top
            self.clicks.append((x, y))
            
            canvas_x = (relative_x_region / self.region_width) *  alto
            canvas_y = (relative_y_region / self.region_height) * ancho

            self.canvas.create_oval(canvas_x - 5, canvas_y - 5, canvas_x + 5, canvas_y + 5, fill="yellow")
            print(f"Clic relativo a region detectado en: ({relative_x_region}, {relative_y_region})")
            self.text_datos.insert(tk.END, f"Clic en: ({x}, {y})\n")
            self.text_datos.see(tk.END)  # Autoscroll al final del texto
        except Exception as e:
            print(f"Error en registrar_clic: {e}")
    
    def guardar_clics_ventana(self):
        if self.clicks and self.selected_window:
            filename = f"clics_{self.selected_window.title.replace('.exe', '').replace(' ', '_')}.json"
            with open(filename, "w") as f:
                json.dump(self.clicks, f)
            self.stop_thread = True
            self.thread.join()
            print(f"Clics guardados en {filename}")
            self.limpiar_canvas()
            self.dibujar_grid()
            self.clicks = []
        else:
            print("No hay clics para guardar.")
    

root = tk.Tk()
app = App(root)
root.mainloop()
