import PySimpleGUI as sg
import os
import subprocess
import sys
sg.theme('DarkAmber')  
layout = [  
    
    
            [sg.Text('Change Permissions')],
            
            [sg.InputCombo((' ACCEPT',' DROP'),default_value='DROP',enable_events=True, key='accept',size=(20,3)),sg.Button('Change Policies')],
            
            [
                     sg.Text('Append'),sg.InputCombo(('-A ', ' -I '),default_value=' -A ',enable_events=True, key='append',size=(4,3)),
                     sg.Text('Select Chain'),sg.InputCombo(('INPUT ', 'FORWARD ','OUTPUT '),default_value='OUTPUT',enable_events=True,key='chain',size=(10,3)),
                     sg.Text('Source IP/MAC'), sg.InputText(key="sip",size=(20,1)),
                     sg.Text('Destination IP'), sg.InputText(key="dip",size=(20,1))
            ],
            
	    [ 
                
		    sg.Text('Protocol'),sg.InputText(key="protocol",size=(10,1)),
                    sg.Text('       Destination Port'), sg.InputText(key="dport",size=(10,1)),
                    sg.Text('       Source Port'), sg.InputText(key="sport",size=(10,1)),sg.Text('       '),
              	    sg.InputCombo(('ACCEPT', 'REJECT','DROP'),default_value='ACCEPT',enable_events=True, key='action',size=(10,3)),
                    sg.Button('Insert')
                
            ],
	
            [sg.Button('View'),sg.Button('Clear')],[sg.Output(size=(100,20),key="op")],
            
            [sg.Button('Delete'),sg.Text('Line number'), sg.InputText(key="delete",size=(10,1)),sg.Button('Flush')],
            
            
            
        ]   

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


def create_command(sip,dip,protocol,io,dport,sport): 
    command=""
                 
   
    if protocol!="":
        command+=" -p "
        command+=protocol
    if dport!="":
        command+=" --dport "
        command+=dport
    if dport!="":
        command+=" --sport "
        command+=sport
    if sip!="":
        if ':' in sip:
            command+= ' -m mac --mac-source '
        else:
            command+=" -s "
        command+=sip
    if dip!="":
        command+=" -d "
        command+=dip
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
        window.FindElement('op').Update('')
        
    if event in ('View'):
        cmd = 'sudo iptables -L --line-numbers'
        runCommand(cmd, window=window)
    if event in ('Change Policies'):
        cmd=""
        cmd="sudo iptables -P "+values["chain"]+" "+values["accept"]
        runCommand(cmd, window=window)
        print(cmd)
    if event in ('Insert'):
        cmd=""
        action=values['action']
        cmd="sudo iptables "+values["append"]+values["chain"]+create_command(values["sip"],values["dip"],values["protocol"],action,values["dport"],values["sport"])
        runCommand(cmd, window=window)
        print(cmd)
        
    if event in ('Clear'):   
        window.FindElement('op').Update('')

    if event in ('Delete'):   
        cmd ="sudo iptables -D "
        cmd=cmd+values['chain']+" "+values['delete']
        runCommand(cmd,window=window)
window.close()
    
