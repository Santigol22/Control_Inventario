"""
==========================================================
SISTEMA DE SEGUIMIENTO DE INVENTARIO - DROPSHIPPING
==========================================================
Archivo principal del programa. Contiene el menú, las
validaciones de entrada, las operaciones CRUD, la búsqueda
y el conteo del inventario.

El manejo del archivo CSV se importa desde persistencia.py.
"""

# Importación de las funciones del módulo de persistencia
from persistencia import crear_archivo, leer_productos, guardar_productos

# Cantidad mínima a partir de la cual un producto necesita reabastecerse
LIMITE_REABASTECER = 5


# ----------------------------------------------------------
# FUNCIÓN PARA VALIDAR NÚMEROS ENTEROS
# ----------------------------------------------------------
def pedir_entero(mensaje):
    """Solicita un número entero no negativo y evita entradas incorrectas."""
    while True:
        try:
            numero = int(input(mensaje))
            if numero < 0:
                print("Error: el número no puede ser negativo.")
            else:
                return numero
        except ValueError:
            print("Error: debes ingresar un número entero.")


# ----------------------------------------------------------
# FUNCIÓN PARA VALIDAR PRECIOS
# ----------------------------------------------------------
def pedir_precio(mensaje):
    """Solicita un precio válido (numérico y mayor que cero)."""
    while True:
        try:
            # Se permite escribir el precio con coma decimal (ej: 25000,50)
            precio = float(input(mensaje).replace(",", "."))
            if precio <= 0:
                print("Error: el precio debe ser mayor que cero.")
            else:
                return precio
        except ValueError:
            print("Error: debes ingresar un valor numérico.")


# ----------------------------------------------------------
# FUNCIÓN PARA VALIDAR TEXTOS NO VACÍOS
# ----------------------------------------------------------
def pedir_texto(mensaje, campo):
    """Solicita un texto que no quede vacío (nombre o categoría)."""
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print(f"Error: {campo} no puede quedar vacío.")


# ==========================================================
# CRUD - CREATE
# ==========================================================
def crear_producto():
    """Registra un nuevo producto en el inventario."""
    productos = leer_productos()
    # Si hubo error de lectura no se continúa, para no perder datos
    if productos is None:
        return

    print("\n--- REGISTRAR PRODUCTO ---")

    # Generar un nuevo ID consecutivo
    if len(productos) == 0:
        nuevo_id = 1
    else:
        nuevo_id = max(producto["id"] for producto in productos) + 1

    # Validación del nombre y la categoría
    nombre = pedir_texto("Nombre del producto: ", "el nombre")
    categoria = pedir_texto("Categoría: ", "la categoría")

    cantidad = pedir_entero("Cantidad disponible: ")
    precio = pedir_precio("Precio del producto: ")

    # Diccionario que representa un producto
    producto = {
        "id": nuevo_id,
        "nombre": nombre,
        "categoria": categoria,
        "cantidad": cantidad,
        "precio": precio
    }

    # Inserción del nuevo producto en la lista y guardado en el CSV
    productos.append(producto)

    if guardar_productos(productos):
        print("\nProducto registrado correctamente.")
        print("ID asignado:", nuevo_id)
    else:
        print("El producto no pudo registrarse.")


# ==========================================================
# CRUD - READ
# ==========================================================
def leer_y_mostrar_productos():
    """Muestra todos los productos almacenados."""
    productos = leer_productos()
    if productos is None:
        return

    print("\n--- INVENTARIO ---")

    if len(productos) == 0:
        print("No hay productos registrados.")
        return

    # Recorrido de la lista para mostrar los productos
    for producto in productos:
        cantidad = producto["cantidad"]

        # Determinar el estado del inventario
        if cantidad <= LIMITE_REABASTECER:
            estado = "REABASTECER"
        else:
            estado = "Disponible"

        print("----------------------------------")
        print("ID:", producto["id"])
        print("Producto:", producto["nombre"])
        print("Categoría:", producto["categoria"])
        print("Cantidad:", cantidad)
        print("Precio: $", format(producto["precio"], ",.0f"))
        print("Estado:", estado)

    print("----------------------------------")


