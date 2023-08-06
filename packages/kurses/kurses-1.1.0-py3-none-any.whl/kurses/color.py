def rgb(r, g, b): return f"\u001b[38;2;{r};{g};{b}m"
def rgb_bg(r, g, b): return f"\u001b[48;2;{r};{g};{b}m"


red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

purple = (255,0,255)
yellow = (255,255,0)
cyan = (0,255,255)

white = (255,255,255)
black = (0,0,0)

def colored(text, fg=(255,255,255),bg=(0,0,0)):
  
  return rgb(*fg) + rgb_bg(*bg) + text + "\u001b[0m"
  




