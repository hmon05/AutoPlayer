import threading
import time
import win32api
import win32con

def iniciar_mapeo_ventana(self):
    if self.selected_window:
        self.mapping_active = True
        print(f"Iniciando mapeo de clics en la ventana: {self.selected_window}")
        self.stop_thread = False
        self.thread = threading.Thread(target=lambda: monitorear_clics_ventana(self))
        self.thread.start()
    else:
        print("Selecciona una ventana primero.")

def detener_mapeo_ventana(self):
    self.mapping_active = False
    self.stop_thread = True
    if hasattr(self, 'thread') and self.thread.is_alive():
        self.thread.join()
    print("Mapeo detenido.")

def monitorear_clics_ventana(app_instance):
    while not app_instance.stop_thread:
        if not app_instance.mapping_active:
            break
        if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0:
            x, y = win32api.GetCursorPos()
            app_instance.registrar_clic(x, y)
        time.sleep(0.1)