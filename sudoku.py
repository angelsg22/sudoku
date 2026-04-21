import random  # Para mezclar números y hacer tableros distintos cada vez
import copy    # Para hacer copias independientes de listas (importante en Python)

# Comprueba si podemos poner el número `num` en la posición (fila, col)
#   - El número no puede repetirse en la misma fila
#   - El número no puede repetirse en la misma columna
#   - El número no puede repetirse en el mismo cuadrado 3x3

def es_valido(tablero, fila, col, num):
    # --- Regla 1: el número no puede estar ya en la misma fila ---
    if num in tablero[fila]:
        return False

    # --- Regla 2: el número no puede estar ya en la misma columna ---
    # Recorremos todas las filas y miramos la misma columna
    for f in range(9):
        if tablero[f][col] == num:
            return False

    # --- Regla 3: el número no puede estar en el mismo cuadrado 3x3 ---
    # Calculamos en qué cuadrado 3x3 estamos
    inicio_fila = (fila // 3) * 3
    inicio_col  = (col  // 3) * 3

    for f in range(inicio_fila, inicio_fila + 3):
        for c in range(inicio_col, inicio_col + 3):
            if tablero[f][c] == num:
                return False

    return True


#   1. Encuentra una celda vacía (valor 0)
#   2. Prueba números del 1 al 9
#   3. Si el número es válido → ponlo y avanza a la siguiente celda
#   4. Si llegamos al final sin errores → ¡resuelto!
#   5. Si llegamos a un punto sin salida → "vuelve atrás" (backtrack)
#      y prueba el siguiente número en la celda anterior

# Parámetros:
#   tablero → matriz 9x9 (0 = vacío, 1-9 = números)

def resolver(tablero):
    # Buscamos la próxima celda vacía (valor 0)
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                # Encontramos una celda vacía → probamos números del 1 al 9
                for num in range(1, 10):
                    if es_valido(tablero, fila, col, num):
                        # El número es válido → lo colocamos
                        tablero[fila][col] = num

                        # Llamamos a resolver() de forma recursiva
                        # Si la recursión llega al final → ¡éxito!
                        if resolver(tablero):
                            return True

                        # Si la recursión fracasó → backtrack
                        # Borramos el número y probamos el siguiente
                        tablero[fila][col] = 0

                # Ningún número del 1 al 9 funcionó → camino sin salida
                return False

    # Si llegamos aquí sin encontrar celdas vacías → ¡tablero resuelto!
    return True


def generar_tablero_completo():
    # Empezamos con un tablero vacío (todo ceros)
    tablero = [[0] * 9 for _ in range(9)]

    # Función interna que aplica backtracking con números aleatorios
    def rellenar(tablero):
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] == 0:
                    # Mezclamos los números 1-9 para que el tablero sea único
                    numeros = list(range(1, 10))
                    random.shuffle(numeros)

                    for num in numeros:
                        if es_valido(tablero, fila, col, num):
                            tablero[fila][col] = num

                            if rellenar(tablero):
                                return True

                            tablero[fila][col] = 0

                    return False
        return True

    rellenar(tablero)
    return tablero



# Dificultades (celdas que se eliminan):
#   - "facil"  → 35 celdas eliminadas 
#   - "medio"  → 45 celdas eliminadas
#   - "dificil"→ 55 celdas eliminadas

# Parámetros:
#   dificultad → string: "facil", "medio" o "dificil"

# Devuelve: diccionario con:
#   "puzzle"    → tablero con ceros en las celdas vacías
#   "solucion"  → tablero completo (para validar y dar pistas)

def generar_puzzle(dificultad="medio"):
    # Primero generamos un tablero completamente resuelto
    solucion = generar_tablero_completo()

    # Hacemos una copia del tablero resuelto para convertirlo en puzzle
    # IMPORTANTE: copy.deepcopy hace una copia INDEPENDIENTE de la lista
    # (sin deepcopy, modificar puzzle también modificaría solucion)
    puzzle = copy.deepcopy(solucion)

    # Decidimos cuántas celdas eliminar según la dificultad
    celdas_a_eliminar = {
        "facil":   35,
        "medio":   45,
        "dificil": 55
    }.get(dificultad, 45)  # Si la dificultad no existe, usamos "medio"

    posiciones = [(f, c) for f in range(9) for c in range(9)]
    random.shuffle(posiciones)

    # Eliminamos las celdas
    eliminadas = 0
    for fila, col in posiciones:
        if eliminadas >= celdas_a_eliminar:
            break  # Ya eliminamos suficientes

        puzzle[fila][col] = 0
        eliminadas += 1

    return {
        "puzzle": puzzle,
        "solucion": solucion
    }



# MODO APUNTE


# ¿Qué es un candidato en Sudoku?
#   Es un número que PODRÍA ir en una celda concreta sin violar ninguna regla.
#   Por ejemplo, si en la fila 2, columna 4 ya no están el 1, el 3 ni el 7
#   (porque aparecen en la misma fila, columna o bloque), los candidatos
#   serían todos los números del 1 al 9 excepto esos tres.


def calcular_candidatos(tablero):
    candidatos = {}

    for fila in range(9):
        for col in range(9):
            # Solo calculamos candidatos para celdas vacías
            if tablero[fila][col] == 0:
                posibles = []

                # Probamos cada número del 1 al 9 con las reglas del Sudoku
                for num in range(1, 10):
                    if es_valido(tablero, fila, col, num):
                        posibles.append(num)

                # Solo añadimos la celda si tiene al menos un candidato
                if posibles:
                    clave = f"{fila}-{col}"
                    candidatos[clave] = posibles

    return candidatos

# Devuelve: diccionario con:
#   "correcto"  -> True/False: ¿está todo bien?
#   "errores"   -> lista de posiciones [fila, col] con errores
#   "completo"  -> True si no hay celdas vacías (el usuario terminó)

def validar_solucion(respuesta, solucion):
    errores = []
    hay_vacias = False

    for fila in range(9):
        for col in range(9):
            valor_usuario = respuesta[fila][col]
            valor_correcto = solucion[fila][col]

            if valor_usuario == 0:
                # Hay celdas sin rellenar
                hay_vacias = True
            elif valor_usuario != valor_correcto:
                # El usuario puso un número incorrecto
                errores.append([fila, col])

    return {
        "correcto": len(errores) == 0 and not hay_vacias,
        "errores": errores,
        "completo": not hay_vacias
    }

# Devuelve: diccionario con:
#   "fila", "col" → posición de la pista
#   "valor"       → número correcto en esa posición

def obtener_pista(respuesta, solucion):
    # Buscamos celdas que el usuario no ha rellenado correctamente
    celdas_disponibles = []

    for fila in range(9):
        for col in range(9):
            if respuesta[fila][col] != solucion[fila][col]:
                celdas_disponibles.append((fila, col))

    if not celdas_disponibles:
        # El tablero ya está resuelto correctamente
        return None

    # Elegimos una celda aleatoria de las disponibles
    fila, col = random.choice(celdas_disponibles)

    return {
        "fila": fila,
        "col": col,
        "valor": solucion[fila][col]
    }
