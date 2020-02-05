import tkinter as tk

class Example(tk.Tk):
    def __init__(self):
        super().__init__()
        canvas = tk.Canvas(self)
        canvas.pack()
        self.startGame = tk.Button(canvas, text="hide",
                                   background='white', font=("Helvetica"),
                                   command=lambda: self.hide_me(self.startGame))
        self.startGame.place(x=150, y=100)

        self.stopGame = tk.Button(canvas, text="show",
                                   background='white', font=("Helvetica"),
                                   command=lambda: self.show_me(self.startGame))
        #self.stopGame.place(x=250, y=200)
    def show_me(self, event):
        print("show me")
        event.place(x=150, y=100)

    def hide_me(self, event):
        print('hide me')
        event.place_forget()
        #secondevent.place(x=10, y=10)

if __name__ == "__main__":
    Example().mainloop()
