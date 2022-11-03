import getch
import socket
import struct
from enum import Enum

UDP_IP = "127.0.0.1"
UDP_PORT = 9090

BTN_UP    = 1 # Up
BTN_DOWN  = 2 # Down
BTN_PLAY  = 3 # Play
BTN_SEL   = 4 # Select
BTN_BACK  = 5 # Back
BTN_NEXT  = 6 # Next
BTN_PREV  = 7 # Prev
BTN_ESC   = 8 # Esc

while True:
  key = getch.getch().lower()
  sendKey = 0
  
  if(key == "w"):
    sendKey = BTN_UP
  if(key == "a"):
    sendKey = BTN_NEXT
  if(key == "s"):
    sendKey = BTN_DOWN
  if(key == "d"):
    sendKey = BTN_PREV

  buttonMsg = [sendKey,0,0]

  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
      s.connect((UDP_IP, UDP_PORT))
      s.send(bytes(buttonMsg))