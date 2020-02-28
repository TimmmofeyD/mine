from tkinter import *
from tkinter import messagebox 
import random
from collections import deque
class Minesweeper:
    def __init__(self, master):
        self.tile_plain = PhotoImage(file="images/tile_plain.png")
        self.tile_clicked = PhotoImage(file="images/tile_clicked.png")
        self.tile_mine = PhotoImage(file="images/tile_mine.png")
        self.tile_flag = PhotoImage(file="images/tile_flag.png")
        self.tile_wrong = PhotoImage(file="images/tile_wrong.png")
        self.tile_no = []
        for x in range(1, 9):
            self.tile_no.append(PhotoImage(file="images/tile_"+str(x)+".png"))
        frame = Frame(master)
        frame.pack()
        self.label1 = Label(frame, text="Сапер")
        self.label1.grid(row=0, column=0, columnspan=10)
        self.flags = 0
        self.correct_flags = 0
        self.clicked = 0
        self.buttons = dict({})
        self.mines = 0
        x_coord = 1
        y_coord = 0
        for x in range(0, 100):
            mine = 0
            gfx = self.tile_plain
            if random.uniform(0.0, 0.5) < 0.1:
                mine = 1
                self.mines += 1
            self.buttons[x] = [Button(frame, image=gfx),
                               mine,
                               0,
                               x,
                               [x_coord, y_coord],
                               0]
            self.buttons[x][0].bind('<Button-1>', self.lclicked_wrapper(x))
            self.buttons[x][0].bind('<Button-3>', self.rclicked_wrapper(x)) 
            y_coord += 1
            if y_coord == 10:
                y_coord = 0
                x_coord += 1
        for key in self.buttons:
            self.buttons[key][0].grid(
                row=self.buttons[key][4][0], column=self.buttons[key][4][1])
        for key in self.buttons:
            nearby_mines = 0
            if self.check_for_mines(key-9):
                nearby_mines += 1
            if self.check_for_mines(key-10):
                nearby_mines += 1
            if self.check_for_mines(key-11):
                nearby_mines += 1
            if self.check_for_mines(key-1):
                nearby_mines += 1
            if self.check_for_mines(key+1):
                nearby_mines += 1
            if self.check_for_mines(key+9):
                nearby_mines += 1
            if self.check_for_mines(key+10):
                nearby_mines += 1
            if self.check_for_mines(key+11):
                nearby_mines += 1
            self.buttons[key][5] = nearby_mines
        self.label2 = Label(frame, text="Мины: "+str(self.mines))
        self.label2.grid(row=11, column=0, columnspan=5)

        self.label3 = Label(frame, text="Флажки: "+str(self.flags))
        self.label3.grid(row=11, column=4, columnspan=5)
    def check_for_mines(self, key):
        try:
            if self.buttons[key][1] == 1:
                return True
        except KeyError:
            pass
    def lclicked_wrapper(self, x): 
        return lambda Button: self.lclicked(self.buttons[x])
    def rclicked_wrapper(self, x):
        return lambda Button: self.rclicked(self.buttons[x])
    def lclicked(self, button_data):
        if button_data[1] == 1:
            for key in self.buttons:
                if self.buttons[key][1] != 1 and self.buttons[key][2] == 2:
                    self.buttons[key][0].config(image=self.tile_wrong)
                if self.buttons[key][1] == 1 and self.buttons[key][2] != 2:
                    self.buttons[key][0].config(image=self.tile_mine)
            self.gameover()
        else:
            if button_data[5] == 0:
                button_data[0].config(image=self.tile_clicked)
                self.clear_empty_tiles(button_data[3])
            else:
                button_data[0].config(image=self.tile_no[button_data[5]-1])
            if button_data[2] != 1:
                button_data[2] = 1
                self.clicked += 1
            if self.clicked == 100 - self.mines:
                self.victory()
    def rclicked(self, button_data):
        if button_data[2] == 0:
            button_data[0].config(image=self.tile_flag)
            button_data[2] = 2
            button_data[0].unbind('<Button-1>')
            if button_data[1] == 1:
                self.correct_flags += 1
            self.flags += 1
            self.update_flags()
        elif button_data[2] == 2:
            button_data[0].config(image=self.tile_plain)
            button_data[2] = 0
            button_data[0].bind(
                '<Button-1>', self.lclicked_wrapper(button_data[3]))
            if button_data[1] == 1:
                self.correct_flags -= 1 
            self.flags -= 1
            self.update_flags()
    def check_tile(self, key, queue):
        try:
            if self.buttons[key][2] == 0:
                if self.buttons[key][5] == 0:
                    self.buttons[key][0].config(image=self.tile_clicked)
                    queue.append(key)
                else:
                    self.buttons[key][0].config(
                        image=self.tile_no[self.buttons[key][5]-1])
                self.buttons[key][2] = 1
                self.clicked += 1
        except KeyError:
            pass
    def clear_empty_tiles(self, main_key):
        queue = deque([main_key])
        while len(queue) != 0:
            key = queue.popleft()
            self.check_tile(key-9, queue)  
            self.check_tile(key-10, queue)  
            self.check_tile(key-11, queue)  
            self.check_tile(key-1, queue) 
            self.check_tile(key+1, queue)  
            self.check_tile(key+9, queue) 
            self.check_tile(key+10, queue)  
            self.check_tile(key+11, queue)  
    def gameover(self):
        messagebox.showinfo("Ты проиграл", "Попоробуй еще раз!")
        global root
        root.destroy()
    def victory(self):
        messagebox.showinfo("Конец игры", "Ты победил!")
        global root
        root.destroy()
    def update_flags(self):
        self.label3.config(text="Флажки: "+str(self.flags))
def main():
    global root
    root = Tk()
    root.title("Сапер")
    minesweeper = Minesweeper(root)
    root.mainloop()
if __name__ == "__main__":
    main() 