from flask import Flask
import time
import datetime
from flask.json import jsonify
import psutil
import socket

ip = socket.gethostbyname(socket.gethostname())
app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to SmortStat Server'

@app.route('/CPU', methods=['GET'])
def CPU():
    return jsonify(CPUUSE=str(psutil.cpu_percent(interval=0.1, percpu=True)),
                   CPUTIME=str(psutil.cpu_times_percent(interval=0.1, percpu=False)),
                   CPUCORECOUNT=str(psutil.cpu_count(logical=True)),
                   CPUSPEED=str(psutil.cpu_freq(percpu=True)),
                   )
@app.route('/LAN', methods=['GET'])
def LAN():
    return jsonify(LANSTATS= str(psutil.net_io_counters())
                   )
@app.route('/RAM', methods=['GET'])
def RAM():
    return jsonify(
        RAM=str(psutil.virtual_memory()),
        RAMINSTALLED=str(psutil.swap_memory()),
                   )

if __name__== "__main__":
    print("Enter this in the APP")
    print(ip)
    app.run(host ='0.0.0.0',port=5000)



