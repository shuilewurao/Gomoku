from tkinter import *
import tkinter.messagebox

global entry1, entry2, player1, player2
global c
global who

who = 0

r = Tk()
f = Frame(r)
c = Canvas(r)
text_var = StringVar(r)

def board_init () :
    global board
    board = [['empty' for x in range(15)] for x in range(15)]
    
def check_legality(row, col) :
    
    if (board[int((row - 2) / 29)][int((col - 2) / 29)] == 'empty') :
        return TRUE
    else :
        return FALSE

def check_win(a, b, color) :
    row = int((a - 2) / 29)
    col = int((b - 2) / 29)
    endRow = 0
    endCol = 0

    direct = [-1 ,0 , 1]
    for x in direct:
        for y in direct:
            endRow = 0
            endCol = 0
            if x == y == 0:
                continue
            else:
                for z in [1, 2, 3, 4]:
                    y_coor = row + z * y
                    x_coor = col + z * x 
                    if(y_coor > 14 or x_coor > 14):
                        break
                    if board[y_coor][x_coor] == color:
                        endRow = row + z * y
                        endCol = col + z * x
            #print(color +": end--"+str(endCol)+":"+str(endRow))
            for z in [1, 2, 3, 4]:
                y_coor = endRow + z * (-1 * y)
                x_coor = endCol + z * (-1 * x)
                if(y_coor > 14 or x_coor > 14):
                    break
                if board[y_coor][x_coor] == color:
                    #print(board[row + z * (-1 * y)][col + z * (-1 * x)]+" Z: "+str(z))
                    if z == 4:
                        tkinter.messagebox.showinfo ('WINNER', color + ' is the Winner!')
                        restart()
                else:
                    break

def playRound(event):
    global who
    
    color = ''
    
    if(who == 0):
        color = 'black'
    else:
        color = 'white'     
    
    pointer_x = r.winfo_pointerx() - r.winfo_rootx()
    pointer_y = r.winfo_pointery() - r.winfo_rooty()
    
    #print ("pointer: " + str(pointer_y))
    #print ("event: " + str(event.y))

    # offset is 104 for x and y
    canvas_x = pointer_x - 104
    canvas_y = pointer_y - 104

    draw_x = round(float(canvas_x / 29)) * 29 + 2
    draw_y = round(float(canvas_y / 29)) * 29 + 2    
    
    #print ("draw pos: " + str(draw_x) + ", " + str(draw_y))
    #print ("board loc: " + str(int((draw_x - 2) / 29)) + " " + str(int((draw_y - 2) / 29)))
    
    # draw pieces
    legality = check_legality(draw_y, draw_x)
    if (legality) :
        circle = c.create_oval(draw_x - 13, draw_y - 13, draw_x + 13, draw_y + 13, fill = color)
        board[int((draw_y - 2) / 29)][int((draw_x - 2) / 29)] = color
        
        check_win(draw_y, draw_x, color)
        
        who = (who + 1) % 2
        if(who == 0):
            if (not player1) :
                text_var.set("Player 1's move")
            else :
                text_var.set(player1 + "'s move")
        else:
            if (not player2) :
                text_var.set("Player 2's move")
            else :
                text_var.set(player2 + "'s move")                
    else :
        tkinter.messagebox.showerror('Invalid Move', 'Please place tile on a legal location')

def create_grid (event = None):
    global c, players_turn
    
    board_init()
    
    w = 408 # Get current width of canvas
    h = 408 # Get current height of canvas
    c.delete('grid_line') # Will only remove the grid_line
    c.create_line(408, 2, 408, 408)
    c.create_line(2, 408, 408, 408)
    
    # Creates 15 vertical lines
    for i in range(2, w, 29):
        c.create_line([(i, 0), (i, h)])

    # Creates 15 horizontal lines
    for i in range(2, h, 29):
        c.create_line([(0, i), (w, i)])
    
    # set turn
    if (not player1) :
        text_var.set("Player 1's move")
    else :
        text_var.set(player1 + "'s move")
        
    players_turn = Label(f, textvariable = text_var, font = ('Helvetica', 18), fg = 'grey')
    players_turn.pack(pady = 35) 
    f.pack()

