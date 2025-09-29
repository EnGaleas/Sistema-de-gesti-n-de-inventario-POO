# Producto.py
# Clase Producto: representa un artículo dentro del inventario
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.id_producto} - {self.nombre} - Cant: {self.cantidad} - ${self.precio}"
