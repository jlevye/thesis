#!/usr/bin/python3
"""
GUI main program
"""
import sys
import math
import pandas as pd
from tkinter import *
import tkinter.filedialog as filedialog
from tkinter.messagebox import *
from graph_functions import *
from svgparser import *

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
        file.add_command(label = "Open csv...",command=self.openfile)
        file.add_command(label = "Open SVG...",command=self.processimage)
        file.add_command(label = "Open folder...",command=self.openfolder)
        file.add_command(label = "Set save directory...",command=self.dummy)
        file.add_command(label = "Quit", command = self.quit)
        self.top.add_cascade(label = "File", menu = file)

        options = Menu(self.top)
        options.add_command(label = "Set vessel mode",command=self.vesseloptionpopup)
        options.add_command(label="Other options",command = self.optionpopup)
        self.top.add_cascade(label = "Options", menu = options)

        analysis = Menu(self.top)
        analysis.add_command(label = "Single graph metrics...", command=self.batchstats)
        analysis.add_command(label = "Batch graph metrics...", command = self.statsfromfile)
        self.top.add_cascade(label = "Analysis", menu = analysis)

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
        BasicParams(pop).pack()

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

    def processimage(self):
        imagefile = filedialog.askopenfilename()
        with open(imagefile) as f:
            image = f.read()
        paths = get_paths(image)
        data_df, data_list, errors = process_movetos(paths)

        for e in errors:
            print(e)

        pop = Toplevel(self)
        ImageSaveOptions(data_df, pop).pack()

    # TODO: Replace with function that makes graph given other parameters etc.
    def run(self):
        if PARAMS["InFolder"].value is not None:
            csvs, svgs = get_batch_files(PARAMS["InFolder"].value)
            total = len(csvs) + len(svgs)
            log = 0
            if total == 0:
                print("No valid files found.")
            else:
                print("{} files found. Beginning now ...".format(total))
            if len(svgs) > 0:
                question = "Split interections in SVGs? If yes, will use {} as minimum length. You can change this value in Options -> Other Options or by processing images individually.".format(PARAMS["thresh"].value)
                split = askyesno(question)
                for file in svgs:
                    with open(file) as f:
                        image = f.read()
                    paths = get_paths(image)
                    data_df, data_list, errors = process_movetos(paths)
                    if split:
                        min = PARAMS["thresh"].value
                        datatmp = split_data(data_df, min, min)
                        data_df = datatmp
                    vertices, edges = makeEV(data_df)
                    g = make_graph(vertices, edges, PARAMS)
                    save_graph(g, file, metadata = PARAMS)
                    print("File number {} of {} processed.".format(log, total))
                    log += 1

            if len(csvs) > 0:
                for file in csvs:
                    segs = check_csv(file)
                    vertices, edges = makeEV(segs)
                    g = make_graph(vertices, edges, PARAMS)
                    save_graph(g, file, metadata=PARAMS)
                    print("File number {} of {} processed.".format(log, total))
                    log += 1

            print("Use the Analysis menu to calculate graph metrics for the graphs produced.")
            return
        elif PARAMS["InFile"].value is not None:
            #Read in file
            filename = PARAMS["InFile"].value
            if filename[-3::].lower() == "csv":
                segs = check_csv(filename)
            elif filename[-3::].lower() == "svg":
                print("Please use Open SVG... command in File menu.")
            else:
                print("Incorrect file type. Please open CSV or SVG file.")

            #Process single graph and save
            vertices, edges = makeEV(segs, PARAMS["thresh"].value)
            g = make_graph(vertices, edges, PARAMS)
            save_graph(g, filename, metadata=PARAMS)

            #Prompts
            pop = Toplevel()
            Button(pop, text = "Show Graph", command = lambda: displayGraph(g)).pack()
            Button(pop, text = "Run stats", command = lambda: self.batchstats(graph=g)).pack()

        else:
            print("No file or folder selected. Please open a file to process and try again.")

    def batchstats(self,graph=None):
        menu = Toplevel(self)
        StatMenu(graph=graph, parent = menu).pack()



    def statsfromfile(self):
        folder = filedialog.askdirectory()
        file_names = [folder + "/" + file for file in os.listdir(folder) if file.endswith(("xml.gz"))]
        count = len(file_names)
        message = "{} files to read. Create new file or add to existing?".format(count)
        choice = askradio(message, ["New","Append"])

        #Opening or setting up data output
        if choice == "New":
            outfile = filedialog.asksaveasfilename()
            first = file_names.pop(0)
            pop = Toplevel(self)
            StatMenu(infile=first, outfile=outfile, parent=pop, verbose = False).pack()
            pop.grab_set()
            pop.focus_set()
            pop.wait_window()
        elif choice == "Append":
            outfile = filedialog.askopenfilename()
        else:
            print("No option chosen.")
            return

        #Once we have a file to continue writing to, process remaining graphs
        names = ["GraphID", "FIlepath","NVertices","AvgDegree","NEdges","TotalLength","Cost","Efficiency","TransportPerformance","LaPlacianSpectra","EdgeBetweennessMean","EdgeBetweennessSD","CheegerLimit","MinCut"]
        req_weight = ["Cost","Efficiency","TransportPerformance","LaPlacianSpectra","EdgeBetweennessMean", "CheegerLimit","MinCut"]

        w = None
        functionCalls = ["parse_name(path)", "path","g.num_vertices()","gt.vertex_average(g, \"total\")","g.num_edges()",
                "sum(g.ep.length.get_array()[:])", "cost_calc(g, {})", "efficiency(g, {})", "performance(g,{})", "spectra(g,{})", "mean_btwn(g,{})[0]", "mean_btwn(g,{})[1]", "cheegerApprox(g,{})", "gt.min_cut(g,{})"]
        lookup = dict(zip(names, functionCalls))

        columns = headerFormatter(parseHeader(outfile))

        if len(columns) == 0:
            print("No valid columns.")
            return
        else:
            for path in file_names:
                g = gt.load_graph(path)
                valid_weights = list(g.edge_properties.keys())

                row = []
                for col in columns:
                    if len(col) == 2:
                        if col[1] in valid_weights:
                            w = "g.ep.{}".format(col[1])
                        else:
                            w = None
                    function = lookup[col[0]]
                    row.append(eval(function.format(w)))
                appendRow(outfile, row)
        print("{} files processed. Please check {} for data.".format(count, outfile))

