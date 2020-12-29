#imports
from flask import Flask , request
from flask.json import jsonify
import flask_monitoringdashboard as dashboard
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

#vars
ip = socket.gethostbyname(socket.gethostname())
app = Flask(__name__)
dashboard.bind(app)
#pw Admin Admin

OHM_hwtypes = [ 'Mainboard', 'SuperIO', 'CPU', 'RAM', 'GpuNvidia', 'GpuAti', 'TBalancer', 'Heatmaster', 'HDD' ]
OHM_sensortypes = [
 'Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow', 'Control', 'Level', 'Factor', 'Power', 'Data', 'SmallData'
]
entsch = "no"

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
    app.logger.error('Temp Request')
    def init_OHM():
        clr.AddReference(os.path.abspath(os.path.dirname(__file__)) + R'\OpenHardwareMonitorLib.dll')
        from OpenHardwareMonitor import Hardware
        hw = Hardware.Computer()
        hw.CPUEnabled, hw.GPUEnabled, = True, True,
        hw.Open()
        return hw

    def fetch_data(handle):
        out = []
        for i in handle.Hardware:
            i.Update()
            for sensor in i.Sensors:
                thing = parse_sensor(sensor)
                if thing is not None:
                    out.append(thing)
            for j in i.SubHardware:
                j.Update()
                for subsensor in j.Sensors:
                    thing = parse_sensor(subsensor)
                    out.append(thing)
        return out

    def parse_sensor(snsr):
        if snsr.Value is not None:
            if snsr.SensorType == OHM_sensortypes.index('Temperature'):
                HwType = OHM_hwtypes[snsr.Hardware.HardwareType]
                return {"Reading": snsr.Value}

    def main():
        return json.dumps({platform.node(): fetch_data(init_OHM())}, indent=1, sort_keys=True, ensure_ascii=False)

    return main()
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

@app.route('/UBD', methods=['GET'])
def update():
    bst = platform.system()
    if bst == "Windows":
        print("Warning: Pog")
        return "Windows detected: Updating via Command Line"
    if bst == "Linux":
        return "Linux detected: Updating via Command Line"
    if bst == "Darwin":
        return "MacOS is not officially supported yet"


if __name__== "__main__":
    print("enable logs yes or no")
    entsch = input()
    print("ignore the errors")
    print("Enter this in the APP")
    print(ip)
    app.run(host ='0.0.0.0', port=80,)