def switch_focus(event = None):
    global entry1, entry2, player1, player2
    
    player1 = entry1.get()
    entry2.focus_set()
    print ("Player 1 is: " + player1)

def start_game(event = None):
    global entry1, entry2, player1, player2, c
    f.pack_forget()
    
    player2 = entry2.get()
    print ("Player 2 is: " + player2)
    
    for widget in f.winfo_children():
        widget.destroy()

    c_height = 14*30
    c_width = 14*30
    r_height = c_height + 200
    r_width = c_width + 200
    
    screen_height = r.winfo_screenheight()
    screen_width = r.winfo_screenwidth()
    
    x = (screen_width/2) - (r_width/2)
    y = (screen_height/2) - (r_height/2)
    
    r.geometry("%dx%d+%d+%d" % (r_width, r_height, x, y))
    
    c = Canvas(r, height = 408, width = 408, bg = 'white')
    c.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    c.bind('<Configure>', create_grid)
    r.bind("<Button-1>", playRound)

def new_game(event = None):
    global entry1, entry2, c
    
    for widget in f.winfo_children():
        widget.destroy()
    
    r_width = 500
    r_height = 500

    screen_height = r.winfo_screenheight()
    screen_width = r.winfo_screenwidth()
 
    x = (screen_width/2) - (r_width/2)
    y = (screen_height/2) - (r_height/2)
    
    r.geometry('%dx%d+%d+%d' % (r_width, r_height, x, y))
    
    text = Label(f, text = 'Press Enter to Record Your Name!', font = ('Helvetica', 18), height = 8)
    text.pack()
    
    entry_f = Frame(f)
    label1 = Label(entry_f, text = 'Enter Name for Player 1: ', font = ('Helvetica', 12))
    entry1 = Entry(entry_f)
    label2 = Label(entry_f, text = 'Enter Name for Player 2: ', font = ('Helvetica', 12))
    entry2 = Entry(entry_f)
    
    label1.grid(column = 0, row = 0)
    entry1.grid(column = 1, row = 0)    
    label2.grid(column = 0, row = 1)
    entry2.grid(column = 1, row = 1)
    
    entry1.focus_set()
    entry1.bind('<Return>', switch_focus)
    
    entry2.bind('<Return>', start_game)
    
    entry_f.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    entry_f.pack()
    
    print ('New game!')
    
# menu and game commands
def restart(event = None):
    #global players_turn
    
    for ele in f.winfo_children():
        ele.destroy()
    c.place_forget()
    
    main()
    
def quit_program(event = None):
    r.destroy()
    print ('Goodbye!')
    
def show_gomoku_rule(event = None) :
    tkinter.messagebox.showinfo('Gomoku Rules', "Gomoku or Go-moku or Five in line, is a traditional oriental game, originally from China. In Japanese language Go means five, and moku pieces (or eyes or dots). \n\nBlack plays first, and players alternate in placing a stone of their color on an empty intersection. The winner is the first player to get an unbroken row of five stones horizontally, vertically, or diagonally.")
    print ('Show Rule')

def show_help(event = None):
    tkinter.messagebox.showinfo('Help', 'Ctrl + G to show rules\n\nCtrl + R to restart\n\nCtrl + Q to quit')
    print ('Show Help')


