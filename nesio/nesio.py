import RPi.GPIO as GPIO
import time
import socket
from enum import Enum

class ButtonEvent(Enum):
  UNDEFINED = 0
  PRESSED   = 1
  RELEASED  = 2
  NO_CHANGE = 3

class RpiButton:
    state: int
    name: str
    id: int
    mappedId: int
    event: ButtonEvent
    
    def __init__(self,name,id,mappedId):
      self.name  = name
      self.id    = id
      self.event = ButtonEvent.UNDEFINED
      self.state = int(GPIO.input(id))
      self.mappedId = mappedId
      
    def update(self):
      curState = int(GPIO.input(self.id))
      if self.state == 1 and curState == 0:
        self.event = ButtonEvent.PRESSED
      elif self.state == 0 and curState == 1:
        self.event = ButtonEvent.RELEASED
      else:
        self.event = ButtonEvent.NO_CHANGE
      self.state = curState

UDP_IP = "127.0.0.1"
UDP_PORT = 9090

# Define GPIOs for buttons
# My Raspberry Pi starts up with them as inputs
BTN_UP = 12 # Up
BTN_DN = 13 # Down
BTN_LT = 14 # Left
BTN_RT = 15 # Right
BTN_ER = 16 # Enter (Middle button)
BTN_A  = 17 # A
BTN_B  = 21 # B (GPIO18 apparently is turning 0 if screen gets black)
BTN_X  = 19 # X
BTN_Y  = 20 # Y

BTN_UP_MAPPED = 1 # Up
BTN_DN_MAPPED = 2 # Down
BTN_LT_MAPPED = 6 # Next
BTN_RT_MAPPED = 7 # Prev
BTN_ER_MAPPED = 4 # Select
BTN_A_MAPPED  = 8 # Escape
BTN_B_MAPPED  = 3 # Play
BTN_X_MAPPED  = 0 # Nothing
BTN_Y_MAPPED  = 5 # Back

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

# Set defined buttons to input
GPIO.setup(BTN_UP, GPIO.IN)
GPIO.setup(BTN_DN, GPIO.IN)
GPIO.setup(BTN_LT, GPIO.IN)
GPIO.setup(BTN_RT, GPIO.IN)
GPIO.setup(BTN_ER, GPIO.IN)
GPIO.setup(BTN_A,  GPIO.IN)
GPIO.setup(BTN_B,  GPIO.IN)
GPIO.setup(BTN_X,  GPIO.IN)
GPIO.setup(BTN_Y,  GPIO.IN)

nes_buttons = dict()

nes_buttons['BTN_UP'] = RpiButton('BTN_UP',BTN_UP,BTN_UP_MAPPED)
nes_buttons['BTN_DN'] = RpiButton('BTN_DN',BTN_DN,BTN_DN_MAPPED)
nes_buttons['BTN_LT'] = RpiButton('BTN_LT',BTN_LT,BTN_LT_MAPPED)
nes_buttons['BTN_RT'] = RpiButton('BTN_RT',BTN_RT,BTN_RT_MAPPED)
nes_buttons['BTN_ER'] = RpiButton('BTN_ER',BTN_ER,BTN_ER_MAPPED)
nes_buttons['BTN_A']  = RpiButton('BTN_A',BTN_A,BTN_A_MAPPED)
nes_buttons['BTN_B']  = RpiButton('BTN_B',BTN_B,BTN_B_MAPPED)
nes_buttons['BTN_X']  = RpiButton('BTN_X',BTN_X,BTN_X_MAPPED)
nes_buttons['BTN_Y']  = RpiButton('BTN_Y',BTN_Y,BTN_Y_MAPPED)

while True:
  for button in nes_buttons:
    nes_buttons[button].update()
    if(nes_buttons[button].event == ButtonEvent.PRESSED):
      print(nes_buttons[button].name + " pressed!")

      buttonMsg = [nes_buttons[button].mappedId,0,0]

      with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((UDP_IP, UDP_PORT))
        s.send(bytes(buttonMsg))
        print(" -> Sent socket message!")
    if(nes_buttons[button].event == ButtonEvent.RELEASED):
      print(nes_buttons[button].name + " released!")
  time.sleep(100/1000)

GPIO.cleanup() # cleanup all GPIO 