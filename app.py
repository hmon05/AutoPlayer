import tkinter as tk
from tkinter import ttk
import json
import pyautogui
import time

class App:
    def __init__(self, master):
        self.master = master
        master.title("Mapeo de Clics")
        
        from modules.window_manager import WindowManager
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.tab_seleccion = ttk.Frame(self.notebook)
        self.tab_mapeo = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_seleccion, text="Selección de Programa")
        self.notebook.add(self.tab_mapeo, text="Mapeo de Clics")
    
        self.crear_tab_seleccion()  # Llama a crear_tab_seleccion aquí
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
        self.btn_iniciar = tk.Button(self.tab_mapeo, text="Iniciar Mapeo", command=self.iniciar_mapeo_ventana)
        self.btn_iniciar.pack(pady=10, side=tk.TOP)  # Align to the top
        
        self.btn_detener = tk.Button(self.tab_mapeo, text="Detener Mapeo", command=self.detener_mapeo_ventana)
        self.btn_detener.pack(side=tk.TOP)  # Align to the top
        
        self.btn_guardar = tk.Button(self.tab_mapeo, text="Guardar Clics", command=self.guardar_clics_ventana)
        self.btn_guardar.pack(side=tk.TOP)  # Align to the top

        self.canvas.pack(side=tk.TOP)
        self.text_datos = tk.Text(self.tab_mapeo, height=10, width=50)
        self.text_datos.pack(side=tk.TOP)
        
    def dibujar_grid(self):
        for i in range(0, 600, 20):  # Dibuja líneas verticales cada 20 píxeles
            self.canvas.create_line(i, 0, i, 400, fill="lightgray")
        for i in range(0, 400, 20):  # Dibuja líneas horizontales cada 20 píxeles
            self.canvas.create_line(0, i, 600, i, fill="lightgray")

    def limpiar_canvas(self):
        self.canvas.delete("all")  # Elimina todos los elementos del Canvas
        
    def seleccionar_ventana(self):
        self.selected_window = self.window_manager.select_window(self.combobox_ventanas)
    
    def iniciar_mapeo_ventana(self):
        if self.selected_window:
            self.mapping_active = True
            self.clicks = []
            self.limpiar_canvas()
            self.dibujar_grid()
            print(f"Iniciando mapeo de clics en la ventana: {self.selected_window}")
            self.monitorear_clics_ventana()
        else:
            print("Selecciona una ventana primero.")
    
    def detener_mapeo_ventana(self):
        self.mapping_active = False
        print("Mapeo detenido.")
    
    def guardar_clics_ventana(self):
        if self.clicks and self.selected_window:
            filename = f"clics_{self.selected_window.title.replace('.exe', '').replace(' ', '_')}.json"
            with open(filename, "w") as f:
                json.dump(self.clicks, f)
            print(f"Clics guardados en {filename}")
        else:
            print("No hay clics para guardar.")
    
    def monitorear_clics_ventana(self):
        while self.mapping_active and self.selected_window:
            x, y = pyautogui.position()
            if self.selected_window.isActive:
                self.clicks.append((x, y))
                self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="yellow")
                print(f"Clic detectado en: ({x}, {y})")

                # Muestra los datos en el widget Text
                self.text_datos.insert(tk.END, f"Clic en: ({x}, {y})\n")
                self.text_datos.see(tk.END)  # Autoscroll al final del texto

            time.sleep(0.1)

root = tk.Tk()
app = App(root)
root.mainloop()