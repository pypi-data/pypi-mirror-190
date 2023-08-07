import turtle
import typing

import color

_screen = turtle.Screen()
_screen.tracer(0, 0)    # 默认关闭动画
_screen.listen()        # 默认开启监听

def setup(width : int = 800, height : int = 600):
    _screen.setup(width, height)
    
def title(title : str = "jrlogo"):
    _screen.title(title)
    
def bgcolor(c : color.Color = None):
    if c is None:
        return _screen.bgcolor()
    c = color.colorstr(c)
    return _screen.bgcolor(c)
    
def bgpic(filename : str):
    if filename is None:
        return _screen.bgpic()
    return _screen.bgpic(filename)

def done():
    _screen.mainloop()

def bye():
    _screen.bye()
    
if __name__=="__main__":
    setup()
    bgcolor(color.yellowgreen)
    done()