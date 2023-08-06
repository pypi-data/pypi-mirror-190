[![PyPI version](https://badge.fury.io/py/TerminalTyping.svg)](https://www.github.com/GreenHexagon/type)
# TerminalTyping
Module for terminal type effects  

## Documentation

"-argument": Delcares an argument as optional.


### Typing 
A class that serves as the overarching class. To use any of the following functions, it must be defined.
```py 
import TerminalTyping

typing = TerminalTyping.Typing()
```

### Typing.t_type(word:string, rgb:list, -delay:float, -newline:boolean)
  
*word: What will be passed in to "type" to the terminal*  
*rgb: The color of the text. [r value, g value, b value]. Defaults to [0,0,0] or TypingColor(0,0,0)*  
*delay: the delay between each character in seconds.*  
*newline: whether or not a new line is created after the typing is done. Defaults to true.*

```py
import TerminalTyping

typing = TerminalTyping.Typing()
typing.ttype("word",[1,255,0],1, True)
```

### TypingColor(r, g, b)
A custom clas that can be passed into [the typing class](#typing) instead of passing in a list.
