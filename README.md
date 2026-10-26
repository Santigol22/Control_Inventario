# Sistema de Seguimiento de Inventario para Dropshipping

Programa de consola en Python para administrar el inventario de una tienda de dropshipping. Permite registrar, consultar, buscar, actualizar, eliminar y contar productos. Los datos se guardan en un archivo CSV, por lo que se conservan al cerrar y volver a abrir el programa.

## Requisitos

- Python 3.8 o superior.
- No necesita librerías externas (solo usa `csv` y `os`, que vienen con Python).

## Cómo ejecutar

1. Coloque `main.py` y `persistencia.py` en la misma carpeta.
2. Abra una terminal en esa carpeta.
3. Ejecute:

```bash
python main.py
```

(En algunos sistemas el comando es `python3 main.py`.)

La primera vez se crea automáticamente el archivo `inventario.csv` en la carpeta desde la que se ejecuta el programa.

## Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `main.py` | Archivo principal. Contiene el menú, las validaciones de entrada (`pedir_entero`, `pedir_precio`, `pedir_texto`), las operaciones CRUD, la búsqueda y el conteo del inventario. Importa las funciones de `persistencia.py`. |
| `persistencia.py` | Módulo encargado del archivo CSV: `crear_archivo()`, `leer_productos()` y `guardar_productos()`, con manejo de errores de lectura y escritura. |
| `inventario.csv` | Se genera automáticamente. Guarda los productos con las columnas `id, nombre, categoria, cantidad, precio`. |
| `README.md` | Este documento. |

## Opciones del menú

1. **Crear producto:** registra un producto con ID automático, nombre, categoría, cantidad y precio.
2. **Leer inventario:** muestra todos los productos y su estado (*REABASTECER* si la cantidad es 5 o menos, *Disponible* en otro caso).
3. **Buscar producto:** busca por nombre (o parte del nombre) sin distinguir mayúsculas.
4. **Actualizar producto:** cambia la cantidad y, si se desea, el precio de un producto por su ID.
5. **Eliminar producto:** borra un producto por su ID, pidiendo confirmación.
6. **Contar productos:** muestra el total de productos y cuántos necesitan reabastecimiento.
7. **Salir.**

## Validaciones y manejo de errores

- Nombre, categoría y texto de búsqueda no pueden quedar vacíos.
- Cantidades e IDs deben ser enteros no negativos.

## Organización del proyecto

- main.py: contiene el menú principal y las operaciones CRUD.
- persistencia.py: contiene las funciones para crear, leer y guardar los productos en el archivo CSV.
- README.md: contiene la descripción del proyecto y las instrucciones de uso.

- ## Persistencia de datos

El sistema utiliza un archivo CSV para almacenar los productos registrados. Esto permite conservar la información entre ejecuciones del programa.

## Control de versiones

Se utilizó Git para registrar cambios del proyecto y GitHub para publicar los archivos y documentar su evolución.
- El precio debe ser numérico y mayor que cero (acepta punto o coma decimal).
- Si el CSV no se puede crear, leer o escribir (por ejemplo, por permisos), se muestra un mensaje y el inventario no se sobrescribe.
- Si una fila del CSV tiene datos dañados, se omite con una advertencia y el resto del inventario se carga normalmente.
- 
- Si el archivo se borra mientras el programa está abierto, se vuelve a crear.
- `Ctrl+C` cierra el programa sin mostrar errores.
