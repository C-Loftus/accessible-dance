from __future__ import print_function
from inputs import get_gamepad, devices, UnpluggedError
import pyautogui, sys
from config import application_config
import automation

PRESSED = 1
RELEASED = 0

def handle_event(event, conf, gamepad) -> None:
 
    if event.ev_type == "Key":

        actions = conf.decode_press(gamepad, event.code)
        
        if event.state == PRESSED:
            for action in actions:
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
    conf = application_config()
    gamepad = str(devices.gamepads[0])

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
