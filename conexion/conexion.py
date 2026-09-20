import mysql.connector


def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Heidy2006.",
        database="smartventas"
    )

    return conexion