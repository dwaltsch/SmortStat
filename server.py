#imports
from flask import Flask , request
from flask.json import jsonify
import time
import datetime
import psutil
import socket
import clr
import json
import platform
import os
import requests
import logging
import platform
import sys
from logging.handlers import TimedRotatingFileHandler

#vars
ip = socket.gethostbyname(socket.gethostname()) # fix wrong IP
app = Flask(__name__)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = TimedRotatingFileHandler('log.smortstat', when="midnight", interval=1, encoding='utf8')
handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

#currently based on flask and psutil rewrite in c++
#add logging support

@app.route('/')
def home():
    return 'Welcome to SmortStat Server'

@app.route('/CPU', methods=['GET'])
def CPU():
    app.logger.error('CPU Request')
    return jsonify(CPUUSE=str(psutil.cpu_percent(interval=0.1, percpu=True)),
                   CPUTIME=str(psutil.cpu_times_percent(interval=0.1, percpu=False)),
                   CPUCORECOUNT=str(psutil.cpu_count(logical=True)),
                   CPUSPEED=str(psutil.cpu_freq(percpu=True)),
                   )

@app.route('/LAN', methods=['GET'])
def LAN():
    app.logger.error('LAN Request')
    return jsonify(LANSTATS= str(psutil.net_io_counters())
                   )
@app.route('/NAME', methods=['GET'])
def Name():
    app.logger.error('Name Request')
    return jsonify(NAME= str(socket.gethostname())
                   )

@app.route('/TEMP', methods=['GET'])
def TEMP():
    return "not yet implemented" #implement some way or switch plattform


@app.route('/RAM', methods=['GET'])
def RAM():
    app.logger.error('RAM Request')
    return jsonify(
        RAM=str(psutil.virtual_memory()),
        RAMINSTALLED=str(psutil.swap_memory()),
                   )
@app.route('/RES', methods=['GET'])
def res():
    os.system("shutdown /r /t 1");
    return "Restarting"

@app.route('/SDW', methods=['GET'])
def sdw():
    os.system("shutdown /s /t 1");
    return "Shutting Down"

@app.route('/UBD', methods=['GET']) #not implemented
def update():
    os = platform.system()
    if os == "Windows":
        print("Warning: Pog")
        return "Windows detected: Updating via Command Line"
    if os == "Linux":
        return "Linux detected: Updating via Command Line"
    if os == "Darwin":
        return "MacOS is not officially supported yet"


if __name__== "__main__":
    logger.error('An exception occurred at %s', 'Error') #experimental not yet working
    print("Enter this in the APP")
    print(ip)
    app.run(host ='0.0.0.0', port=80,)
