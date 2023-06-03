#132BK178x.py

from time import sleep
from epics import caput
import sys, ps178x
try:
    from win32com.client import Dispatch
except:
    pass
err = sys.stderr.write

def test(cmd, results):
    if results:
        print(cmd, "failed:")
        print("  ", results)
        exit(1)
    else:
        print(cmd)

def TalkToPS(ps, port, baudrate):
    '''load is either a COM object or a PS178x object.  They have the 
    same interface, so this code works with either.
 
    port is the COM port on your PC that is connected to the power supply.
    baudrate is a supported baud rate of the power supply.
    '''

    ps.Initialize(port, baudrate) # Open a serial connection
    print("Time from Power Supply =", ps.TimeNow())
    test("Set to remote control", ps.SetRemoteControl())
    test("Set max voltage", ps.SetMaxVoltage(1.5))
    test("Set output voltage", ps.SetOutVoltage(0.3))
    test("Set output current", ps.SetOutCurrent(0.01))
    print("  Input values:" )
    values = ps.GetReading()
    for value in values.split("\t"): print("    ", value)
    print("  Product info:")
    values = ps.GetProductInformation()
    for value in values.split("\t"): print("    ", value)
    test("Set to local control", ps.SetLocalControl())


def Usage():
    name = sys.argv[0]
    msg = '''Usage:  %(name)s {com|obj} port baudrate
Demonstration python script to talk to a B&K Power supply 1785B series either via the COM
(component object model) interface or via a PS178x object (in PS178x.py).
port is the COM port number on your PC that the power supply is connected to.  
baudrate is the baud rate setting, 9600, of the power supply
''' % locals()
    print(msg)
    exit(1)

def main():
    if len(sys.argv) != 4: 
        Usage()
    access_type = sys.argv[1]
    port        = int(sys.argv[2])
    baudrate    = int(sys.argv[3])
    if access_type == "com":
        ps = Dispatch('BKServers.PS178x')
    elif access_type == "obj":
        ps = ps178x.PS178x()
    else:
        Usage()
    TalkToPS(ps, port, baudrate)
    return 0

ps.Initialize(port, baudrate) # Open a serial connection
#print "Time from Power Supply =", ps.TimeNow()
test("Set to remote control", ps.SetRemoteControl())

APX_R0=10.0
APX_RC=0.00431034
APX_PS1_V_RV=0.3
APX_PS1_V_MX=1.0
APX_PS1_I_RV=0.03
APX_PS1_I_MX=0.24
caput('APX:PS1_V_RV',APX_PS1_V_RV)
caput('APX:PS1_I_RV',APX_PS1_I_RV)
APX_PS1_V_OV=APX_PS1_V_RV
sleep(2)
main()

test("Set max voltage", ps.SetMaxVolatge(APX_PS1_V_MX))
test("Set output voltage", ps.SetOutVoltage(APX_PS1_V_RV))
test("Set output current", ps.SetOutCurrent(APX_PS1_I_RV))

try:
    while True:
        caget('APX:PS1_V_RV',APX_PS1_V_RV,0.3)
        caget('APX:PS1_I_RV',APX_PS1_I_RV,0.01)
        sleep(0.5)

        if APX_PS1_V_RV <APX_PS1_V_MX:
            APX_PS1_V_OV=APX_PS1_V_RV
#            if APX_PS1_V_RV> APX_PS1_V_OV:
#                APX_PS1_V_OV=APX_PS1_V_OV+0.01
#            elif APX_PS1_V_RV< APX_PS1_V_OV:
#                APX_PS1_V_OV=APX_PS1_V_OV-0.01
        else:
            APX_PS1_V_OV = APX_PS1_V_MX

        if APX_PS1_I_RV <APX_PS1_I_MX:
            APX_PS1_I_OV=APX_PS1_I_RV
        else:
            APX_PS1_V_OV = APX_PS1_V_MX

        test("Set output voltage", ps.SetOutVoltage(APX_PS1_V_OV))
        test("Set output current", ps.SetOutCurrent(APX_PS1_I_OV))
        sleep(0.5)
        values = ps.GetReading()
        APX_PS1_V_MV=values[0]
        APX_PS1_I_MV=values[1]
        sleep(0.5)
        caput('APX:PS1_V_MV',APX_PS1_V_MV)
        caput('APX:PS1_I_MV',APX_PS1_I_MV)
        APX_Theater=300/APX_RC*(APX_R0-1)*APX_PS1_V_MV/APX_PS1_I_MV
        caput('APX:PS1_I_MV',APX_Theater)

except KeyboardInterrupt:
    APX_PS1_V_RV=0.3
    APX_PS1_V_MX=1.0
    APX_PS1_I_RV=0.03
    caput('APX:PS1_V_RV',APX_PS1_V_RV)
    caput('APX:PS1_I_RV',APX_PS1_I_RV)
    APX_PS1_V_OV=APX_PS1_V_RV

    test("Set max voltage", ps.SetMaxVolatge(APX_PS1_V_MX))
    test("Set output voltage", ps.SetOutVoltage(APX_PS1_V_RV))
    test("Set output current", ps.SetOutCurrent(APX_PS1_I_RV))

    test("Set to local control", ps.SetLocalControl())
