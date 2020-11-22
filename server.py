from flask import Flask
import time
import datetime
from flask.json import jsonify
import psutil


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
@app.route('/RAM', methods=['GET'])
def RAM():
    return jsonify(
        RAM=str(psutil.virtual_memory()),
        RAMINSTALLED=str(psutil.swap_memory()),
                   )

if __name__=="__main__":
    app.run()

