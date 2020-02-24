import PySimpleGUI as sg
import os
import subprocess
import sys
sg.theme('DarkAmber')  
layout = [  [sg.Text('Change Permissions')],
            [ sg.InputCombo((' ACCEPT',' DROP'),default_value='DROP',enable_events=True, key='accept',size=(20,3)),
	     sg.Button('Change Policies')],
	    [sg.Text('To Bolck IP')],
            [sg.Text('Append'),sg.InputCombo(('-A ', ' -I '),default_value=' -A ',enable_events=True, key='append',size=(10,1)),
             sg.Text('IP'), sg.InputText(key="ip",size=(20,1)),
            sg.Text('Protocol'), sg.InputText(key="protocol",size=(10,1)),sg.Text('Destination Port'), sg.InputText(key="dport",size=(10,1)),
            sg.InputCombo(('ACCEPT', 'REJECT','DROP'),default_value='ACCEPT',enable_events=True, key='action',size=(20,3))],
            [sg.Text('Chains'),sg.InputCombo(('INPUT', 'FORWARD','OUTPUT'),default_value='OUTPUT',enable_events=True, key='chains',size=(20,3))],
            [sg.Button('Insert'),sg.Button('Flush'),sg.Button('Save')],
            [sg.Button('View')],[sg.Output(size=(100,20),key="op")],[sg.Button('Clear')]]   

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


def create_command(ip,protocol,io,dport): 
    command=""
                 
   
    if protocol!="":
        command+=" -p "
        command+=protocol
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
    if event in (None,):  
        break
   

    if event in ('Flush'):
        qcmd = 'sudo iptables -F'
        runCommand(qcmd, window=window)
        
    if event in ('View'):
        cmd = 'sudo iptables -L'
        runCommand(cmd, window=window)
    if event in ('Change Policies'):
        cmd=""
        cmd="sudo iptables -P "+values["chains"]+" "+values["accept"]
        runCommand(cmd, window=window)
        print(cmd)
    if event in ('Insert'):
        cmd=""
        action=values['action']
        cmd="sudo iptables "+values["append"]+values["chains"]+create_command(values["ip"],values["protocol"],action,values["dport"])
        runCommand(cmd, window=window)
        print(cmd)
        
    if event in ('Clear'):   
        window.FindElement('op').Update('')
    if event in ('Save'):
        cmd="service netfilter-persistent start"
        runCommand(cmd, window=window)
        cmd1="netfilter-persistent save"
        runCommand(cmd1, window=window)
        #cmd2="ip6tables-save"
        #runCommand(cmd2, window=window)
window.close()
    
