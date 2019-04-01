import sys
from tkinter import *
from tkinter import
import graph_functions
#from Roi_to_graph import *

class Param():
    def __init__(self, id, longname, value=None, flag = False):
        self.id = id
        self.value = value
        self.flag = flag
        self.longname = longname

class MainWIndow(Tk):
    def __init__(self):
        Tk.__init__(self)
        #menu
        self.top = Menu(self, tearoff=False)
        #self.config(menu = self.top)
        file = Menu(self.top)
        file.add_command(label = "Open single file...",command=self.openfile)
        file.add_command(label = "Open folder...",command=self.openfolder)
        file.add_command(label = "Set save directory...",command=self.dummy)
        file.add_command(label = "Quit", command = self.quit)
        self.top.add_cascade(label = "File", menu = file)

        options = Menu(self.top)
        options.add_command(label = "Set vessel mode",command=self.vesseloptionpopup)
        options.add_command(label="Other options",command = self.optionpopup)
        self.top.add_cascade(label = "Options", menu = options)

        #parameters
        self.left = Frame(self)
        self.params = ParamDisplay(self.left)
        self.params.pack()
        self.bind('<FocusIn>',(lambda event: self.params.update()))

        #status
        self.right = Frame(self)
        self.text = Text(self.right,wrap="word")
        self.text.pack(expand=True,fill=BOTH)

        sys.stdout = PrintRedirect(self.text)

        #buttons
        self.buttons = Frame(self)
        Button(self.buttons,text="Run",command=self.run).pack(side=LEFT)
        Button(self.buttons,text="Quit",command=self.quit).pack(side=LEFT)

        #attributes
        self.mode = StringVar()

        #layout
        self.buttons.pack(side=BOTTOM, expand=True,fill=X)
        self.left.pack(side=LEFT,expand=True,fill=X)
        self.right.pack(side=LEFT, expand=True, fill=X)

    def vesseloptionpopup(self):
        pop = Toplevel(self)
        SetDiamOptions(pop).pack()

    def optionpopup(self):
        pop = Toplevel(self)


    def dummy(self):
        pass

    def openfolder(self):
        global PARAMS
        directory = filedialog.askdirectory()
        if directory != "":
            PARAMS["InFolder"].value = directory
            PARAMS["InFolder"].flag  = True
            PARAMS["InFile"].flag = False
            PARAMS["InFile"].value=None
        else:
            pass

    def openfile(self):
            global PARAMS
            filename = filedialog.askopenfilename()
            if filename != "":
                PARAMS["InFile"].value = filename
                PARAMS["InFile"].flag  = True
                PARAMS["InFolder"].flag = False
                PARAMS["InFolder"].value = None
            else:
                pass

    # TODO: Replace with function that makes graph given other parameters etc.
    def run(self):
        if PARAMS["InFolder"].value is not None:
            ## TODO: Start by reading in folder contents
            ## TODO: Process graphs
            ## TODO: Save graphs for processing
            ## TODO: Propmpt when function is complete asking to run statistics
            break #or return?
        elif PARAMS["InFile"].value is not None:
            ## TODO: Read in file
            ## TODO: process single graph and save
            ## TODO: Propmpt to display & designate source
            ## TODO: Propmpt for statistics
        else:
            print("No file or folder selected. Please open a file to process and try again.")

class ParamDisplay(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self,parent)
        self.fillgrid()

    def fillgrid(self):
        r = 0
        for param in PARAMS.values():
            if param.flag:
                color = "black"
            else:
                color = "gray"

            Label(self,text = param.longname,fg=color).grid(row=r,column=0)
            Label(self,text=param.value,fg=color).grid(row=r,column=1)
            r += 1

    def update(self):
        for child in self.winfo_children():
            child.destroy()
        self.fillgrid()

class PrintRedirect(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end",str,(self.tag,))
        self.widget.configure(state="disabled")

    def flush(self):
        pass

class SetDiamOptions(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.right = Frame(self)
        self.left = Frame(self)
        self.right.pack(side=RIGHT)
        self.left.pack(side=LEFT)
        self.choice = StringVar()

        modes = {
            "const_n":"Fixed number of vessels, diameter depending on vein width",
            "const_d":"Constant vessel diameter, number of vessels depending on vein width",
            "taper":"Size and number vary, vessel diameter scales to fractional power of vein width"
        }
        for key in modes.keys():
            Radiobutton(self.left, text=modes[key],
                        command=lambda: self.fill( self.choice.get()),
                        value=key,
                        var=self.choice).pack()

        Button(self, text="Save values and close",command = self.save_and_quit).pack(side=BOTTOM)

    def fill(self, option):
        params = {
            "const_n":["n","prop"],
            "const_d":["d","prop"],
            "taper":["alpha","prop"]
        }

        for child in self.right.winfo_children():
            child.destroy()

        for value in params[option]:
            row = Frame(self.right)
            lab = Label(row, text = value)
            ent = Entry(row)
            row.pack(side=TOP, fill = X)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill = X)

    def save_and_quit(self):
        global PARAMS
        PARAMS["DiamMode"].value = self.choice.get()
        for row in self.right.winfo_children():
            if type(row) is Frame:
                for child in row.winfo_children():
                    if type(child) is Label:
                        key = child["text"]
                    elif type(child) is Entry:
                        value = child.get()
                    else:
                        continue
                try:
                    PARAMS[key].value = value
                    PARAMS[key].flag = True
                except KeyError:
                    pass
        mode_flags()
        if self.parent is not None:
            self.parent.destroy()
        else:
            self.destroy()


def init_params(ver):
    params_list = [
        Param("InFile", "Input filename"),
        Param("InFolder","Input folder"),
        Param("units","Units","pixels",True)
        Param("DiamMode","Vessel diameter mode", "const_n", True),
        Param("n","Vessels per vein", 1, True),
        Param("alpha","Vessel size power scaling", 0.167, False),
        Param("prop","Vessel area to vein area ratio", 1, True),
        Param("d","Fixed vessel size"),
        Param("thresh","Cut-off distance for shared end-points",2*math.sqrt(2),True),
        Param("scale","Pixels per unit")
    ]
    params_dict = dict([(param.id, param) for param in params_list])

    if ver == "list":
        return params_list
    elif ver == "dict":
        return params_dict
    else:
        return

def mode_flags():
    global PARAMS
    mode = PARAMS["DiamMode"].value

    if mode != "const_n":
        PARAMS["n"].flag = False
    if mode != "const_d":
        PARAMS["d"].flag = False
    if mode != "taper":
        PARAMS["alpha"].flag = False

if __name__ == "__main__":
    PARAMS = init_params("dict")

    win = MainWIndow()
    win.config(menu=win.top)
    win.mainloop()
