# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 16:11:21 2019

@author: ravi9

FINAL MINE SWEEPER
"""
''' cleaning of code has to be performed still'''


import tkinter
from tkinter import ttk#,PhotoImage
from PIL import Image,ImageTk
import random

rows = 0    #size of rows
cols = 0    #size of cols
w = 40  # height and width of the cells
grid = list()
cell_reaveled = 0
top = tkinter.Tk()
top.wm_title("!!! Mine Sweeper !!!")
c = tkinter.Canvas(top, bg="white", height = 405, width = 405, bd = 0)
img = Image.open('ball.jpg')
c.image = ImageTk.PhotoImage(img)
bombs = 9
total_revealed = 0

class cell(object):
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w
        self.count = -1
        self.bomb = False
        self.reveled = False

def no_of_bomb(i, j):
    count = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            xoff = x + i
            yoff = y + j
            if xoff > -1 and xoff < 10 and yoff > -1 and yoff < 10:
                if grid[xoff][yoff].bomb == True :
                    count = count + 1
    return count

def draw_text(i,j,bomb_no):
    global c
    x = i * 40 + 20
    y = j*40 + 20

    c.create_text(x, y, text = bomb_no,fill = "red",font ="Verdana" )
    c.pack()

def draw_box(i,j,color):
    x1 = grid[i][j].x + 2
    y1 = grid[i][j].y + 2
    x2 = x1 + 40
    y2 = y1 + 40
    coord = x1, y1, x2, y2
    c.create_rectangle(coord, fill = color,outline = "black",width = 3)

def draw_bomb(i,j):
        global c
        x1 = grid[i][j].x
        y1 = grid[i][j].y
        c.create_image(x1+20, y1+20, image = c.image, anchor = "center")
        



def neigh(i,j):
    global grid
    #global total_revealed
    for x in range(-1, 2):
        for y in range(-1, 2):
            xoff = x + i
            yoff = y + j
            if xoff > -1 and xoff < 10 and yoff > -1 and yoff < 10 :
                if grid[xoff][yoff].bomb == False and grid[xoff][yoff].reveled == False:
                    grid[xoff][yoff].reveled = True
                    reaveled(xoff,yoff)


def callback(event):
    x = event.x
    y = event.y
    print(x,y)
    i = x//40
    j = y//40
    if grid[i][j].reveled == False:
        #grid[i][j].reveled = True
    
        reaveled(i,j)

def reaveled(i,j):
        global total_revealed
        if grid[i][j].bomb == True :
            draw_bomb(i,j)
            game_over()
            popupmsg("GameOver !!!")
        elif grid[i][j].bomb == False  :
            total_revealed += 1
            print (total_revealed)
            if grid[i][j].count == 0:
                draw_box(i,j,"grey")
                win(total_revealed)
                neigh(i, j)
            else:
                win(total_revealed)
                draw_text(i,j,grid[i][j].count)
                


def win(total):
    global total_revealed
    if(total_revealed == 97):
        total_revealed = 0
        game_over()
        popupmsg("You Win !!!!")


def game_over():
    rows = 10
    cols = 10
    for i in range(0, cols):
        for j in range(0, rows):
            if grid[i][j].reveled == False:
                grid[i][j].reveled = True
                if grid[i][j].bomb == True :
                    draw_bomb(i,j)
                elif grid[i][j].bomb == False  :
                    if grid[i][j].count == 0:
                        draw_box(i,j,"grey")
                    else:
                        draw_text(i,j,grid[i][j].count)
    global cell_reaveled
    return


c.bind("<Button-1>", callback)
c.pack()


def make2darray(cols, rows):
    e_list = list()
    for i in range(0, cols):
        new = list()
        for j in range(0, rows):
            new.append(None)
        e_list.append(new)

    return e_list



def draw_cell(cols, rows):
        global c
        global grid
        for i in range(0,cols):
            for j in range(0,rows):
                draw_box(i,j,"white")


def setting_bomb(cols, rows):
    global grid
    bomb_no = 0
    bomb_cols = list()
    bomb_rows = list()
    while bomb_no <= bombs :
        i = random.randint(0, (cols-1))
        j = random.randint(0, (rows-1))
               #used for debug
        if  i not in bomb_cols or j not in bomb_rows :
            print(i,j)
            bomb_cols.append(i)
            bomb_rows.append(j)
            grid[i][j].bomb = True
            bomb_no += 1



def popupmsg(msg):
    def deco():  #inner function for restart
        popup.destroy()
        setup()
        
    def deco1():#inner function for game over
        popup.destroy()
        top.destroy()
        
    
    popup = tkinter.Tk()
    label = ttk.Label(popup, text=msg,font = "Verdana", anchor = "n")
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Restart", command = deco)
    B1.pack()
    B2 = ttk.Button(popup, text="Quit", command = deco1)
    B2.pack()
    popup.mainloop()

    





def setup():
    height = 405
    width = 405
    rows = height // w
    cols = width // w
    global grid
    grid = make2darray(cols, rows)
    total_revealed = 0

    for i in range(0, cols):
            for j in range(0, rows):
                grid[i][j] = cell(i*w , j*w, w)
    setting_bomb(cols, rows)
    for i in range(0, cols):
        for j in range(0,rows):
            if  grid[i][j].bomb == False :
                grid[i][j].count = no_of_bomb(i,j)
        #print (grid[i][j].count, end = " ")

    draw_cell(cols,rows)
    top.mainloop()

setup()

