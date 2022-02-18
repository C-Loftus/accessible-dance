import enum

class Button(enum.Enum):
    SELECT = "SELECT"
    START  = "START"
    X      = "X"
    O      = "O"
    TRI    = "TRI"
    SQR    = "SQR"
    UP     = "UP"
    DOWN   = "DOWN"
    LEFT   = "LEFT"
    RIGHT  = "RIGHT"
    MID    = "MID"

class OSTENT:
    key_maps = {
    "BTN_BASE"    : Button.X,
    "BTN_BASE2"   : Button.O,
    "BTN_PINKIE"  : Button.TRI,
    "BTN_TOP2"    : Button.SQR,
    "BTN_THUMB2"  : Button.UP,
    "BTN_TRIGGER" : Button.LEFT,
    "BTN_TOP"     : Button.RIGHT,
    "BTN_THUMB"   : Button.DOWN,
    "BTN_ABS_Y"   : Button.MID,
    "BTN_BASE3"   : Button.SELECT,
    "BTN_BASE4"   : Button.START,
    }

    def decode_key(key) -> str:
        return OSTENT.key_maps[key].value