# ==========================================================
# FUNCIÓN DE BÚSQUEDA
# ==========================================================
def buscar_producto():
    """Busca productos cuyo nombre contenga el texto ingresado."""
    productos = leer_productos()
    if productos is None:
        return

    print("\n--- BUSCAR PRODUCTO ---")
    nombre_buscar = pedir_texto(
        "Ingrese el nombre del producto: ", "la búsqueda"
    ).lower()

    encontrados = []

    # Recorrido de la lista para realizar la búsqueda (sin distinguir mayúsculas)
    for producto in productos:
        if nombre_buscar in producto["nombre"].lower():
            encontrados.append(producto)

    if len(encontrados) == 0:
        print("No se encontró ningún producto.")
    else:
        print("\nProductos encontrados:")
        for producto in encontrados:
            print(
                producto["id"],
                "-",
                producto["nombre"],
                "- Cantidad:",
                producto["cantidad"]
            )


# ==========================================================
# FUNCIÓN PARA CONTAR PRODUCTOS
# ==========================================================
def contar_productos():
    """Cuenta los productos registrados y los que necesitan reabastecimiento."""
    productos = leer_productos()
    if productos is None:
        return

    print("\n--- CONTEO DEL INVENTARIO ---")
    print("Cantidad de productos registrados:", len(productos))

    # Contar productos que necesitan reabastecimiento
    necesitan_reabastecimiento = 0
    for producto in productos:
        if producto["cantidad"] <= LIMITE_REABASTECER:
            necesitan_reabastecimiento += 1

    print(
        "Productos que necesitan reabastecimiento:",
        necesitan_reabastecimiento
    )


# ==========================================================
# CRUD - UPDATE
# ==========================================================
def actualizar_producto():
    """Modifica la cantidad y, opcionalmente, el precio de un producto."""
    productos = leer_productos()
    if productos is None:
        return

    print("\n--- ACTUALIZAR PRODUCTO ---")
    id_buscar = pedir_entero("Ingrese el ID del producto: ")

    encontrado = False

    # Recorrido de la lista para encontrar el producto
    for producto in productos:
        if producto["id"] == id_buscar:
            encontrado = True
            print("\nProducto encontrado:", producto["nombre"])

            # Actualización de la cantidad
            producto["cantidad"] = pedir_entero("Nueva cantidad disponible: ")

            # Actualización opcional del precio
            cambiar_precio = input(
                "¿Desea actualizar el precio? (s/n): "
            ).strip().lower()

            if cambiar_precio == "s":
                producto["precio"] = pedir_precio("Nuevo precio: ")
            break

    if encontrado:
        if guardar_productos(productos):
            print("Producto actualizado correctamente.")
    else:
        print("No existe un producto con ese ID.")


# ==========================================================
# CRUD - DELETE
# ==========================================================
def eliminar_producto():
    """Elimina un producto del inventario después de confirmar."""
    productos = leer_productos()
    if productos is None:
        return

    print("\n--- ELIMINAR PRODUCTO ---")
    id_eliminar = pedir_entero("Ingrese el ID del producto: ")

    encontrado = False

    # Recorrido para localizar el producto
    for producto in productos:
        if producto["id"] == id_eliminar:
            encontrado = True
            confirmacion = input(
                f"¿Desea eliminar '{producto['nombre']}'? (s/n): "
            ).strip().lower()

            if confirmacion == "s":
                # Eliminación del producto de la lista y guardado
                productos.remove(producto)
                if guardar_productos(productos):
                    print("Producto eliminado correctamente.")
            else:
                print("Operación cancelada.")
            break

    if not encontrado:
        print("No existe un producto con ese ID.")


# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================
def menu():
    """Muestra el menú principal y ejecuta la opción elegida."""
    # Si el archivo no se puede crear, el programa no puede funcionar
    if not crear_archivo():
        print("El programa no puede continuar sin el archivo de inventario.")
        return

    while True:
        print("\n====================================")
        print(" SISTEMA DE INVENTARIO - DROPSHIPPING")
        print("====================================")
        print("1. Crear producto")
        print("2. Leer inventario")
        print("3. Buscar producto")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Contar productos")
        print("7. Salir")
        print("====================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            crear_producto()
        elif opcion == "2":
            leer_y_mostrar_productos()
        elif opcion == "3":
            buscar_producto()
        elif opcion == "4":
            actualizar_producto()
        elif opcion == "5":
            eliminar_producto()
        elif opcion == "6":
            contar_productos()
        elif opcion == "7":
            print("Programa finalizado.")
            break
        else:
            print("Error: opción no válida.")


# ==========================================================
# INICIO DEL PROGRAMA
# ==========================================================
if __name__ == "__main__":
    try:
        menu()
    except (KeyboardInterrupt, EOFError):
        # Permite cerrar el programa con Ctrl+C sin mostrar errores largos
        print("\nPrograma interrumpido por el usuario.")
