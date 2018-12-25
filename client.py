#!flask/bin/python
import argparse
import httplib  # in python3 this module changes to http.client
import json
from prettytable import PrettyTable
import socket
import time

port = 10100

p = PrettyTable()
d = PrettyTable()
p.field_names = ["Key", "Value"]
d.field_names = ["Key", "Value"]
# establish connection with server and setting content type
connection = httplib.HTTPConnection('localhost', port=5000)
headers = {'Content-type': 'application/json'}

#Set up client socket for UDP Broadcast
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('',port))


#Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--get", nargs='?', const=True, help="Get the Value associated with key. Don't specify any value to get the whole KV Store")
parser.add_argument("--set", help="Set the Value associated with key : --set key=value")
parser.add_argument("--clear", help="Clear all data", action='store_true')
parser.add_argument("--listen", help="listen to changes by other clients", action='store_true')

args = parser.parse_args()
print(args)
if args.set:
    key, value = args.set.split('=')
    connection.request('POST', '/set/%s?value=%s' % (key, value), headers=headers)
    time.sleep(1)
    p.add_row([key, value])
    print(p)
    p.clear_rows()
elif args.clear:
    connection.request('GET', '/clear', headers=headers)
elif args.listen:
    while True:
        message, __ = s.recvfrom(1024)
        key, value = message.split(',')
        p.add_row([key, value])
        print(p)
        p.clear_rows()
elif args.get:
    if not isinstance(args.get, bool):
        connection.request('GET', '/get/%s' % args.get, headers=headers)
        response = connection.getresponse().read()
        data = (json.loads(response.decode()))
        if data:
            p.add_row([args.get, data['value']])
            print(p)
            p.clear_rows()
        else:
            print("Either No data in KV Store or Wrong Key Specified!")
    else:
        connection.request('GET', '/get_all')
        response = connection.getresponse().read()
        data = (json.loads(response.decode())).get('data', None)
        for key in data.keys():
            d.add_row([key, data[key]['value']])
        print(d)
        p.clear_rows()
