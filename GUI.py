from tkinter import *
from Genetic import Gene as G
    

Graphic = Tk()
W = G([], 0)
Label(Graphic, text= "Generations").grid(row=0)
Label(Graphic, text= "Population Size" ).grid(row=1)

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()

inp1 = IntVar()
inp2 = IntVar()
inp3 = IntVar()

inpcheck = BooleanVar()

e1 = Entry(Graphic, textvariable=inp1)
e2 = Entry(Graphic, textvariable=inp2)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

Checkbutton(Graphic, text= "Mutation",variable=inpcheck, onvalue=True, offvalue=False, command=lambda: W.setMutation(bool(inpcheck.get()))).grid(row=2)


Graphic.title("Neural Net Genetic Alg")
Button(Graphic,text= "Run", width= 25, command=lambda:W.plotData()).grid(row=4, column=1)
Button(Graphic,text= "Enter", width= 25, command=lambda: W.setPopSize(int(e2.get()))).grid(row=1, column = 2)
Button(Graphic,text= "Enter", width= 25, command=lambda: W.setGenerations(int(e1.get()))).grid(row=0, column = 2)

Graphic.mainloop()
