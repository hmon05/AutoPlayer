import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
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
        self.tab_mapeo.columnconfigure(0, weight=1)
        self.tab_mapeo.columnconfigure(1, weight=1)
        self.tab_mapeo.columnconfigure(2, weight=1)

        self.btn_iniciar = tk.Button(self.tab_mapeo, text="Iniciar Mapeo", command=lambda: threads.iniciar_mapeo_ventana(self))
        self.btn_iniciar.grid(row=0, column=0, padx=35, pady=20, sticky="w")

        self.btn_detener = tk.Button(self.tab_mapeo, text="Detener Mapeo", command=lambda: threads.detener_mapeo_ventana(self))
        self.btn_detener.grid(row=0, column=1, pady=20, sticky="w")
        
        self.btn_guardar = tk.Button(self.tab_mapeo, text="Guardar Clics", command=self.guardar_clics_ventana)
        self.btn_guardar.grid(row=0, column=2, padx=30, pady=20, sticky="w")

        self.canvas = tk.Canvas(self.tab_mapeo, width=382, height=382, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=3, padx=5)
        self.text_datos = tk.Text(self.tab_mapeo, height=10, width=45)
        self.text_datos.grid(row=2, column=0, columnspan=3, padx=10, pady=15)


        
    def inicializar_mapeo(self):
        self.clicks = []
        self.limpiar_canvas()
        self.dibujar_grid()

    def dibujar_grid(self):
        for i in range(-10, 382, 10):  # Dibuja líneas verticales cada 20 píxeles
            self.canvas.create_line(i, -10, i, 382, fill="lightgray")
        for i in range(-10, 382, 10):  # Dibuja líneas horizontales cada 20 píxeles
            self.canvas.create_line(-10, i, 382, i, fill="lightgray")

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

            self.region_left = 305
            self.region_top = 42
            self.region_width = 1242 - self.region_left
            self.region_height = 707 - self.region_top
    
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
            
            canvas_x = (relative_x_region / self.region_width) *  380
            canvas_y = (relative_y_region / self.region_height) * 380

            self.canvas.create_oval(canvas_x - 3, canvas_y - 3, canvas_x + 3, canvas_y + 3, fill="yellow")
            print(f"Clic relativo a region detectado en: ({relative_x_region}, {relative_y_region})")
            self.text_datos.insert(tk.END, f"Clic en: ({x}, {y})\n")
            self.text_datos.see(tk.END)  # Autoscroll al final del texto
        except Exception as e:
            print(f"Error en registrar_clic: {e}")
    
    def guardar_clics_ventana(self):
        if self.clicks:
            # Solicitar al usuario que elija el nombre del archivo
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

            if not file_path:
                print("Guardado cancelado por el usuario.")
                return  # No guardar nada si el usuario cancela
            
            try:
                with open(file_path, "w") as f:
                json.dump(self.clicks, f)
                print(f"Clics guardados en {file_path}")
                self.limpiar_canvas()
                self.dibujar_grid()
                self.clicks = []
            except Exception as e:
                print(f"Error al guardar los clics: {e}")
        else:
            print("No hay clics para guardar.")
    

root = tk.Tk()
app = App(root)
root.mainloop()
