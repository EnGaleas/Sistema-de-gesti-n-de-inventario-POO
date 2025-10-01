# interfaz.py
# UNIVERSIDAD ESTATAL AMAZÓNICA
# INGENIERÍA EN TECNOLOGÍAS DE LA INFORMACIÓN
# PROGRAMACIÓN ORIENTADA A OBJETOS
# Estudiante: Erminia Galeas - Paralelo A
# Sistema de gestión de inventario con POO, GUI y archivos

import tkinter as tk
from tkinter import ttk, messagebox
from Inventario import Inventario
from Producto import Producto


class App:
    def __init__(self, root):
        # Objeto Inventario
        self.inventario = Inventario()
        self.inventario.cargar_desde_archivo()

        # Configuración de la ventana principal
        root.title("Sistema de Inventario - UNIVERSIDAD ESTATAL AMAZÓNICA")
        root.geometry("650x450")

        # Etiquetas con información institucional y del estudiante
        tk.Label(root, text="UNIVERSIDAD ESTATAL AMAZÓNICA", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(root, text="Carrera: Ingeniería en Tecnologías de la Información", font=("Arial", 10)).pack()
        tk.Label(root, text="Asignatura: Programación Orientada a Objetos", font=("Arial", 10)).pack()
        tk.Label(root, text="Estudiante: Erminia Galeas", font=("Arial", 10)).pack()
        tk.Label(root, text="Paralelo: A", font=("Arial", 10)).pack()

        # Menú principal
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        menu_productos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opciones", menu=menu_productos)
        menu_productos.add_command(label="Productos", command=self.abrir_productos)
        menu_productos.add_separator()
        menu_productos.add_command(label="Salir", command=root.quit)

    # Ventana de gestión de productos
    def abrir_productos(self):
        top = tk.Toplevel()
        top.title("Gestión de Productos")
        top.geometry("600x400")

        # Tabla de productos
        self.tree = ttk.Treeview(
            top, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Frame para botones
        frame = tk.Frame(top)
        frame.pack()

        tk.Button(frame, text="Agregar", command=self.agregar_producto).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Modificar", command=self.modificar_producto).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Eliminar", command=self.eliminar_producto).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Guardar", command=self.guardar).grid(row=0, column=3, padx=5)

        # Cargar productos en la tabla
        self.refrescar_tabla()

        # Atajos de teclado
        top.bind("<Delete>", lambda e: self.eliminar_producto())  # tecla Delete elimina
        top.bind("<Escape>", lambda e: top.destroy())  # tecla Escape cierra ventana productos

    # Agregar producto
    def agregar_producto(self):
        ventana = tk.Toplevel()
        ventana.title("Agregar Producto")

        tk.Label(ventana, text="ID:").grid(row=0, column=0)
        tk.Label(ventana, text="Nombre:").grid(row=1, column=0)
        tk.Label(ventana, text="Cantidad:").grid(row=2, column=0)
        tk.Label(ventana, text="Precio:").grid(row=3, column=0)

        id_entry = tk.Entry(ventana); id_entry.grid(row=0, column=1)
        nombre_entry = tk.Entry(ventana); nombre_entry.grid(row=1, column=1)
        cant_entry = tk.Entry(ventana); cant_entry.grid(row=2, column=1)
        precio_entry = tk.Entry(ventana); precio_entry.grid(row=3, column=1)

        def guardar_producto():
            try:
                prod = Producto(
                    id_entry.get(),
                    nombre_entry.get(),
                    int(cant_entry.get()),
                    float(precio_entry.get())
                )
                self.inventario.agregar_producto(prod)
                self.refrescar_tabla()
                ventana.destroy()
            except ValueError:
                messagebox.showerror("Error", "Cantidad y Precio deben ser números")

        tk.Button(ventana, text="Guardar", command=guardar_producto).grid(row=4, column=1)

    # Modificar producto
    def modificar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un producto")
            return
        item = self.tree.item(selected[0])
        id_producto = item["values"][0]

        ventana = tk.Toplevel()
        ventana.title("Modificar Producto")

        tk.Label(ventana, text="Nuevo Nombre:").grid(row=0, column=0)
        tk.Label(ventana, text="Nueva Cantidad:").grid(row=1, column=0)
        tk.Label(ventana, text="Nuevo Precio:").grid(row=2, column=0)

        nombre_entry = tk.Entry(ventana); nombre_entry.grid(row=0, column=1)
        cant_entry = tk.Entry(ventana); cant_entry.grid(row=1, column=1)
        precio_entry = tk.Entry(ventana); precio_entry.grid(row=2, column=1)

        def actualizar():
            try:
                nombre = nombre_entry.get() or None
                cantidad = int(cant_entry.get()) if cant_entry.get() else None
                precio = float(precio_entry.get()) if precio_entry.get() else None
                self.inventario.modificar_producto(id_producto, nombre, cantidad, precio)
                self.refrescar_tabla()
                ventana.destroy()
            except ValueError:
                messagebox.showerror("Error", "Cantidad y Precio deben ser números")

        tk.Button(ventana, text="Actualizar", command=actualizar).grid(row=3, column=1)

    # Eliminar producto
    def eliminar_producto(self):
        selected = self.tree.selection()
        if not selected:
            return
        id_producto = self.tree.item(selected[0])["values"][0]
        self.inventario.eliminar_producto(id_producto)
        self.refrescar_tabla()

    # Guardar inventario en archivo
    def guardar(self):
        self.inventario.guardar_en_archivo()
        messagebox.showinfo("Éxito", "Inventario guardado en archivo")

    # Actualizar tabla
    def refrescar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.inventario.mostrar_productos():
            self.tree.insert("", tk.END, values=(p.id_producto, p.nombre, p.cantidad, p.precio))


# Punto de entrada de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
