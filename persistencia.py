
import csv
import os

# ==========================================================
# MODULO DE PERSISTENCIA - INVENTARIO DROPSHIPPING
# Este modulo se encarga de crear, leer y guardar el CSV.
# ==========================================================

# Nombre del archivo donde se almacenan los productos.
# Se utiliza una ruta relativa para que funcione en Colab.
ARCHIVO = "inventario.csv"

# Columnas del archivo CSV.
CAMPOS = ["id", "nombre", "categoria", "cantidad", "precio"]


# ==========================================================
# FUNCION PARA CREAR EL ARCHIVO CSV
# ==========================================================
def crear_archivo():
    """Crea el archivo CSV si todavia no existe."""

    if os.path.exists(ARCHIVO):
        return True

    try:
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(CAMPOS)

        return True

    except OSError as error:
        print(f"Error al crear el archivo: {error}")
        return False


# ==========================================================
# FUNCION PARA LEER LOS PRODUCTOS
# ==========================================================
def leer_productos():
    """Lee los productos del CSV y los devuelve como lista."""

    if not crear_archivo():
        return None

    productos = []

    try:
        with open(ARCHIVO, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            # Verifica que el archivo tenga las columnas necesarias.
            if (
                lector.fieldnames is None
                or not all(campo in lector.fieldnames for campo in CAMPOS)
            ):
                print("Error: los encabezados del CSV no son validos.")
                return None

            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    producto = {
                        "id": int(fila["id"]),
                        "nombre": fila["nombre"].strip(),
                        "categoria": fila["categoria"].strip(),
                        "cantidad": int(fila["cantidad"]),
                        "precio": float(fila["precio"])
                    }

                    # Valida los datos almacenados.
                    if (
                        producto["id"] <= 0
                        or not producto["nombre"]
                        or not producto["categoria"]
                        or producto["cantidad"] < 0
                        or producto["precio"] <= 0
                    ):
                        print(f"Advertencia: datos invalidos en la fila {numero_fila}.")
                        continue

                    productos.append(producto)

                except (ValueError, TypeError, KeyError, AttributeError):
                    # Omite filas dañadas sin detener todo el programa.
                    print(f"Advertencia: fila {numero_fila} omitida por datos incorrectos.")

    except (OSError, csv.Error, UnicodeError) as error:
        print(f"Error al leer el archivo CSV: {error}")
        return None

    return productos


# ==========================================================
# FUNCION PARA GUARDAR LOS PRODUCTOS
# ==========================================================
def guardar_productos(productos):
    """Guarda los productos en el archivo CSV."""

    try:
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)

            # Escribe los encabezados y los productos.
            escritor.writeheader()
            escritor.writerows(productos)

        return True

    except (OSError, csv.Error, TypeError, ValueError) as error:
        print(f"Error al guardar los productos: {error}")
        return False

