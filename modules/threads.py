import heapq, pyautogui
import time
 
# Diccionario de restricciones de movimiento
restricciones_movimiento = {
    (2, -10): ["arriba"],
    (2, -17): ["derecha"],
    (2, -19): ["derecha"],
    (3, -16): ["arriba"],
    (3, -17): ["izquierda", "abajo"],
    (3, -19): ["izquierda", "arriba"],
    (3, -20): ["abajo"],
    (3, -23): ["abajo", "arriba", "izquierda", "derecha"],
    (4, -16): ["arriba"],
    (4, -17): ["abajo"],
    (5, -19): ["arriba"],
    (5, -20): ["abajo"],
    (6, -16): ["arriba"],   
    (6, -17): ["derecha", "abajo"],
    (6, -19): ["derecha", "arriba"],     
    (6, -20): ["abajo"],
    (7, -17): ["izquierda"],
    (7, -19): ["izquierda"]    
}

# Movimientos posibles en el mapa con la convención corregida
movimientos = {
    "arriba": (0, -1),
    "abajo": (0, 1),
    "izquierda": (-1, 0),
    "derecha": (1, 0)
}

# Posiciones del mouse para mover el mapa
acciones_mouse = {
    "arriba": (927, 34),
    "abajo": (705, 891),
    "izquierda": (142, 603),
    "derecha": (1570, 905)
}


def Mov_Personaje(Pos_actual, Pos_destino, VentanaPersonaje):
    destino_x, destino_y = Pos_destino[0], Pos_destino[1]    
    """Simula el movimiento del personaje desde la posición actual hasta el destino usando A* y `pyautogui`."""
    # global mapcoords , posicion_actual
    # mapcoords = posicion_actual
    print(f"Moviendo desde {Pos_actual} hasta ({destino_x}, {destino_y})")

    # Calcular la ruta utilizando A* para evitar restricciones
    rutaRecorrer = a_estrella(Pos_actual, (destino_x, destino_y))

    if not rutaRecorrer:
        print("No se encontró una ruta válida.")
        posicion_actual = ruta_seleccionada [0][0], ruta_seleccionada[0][1]
        return posicion_actual

    print("Ruta a seguir:", rutaRecorrer)

    for direccion in rutaRecorrer:
        # Mover el mouse a la posición correcta antes de hacer clic
        x, y = acciones_mouse[direccion]
        pyautogui.moveTo(x, y, 0.2)

        # Pequeña pausa para asegurar movimiento correcto
        wait_for_map_load()

        # Simulación de actualización de coordenadas
        Pos_actual = (Pos_actual[0] + movimientos[direccion][0], Pos_actual[1] + movimientos[direccion][1])
        print(f"Se movió {direccion}: {Pos_actual}")
    posicion_actual = Pos_actual 
    return posicion_actual


def a_estrella(inicio, destino):
    """Encuentra la ruta más corta evitando restricciones con el algoritmo A*."""
    open_set = []  # Cola de prioridad para explorar caminos
    heapq.heappush(open_set, (0, inicio, []))  # (costo estimado, posición actual, camino recorrido)
    visitados = set()

    while open_set:
        _, (x, y), camino = heapq.heappop(open_set)

        if (x, y) == destino:
            return camino  # Ruta encontrada

        visitados.add((x, y))

        # Obtener movimientos válidos desde la posición actual respetando restricciones
        movimientos_permitidos = GetMov_permitidos((x, y))

        # Priorizar movimientos en el orden correcto: primero arriba, luego izquierda, luego bajar
        prioridad = ["arriba", "izquierda", "abajo", "derecha"]
        movimientos_ordenados = sorted(
            movimientos_permitidos.items(),
            key=lambda d: prioridad.index(d[0]) if d[0] in prioridad else len(prioridad)
        )

        for direccion, (dx, dy) in movimientos_ordenados:
            nueva_pos = (x + dx, y + dy)

            # Validar si la nueva posición respeta restricciones y no ha sido visitada
            if nueva_pos not in visitados and direccion not in restricciones_movimiento.get((x, y), []):
                if nueva_pos not in restricciones_movimiento or direccion not in restricciones_movimiento[nueva_pos]:
                    costo_estimado = abs(nueva_pos[0] - destino[0]) + abs(nueva_pos[1] - destino[1])
                    heapq.heappush(open_set, (costo_estimado, nueva_pos, camino + [direccion]))

    return None  # Si no encuentra ruta


def GetMov_permitidos(actual):
    x, y = actual
    movimientos_permitidos = {}

    for direccion, (dx, dy) in movimientos.items():
        nueva_pos = (x + dx, y + dy)
        
        # Si la posición actual tiene una restricción en esa dirección, ignorarla
        if actual in restricciones_movimiento and direccion in restricciones_movimiento[actual]:
            continue
        
        # Si la nueva posición tiene restricciones en la dirección opuesta, evitarla
        if nueva_pos in restricciones_movimiento:
            direccion_opuesta = {
                "arriba": "abajo",
                "abajo": "arriba",
                "izquierda": "derecha",
                "derecha": "izquierda"
            }
            if direccion_opuesta[direccion] in restricciones_movimiento[nueva_pos]:
                continue

        movimientos_permitidos[direccion] = (dx, dy)
    
    return movimientos_permitidos


def wait_for_map_load():
    region = (375, 40, 1168, 835)
    timeout = 10
    start_time = time.time()
    detected_black_screen = False  # Variable para saber si detectamos pantalla negra

    # print("Esperando que aparezca la pantalla negra...")

    # Esperar hasta que la pantalla se vuelva negra
    while time.time() - start_time < timeout:
        if is_screen_black(region):
            # print("Pantalla negra detectada. Esperando carga del mapa...")
            detected_black_screen = True
            break
        time.sleep(0.2)

    # Si nunca detectamos pantalla negra, significa que el personaje sigue en el mismo mapa
    if not detected_black_screen:
        # print("Personaje en el mismo mapa. No se detectó pantalla negra.")
        return

    # Esperar a que la pantalla vuelva a mostrar imagen (mapa cargado)
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not is_screen_black(region):
            # print("Mapa cargado. Continuando con el siguiente movimiento.")
            return
        time.sleep(0.2)


def is_screen_black(region):
    threshold = 10
    screenshot = pyautogui.screenshot(region=region)
    screenshot_gray = screenshot.convert("L")  # Convertir a escala de grises
    pixels = list(screenshot_gray.getdata())  # Obtener los valores de los píxeles

    # Calcular el promedio de los valores de los píxeles (0 = negro, 255 = blanco)
    avg_brightness = sum(pixels) / len(pixels)

    return avg_brightness < threshold  # True si la pantalla es negra