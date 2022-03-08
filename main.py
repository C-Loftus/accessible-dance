from __future__ import print_function
from inputs import get_gamepad, devices, UnpluggedError
import pyautogui, sys
from config import application_config
import automation

import sys, os, time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

PRESSED = 1
RELEASED = 0

conf = application_config()
class ConfigWatcher(LoggingEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.yaml'):
            print("Config file changed and reloaded")
            # just makes message passing easy for this simple case
            global conf
            conf = application_config()

def handle_event(event, conf, gamepad) -> None:
 
    if event.ev_type == "Key":

        actions = conf.decode_step(gamepad, event.code)
        
        if event.state == PRESSED:
            for action in actions:
                # needed to not drop commands due to going too quickly
                time.sleep(.2)
                automation.perform_action(action)

        elif event.state == RELEASED:
            for action in actions:
                pyautogui.keyUp(action)

####### TODO ########
    elif event == "Sync":
        pass
    elif event == "Misc":
        pass

def main():
    
    ROOT_DIR = os.path.realpath(os.path.dirname(__file__))

    event_handler = ConfigWatcher()
    observer = Observer()
    observer.schedule(event_handler, path=ROOT_DIR, recursive=False)
    observer.start()

    global conf

    while 1:

        try:
            events = get_gamepad()
            gamepad = str(devices.gamepads[0])
        
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            sys.exit(0)

        except UnpluggedError:
            text = "No Device Found in Your Plugged in Devices: \n\n" + "\n".join(str(d) for d in devices)
            pyautogui.alert(text, title='Failure to find dancepad', button='OK')
            observer.stop()
            observer.join()
            sys.exit(1)

        for event in events:
            handle_event(event, conf, gamepad)


if __name__ == "__main__":
    main()
