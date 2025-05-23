import pygetwindow as gw
from pywinauto import Desktop

class WindowManager:
    def cargar_ventanas(self, combobox_ventanas):
        self.ventanas = [ventana for ventana in gw.getAllTitles() if ventana.strip()]
        combobox_ventanas['values'] = self.ventanas

    def select_window(self, combobox_ventanas):
        window_name = combobox_ventanas.get()
        try:
            selected_window = gw.getWindowsWithTitle(window_name)[0]
            print(f"Ventana seleccionada: {selected_window.title}")
            return selected_window
        except IndexError:
            print(f"Ventana '{window_name}' no encontrada.")
            return None
        
    def centrar_ventana(self, ancho, alto):
        """Centrar la ventana en la pantalla."""
        # Obtener el tamaño de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        # Calcular la posición para centrar
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)

        # Establecer la geometría de la ventana
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def Ventana_Personaje(self, search_title):
        windows = Desktop(backend="uia").windows()

        # Obtener las ventanas abiertas
        windows = gw.getWindowsWithTitle(search_title) 

        # Buscar una ventana que contenga el título buscado
        if windows:
            win = windows[0]  # Tomar la primera coincidencia
            win.activate()  # Traer la ventana al frente        
            return win.title  # Retorna el nombre completo de la ventana encontrada
        else:
            print(f"No se encontró ninguna ventana que contenga: '{search_title}'")
    def validacion(texto):
        if texto == "":
            return True
        patron = r"^-?\d+(\.\d+)?,\s?-?\d+(\.\d+)?$"
        return bool(re.match(patron, texto))