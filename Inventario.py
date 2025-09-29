# Inventario.py
import json
from Producto import Producto

# Clase Inventario: gestiona una colección de productos
class Inventario:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, producto: Producto):
        self.productos[producto.id_producto] = producto

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]

    def modificar_producto(self, id_producto, nombre=None, cantidad=None, precio=None):
        if id_producto in self.productos:
            prod = self.productos[id_producto]
            if nombre: prod.nombre = nombre
            if cantidad: prod.cantidad = cantidad
            if precio: prod.precio = precio

    def mostrar_productos(self):
        return list(self.productos.values())

    def guardar_en_archivo(self, archivo="inventario.json"):
        with open(archivo, "w") as f:
            json.dump({id: vars(p) for id, p in self.productos.items()}, f, indent=4)

    def cargar_desde_archivo(self, archivo="inventario.json"):
        try:
            with open(archivo, "r") as f:
                data = json.load(f)
                for id, prod in data.items():
                    self.productos[id] = Producto(**prod)
        except FileNotFoundError:
            pass
