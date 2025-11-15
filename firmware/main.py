# You import all the IOs of your board
import board
import busio

# These are imports from the kmk library
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.keys import KC
from kmk.extensions.RGB import RGB
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.macros import Press, Release, Tap, Macros

# This is the main instance of your keyboard
keyboard = KMKKeyboard()

# display: see https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/Display.md
i2c_bus = busio.I2C(board.D5, board.D4)
driver = SSD1306(
    # Mandatory:
    i2c=i2c_bus,
    device_address=0x3C
)

# For all display types
display = Display(
    # Mandatory:
    display=driver,
    # Optional:
    width=128, # screen size
    height=32, # screen size
    flip = False, # flips your display content
    flip_left = False, # flips your display content on left side split
    flip_right = False, # flips your display content on right side split
    brightness=0.8, # initial screen brightness level
    brightness_step=0.1, # used for brightness increase/decrease keycodes
    dim_time=20, # time in seconds to reduce screen brightness
    dim_target=0.1, # set level for brightness decrease
    off_time=120, # time in seconds to turn off screen
    powersave_dim_time=10, # time in seconds to reduce screen brightness
    powersave_dim_target=0.1, # set level for brightness decrease
    powersave_off_time=30, # time in seconds to turn off screen
    entries=[
        TextEntry(text='wasd', x=0, y=0, inverted=False, layer=0),
        TextEntry(text='media', x=12, y=0, inverted=False, layer=1),
        TextEntry(text='undertale', x=24, y=0, inverted=False, layer=2),
    ],
)


# Add the macro extension
macros = Macros()
keyboard.modules.append(macros)

# layers: see https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/layers.md
keyboard.modules.append(Layers())

# holdtap: see https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/holdtap.md
holdtap = HoldTap()
holdtap.tap_time = 300
keyboard.modules.append(holdtap)

# rgb: see https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/rgb.md
rgb = RGB(pixel_pin=board.D10, num_pixels=8,
          val_limit=100,
          rgb_order=(1, 0, 2),
          animation_mode = "swirl")
keyboard.extensions.append(rgb)


# media keys: see https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/media_keys.md
keyboard.extensions.append(MediaKeys())

# Define your pins here!
keyboard.col_pins = (board.D0, board.D1, board.D2)
keyboard.row_pins = (board.D3, board.D6)
keyboard.diode_orientation = DiodeOrientation.COL2ROW



# Here you define the buttons corresponding to the pins
# Look here for keycodes: https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/keycodes.md
# And here for macros: https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/macros.md

MDIA = KC.LT(1, KC.Q, prefer_hold=False) # media (volume + layer selection)
keyboard.keymap = [
	# Base layer
	[
		MDIA,   KC.W,   KC.E,	
		KC.A,   KC.S,   KC.D,
	],

	# music controls
	[
		KC.MPLY, KC.VOLU,KC.MNXT,
		KC.LT(0),KC.VOLD,KC.LT(2),	
	],

    # arrow keys instead of wasd
    [
		MDIA,   KC.UP,  KC.E,	
		KC.LEFT,KC.DOWN,KC.RIGHT,
    ]

]

# Start kmk!
if __name__ == '__main__':
    keyboard.go()