import PySimpleGUI as sg
import os

sg.theme('DarkAmber')  
layout = [  [sg.Text('Change Permissions')],
            [sg.Text('Enter IP'), sg.InputText()],
            [sg.Button('Accept'), sg.Button('Clear')] ]
window = sg.Window('Linux Firewall', layout)
while True:
    event, values = window.read()
    if event in (None,):  
        break
    if event in ('Clear'):
        cmd = 'sudo iptables -F'	
        os.system(cmd)
        os.system('sudo iptables -L')
        break
    print('You entered ', values[0])
    cm='sudo iptables -A INPUT -s '
    ccm=' -j ACCEPT'
    cam=cm+values[0]+ccm
    print (cam)
    os.system(cam)
    os.system('sudo iptables -L')    
window.close()

