import tkinter as tk
import time

root = tk.Tk()

w = tk.Label(root, text="some words").pack()

frame = tk.Frame(root).pack()

d = {}

def hidefun(self):
    self.widget.pack_forget()
def bringback(self):
    self.widget.pack()


def makedict(foodname, food):
    print("adding to dictionary")
    d[foodname] = food
    for (key, value) in d.items() :
        print(key , " :: ", value )


root.title("salvation army")

button = tk.Button(frame, text="Quit", command=quit).pack()
button1 = tk.Button(frame, text="yello bannanas", command= lambda: makedict('b', 'bannanas')).pack()
button2 = tk.Button(frame, text="carrots", command = lambda: makedict('c', 'carrots')).pack()
button3 = tk.Button(frame, text="fuji apples", command = lambda: makedict('a', 'apples')).pack()




root.mainloop()