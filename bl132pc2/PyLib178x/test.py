'''
Open Source Initiative OSI - The MIT License:Licensing
Tue, 2006-10-31 04:56 nelson

The MIT License

Copyright (c) 2009 BK Precision

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

This script talks to the 1785B - 1788 power supply in two ways:
    1.  Using a PS178x object (you'd use this method when you write a
        python application that talks to the power supply.

    2.  Using the COM interface.  This shows how python code uses the
        COM interface.  Other programming environments (e.g., Visual
        Basic and Visual C++) would use very similar techniques to
        talk to the power supply via COM.

Note that the PS178x object and the COM server interface functions
always return strings.

$RCSfile: test.py $ 
$Revision: 1.0 $
$Date: 2008/12/19 21:02:50 $
$Author:  Jeremy Lo, Don Peterson $
'''

import sys, ps178x
try:
    from win32com.client import Dispatch
except:
    pass
err = sys.stderr.write

def TalkToPS(ps, port, baudrate):
    '''load is either a COM object or a PS178x object.  They have the 
    same interface, so this code works with either.
 
    port is the COM port on your PC that is connected to the power supply.
    baudrate is a supported baud rate of the power supply.
    '''
    def test(cmd, results):
        if results:
            print cmd, "failed:"
            print "  ", results
            exit(1)
        else:
            print cmd
    ps.Initialize(port, baudrate) # Open a serial connection
    print "Time from Power Supply =", ps.TimeNow()
    test("Set to remote control", ps.SetRemoteControl())
    test("Set max voltage", ps.SetMaxVoltage(5))
    test("Set output voltage", ps.SetOutVoltage(2.5))
    test("Set output current", ps.SetOutCurrent(5))
    print "  Input values:" 
    values = ps.GetReading()
    for value in values.split("\t"): print "    ", value
    print "  Product info:"
    values = ps.GetProductInformation()
    for value in values.split("\t"): print "    ", value
    test("Set to local control", ps.SetLocalControl())

def Usage():
    name = sys.argv[0]
    msg = '''Usage:  %(name)s {com|obj} port baudrate
Demonstration python script to talk to a B&K Power supply 1785B series either via the COM
(component object model) interface or via a PS178x object (in PS178x.py).
port is the COM port number on your PC that the power supply is connected to.  
baudrate is the baud rate setting of the power supply
''' % locals()
    print msg
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

main()
