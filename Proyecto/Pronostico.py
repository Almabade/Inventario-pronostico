import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sqlite3
import pandas as pd
import matplotlib.pylab as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Cargar el archivo UI generado por Qt Designer

class Pronosticopre(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Pronostico.ui', self)
        self.actionAbrir.triggered.connect(self.abrir_archivo)
        self.grafica.clicked.connect(self.mostrar_grafica)
        self.pronosticar.clicked.connect(self.mostrar_pronostico)
        self.cambiar.clicked.connect(self.cambiar_precio)
        self.df = None
        self.predicted_price = None # Variable de instancia para almacenar el DataFrame
        self.conn = sqlite3.connect('datos_inventario.db')
        self.c = self.conn.cursor()
        self.populate_table()

    def abrir_archivo(self):
        # Mostrar el diálogo de selección de archivo
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Archivos CSV (*.csv)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            # Obtener la ruta del archivo seleccionado
            archivo_seleccionado = file_dialog.selectedFiles()[0]
            # Leer el archivo CSV utilizando pandas
            self.df = pd.read_csv(archivo_seleccionado)
            print(self.df.head())

    def mostrar_grafica(self):
        if self.df is not None:  # Verificar si se ha cargado un archivo
            # Realizar descripción estadística de la columna 'Precio'
            plt.hist(self.df['AveragePrice'], bins=20)
            plt.xlabel('AveragePrice')
            plt.ylabel('Total Volume')
            plt.title('Distribución de los precios por el volumen')
            plt.show()
            print(self.df.head())
        else:
            print("No se ha cargado ningún archivo CSV.")

    def mostrar_pronostico(self):
        if self.df is not None:
            df_descripcion = self.df['AveragePrice'].describe()
            print(df_descripcion)
            self.df['type'] = self.df['type'].map({'conventional': 0, 'organic': 1})
            self.df = self.df.dropna()
            self.df = self.df.drop(['Unnamed: 0','Date', '4046', '4225', '4770', 'Small Bags', 'Large Bags', 'XLarge Bags', 'year', 'region'], axis=1)
            print(self.df.head())
            features = self.df.drop(['AveragePrice'], axis=1)
            labels = self.df['AveragePrice']
            X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
            model = LinearRegression()
            model.fit(X_train, y_train)
            new_price = pd.DataFrame({
                'Total Volume': [49500],
                'Total Bags': [7523],
                'type': [3],
            })

            predicted_price = model.predict(new_price)
            self.predicted_price = predicted_price
            print('Precio pronosticado para el nuevo auto:', predicted_price)
            self.dato.setText(", ".join(str(price) for price in predicted_price))
        else:
            print("No se ha cargado ningún archivo CSV.")



    def populate_table(self):
        self.tabla_int1.setRowCount(0)
        self.c.execute("SELECT * FROM inventario")
        rows = self.c.fetchall()
        for row_number, row_data in enumerate(rows):
            self.tabla_int1.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Deshabilitar la edición de celdas
                self.tabla_int1.setItem(row_number, column_number, item)

        self.tabla_int1.cellClicked.connect(self.seleccionar_elemento)  # Conexión de señal y ranura

    def seleccionar_elemento(self, row, column):
        codigo = self.tabla_int1.item(row, 0).text()
        producto = self.tabla_int1.item(row, 1).text()
        descripcion = self.tabla_int1.item(row, 2).text()
        cantidad = self.tabla_int1.item(row, 3).text()
        precio_und = self.tabla_int1.item(row, 4).text()


    def cambiar_precio(self):
        precio_und = self.dato.text()
        codigo_actual = self.tabla_int1.item(self.tabla_int1.currentRow(), 0).text()

        self.c.execute("UPDATE inventario SET precio_und = ? WHERE codigo = ?", (precio_und, codigo_actual))
        self.conn.commit()

        self.dato.clear()

        self.populate_table()


