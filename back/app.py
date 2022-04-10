from flask import Flask, request, jsonify
from flask_cors import CORS
import globals_vars
import mysql.connector
import threading
from flask_socketio import SocketIO
import json

from secret import USER, PASSWORD, ENDPOINT, PORT, DBNAME

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins='*'
#, async_mode='threading'
)


@socketio.on('pixel')
def handle_pixel(data):
    sid = request.sid
    pixel = data['data']
    globals_vars.pixels[pixel[0]] = pixel[1]
    socketio.emit('pixels', {pixel[0]: pixel[1]}, skip_sid=sid)

@socketio.on('connect')
def connect():
    sid = request.sid
    enviar_pixels(sid=sid)

def guardarAmazon():
    conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=PASSWORD, port=PORT, database=DBNAME)
    cursor = conn.cursor()

    tuples_pixels = [(k,v) for k,v in globals_vars.pixels.items()]
    cursor.execute("delete from pixels")
    sql = """insert into pixels (id, color) values (%s, %s)"""
    cursor.executemany(sql, tuples_pixels)

    conn.commit()
    conn.close()
    threading.Timer(20.0, guardarAmazon).start()

def cargarAmazon():
    conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=PASSWORD, port=PORT, database=DBNAME)
    sql = "select * from pixels"
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    globals_vars.pixels = {x[0]:x[1] for x in rows}

def enviar_pixels(sid=None):
    if sid is None:
        socketio.emit('pixels', globals_vars.pixels)
        threading.Timer(5.0, enviar_pixels).start()
    else:
        socketio.emit('pixels', globals_vars.pixels, to=sid)

cargarAmazon()
threading.Timer(5.0, enviar_pixels).start()
threading.Timer(20.0, guardarAmazon).start()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=6942)