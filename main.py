from __future__ import print_function
from inputs import get_gamepad, devices, UnpluggedError
import pyautogui, sys
from config import application_config
from manufacturer import OSTENT
from subprocess import Popen, PIPE
from os import environ
import subprocess

def check_talon_mimic(cmd) -> None:
    try:
        talon_cmd = cmd.split("mimic:")[1].strip()
        shell_cmd = f'echo "mimic(\'{talon_cmd}\')" | ~/.talon/bin/repl'
        p = Popen(shell_cmd, shell=True)
        print("Running Talon Mimic for: " + talon_cmd)
        p.wait()
        return True
    except:
        return False

def check_shell(cmd) -> None:
    shell = environ['SHELL']
    try:
        shell_cmd = cmd.split("shell:")[1].strip()
        subprocess.call([shell, '-i', '-c', shell_cmd])
        return True
    except:
        return False

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
        pyautogui.press(action)

def parse_keys_to_actions(keys, conf, event) -> list:
    key = OSTENT.decode_key(event.code)
    actions = conf.get_config()[key]
    return actions

def handle_event(event, conf, gamepad) -> None:
    PRESSED = 1
    RELEASED = 0

    if event.ev_type == "Key":
        actions = parse_keys_to_actions(event.code, conf, event)
        
        if event.state == PRESSED:
            for action in actions:
                if check_talon_mimic(action) == False and \
                    check_shell(action) == False:

                    run_action(action)

        elif event.state == RELEASED:
            for action in actions:
                pyautogui.keyUp(action)
####### TODO ########
    elif event == "Sync":
        pass
    elif event == "Misc":
        pass



def main():
    conf = application_config()
    gamepad = devices.gamepads[0]  

    while 1:

        try:
            events = get_gamepad()
        except KeyboardInterrupt:
            sys.exit(0)
        except UnpluggedError:
            text = "No Device Found in Your Plugged in Devices: \n\n" + "\n".join(str(d) for d in devices)
            pyautogui.alert(text, title='Failure to find dancepad', button='OK')
            sys.exit(1)

        for event in events:
            handle_event(event, conf, gamepad)


if __name__ == "__main__":
    main()
