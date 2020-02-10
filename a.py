import PySimpleGUI as sg
import os
import subprocess
import sys
sg.theme('DarkAmber')  
layout = [  [sg.Text('Change Permissions')],
            [sg.Text('Enter IP'), sg.InputText(key="ip")],
            # [sg.Button('Accept'), sg.Button('Clear')],
            [sg.InputCombo(('ACCEPT', 'REJECT','DROP'),enable_events=True, key='action',size=(20,3)),
            sg.Button('Test'),sg.Button('Clear')],
            [sg.Button('View')],[sg.Output(size=(100,20),key="op")],
            [sg.Exit()] ]

window = sg.Window('Linux Firewall', layout)

def runCommand(cmd, timeout=None, window=None):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None        
    retval = p.wait(timeout)
    
    return (retval, output)  


def create_command(type1,ip,port,io,dport): 
    command="sudo iptables"
    if type1!="":
        command+=" "
        command+=type1
    if port!="":
        command+=" -p "
        command+=port
    if dport!="":
        command+=" --dport "
        command+=dport
    if ip!="":
        command+=" -s "
        command+=ip
    if io!="":
        command+=" -j "
        command+=io
    return command


while True:
    event, values = window.read()
    if event in (None, 'Exit'):  
        break
    if event in ('Clear'):
        cmd = 'sudo iptables -F'
        os.system(cmd)
        window.FindElement('op').Update('')
        
    if event in ('View'):
        cmd = 'sudo iptables -L'
        runCommand(cmd, window=window)


    if event in ('Test'):
        cmd=""
        action=values['action']
        cmd=create_command("-A INPUT",values["ip"],"",action,"")
        runCommand(cmd, window=window)
        print(cmd)
window.close()
    