class ImageSaveOptions(Frame):
    def __init__(self, indata, parent = None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.input = indata

        self.min = StringVar()
        self.min.set(0)

        Label(self, text = "Split paths to create nodes at intersections?").pack()
        Label(self, text = "Minimum length. Enter any non-numeric value to use existing minimum as cut-off.").pack(side = LEFT)
        Entry(self, textvariable = self.min).pack(side = RIGHT)

        Button(self, text = "Yes", command = self.split_and_save).pack(side = LEFT)
        Button(self, text = "No", command = self.save_only).pack(side = RIGHT)

    def split_and_save(self):
        global PARAMS
        minimum = self.min.get()
        newDF = split_data(self.input, minimum)

        filename = filedialog.asksaveasfilename()
        newDF.to_csv(filename)
        PARAMS["InFile"].value = filename

        if self.parent is not None:
            self.parent.destroy()
        else:
            self.destroy()

    def save_only(self):
        global PARAMS
        filename = filedialog.asksaveasfilename()
        self.input.to_csv(filename)
        PARAMS["InFile"].value = filename

        if self.parent is not None:
            self.parent.destroy()
        else:
            self.destroy()

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

            Label(self,text = param.longname,fg=color, wraplength=200).grid(row=r,column=0)
            Label(self,text=param.value,fg=color, wraplength=200).grid(row=r,column=1)
            r += 1

    def update(self):
        for child in self.winfo_children():
            child.destroy()
        self.fillgrid()

class StatMenu(Frame):
    def __init__(self, graph = None, infile = None, outfile = None, parent = None, verbose = True):
        Frame.__init__(self, parent)
        self.parent = parent
        self.outfile = outfile
        self.verbose = verbose

        if graph is not None:
            self.graph = graph
            self.path = PARAMS["InFile"].value
        else:
            if infile is not None:
                self.path = infile
            else:
                self.path = filedialog.askopenfilename()

            try:
                graph = gt.load_graph(self.path)
                self.graph = graph
            except ValueError:
                print("Please choose a graph file in the gt format.")
                self.destroy()

        self.weights = ["None"]+list(graph.edge_properties.keys())

        self.names = ["GraphID", "FIlepath","NVertices","AvgDegree","NEdges","TotalLength","Cost","Efficiency","TransportPerformance","LaPlacianSpectra",
            "EdgeBetweennessMean","EdgeBetweennessSD","CheegerLimit","MinCut"]

        req_weight = ["Cost","Efficiency","TransportPerformance","LaPlacianSpectra","EdgeBetweennessMean", "CheegerLimit","MinCut"]

        self.choices = []
        self.weightselect = []

        gridbox = Frame(self)
        r = 0
        for name in self.names:
            choice = IntVar()
            Checkbutton(gridbox, text = name, variable = choice).grid(row = r, column = 0)
            choice.set(1)
            self.choices.append(choice)
            if name in req_weight:
                weight = StringVar()
                weight.set(self.weights[0])
                menu = OptionMenu(gridbox, weight,*self.weights)
                menu.grid(row = r, column = 1)
                self.weightselect.append(weight)
            else:
                self.weightselect.append(None)
            r += 1

        if self.outfile is None:
            self.save = IntVar()
            Checkbutton(gridbox, text = "Save to file?", variable = self.save).grid(row = r, column = 0)

        button = Button(self, text = "Run", command = self.run)
        gridbox.pack()
        button.pack()

    def run(self):
        w = None
        functionCalls = ["parse_name(self.path)", "self.path","self.graph.num_vertices()", "gt.vertex_average(self.graph, \"total\")","self.graph.num_edges()", "sum(self.graph.ep.length.get_array()[:])", "cost_calc(self.graph, {})", "efficiency(self.graph, {})", "performance(self.graph,{})", "spectra(self.graph,{})", "mean_btwn(self.graph,{})[0]", "mean_btwn(self.graph,{})[1]", "cheegerApprox(self.graph,{})", "gt.min_cut(self.graph,{})"]

        #Get the options and run
        header = []
        values = []

        for i in range(len(self.names)):
            if self.choices[i].get() == 1:
                function = functionCalls[i]
                if self.weightselect[i] is not None:
                    w_name = self.weightselect[i].get()
                    if w_name == "None":
                        w = w_name
                    else:
                        w = "self.graph.ep.{}".format(w_name)
                if w is None:
                    header.append(self.names[i] + ".Unweighted")
                else:
                    header.append(self.names[i] + "." + w_name)
                values.append(eval(function.format(w)))

        #Store and save
        if self.verbose:
            for i in range(len(header)):
                print("{}: {}".format(header[i],values[i]))
        else:
            if self.names[0] == "GraphID":
                print("{} complete".format(self.names[0]))
            else:
                print("Analysis complete. Check for file.")

        val_out = [[v] for v in values]
        d = dict(zip(header, val_out))

        if self.outfile is not None:
            data = pd.DataFrame(d, index = [0])
            data.to_csv(self.outfile, index=False)
        else:
            if self.save.get() == 1:
                outfile = filedialog.asksaveasfilename()
                data = pd.DataFrame(d, index = [0])
                data.to_csv(outfile, index=False)

        if self.parent is not None:
            self.parent.destroy()
        else:
            self.destroy()

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
                    PARAMS[key].value = float(value)
                    PARAMS[key].flag = True
                except KeyError:
                    pass
        mode_flags()
        if self.parent is not None:
            self.parent.destroy()
        else:
            self.destroy()

#Kludgy and hard-coded, but sufficient for now
class BasicParams(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()

        #Variables
        self.units = StringVar()
        self.units.set(PARAMS["units"].value)
        self.thresh = DoubleVar()
        self.thresh.set(PARAMS["thresh"].value)

        self.row1 = Frame(self)
        self.row2 = Frame(self)

        self.row1.pack()
        self.row2.pack()

        Label(self.row1, text="Units:").pack(side=LEFT)
        Label(self.row2, text="Minimum distance between nodes:").pack(side=LEFT)

        Entry(self.row1, textvariable = self.units).pack(side=RIGHT)
        Entry(self.row2, textvariable = self.thresh).pack(side=RIGHT)

        Button(self, text="Save and close", command = self.save_quit).pack()

    def save_quit(self):
        global PARAMS
        PARAMS["units"].value = self.units.get()
        PARAMS["thresh"].value = self.thresh.get()

        if self.parent is not None:
            self.parent.destroy()
        else:
            self.destroy()

# TODO: add fault testing menus
class OrderedFaultTest(Frame):
    def __init__(self, graph, parent = None):
        Frame.__init__(self, parent)
        self.parent = parent

        if graph is None:
            self.graph = gt.load_graph(filedialog.askopenfilename())
        else:
            self.graph = graph

        self.weights = self.graph.edge_properties.keys()

    def run(self):
        g = self.graph
        outfile = filedialog.asksaveasfilename()
        if outfile:
            fault_tolerance(g, outfile, )



class IteratedFaultTest(Frame):
    def __init__(self, graph, parent = None):
        Frame.__init__(self, parent)
        self.parent = parent


#Modal dialog for radiobuttons
def makeradio(parent, answers):
    choices = []
    result = StringVar()
    for a in answers:
        Radiobutton(parent, text = a, value = a, variable = result).pack()
    choices.append(result)
    return choices

def fetch(input, output):
    for item in input:
        output.append(item.get())

def show(select, out, popup):
    fetch(select, out)
    popup.destroy()

def askradio(question, answers):
    out = []
    popup = Toplevel()
    Label(popup, text = question).pack()
    select = makeradio(popup, answers)
    Button(popup, text = "OK", command = (lambda: show(select, out, popup))).pack()
    popup.grab_set()
    popup.focus_set()
    popup.wait_window()

    return out[0]

#Generate initial parameter list
def init_params(ver):
    params_list = [
        Param("InFile", "Input filename"),
        Param("InFolder","Input folder"),
        Param("units","Units","pixels",True),
        Param("DiamMode","Vessel diameter mode", "const_n", True),
        Param("n","Vessels per vein", 1, True),
        Param("alpha","Vessel size power scaling", 0.167, False),
        Param("prop","Vessel area to vein area ratio", 1, True),
        Param("d","Fixed vessel size"),
        Param("thresh","Cut-off distance for shared end-points",2*math.sqrt(2),True),
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

#Main method
if __name__ == "__main__":
    PARAMS = init_params("dict")

    win = MainWIndow()
    win.config(menu=win.top)
    win.mainloop()
