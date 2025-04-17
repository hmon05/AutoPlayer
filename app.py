import tkinter as tk
from tkinter import ttk
import pyautogui
import json
import psutil
import time

class App:
    def __init__(self, master):
        self.master = master
        master.title("Mapeo de Clics")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_seleccion = ttk.Frame(self.notebook)
        self.tab_mapeo = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_seleccion, text="Selección de Programa")
        self.notebook.add(self.tab_mapeo, text="Mapeo de Clics")

        self.crear_tab_seleccion()
        self.crear_tab_mapeo()

        self.selected_process = None
        self.mapping_active = False
        self.clicks = []

    def crear_tab_seleccion(self):
        self.processes_listbox = tk.Listbox(self.tab_seleccion, width=50)
        self.processes_listbox.pack(pady=10)

        self.btn_actualizar = tk.Button(self.tab_seleccion, text="Actualizar Lista", command=self.actualizar_lista_procesos)
        self.btn_actualizar.pack()

        self.btn_seleccionar = tk.Button(self.tab_seleccion, text="Seleccionar", command=self.seleccionar_proceso)
        self.btn_seleccionar.pack()
    
        self.actualizar_lista_procesos()  # Llenar la lista al inicio

    def crear_tab_mapeo(self):
        self.btn_iniciar = tk.Button(self.tab_mapeo, text="Iniciar Mapeo", command=self.iniciar_mapeo)
        self.btn_iniciar.pack(pady=10)
    
        self.btn_detener = tk.Button(self.tab_mapeo, text="Detener Mapeo", command=self.detener_mapeo)
        self.btn_detener.pack()
    
        self.btn_guardar = tk.Button(self.tab_mapeo, text="Guardar", command=self.guardar_clics)
        self.btn_guardar.pack()

    def actualizar_lista_procesos(self):
        self.processes_listbox.delete(0, tk.END)
        self.processes = {}
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['name'] and proc.info.get('exe'):
                    self.processes[proc.info['pid']] = {'name': proc.info['name'], 'exe': proc.info['exe']}
                    self.processes_listbox.insert(tk.END, f"{proc.info['pid']} - {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def seleccionar_proceso(self):
        selection = self.processes_listbox.curselection()
        if seleccion:
            process_info = self.processes_listbox.get(selection[0])
            pid = int(process_info.split(" - ")[0])
            self.selected_process = self.processes[pid]
            print(f"Programa seleccionado: {self.selected_process['name']} (PID: {pid})")

    def iniciar_mapeo(self):
        if self.selected_process:
            self.mapping_active = True
            self.clicks = []
            print(f"Iniciando mapeo de clics en: {self.selected_process['name']}")
            self.monitorear_clics()
        else:
            print("Selecciona un programa primero.")

    def monitorear_clics(self):
        while self.mapping_active:
            if pyautogui.is_pressed("mouse1"):  # Clic izquierdo
                x, y = pyautogui.position()
                self.clicks.append((x, y))
                print(f"Clic detectado en: ({x}, {y})")
                time.sleep(0.1)  # Pequeña pausa para evitar múltiples detecciones del mismo clic
            time.sleep(0.01)  # Reducir el uso de CPU

    def detener_mapeo(self):
        self.mapping_active = False
        print("Mapeo detenido.")

    def guardar_clics(self):
        if self.clicks and self.selected_process:
            filename = f"clics_{self.selected_process['name'].replace('.exe', '')}.json"
            with open(filename, "w") as f:
                json.dump(self.clicks, f)
            print(f"Clics guardados en {filename}")
        else:
            print("No hay clics para guardar.")
root = tk.Tk()
app = App(root)
root.mainloop()