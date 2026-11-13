# Sistema de Seguimiento de Inventario para Dropshipping

## 1. Descripción del proyecto

Este proyecto es una aplicación de consola desarrollada en Python para administrar el inventario de una tienda de dropshipping. Permite registrar, consultar, buscar, actualizar, eliminar y contar productos.

La información se almacena en un archivo CSV llamado `inventario.csv`. De esta manera, los productos permanecen guardados cuando se cierra el programa y se vuelve a ejecutar.

## 2. Objetivo

Desarrollar un sistema sencillo y modular que facilite el control de productos, cantidades disponibles y precios, aplicando operaciones CRUD, validación de datos y almacenamiento persistente mediante archivos CSV.

## 3. Requisitos

- Python 3.8 o una versión posterior.
- No requiere instalar librerías externas. Utiliza los módulos estándar `csv`, `math` y `os` incluidos en Python.

## 4. Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `main.py` | Contiene el menú principal, las validaciones de entrada y las operaciones CRUD. |
| `persistencia.py` | Contiene las funciones para crear, leer y guardar la información en el archivo CSV. |
| `inventario.csv` | Archivo de datos. Se crea automáticamente y almacena los productos registrados. |
| `README.md` | Documento con la descripción, instalación y uso del sistema. |

## 5. Instalación y ejecución

1. Instalar Python 3.8 o superior.
2. Descargar o clonar este repositorio de GitHub.
3. Verificar que los archivos `main.py` y `persistencia.py` estén en la misma carpeta.
4. Abrir una terminal o consola dentro de esa carpeta.
5. Ejecutar el programa con el comando:

```bash
python main.py
```

En algunos equipos puede ser necesario utilizar:

```bash
python3 main.py
```

Al iniciar, el programa crea automáticamente `inventario.csv` si el archivo no existe o está vacío. No se necesita crear manualmente.

## 6. Uso del sistema

Al ejecutar el programa aparece un menú con las siguientes opciones:

1. **Crear producto:** registra un producto con identificador automático, nombre, categoría, cantidad y precio.
2. **Leer inventario:** muestra los productos almacenados y su estado.
3. **Buscar producto:** permite buscar por el nombre completo o una parte del nombre, sin distinguir mayúsculas y minúsculas.
4. **Actualizar producto:** permite cambiar la cantidad y, opcionalmente, el precio de un producto mediante su ID.
5. **Eliminar producto:** elimina un producto después de solicitar confirmación.
6. **Contar productos:** muestra el número total de productos y cuántos requieren reabastecimiento.
7. **Salir:** finaliza la ejecución.

### Ejemplo de registro

Al seleccionar la opción 1, el sistema solicita los datos del producto. Por ejemplo:

- Nombre: Teclado
- Categoría: Periféricos
- Cantidad: 8
- Precio: 75000

El sistema asigna automáticamente un ID y guarda el producto en `inventario.csv`.

### Estado del inventario

El sistema muestra el estado **REABASTECER** cuando un producto tiene 5 unidades o menos. Si tiene más de 5 unidades, muestra **Disponible**.

## 7. Validaciones y manejo de errores

- Los campos de nombre, categoría y búsqueda no pueden quedar vacíos.
- La cantidad debe ser un número entero igual o mayor que cero.
- Los identificadores solicitados para actualizar o eliminar deben ser enteros mayores o iguales que uno.
- El precio debe ser un número mayor que cero y no puede ser infinito ni un valor no numérico especial.
- Si se ingresan letras en un campo numérico, el sistema muestra un mensaje y solicita nuevamente el dato.
- Si el archivo CSV no existe o está vacío, se crea o inicializa con los encabezados requeridos.
- Si una fila contiene datos incorrectos, se omite y se muestra una advertencia para continuar con las demás filas.
- Si los encabezados del CSV no son válidos o ocurre un error de lectura, se informa el problema y no se procesa el inventario.

## 8. Organización y persistencia

El programa está dividido en dos módulos para separar responsabilidades:

- `main.py`: gestiona la interacción con el usuario, las validaciones y las operaciones del inventario.
- `persistencia.py`: administra la creación, lectura y escritura del archivo CSV.

Cuando se registra, actualiza o elimina un producto, el programa envía la lista modificada a la función `guardar_productos()`. Esta escribe los encabezados y los registros en `inventario.csv`. Al consultar el inventario, `leer_productos()` recupera los registros y los convierte en una lista de diccionarios para que el programa pueda trabajar con ellos.

## 9. Control de versiones

El proyecto utiliza Git para el seguimiento de cambios y GitHub como plataforma de alojamiento del repositorio y colaboración.

Repositorio: https://github.com/Santigol22/Control_Inventario

## 10. Créditos y referencias

Documentación consultada en formato APA 7:

- Python Software Foundation. (s. f.). *csv — CSV File Reading and Writing*. Python documentation. https://docs.python.org/3/library/csv.html
- Python Software Foundation. (s. f.). *math — Mathematical functions*. Python documentation. https://docs.python.org/3/library/math.html
- Python Software Foundation. (s. f.). *Built-in exceptions*. Python documentation. https://docs.python.org/3/library/exceptions.html
- Git. (s. f.). *Git documentation*. https://git-scm.com/doc
- GitHub. (s. f.). *GitHub documentation*. https://docs.github.com/
