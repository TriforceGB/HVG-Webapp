from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from unit16_converters import floatToUint16, floatConvertion
from ModbusTCPClient import Modbus
from datetime import datetime

# My App Setup
app = Flask(__name__)
Scss(app)

ModbusHost = 'localhost'
Modbusport = 1562
unitID = 1

modbusClient = Modbus(ModbusHost,Modbusport,unitID)
connection = modbusClient.modbusConnect()    
#Home Page
@app.route('/',methods=['POST', 'GET'])
def index():
    IR = modbusClient.modbusRead('ir',0,6)
    HR = modbusClient.modbusRead('hr',0,4)
    wantedTemp = floatConvertion(HR[0], HR[1])
    wantedHimid = floatConvertion(HR[2], HR[3]) 
    roomTemp = floatConvertion(IR[0], IR[1])
    roomHimid = floatConvertion(IR[4], IR[5])
    return render_template('index.html',roomTemp=roomTemp, roomHimid=roomHimid, wantedTemp=wantedTemp, wantedHimid=wantedHimid)

@app.route('/submit',methods=['POST'])
def submit():
    if request.method == 'POST':
        wantedTemp = request.form['tempInput']
        wantedHimid = request.form['humidityInput']
        return wantedTemp+wantedHimid


# Runner and Dubgger
if __name__ == '__main__':
    app.run(debug=True)