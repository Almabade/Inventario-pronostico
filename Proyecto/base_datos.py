import sqlite3

conn=sqlite3.connect('datos_inventario.db')
c=conn.cursor()

def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS inventario(codigo TEXT,producto TEXT ,descripcion TEXT,cantidad TEXT,precio_und TEXT)")
	conn.commit()
	c.execute("INSERT INTO inventario values ('1f25','Palta','La palta es una fruta','1234','3')")
	conn.commit()

	c.close()
	conn.close()

create_table()