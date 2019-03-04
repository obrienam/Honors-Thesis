import buttonshim
import signal
import os
@buttonshim.on_press(buttonshim.BUTTON_A)
def handler(button, pressed):
	clear = lambda: os.system('clear')
	clear()
	print("A")
signal.pause()

