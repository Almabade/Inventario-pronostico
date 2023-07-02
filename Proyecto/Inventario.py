import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sqlite3

class Inventariopre(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Inventario.ui', self)
        self.conn = sqlite3.connect('datos_inventario.db')
        self.c = self.conn.cursor()
        self.create_table()
        self.populate_table()
        self.bot_agregar.clicked.connect(self.agregar_elemento)
        self.modificar.clicked.connect(self.modificar_elemento)
        self.eliminar.clicked.connect(self.eliminar_elemento)


    def create_table(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS inventario(codigo TEXT,producto TEXT ,descripcion TEXT,cantidad TEXT,precio_und TEXT)")
        self.conn.commit()

    def populate_table(self):
        self.tabla_int.setRowCount(0)
        self.c.execute("SELECT * FROM inventario")
        rows = self.c.fetchall()
        for row_number, row_data in enumerate(rows):
            self.tabla_int.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Deshabilitar la edición de celdas
                self.tabla_int.setItem(row_number, column_number, item)

        self.tabla_int.cellClicked.connect(self.seleccionar_elemento)  # Conexión de señal y ranura

    def agregar_elemento(self):
        codigo = self.cod_bus.text()
        producto = self.nombre.text()
        descripcion = self.des.text()
        precio_und = self.precio.text()
        cantidad = self.cant.text()

        print("Codigo:", codigo)
        print("Producto:", producto)
        print("Descripción:", descripcion)
        print("Cantidad:", cantidad)
        print("Precio unidad:", precio_und)
        self.c.execute("INSERT INTO inventario (codigo,producto,descripcion,cantidad,precio_und) values (?, ?, ?, ?, ?)",(codigo, producto, descripcion, cantidad, precio_und))
        self.conn.commit()

        self.cod_bus.clear()
        self.nombre.clear()
        self.des.clear()
        self.cant.clear()
        self.precio.clear()

        self.populate_table()

    def seleccionar_elemento(self, row, column):
        codigo = self.tabla_int.item(row, 0).text()
        producto = self.tabla_int.item(row, 1).text()
        descripcion = self.tabla_int.item(row, 2).text()
        cantidad = self.tabla_int.item(row, 3).text()
        precio_und = self.tabla_int.item(row, 4).text()

        self.cod_bus.setText(codigo)
        self.nombre.setText(producto)
        self.des.setText(descripcion)
        self.cant.setText(cantidad)
        self.precio.setText(precio_und)


    def modificar_elemento(self):
        codigo_actual = self.cod_bus.text()
        producto = self.nombre.text()
        descripcion = self.des.text()
        precio_und = self.precio.text()
        cantidad = self.cant.text()

        self.c.execute("UPDATE inventario SET producto = ?, descripcion = ?, cantidad = ?, precio_und = ? WHERE codigo = ?", (producto, descripcion, cantidad, precio_und, codigo_actual))
        self.conn.commit()

        self.cod_bus.clear()
        self.nombre.clear()
        self.des.clear()
        self.cant.clear()
        self.precio.clear()

        self.populate_table()
    def eliminar_elemento(self):
        codigo_actual = self.cod_bus.text()

        # Verificar si se seleccionó un elemento en la tabla
        if codigo_actual:
            # Mostrar un mensaje de confirmación antes de eliminar el elemento
            respuesta = QMessageBox.question(self, 'Confirmar Eliminación', '¿Estás seguro de eliminar este elemento?', QMessageBox.Yes | QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                self.c.execute("DELETE FROM inventario WHERE codigo = ?", (codigo_actual,))
                self.conn.commit()

                self.cod_bus.clear()
                self.nombre.clear()
                self.des.clear()
                self.cant.clear()
                self.precio.clear()

                self.populate_table()
        else:
            QMessageBox.warning(self, 'Elemento no seleccionado', 'No se ha seleccionado ningún elemento de la tabla.')

