# =============================================================================
# sudoku.py — Lógica del juego de Sudoku
# =============================================================================
#
# Este archivo contiene TODA la lógica matemática del Sudoku:
#   1. Cómo verificar si un número puede ir en una celda
#   2. Cómo resolver un tablero usando backtracking
#   3. Cómo generar un tablero nuevo con celdas vacías
#
# El frontend (HTML/JS) no sabe nada de esto. Solo recibe los resultados.
# =============================================================================

import random  # Para mezclar números y hacer tableros distintos cada vez
import copy    # Para hacer copias independientes de listas (importante en Python)


# =============================================================================
# FUNCIÓN: es_valido
# =============================================================================
# Comprueba si podemos poner el número `num` en la posición (fila, col)
# sin romper las reglas del Sudoku:
#   - El número no puede repetirse en la misma fila
#   - El número no puede repetirse en la misma columna
#   - El número no puede repetirse en el mismo cuadrado 3x3
#
# Parámetros:
#   tablero  → matriz 9x9 con números (0 = celda vacía)
#   fila     → índice de fila (0 a 8)
#   col      → índice de columna (0 a 8)
#   num      → número que queremos colocar (1 a 9)
#
# Devuelve: True si es válido, False si no lo es
# =============================================================================
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
    # Ejemplo: fila=5, col=7 → inicio_fila=3, inicio_col=6
    inicio_fila = (fila // 3) * 3
    inicio_col  = (col  // 3) * 3

    for f in range(inicio_fila, inicio_fila + 3):
        for c in range(inicio_col, inicio_col + 3):
            if tablero[f][c] == num:
                return False

    # Si pasó todas las reglas, el número es válido
    return True


# =============================================================================
# ALGORITMO: Backtracking (vuelta atrás)
# =============================================================================
# Backtracking es una técnica para resolver problemas de "prueba y error":
#
#   1. Encuentra una celda vacía (valor 0)
#   2. Prueba números del 1 al 9
#   3. Si el número es válido → ponlo y avanza a la siguiente celda
#   4. Si llegamos al final sin errores → ¡resuelto!
#   5. Si llegamos a un punto sin salida → "vuelve atrás" (backtrack)
#      y prueba el siguiente número en la celda anterior
#
# Es como resolver un laberinto: avanzas hasta que te bloqueas,
# y entonces retrocedes para tomar otro camino.
# =============================================================================


# =============================================================================
# FUNCIÓN: resolver
# =============================================================================
# Resuelve un tablero de Sudoku usando backtracking.
# Modifica el tablero directamente (en Python, las listas se pasan por referencia).
#
# Parámetros:
#   tablero → matriz 9x9 (0 = vacío, 1-9 = números)
#
# Devuelve: True si encontró solución, False si el tablero no tiene solución
# =============================================================================
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


# =============================================================================
# FUNCIÓN: generar_tablero_completo
# =============================================================================
# Genera un tablero de Sudoku completamente resuelto y válido.
# Usa backtracking pero con los números en orden ALEATORIO para que
# cada partida sea diferente.
#
# Devuelve: matriz 9x9 completamente rellena y válida
# =============================================================================
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


# =============================================================================
# FUNCIÓN: generar_puzzle
# =============================================================================
# Toma un tablero completo y elimina celdas para crear el puzzle jugable.
# Cuantas más celdas eliminamos, más difícil es el puzzle.
#
# Dificultades (celdas que se eliminan):
#   - "facil"  → 35 celdas eliminadas (quedan 46 con número)
#   - "medio"  → 45 celdas eliminadas (quedan 36 con número)
#   - "dificil"→ 55 celdas eliminadas (quedan 26 con número)
#
# Parámetros:
#   dificultad → string: "facil", "medio" o "dificil"
#
# Devuelve: diccionario con:
#   "puzzle"    → tablero con ceros en las celdas vacías
#   "solucion"  → tablero completo (para validar y dar pistas)
# =============================================================================
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

    # Creamos una lista con todas las posiciones del tablero y la mezclamos
    # Así eliminamos celdas en orden aleatorio
    posiciones = [(f, c) for f in range(9) for c in range(9)]
    random.shuffle(posiciones)

    # Eliminamos las celdas poniendo un 0
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


# =============================================================================
# FUNCIÓN: calcular_candidatos
# =============================================================================
# Calcula los "candidatos" de cada celda vacía del tablero.
#
# ¿Qué es un candidato en Sudoku?
#   Es un número que PODRÍA ir en una celda concreta sin violar ninguna regla.
#   Por ejemplo, si en la fila 2, columna 4 ya no están el 1, el 3 ni el 7
#   (porque aparecen en la misma fila, columna o bloque), los candidatos
#   serían todos los números del 1 al 9 excepto esos tres.
#
# Parámetros:
#   tablero → matriz 9x9 (0 = celda vacía, 1-9 = número colocado)
#
# Devuelve: diccionario donde la clave es "fila-col" y el valor es
#           una lista de números candidatos para esa posición.
#   Ejemplo: { "2-4": [1, 3, 7], "5-0": [2, 6], ... }
#
# Solo incluye celdas que tienen al menos un candidato.
# =============================================================================
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


# =============================================================================
# FUNCIÓN: validar_solucion
# =============================================================================
# Comprueba si la respuesta del usuario es correcta.
# Compara celda por celda con la solución real.
#
# Parámetros:
#   respuesta → matriz 9x9 con los números del usuario (0 = celda vacía)
#   solucion  → matriz 9x9 con la solución correcta
#
# Devuelve: diccionario con:
#   "correcto"  → True/False: ¿está todo bien?
#   "errores"   → lista de posiciones [fila, col] con errores
#   "completo"  → True si no hay celdas vacías (el usuario terminó)
# =============================================================================
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


# =============================================================================
# FUNCIÓN: obtener_pista
# =============================================================================
# Devuelve UNA celda resuelta para ayudar al usuario.
# Elige aleatoriamente entre las celdas que el usuario no ha rellenado bien.
#
# Parámetros:
#   respuesta → matriz 9x9 con la respuesta actual del usuario
#   solucion  → matriz 9x9 con la solución correcta
#
# Devuelve: diccionario con:
#   "fila", "col" → posición de la pista
#   "valor"       → número correcto en esa posición
#   O None si el tablero ya está completo
# =============================================================================
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
