import getch as g

block = "\u2588"


def getkeypress():
  return g.getch()


class screen:
  print("\u001b[2J",end="",flush=True)
  def __init__(self,w,h,init=" "):
    print('\033[?25l', end="")
    self.screen = [[init for _2 in range(w) ] for _ in range(h//2)]
    self.h = h
    self.w = w
    print("\u001b[2J",end="",flush=True)
    
  def display(self):
    print("\u001b[0;0H\r")

    for a in self.screen:
      for b in a:
        print(b,end="")
      print()
  
  def update(self,x,y,char):
    self.screen[y//2][x] = char

  def fill(self,init=" "):
    self.screen = [[init for _2 in range(self.w) ] for _ in range(self.h//2)]


class rect:
  def __init__(self,x,y,c,sx,sy,s):
    self.x = x
    self.y = y
    self.char = c 
    self.s = s
    
    self.sizex = sx
    self.sizey = sy
  def draw(self):
    cords = []
    
    for x2 in range(self.x, self.x+self.sizex):
      for y2 in range(self.y,self.y+self.sizey):
        cords.append(tuple([x2,y2]))
    
    
    for cp in cords:
      
      self.s.update(*cp,self.char)  
    return cords
    
      
    
class circle:
  def __init__(self,x,y,r,s,c):
    self.x = x
    self.y = y
    self.rad = r
    self.screen = s
    self.char = c
  def draw(self):
    rady = self.rad//2
    end = self.y + rady
    start = self.y- rady
    ind = 0
    for yv in range(start,end):
      
      end = self.x + ((self.rad//4)-ind)
      
      start = self.x - ((self.rad//4)-ind)
    
      for xv in range(start, end):
        self.screen.update(xv,yv,self.char)
      if yv >= self.y:
        ind += 1
      else:
        ind -= 1

