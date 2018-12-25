#!flask/bin/python

from flask import Flask, jsonify, request
import socket

# Set key "field1": http://localhost:5000/set/field1?value=42
# Get key "field1": http://localhost:5000/get/field1
# Get             : http://localhost:5000/get
# Clear all :       http://localhost:5000/clear

app = Flask(__name__)

d = {}
d['data'] = {}

#Set up server socket for UDP Broadcast
dest = ('<broadcast>',10100)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)



@app.route('/clear', methods=['GET'])
def clear():
    global d
    d['data'] = {}
    return jsonify(d)

@app.route('/get/<name>', methods=['GET'])
def get_name(name):
    return jsonify(d['data'].get(name, {}))

@app.route('/get_all', methods=['GET'])
def get_all():
    return jsonify(d)

@app.route('/set/<name>', methods=['GET', 'POST'])
def set(name):
    global d
    d['data'][name] = d['data'].get(name, {})
    d['data'][name]['value'] = request.args.get('value') or float('nan')
    key = name
    value = d['data'][name]['value']
    msg = ("%s,%s"%(key, value))
    s.sendto(msg, dest)
    return 'success'

if __name__ == '__main__':
    app.run()
