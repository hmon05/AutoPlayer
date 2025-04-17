import pygetwindow as gw

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