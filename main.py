
"""
SISTEMA DE SEGUIMIENTO DE INVENTARIO - DROPSHIPPING

Archivo principal del programa.
Contiene el menu, las validaciones y las operaciones CRUD.
La lectura y escritura del CSV se realizan en persistencia.py.
"""

# Importa las funciones del modulo de persistencia.
from persistencia import crear_archivo, leer_productos, guardar_productos

# Cantidad minima para recomendar reabastecimiento.
LIMITE_REABASTECER = 5


# ==========================================================
# VALIDACION DE TEXTOS
# ==========================================================
def pedir_texto(mensaje):
    """Solicita texto y evita que el campo quede vacio."""

    while True:
        texto = input(mensaje).strip()

        if texto:
            return texto

        print("Error: este campo no puede quedar vacio.")


# ==========================================================
# VALIDACION DE NUMEROS ENTEROS
# ==========================================================
def pedir_entero(mensaje):
    """Solicita un numero entero no negativo."""

    while True:
        try:
            numero = int(input(mensaje))

            if numero < 0:
                print("Error: el numero no puede ser negativo.")
            else:
                return numero

        except ValueError:
            print("Error: debes ingresar un numero entero.")


# ==========================================================
# VALIDACION DE PRECIOS
# ==========================================================
def pedir_precio(mensaje):
    """Solicita un precio numerico mayor que cero."""

    while True:
        try:
            precio = float(input(mensaje))

            if precio <= 0:
                print("Error: el precio debe ser mayor que cero.")
            else:
                return precio

        except ValueError:
            print("Error: debes ingresar un valor numerico.")


# ==========================================================
# VALIDACION DE CONFIRMACIONES
# ==========================================================
def pedir_confirmacion(mensaje):
    """Solicita una respuesta afirmativa o negativa."""

    while True:
        respuesta = input(mensaje).strip().lower()

        if respuesta in ("s", "si", "sí"):
            return True

        elif respuesta == "n":
            return False

        else:
            print("Escribe 's' para si o 'n' para no.")


# ==========================================================
# CRUD - CREATE: REGISTRAR PRODUCTO
# ==========================================================
def crear_producto():
    """Registra un producto nuevo en el inventario."""

    productos = leer_productos()

    # Si ocurre un error al leer, no se modifica el inventario.
    if productos is None:
        return

    print("\n--- REGISTRAR PRODUCTO ---")

    # Genera un ID consecutivo a partir del mayor ID existente.
    nuevo_id = max(
        (producto["id"] for producto in productos),
        default=0
    ) + 1

    nombre = pedir_texto("Nombre del producto: ")
    categoria = pedir_texto("Categoria: ")
    cantidad = pedir_entero("Cantidad disponible: ")
    precio = pedir_precio("Precio del producto: ")

    # Diccionario con los datos del producto.
    producto = {
        "id": nuevo_id,
        "nombre": nombre,
        "categoria": categoria,
        "cantidad": cantidad,
        "precio": precio
    }

    # Agrega el producto y guarda los cambios en el CSV.
    productos.append(producto)

    if guardar_productos(productos):
        print("\nProducto registrado correctamente.")
        print("ID asignado:", nuevo_id)


# ==========================================================
# CRUD - READ: MOSTRAR INVENTARIO
# ==========================================================
def leer_y_mostrar_productos():
    """Muestra todos los productos registrados."""

    productos = leer_productos()

    if productos is None:
        return

    print("\n--- INVENTARIO ---")

    if not productos:
        print("No hay productos registrados.")
        return

    # Recorre la lista y muestra la informacion de cada producto.
    for producto in productos:

        if producto["cantidad"] <= LIMITE_REABASTECER:
            estado = "REABASTECER"
        else:
            estado = "Disponible"

        print("----------------------------------")
        print("ID:", producto["id"])
        print("Producto:", producto["nombre"])
        print("Categoria:", producto["categoria"])
        print("Cantidad:", producto["cantidad"])
        print(f"Precio: ${producto['precio']:,.0f}")
        print("Estado:", estado)

    print("----------------------------------")


