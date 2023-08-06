"""Terminal Typing, c 2023, GreenHexagon"""
import sys
from time import sleep

class TypingColor():
  """Class for Colors"""
  def __init__(self,r:int,g:int,b:int):
      if r > 255:
        raise ValueError
      if g > 255:
        raise ValueError
      if b > 255:
        raise ValueError
      self.r = r
      self.g = g
      self.b = b
      self.rgb = str(r) + str(g) + str(b)

class Typing():
  """Top level class for module"""
  def t_type(self, word:str, rgb:list | TypingColor | None, delay=0.25, newline=True):
    """Base typing module"""
    if rgb is None:
      rgb = TypingColor(0,0,0)
    if isinstance(rgb, list):
      r = rgb[0]
      g = rgb[1]
      b = rgb[2]
    if isinstance(rgb, TypingColor):
      r = rgb.r
      g = rgb.g
      b = rgb.b
    sys.stdout.write(f"\033[38;2;{r};{g};{b}m")
    sys.stdout.flush()
    for char in word:
      sys.stdout.write(char)
      sys.stdout.flush()
      sleep(delay)
    if newline:
      print("")
      print("\033[0m")
