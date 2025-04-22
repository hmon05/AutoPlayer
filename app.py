import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os, json, sys, re , win32api, win32con, threading, time
from modules.threads import Mov_Personaje
import pygetwindow as gw
from PIL import Image, ImageTk
from modules.window_manager import WindowManager 

ancho, alto = 400 , 700

class App:
    def __init__(self, master):
        self.master = master
        master.title("BOT")
        master.iconbitmap(os.path.abspath("icons/dof.ico"))
        
        ancho_pantalla = root.winfo_screenwidth()
        alto_pantalla = root.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        master.geometry(f"{ancho}x{alto}+{x}+{y}")        
        
        self.bar_menu()

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.tab_seleccion = ttk.Frame(self.notebook)
        self.tab_mapeo = ttk.Frame(self.notebook)
        
        self.selecction_image = Image.open(os.path.abspath("icons/dof.png"))
        resized_selecctionImage = self.selecction_image.resize((17, 17)) 
        self.selecction_image = ImageTk.PhotoImage(resized_selecctionImage)
        self.notebook.add(self.tab_seleccion, text="Selección de Programa", image=self.selecction_image , compound=tk.LEFT)

        self.mapeo_image = Image.open(os.path.abspath("icons/map.png"))
        resized_mapeoImage = self.mapeo_image.resize((17, 17)) 
        self.mapeo_image = ImageTk.PhotoImage(resized_mapeoImage)
        self.notebook.add(self.tab_mapeo, text="Mapeo de Clics", image=self.mapeo_image , compound=tk.LEFT)
        self.notebook.tab(self.tab_mapeo, state="disabled")
        self.icono_minimapa = Image.open(os.path.abspath("icons/map.png"))
        self.icono_minimapa = ImageTk.PhotoImage(self.icono_minimapa.resize((17,17)))
        self.icono_log = Image.open(os.path.abspath("icons/dof.png"))
        self.icono_log = ImageTk.PhotoImage(self.icono_log.resize((17,17)))
        ##########Seleccionar de ventana y/o personaje##########
        self.imagenes_razas = {
            "Feca": os.path.abspath("imgs/anu.png"),
            "Osamodas": os.path.abspath("imgs/osa.png"),
            "Anutrof": os.path.abspath("imgs/anu.png"),
            "Sram": os.path.abspath("imgs/sram.png"),
            "Xelor": os.path.abspath("imgs/xelor.png"),
            "Zurcarák": os.path.abspath("imgs/zurk.png"),
            "Aniripsa": os.path.abspath("imgs/eni.png"),
            "Yopuka": os.path.abspath("imgs/ypk.png"),
            "Ocra": os.path.abspath("imgs/ocra.png"),
            "Sadida": os.path.abspath("imgs/sadi.png"),
            "Sacrógrito": os.path.abspath("imgs/sacro.png"),
            "Pandawa": os.path.abspath("imgs/panda.png"),
            "tymador": os.path.abspath("imgs/tyma.png"),
            "Zobal": os.path.abspath("imgs/zobal.png"),
            "Steamer": os.path.abspath("imgs/steam.png"),
            "Selotrop": os.path.abspath("imgs/selo.png"),
            "Hipermago": os.path.abspath("imgs/hiper.png"),
            "Uginak": os.path.abspath("imgs/ugi.png"),
            "Forjalanza": os.path.abspath("imgs/forja.png"),
        }

        ##########Tab Mapeo###########
        self.canvas = tk.Canvas(self.tab_mapeo, bg="white", width=380, height=380)
        
        self.crear_tab_mapeo()  # Llama a crear_tab_mapeo aquí
    
        self.selected_window = None
        self.mapping_active = False
        self.clicks = []
    
        self.window_manager = WindowManager()  # Crea una instancia de WindowManager
        self.labelSelecction = tk.Label(self.tab_seleccion, text="Seleccione la ventana del programa de la lista:", font = ('Comfortaa', 10))
        self.labelSelecction.pack(pady = (20,10))
        
        self.combobox_ventanas = ttk.Combobox(self.tab_seleccion, width=34, font=('Comfortaa', 10), state="readonly", justify="center")
        self.combobox_ventanas.pack(pady=10)
        self.cargar_ventanas()
        self.combobox_ventanas.bind("<<ComboboxSelected>>", self.mostrar_ImRazas)

        # Etiqueta para mostrar la imagen
        self.labe_raza = tk.Label(self.tab_seleccion, width = 290, height = 320)
        self.labe_raza.pack(pady = (0, 10))
        
        self.btn_seleccionar_ventana = tk.Button(self.tab_seleccion, text="Seleccionar Ventana",font = ('Comfortaa', 10), command=self.seleccionar_ventana)
        self.btn_seleccionar_ventana.pack(pady=5)

    def cargar_ventanas(self):
        self.window_manager.cargar_ventanas(self.combobox_ventanas)

    def mostrar_ImRazas(self, event=None):        
        # Crear un diccionario con claves en minúsculas para evitar errores de coincidencia
        pj_seleccionada = self.combobox_ventanas.get()
        partes = pj_seleccionada.split(" - ")
        if len(partes) >= 3:
            raza_extraida = partes[-3]  # Convertimos a minúsculas para comparación
        else:
            raza_extraida = ""
        
        if raza_extraida in self.imagenes_razas:
            try:
                # Cargar la imagen asociada a la ruta
                imagen = Image.open(self.imagenes_razas[raza_extraida])                
                imagen = imagen.resize((285, 315), Image.LANCZOS)  
                img_tk = ImageTk.PhotoImage(imagen)   
                self.labe_raza.config(image = img_tk) 
                self.labe_raza.image = img_tk          
            except Exception as e:
                pass
        else:
            # Si la raza no tiene imagen asociada, limpiar la imagen en la etiqueta
            self.labe_raza.config(image = "")
            self.labe_raza.image = None


    

    def crear_tab_mapeo(self):
        self.tab_mapeo.columnconfigure(0, weight=1)
        self.tab_mapeo.columnconfigure(1, weight=1)
        self.tab_mapeo.columnconfigure(2, weight=1)

        self.btn_iniciar = tk.Button(self.tab_mapeo, text="Iniciar Mapeo", command=self.iniciar_mapeo_ventana)
        self.btn_iniciar.grid(row=0, column=0, padx=35, pady=20, sticky="w")

        self.btn_detener = tk.Button(self.tab_mapeo, text="Detener Mapeo", command=self.detener_mapeo_ventana)
        self.btn_detener.grid(row=0, column=1, pady=20, sticky="w")
        
        self.btn_guardar = tk.Button(self.tab_mapeo, text="Guardar Clics", command=self.guardar_clics_ventana)
        self.btn_guardar.grid(row=0, column=2, padx=30, pady=20, sticky="w")

        # Frame para el nombre del archivo
        self.frame_nombre_archivo = tk.Frame(self.tab_mapeo, bg="lightgrey", bd=1)
        self.frame_nombre_archivo.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        self.label_nombre_archivo = tk.Label(self.frame_nombre_archivo, text="Nombre:", bg="lightgrey")
        self.label_nombre_archivo.pack(side=tk.LEFT, padx=5)
        
        self.entry_nombre_archivo = tk.Entry(self.frame_nombre_archivo, width=30)
        self.entry_nombre_archivo.pack(side=tk.LEFT)

        # Frame para el Canvas
        self.frame_canvas = tk.Frame(self.tab_mapeo, bg="lightgrey", bd=2, relief=tk.SOLID)  # Simula el borde general
        self.frame_canvas.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self.frame_canvas, width=382, height=382, bg="white", highlightthickness=0)  # Canvas dentro
        self.canvas.pack(padx=5, pady=5) # Añade un padding para separar del borde simulado
        self.minimap_image = Image.open(os.path.abspath("icons/radar.ico"))
        resized_minimapImage = self.minimap_image.resize((17, 17)) 
        self.minimap_image = ImageTk.PhotoImage(resized_minimapImage)
        self.label_canvas = tk.Label(self.frame_canvas,text="Minimapa", image=self.minimap_image, compound=tk.LEFT,bg="lightgrey")
        self.label_canvas.place(relx=0, rely=0, x=0, y=0)  # Superpone en la esquina superior izquierda

        #Frame edicion de clics
        self.frame_edicion = tk.Frame(self.tab_mapeo, bg="lightgrey", bd=2, relief=tk.SOLID, width=150)
        self.frame_edicion.grid(row=2, column=2, padx=5, pady=5)
        
        self.btn_agregar = tk.Button(self.frame_edicion, text="Agregar un recurso")
        self.btn_agregar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.btn_borrar = tk.Button(self.frame_edicion, text="Borrar")
        self.btn_borrar.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.btn_subir = tk.Button(self.frame_edicion, text="↑")
        self.btn_subir.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.btn_bajar = tk.Button(self.frame_edicion, text="↓")
        self.btn_bajar.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.btn_borrar_todo = tk.Button(self.frame_edicion, text="Borrar todo")
        self.btn_borrar_todo.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        self.btn_guardar_editado = tk.Button(self.frame_edicion, text="Guardar")
        self.btn_guardar_editado.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        #frame de visualizacion de los clics
        self.label_list_clics = tk.Label(self.tab_mapeo, text="Clics:", image=self.log_image, compound=tk.LEFT, bg="lightgrey")
        self.label_list_clics.grid(row=3, column=0, padx=5, pady=(10, 0))
        self.text_datos = tk.Text(self.tab_mapeo, height=10, width=45, highlightthickness=0) #Textbox dentro del Frame
        self.text_datos.grid(row=4, column=0, columnspan=3, padx=10, pady=15) #Empaquetar el Textbox dentro del Frame
        
        
        # Label superpuesto para el Textbox
        self.label_text = tk.Label(self.tab_mapeo,text="Log",)
        self.log_image = Image.open(os.path.abspath("icons/log.png"))
        resized_logImage = self.log_image.resize((15, 15)) 
        self.log_image = ImageTk.PhotoImage(resized_logImage)
        # self.label_text.image = self.icono_log
        self.label_text.place(relx=0, rely=0, x=0, y=0)
        
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
            self.notebook.tab(self.tab_mapeo, state = "normal")
            self.notebook.tab(self.tab_seleccion, state="disabled")
            self.notebook.select(self.tab_mapeo)  # Cambia a la pestaña de mapeo
            self.inicializar_mapeo()

            # Guardar las dimensiones de la ventana mapeada y de la region
            self.window_width = self.selected_window.width
            self.window_height = self.selected_window.height
            self.window_left = self.selected_window.left 
            self.window_top = self.selected_window.top

            self.region_left = 370
            self.region_top = 40
            self.region_width = 1560 - self.region_left
            self.region_height = 890 - self.region_top
    
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
            # Obtener la ruta al directorio actual del script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Definir la ruta predeterminada a la carpeta "recursos"
            default_dir = os.path.join(current_dir, "recursos")
            # Solicitar al usuario que elija el nombre del archivo
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialdir=default_dir)

            if not file_path :
                print("Guardado cancelado por el usuario.")
                return  # No guardar nada si el usuario cancela
            
            self.text_datos.delete("1.0", tk.END)  # Borra el contenido del Textbox
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
    
    ##########Funciones para la Barra de Menu##########
    def bar_menu(self):
        barr_menu = tk.Menu(self.master)
        self.master.config(menu = barr_menu)

        menu_inicio = tk.Menu(barr_menu, tearoff = 0)
        barr_menu.add_cascade(label = 'Inicio', menu = menu_inicio)        
        menu_inicio.add_command(label = 'Reiniciar', font = ('Comfortaa', 9) ,command = self.volver_inicio)
        menu_inicio.add_command(label = 'Salir',font = ('Comfortaa', 9), command = self.destroy)

        barr_menu.add_cascade(label = 'Mover personaje', command = self.moveMap) 
    
    def volver_inicio(self):
        self.text_datos.delete("1.0", tk.END)  # Borra el contenido del Textbox
        self.notebook.select(0)  # Seleccionar la primera pestaña (Ventana de Personaje)
        # Limpiar el Combobox y recargarlo
        self.combobox_ventanas.set("")  # Limpia la selección
        self.cargar_ventanas()  # Recarga las opciones del combobox
        # Limpiar el label de imagen
        self.labe_raza.config(image="")
        self.labe_raza.image = None
        # Bloquear las otras pestañas nuevamente
        self.notebook.tab(0, state = "normal")  # Desbloquear "Ventana de Personaje"
        self.notebook.tab(1, state = "disabled")  # Bloquea "Mapa inicial y Ruta"

    def destroy(self):
        """Restaurar stdout al cerrar la ventana."""
        self.detener_mapeo_ventana()
        sys.stdout = sys.__stdout__
        self.master.destroy()

    def moveMap(self):
        widthWindow, heightWindow = 480, 265
        if hasattr(self, 'WindowMap') and self.WindowMap.winfo_exists():
            self.WindowMap.lift()
            return
        # Crear ventana principal
        self.WindowMap = tk.Toplevel(self.master)
        self.WindowMap.title("Lleva el personaje a la posición deseada")
        self.WindowMap.iconbitmap(os.path.abspath("icons/dof.ico"))
        ancho_pantalla = root.winfo_screenwidth()
        alto_pantalla = root.winfo_screenheight()
        x = (ancho_pantalla // 2) - (widthWindow // 2)
        y = (alto_pantalla // 2) - (heightWindow // 2)
        self.WindowMap.geometry(f"{widthWindow}x{heightWindow}+{x}+{y}") 

        # self.WindowMap.mainloop()

        tk.Label(self.WindowMap, text="Ingrese la posición inicial (formato: X, Y):",font = ('Comfortaa', 10)).pack(pady=5)
        self.Entry_coordStart = tk.Entry(self.WindowMap, validate = "key", validatecommand=(self.validacion, "%P"),font = ('Comfortaa', 10))
        self.Entry_coordStart.pack(pady=5)
        

        tk.Label(self.WindowMap, text="Ingrese la posición destino (formato: X, Y):",font = ('Comfortaa', 10)).pack(pady=5)
        self.Entry_coordEnd = tk.Entry(self.WindowMap, validate = "key", validatecommand=(self.validacion, "%P"),font = ('Comfortaa', 10))
        self.Entry_coordEnd.pack(pady=5)

        # Etiqueta para solicitar el nombre de la ventana
        self.label_programa = tk.Label(self.WindowMap, text="Seleccione la ventana del programa de la lista:", font=('Comfortaa', 10))
        self.label_programa.pack(pady=5)
        
        # Combobox para las ventanas disponibles
        self.combobox_WindowProgram = ttk.Combobox(self.WindowMap, width=34, font=('Comfortaa', 10))#state="readonly"
        self.combobox_WindowProgram.pack(pady=5)
        self.cargar_WindowProgram()
        
        # Botón para confirmar
        self.BT_confWindowMap = tk.Button(self.WindowMap, text="Confirmar", font=('Comfortaa', 10), command= self.MovPer)
        self.BT_confWindowMap .pack(pady = 10)
    
    def validacion(texto):
        if texto == "":
            return True
        patron = r"^-?\d+(\.\d+)?,\s?-?\d+(\.\d+)?$"
        return bool(re.match(patron, texto))
    
    def cargar_WindowProgram(self):
        # Obtener las ventanas abiertas y cargarlas en el Listbox
        self.WindowProgram = [WindowProgram for WindowProgram in gw.getAllTitles() if WindowProgram.strip()]  # Evitar ventanas vacías
        self.combobox_WindowProgram['values'] = self.WindowProgram
    
    def MovPer(self):
        self.coordStart = list(map(int, self.Entry_coordStart.get().split(',')))        
        self.coordEnd = list(map(int, self.Entry_coordEnd.get().split(',')))        
        self.GetProgramWin = self.combobox_WindowProgram.get()        
        self.WindowMap.destroy()        
        thread = threading.Thread(target=Mov_Personaje, args=(self.coordStart, self.coordEnd, self.GetProgramWin))
        thread.daemon = True  # Para que el hilo se cierre si la app se cierra
        thread.start()
        print(f"{Mov_Personaje}")
        print(f"Personaje en {self.coordEnd}")
    
    def iniciar_mapeo_ventana(self):
        if self.selected_window:
            self.mapping_active = True
            print(f"Iniciando mapeo de clics en la ventana: {self.selected_window}")
            self.stop_thread = False
            self.thread = threading.Thread(target=self.monitorear_clics_ventana)
            self.thread.start()
        else:
            print("Selecciona una ventana primero.")

    def detener_mapeo_ventana(self):
        self.mapping_active = False
        self.stop_thread = True
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join()
        print("Mapeo detenido.")

    def monitorear_clics_ventana(self):
        while not self.stop_thread:
            if not self.mapping_active:
                break
            if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0:
                x, y = win32api.GetCursorPos()
                self.registrar_clic(x, y)
            time.sleep(0.1)

root = tk.Tk()
app = App(root)
root.mainloop()
