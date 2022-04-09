from flask import Flask, request, jsonify
from flask_cors import CORS
import globals_vars
import mysql.connector
import threading

from secret import USER, PASSWORD, ENDPOINT, PORT, DBNAME

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/guardar", methods=['POST'])
def guardar():
    new_lista = request.get_json()
    globals_vars.lista_pixeles = new_lista
    return "OK", 200

@app.route("/cargar")
def cargar():
    return jsonify(globals_vars.lista_pixeles), 200

def guardarAmazon():
    conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=PASSWORD, port=PORT, database=DBNAME)
    cursor = conn.cursor()

    tuples_pixels = [(x[0], x[1]) for x in globals_vars.lista_pixeles]
    cursor.execute("delete from pixels")
    sql = """insert into pixels (id, color) values (%s, %s)"""
    cursor.executemany(sql, tuples_pixels)

    conn.commit()
    conn.close()
    threading.Timer(5.0, guardarAmazon).start()

def cargarAmazon():
    conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=PASSWORD, port=PORT, database=DBNAME)
    sql = "select * from pixels"
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    globals_vars.lista_pixeles = rows


if __name__ == '__main__':
    cargarAmazon()
    threading.Timer(5.0, guardarAmazon).start()
    app.run(port=6942)