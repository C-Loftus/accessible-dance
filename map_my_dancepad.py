
from __future__ import print_function


from inputs import get_gamepad


def main():
    """Just print out some event infomation when the gamepad is used."""
    while 1:
        events = get_gamepad()
        for event in events:
            if event.ev_type == "Key" and event.state == 1:
                message = f'You presses key "{event.code}"'
                print(message)


if __name__ == "__main__":
    main()
