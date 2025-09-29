# interfaz.py
import tkinter as tk
from tkinter import ttk, messagebox
from Inventario import Inventario
from Producto import Producto

class App:
    def __init__(self, root):
        self.inventario = Inventario()
        self.inventario.cargar_desde_archivo()

        root.title("Sistema de Inventario - POO")
        root.geometry("600x400")

        tk.Label(root, text="Nombre: Erminia Galeas", font=("Arial", 10)).pack()
        tk.Label(root, text="Carrera: Ing. TI - Paralelo X", font=("Arial", 10)).pack()

        self.tree = ttk.Treeview(root, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.pack(fill=tk.BOTH, expand=True)

        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="Agregar", command=self.agregar_producto).grid(row=0, column=0)
        tk.Button(frame, text="Modificar", command=self.modificar_producto).grid(row=0, column=1)
        tk.Button(frame, text="Eliminar", command=self.eliminar_producto).grid(row=0, column=2)
        tk.Button(frame, text="Guardar", command=self.guardar).grid(row=0, column=3)

        self.refrescar_tabla()
        root.bind("<Delete>", lambda e: self.eliminar_producto())
        root.bind("<Escape>", lambda e: root.quit())

    def agregar_producto(self):
        top = tk.Toplevel()
        top.title("Nuevo Producto")
        tk.Label(top, text="ID:").grid(row=0, column=0)
        tk.Label(top, text="Nombre:").grid(row=1, column=0)
        tk.Label(top, text="Cantidad:").grid(row=2, column=0)
        tk.Label(top, text="Precio:").grid(row=3, column=0)

        id_entry = tk.Entry(top); id_entry.grid(row=0, column=1)
        nombre_entry = tk.Entry(top); nombre_entry.grid(row=1, column=1)
        cant_entry = tk.Entry(top); cant_entry.grid(row=2, column=1)
        precio_entry = tk.Entry(top); precio_entry.grid(row=3, column=1)

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
                top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Cantidad y Precio deben ser números")

        tk.Button(top, text="Guardar", command=guardar_producto).grid(row=4, column=1)

    def modificar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un producto para modificar")
            return

        item = self.tree.item(selected[0])
        id_producto = item["values"][0]

        top = tk.Toplevel()
        top.title("Modificar Producto")
        tk.Label(top, text="Nuevo Nombre:").grid(row=0, column=0)
        tk.Label(top, text="Nueva Cantidad:").grid(row=1, column=0)
        tk.Label(top, text="Nuevo Precio:").grid(row=2, column=0)

        nombre_entry = tk.Entry(top); nombre_entry.grid(row=0, column=1)
        cant_entry = tk.Entry(top); cant_entry.grid(row=1, column=1)
        precio_entry = tk.Entry(top); precio_entry.grid(row=2, column=1)

        def actualizar():
            try:
                nombre = nombre_entry.get() or None
                cantidad = int(cant_entry.get()) if cant_entry.get() else None
                precio = float(precio_entry.get()) if precio_entry.get() else None
                self.inventario.modificar_producto(id_producto, nombre, cantidad, precio)
                self.refrescar_tabla()
                top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Cantidad y Precio deben ser números")

        tk.Button(top, text="Actualizar", command=actualizar).grid(row=3, column=1)

    def eliminar_producto(self):
        selected = self.tree.selection()
        if not selected: return
        id_producto = self.tree.item(selected[0])["values"][0]
        self.inventario.eliminar_producto(id_producto)
        self.refrescar_tabla()

    def guardar(self):
        self.inventario.guardar_en_archivo()
        messagebox.showinfo("Éxito", "Inventario guardado en archivo")

    def refrescar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.inventario.mostrar_productos():
            self.tree.insert("", tk.END, values=(p.id_producto, p.nombre, p.cantidad, p.precio))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
