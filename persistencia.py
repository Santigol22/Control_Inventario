"""
==========================================================
MÓDULO DE PERSISTENCIA - INVENTARIO DROPSHIPPING
==========================================================
Este módulo se encarga únicamente de trabajar con el archivo
CSV: crearlo, leer los productos y guardarlos. Así se separa
el manejo de archivos de la lógica del menú y del CRUD.
"""

import csv
import os

# Nombre del archivo donde se guardan los productos
ARCHIVO = "inventario.csv"

# Columnas (encabezados) que tiene el archivo CSV
CAMPOS = ["id", "nombre", "categoria", "cantidad", "precio"]


# ----------------------------------------------------------
# FUNCIÓN PARA CREAR EL ARCHIVO CSV
# ----------------------------------------------------------
def crear_archivo():
    """Crea el archivo CSV con sus encabezados si todavía no existe.

    Devuelve True si el archivo existe o se creó bien, y False
    si ocurrió un error al intentar crearlo.
    """
    if os.path.exists(ARCHIVO):
        return True

    try:
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            # Encabezados del archivo
            escritor.writerow(CAMPOS)
        return True
    except OSError as error:
        # OSError cubre permisos denegados, disco lleno, ruta inválida, etc.
        print("Error: no se pudo crear el archivo de inventario.")
        print("Detalle:", error)
        return False


# ----------------------------------------------------------
# FUNCIÓN PARA LEER LOS PRODUCTOS
# ----------------------------------------------------------
def leer_productos():
    """Lee el archivo CSV y devuelve una lista de diccionarios.

    - Si el archivo no existe, lo crea y devuelve una lista vacía.
    - Si una fila tiene datos dañados, la omite y avisa al usuario.
    - Si no se puede leer el archivo, devuelve None para que el
      programa NO sobrescriba el inventario con una lista vacía.
    """
    productos = []

    try:
        with open(ARCHIVO, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            # Recorrido de los registros almacenados
            # (start=2 porque la línea 1 son los encabezados)
            for numero_linea, fila in enumerate(lector, start=2):
                try:
                    # Conversión de los textos del CSV a sus tipos reales
                    fila["id"] = int(fila["id"])
                    fila["cantidad"] = int(fila["cantidad"])
                    fila["precio"] = float(fila["precio"])
                    productos.append(fila)
                except (ValueError, TypeError, KeyError):
                    # La fila tiene valores vacíos o no numéricos
                    print(f"Advertencia: la línea {numero_linea} del archivo "
                          "tiene datos inválidos y fue omitida.")

    except FileNotFoundError:
        # Si alguien borró el archivo, se vuelve a crear vacío
        crear_archivo()
        return []
    except (OSError, csv.Error, UnicodeDecodeError) as error:
        print("Error: no se pudo leer el archivo de inventario.")
        print("Detalle:", error)
        return None

    return productos


# ----------------------------------------------------------
# FUNCIÓN PARA GUARDAR LOS PRODUCTOS
# ----------------------------------------------------------
def guardar_productos(productos):
    """Guarda la lista de productos en el archivo CSV.

    Devuelve True si se guardó correctamente y False si hubo
    un error de escritura.
    """
    try:
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(productos)
        return True
    except (OSError, csv.Error) as error:
        print("Error: no se pudieron guardar los cambios en el archivo.")
        print("Detalle:", error)
        return False