def create_root_window(event = None) :
    r.title('GomoKu')
    
    # config key bindings
    r.bind('<Control-Shift-R>', restart)
    r.bind('<Control-Shift-Q>', quit_program)
    r.bind('<Control-Shift-G>', show_gomoku_rule)
    r.bind('<Control-Shift-H>', show_help)
    
    # config window size and position
    r.resizable(width = FALSE, height = FALSE)
    screen_height = r.winfo_screenheight()
    screen_width = r.winfo_screenwidth()
    
    r_width = 500
    r_height = 500
    
    x = (screen_width/2) - (r_width/2)
    y = (screen_height/2) - (r_height/2)
    
    r.geometry('%dx%d+%d+%d' % (r_width, r_height, x, y))    
    
    # config menu 
    menu = Menu(r)
    
    gamemenu = Menu(menu, tearoff = 0)
    gamemenu.add_command(label = 'Restart      Ctrl+R', command = restart)
    gamemenu.add_separator()
    gamemenu.add_command(label = 'Quit         Ctrl+Q', command = quit_program)
    menu.add_cascade(label = 'Game', menu = gamemenu)
    
    helpmenu = Menu(menu, tearoff = 0)
    helpmenu.add_command(label = 'Rules        Ctrl+G', command = show_gomoku_rule)
    helpmenu.add_command(label = 'Help         Ctrl+H', command = show_help)
    menu.add_cascade(label = 'Help', menu = helpmenu)
    
    r.config(menu = menu)
    
    # config welcome image
    spacer = Frame(f, height = 20)
    spacer.pack()
    
    title_img = PhotoImage(file = 'Title.png')
    render = Label(f, image = title_img)
    render.pack()
    
    gomoku_img = PhotoImage(file = 'gomoku.png')
    render = Label (f, image = gomoku_img)
    render.pack()
    
    spacer = Frame(f, height = 5)
    spacer.pack()
    
    # config welcome text
    start = Button(f,  text = 'Start New Game!', font = ('Helvetica', 26), fg = 'white', bg = 'grey', command = new_game)
    start.pack()
    
    f.pack()

    r.mainloop()
    
def main():
    create_root_window()
    r.mainloop()
    
if __name__ == '__main__':
    main()
    
    
def hh():

    #\
    # \
    #
    #
    while (board[row][col] == color and row < 15 and row >= 0 and col < 15 and col >= 0) :
        cnt += 1
        row -= 1
        col -= 1
    print ("1: " + str(cnt))
    check_cnt(cnt)
    cnt = 0
    row = int((x - 2) / 29)
    col = int((y - 2) / 29)    
    #  |
    #  |
    # 
    #
    while (board[row][col] == color and row < 15 and row >= 0 and col < 15 and col >= 0) :
        cnt += 1
        row -= 1
    print ("2: " + str(cnt))
    check_cnt(cnt)
    cnt = 0
    row = int((x - 2) / 29)
    col = int((y - 2) / 29)    
    #   /
    #  /
    #
    while (board[row][col] == color and row < 15 and row >= 0 and col < 15 and col >= 0) :
        cnt += 1
        row -= 1
        col += 1
    print ("3: " + str(cnt))
    check_cnt(cnt)
    cnt = 0
    row = int((x - 2) / 29)
    col = int((y - 2) / 29)    
    #
    #--
    #
    while (board[row][col] == color and row < 15 and row >= 0 and col < 15 and col >= 0) :
        cnt += 1
        col -= 1
    print ("4: " + str(cnt))
    check_cnt(cnt)
    cnt = 0
    row = int((x - 2) / 29)
    col = int((y - 2) / 29)    
    #
    #  --
    #
    while (board[row][col] == color and row < 15 and row >= 0 and col < 15 and col >= 0) :
        cnt += 1
        col += 1
    print ("5: " + str(cnt))
    check_cnt(cnt)
    cnt = 0
    row = int((x - 2) / 29)
    col = int((y - 2) / 29)    
    #
    # /
    #/
    while (board[row][col] == color and row < 15 and row >= 0 and col < 15 and col >= 0) :
        cnt += 1
        row += 1
        col -= 1
    print ("6: " + str(cnt))
    check_cnt(cnt)
    cnt = 0
    row = int((x - 2) / 29)
    col = int((y - 2) / 29)    
    
    #
    #  |
    #  |
    while (board[row][col] == color and row < 15 and row >= 0 and col < 15 and col >= 0) :
        cnt += 1
        row += 1
    print ("7: " + str(cnt))
    check_cnt(cnt)
    cnt = 0
    row = int((x - 2) / 29)
    col = int((y - 2) / 29)    
    #
    #  \
    #   \
    while (board[row][col] == color and row < 15 and row >= 0 and col < 15 and col >= 0) :
        cnt += 1
        row += 1
        col += 1
    print ("8: " + str(cnt))
    check_cnt(cnt)
    cnt = 0    