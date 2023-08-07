import turtle
import typing

import color
import shape

_turtles = [] # type: typing.List[Turtle]

class Turtle:
    def __init__(self) -> None:
        self._turtle = turtle.Turtle()
        self.up()   # 默认抬起画笔
        self.shape(shape.turtle)    # 默认形状为乌龟
        
    def forward(self, distance : float):
        """向前移动指定距离"""
        self._turtle.forward(distance)
    fd = forward
        
    def backward(self, distance : float):
        """向后移动指定距离"""
        self._turtle.backward(distance)
    back = bk = backward
        
    def left(self, angle : float):
        """向左转动指定角度"""
        self._turtle.left(angle)
    lt = left
    
    def right(self, angle : float):
        """向右转动指定角度"""
        self._turtle.right(angle)
    rt = right
    
    def goto(self, x : float, y : float):
        """移动到指定位置"""
        self._turtle.goto(x, y)
    setpos = setposition = goto
    
    def head(self, angle : float):
        """设置朝向"""
        self._turtle.setheading(angle)
    seth = setheading = head
    
    def home(self):
        """移动到原点"""
        self._turtle.home()
        
    def circle(self, radius, extent=None, steps=None):
        """画圆"""
        self._turtle.circle(radius, extent, steps)
        
    def dot(self, size=None, c : color.Color = None):
        """画点"""
        if c is None:
            self._turtle.dot(size)
        else:
            self._turtle.dot(size, color.colorstr(c))
    
    def stamp(self):
        """画图章"""
        self._turtle.stamp()
    
    def clearstamp(self, stampid):
        """清除图章"""
        self._turtle.clearstamp(stampid)
        
    def undo(self):
        """撤销"""
        self._turtle.undo()
        
    def pos(self):
        """获取位置"""
        return self._turtle.pos()
    position = pos
    
    def xcor(self):
        """获取x坐标"""
        return self._turtle.xcor()
    x = xcor
    
    def ycor(self):
        """获取y坐标"""
        return self._turtle.ycor()
    y = ycor
    
    def heading(self):
        """获取朝向"""
        return self._turtle.heading()

    def penup(self):
        """抬起画笔"""
        self._turtle.up()
    pu = up = penup
    
    def pendown(self):
        """落下画笔"""
        self._turtle.down()
    pd = down = pendown
    
    def isdown(self) -> bool:
        """获取画笔状态"""
        return self._turtle.isdown()
    
    def pensize(self, width=None):
        """设置画笔宽度"""
        self._turtle.pensize(width)
    width = pensize
    
    def pencolor(self, c : color.Color = None) -> color.Color:
        """设置画笔颜色"""
        if c is None:
            return self._turtle.pencolor()
        c = color.colorstr(c)
        self._turtle.pencolor(c)
        return c
    
    def fillcolor(self, c : color.Color = None) -> color.Color:
        """设置填充颜色"""
        if c is None:
            return self._turtle.fillcolor()
        c = color.colorstr(c)
        self._turtle.fillcolor(c)
        return c
    
    def filling(self) -> bool:
        """获取填充状态"""
        return self._turtle.filling()
    
    def beginfill(self):
        """开始填充"""
        self._turtle.begin_fill()
        
    def endfill(self):
        """结束填充"""
        self._turtle.end_fill()
    
    def write(self, arg, move=False, align="left", font=("Console", 8, "normal")):
        """写字"""
        self._turtle.write(arg, move, align, font)
        
    def hide(self):
        """隐藏"""
        self._turtle.hideturtle()
    
    def show(self):
        """显示"""
        self._turtle.showturtle()
        
    def shape(self, s : shape.Shape):
        """设置形状"""
        turtle.register_shape(s[0], shape=s[1])
        self._turtle.shape(s[0])
        
    def clone(self):
        """复制"""
        t = Turtle()
        t._turtle = self._turtle.clone()
        return t