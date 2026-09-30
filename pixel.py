#import turtle module as t for graphics
import turtle as t
from turtle import Turtle
#instantiating the class, so we can use it
r = Turtle()
 
#RGB codes which are used in the map
R = (255, 0, 0) #red
B = (0, 0, 0) #black
P = (130, 81, 22) #brown (called it p for poop)
W = (255, 255, 255) #white
T = (242, 185, 153) #tan
Y = (253, 212, 122) #yellow
 
SIDE_LENGTH = 20 #side length for each pixel
 
screen = t.Screen() #screen setup
screen.setup(width=520,height=520)
screen.screensize(480, 480) #setting screen size
t.colormode(255) #lets us use RGB values
 
t.tracer(0) #instant pixel art
 
#Each character is a pixel, and each element is a row
map = ["WWWWWWWWWWWWWWBBBBBBBBWW",
       "WWWWWWWWWWWWWBPPPPPPPBBW",
       "WWWWWWWWWWWWBPPPPPPPPBWW",
       "WWWWWWWBBBBBPPPTTTTTBWWW",
       "WWWWWWBPPPPBPPTBBBTBBBWW",
       "WWWWWBPPPPBTPPTTWBBWBWWW",
       "WWWWBPPPPPBTTPPTWBTWBWWW",
       "WWWBPPPPPPBTTTTTTTBTBBWW",
       "WWBPPPPPPPPBBTTTTTTTTTBW",
       "WWBPPPPPPPPPBTBBTTTTTTTB",
       "WWBPPPPBPBPPBTTTBBBBBBBW",
       "WWBPPPPPBPPTBBTTTTTTTBWW",
       "WBBPPPPPBTTTTBBBBBBBBWWW",
       "BPBBPPPPPBTTTBRRBPPPBWWW",
       "BPPBPPPPPPBTTBRRRBPPPBWW",
       "BPPPBPPPPPPBTBRRRBPPPPBW",
       "BPPPPBPPPPPBTBYYRBPPPPBW",
       "WBPPPPBPPTTBTBYRYBBPPTTB",
       "WWBPPPBTTTTTBBRRRBBBTTTB",
       "WBPPPPBTTTTTBPBRBWBTTTTB",
       "WBTTTTBTTTTTBTBBWWBTBTTB",
       "WBBTTTBBTTTTBTTTBWBBBTTB",
       "WWBBBBBTTTTTBBBBBWWBTTTB",
       "WWWWWWBBBBBBXWWWWWWBBBBW"]
 
#function to draw a square with any color needed
#also goes forward SIDE_LENGTH pixels afterwards to make row effect easier to do
def drawSquare(color):
    r.begin_fill()
    r.pencolor(color)
    r.fillcolor(color)
    for i in range(4):
        r.forward(SIDE_LENGTH)
        r.right(90)
    r.end_fill()
    r.forward(SIDE_LENGTH)
 
#initial screen and turtle setup
X = -230 #staring x coordinate
y = 230 #starting y coordinate
r.penup()
r.goto(X, y)
r.pendown()
 
#takes each pixel of the element in each row and draws a colored square based on the current letter of the map
for i in range(len(map)): #looking at each element (row) in the list
    for j in range(len(map[i])): #looking at each character (pixel) in each element
        if map[i][j] == "W":
            drawSquare(W)
        elif map[i][j] == "B":
            drawSquare(B)
        elif map[i][j] == "P":
            drawSquare(P)
        elif map[i][j] == "R":
            drawSquare(R)
        elif map[i][j] == "T":
            drawSquare(T)
        elif map[i][j] == "Y":
            drawSquare(Y)
        else:
            print('letter not found...')
    y -= 20 #changing the y coordinate 20 units down, so we can go to the next row
    r.penup()
    r.goto(X, y)  
    r.pendown() #gets the turtle ready to start drawing the next row  
t.done()
