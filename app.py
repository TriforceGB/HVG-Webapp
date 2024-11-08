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
    SetTemp = floatConvertion(HR[0], HR[1])
    SetHimid = floatConvertion(HR[2], HR[3]) 
    roomTemp = floatConvertion(IR[0], IR[1])
    roomHimid = floatConvertion(IR[4], IR[5])
    return render_template('index.html',roomTemp=roomTemp, roomHimid=roomHimid, SetTemp=SetTemp, SetHimid=SetHimid)

@app.route('/submit',methods=['POST'])
def submit():
    if request.method == 'POST':
        InputTemp = request.form['InputTemp']
        InputHimid = request.form['InputHimid']
        
        ST_Unit16 = floatToUint16(float(InputTemp))
        SH_Uint16 = floatToUint16(float(InputHimid))
        modbusClient.modbusWrite('hr',0,ST_Unit16, True)
        modbusClient.modbusWrite('hr',2,SH_Uint16, True)
        return redirect('/')


# Runner and Dubgger
if __name__ == '__main__':
    app.run(debug=True)