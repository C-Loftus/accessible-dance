from os import environ
import subprocess
import pyautogui
from subprocess import Popen, PIPE

def is_talon(cmd) -> bool:
    return "mimic:" in cmd

def is_shell(cmd) -> bool:
    return "shell:" in cmd

def run_talon_mimic(cmd) -> None:
    try:
        talon_cmd = cmd.split("mimic:")[1].strip()
        shell_cmd = f'echo "mimic(\'{talon_cmd}\')" | ~/.talon/bin/repl'
        p = Popen(shell_cmd, shell=True)
        print("Running Talon Mimic for: " + talon_cmd)
        p.wait()
    except:
        print("Failed to run Talon Mimic")

def run_shell(cmd) -> None:
    shell = environ['SHELL']
    try:
        shell_cmd = cmd.split("shell:")[1].strip()
        subprocess.call([shell, '-i', '-c', shell_cmd])
    except:
        print("Failed to run shell command")

def run_action(action) -> None:
    print("Running action: " + action)

    multiple_keys = action.split(" ")
    if action == 'scrolldown':
            pyautogui.scroll(-5)
    elif action == 'scrollup':
        pyautogui.scroll(5)
    elif len(multiple_keys) > 1:
        pyautogui.hotkey(*multiple_keys) 
    else: 
        pyautogui.keyDown(action)


def perform_action(action) -> None:
    if is_talon(action):
        run_talon_mimic(action)
    elif is_shell(action):
        run_shell(action)
    else:
        run_action(action)