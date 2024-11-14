import os
import subprocess as sp

paths = {
    'notepad': "C:\\Program Files\\WindowsApps\\Microsoft.WindowsNotepad_11.2309.28.0_x64__8wekyb3d8bbwe\\Notepad\\Notepad.exe",
    'discord': "C:\\Users\\ivann\\AppData\\Local\\Discord\\app-1.0.9025\\Discord.exe",
    'calculator': "C:\\Program Files\\WindowsApps\\Microsoft.WindowsCalculator_11.2307.4.0_x64__8wekyb3d8bbwe\\CalculatorApp.exe"
}


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def open_notepad():
    os.startfile(paths['notepad'])


def open_discord():
    os.startfile(paths['discord'])

def open_cmd():
    os.system('start cmd')

def open_calculator():
    sp.Popen(paths['calculator'])