# ==========================================================
# BUSCAR PRODUCTO
# ==========================================================
def buscar_producto():
    """Busca productos por nombre completo o parcial."""

    productos = leer_productos()

    if productos is None:
        return

    print("\n--- BUSCAR PRODUCTO ---")
    nombre_buscar = pedir_texto(
        "Ingrese el nombre o parte del nombre: "
    ).lower()

    # Encuentra coincidencias sin distinguir mayusculas y minusculas.
    encontrados = [
        producto
        for producto in productos
        if nombre_buscar in producto["nombre"].lower()
    ]

    if not encontrados:
        print("No se encontro ningun producto.")
        return

    print("\nProductos encontrados:")

    for producto in encontrados:
        print(
            f"ID: {producto['id']} | "
            f"{producto['nombre']} | "
            f"Categoria: {producto['categoria']} | "
            f"Cantidad: {producto['cantidad']} | "
            f"Precio: ${producto['precio']:,.0f}"
        )


# ==========================================================
# CONTAR PRODUCTOS
# ==========================================================
def contar_productos():
    """Cuenta productos registrados y productos con stock bajo."""

    productos = leer_productos()

    if productos is None:
        return

    necesitan_reabastecimiento = sum(
        1
        for producto in productos
        if producto["cantidad"] <= LIMITE_REABASTECER
    )

    print("\n--- CONTEO DEL INVENTARIO ---")
    print("Cantidad de productos registrados:", len(productos))
    print(
        "Productos que necesitan reabastecimiento:",
        necesitan_reabastecimiento
    )


# ==========================================================
# CRUD - UPDATE: ACTUALIZAR PRODUCTO
# ==========================================================
def actualizar_producto():
    """Actualiza la cantidad y, opcionalmente, el precio."""

    productos = leer_productos()

    if productos is None:
        return

    print("\n--- ACTUALIZAR PRODUCTO ---")
    id_buscar = pedir_entero("Ingrese el ID del producto: ")

    # Busca el producto mediante su identificador.
    producto = next(
        (p for p in productos if p["id"] == id_buscar),
        None
    )

    if producto is None:
        print("No existe un producto con ese ID.")
        return

    print("Producto encontrado:", producto["nombre"])

    # Actualiza la cantidad disponible.
    producto["cantidad"] = pedir_entero(
        "Nueva cantidad disponible: "
    )

    # El cambio del precio es opcional.
    if pedir_confirmacion("Desea actualizar el precio? (s/n): "):
        producto["precio"] = pedir_precio("Nuevo precio: ")

    if guardar_productos(productos):
        print("Producto actualizado correctamente.")


# ==========================================================
# CRUD - DELETE: ELIMINAR PRODUCTO
# ==========================================================
def eliminar_producto():
    """Elimina un producto despues de solicitar confirmacion."""

    productos = leer_productos()

    if productos is None:
        return

    print("\n--- ELIMINAR PRODUCTO ---")
    id_eliminar = pedir_entero("Ingrese el ID del producto: ")

    # Busca el producto por su ID.
    producto = next(
        (p for p in productos if p["id"] == id_eliminar),
        None
    )

    if producto is None:
        print("No existe un producto con ese ID.")
        return

    confirmacion = pedir_confirmacion(
        f"Desea eliminar '{producto['nombre']}'? (s/n): "
    )

    if not confirmacion:
        print("Operacion cancelada.")
        return

    productos.remove(producto)

    if guardar_productos(productos):
        print("Producto eliminado correctamente.")


# ==========================================================
# MENU PRINCIPAL
# ==========================================================
def menu():
    """Muestra el menu principal del sistema."""

    # Crea el archivo CSV si todavia no existe.
    if not crear_archivo():
        print("No se puede iniciar el programa sin acceso al CSV.")
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

        try:
            opcion = input("Seleccione una opcion: ").strip()

        except (EOFError, KeyboardInterrupt):
            print("\nPrograma interrumpido por el usuario.")
            break

        # Ejecuta la opcion que selecciono el usuario.
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
            print("Error: opcion no valida. Seleccione del 1 al 7.")


# ==========================================================
# INICIO DEL PROGRAMA
# ==========================================================
if __name__ == "__main__":
    menu()
