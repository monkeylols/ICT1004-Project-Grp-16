#Doneby: Chua Jun Hui 1700681
import CsvReader, Classifier, matplotlib, ttk, CatFrequency,NumberofType,NumberOfFeedback, typefreq, tkFileDialog, \
    DownloadCsv,tkMessageBox,cloud, NewEntry, AverageCompletionTime
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Tkinter import *


class GUI:

    def __init__(self, master):
        #calling objects and classes
        self.feedbackinfo_list = []
        self.cloudstr = ""
        self.master = master

        #calling the initial Frame
        self.container = Frame(master)
        self.container.pack(fill="both", expand=True, pady=300)
        master.title("Feedback & Complaint")
        self.label = Label(self.container, text="Welcome! Please select the CSV file which you would like to choose!")
        self.label.pack()

        #creating button
        self.greet_button = Button(self.container, text="OK", command=lambda: self.greet(self))
        self.greet_button.pack()

        #created here as it might be used multiple times
        self.colnames = ["Reported On", "Co. Name", "Requestor", "Property Name", "Category",
                           "Order Group Description", "Floor/unit or space", "Breakdown? (Yes/No)", "Description",
                           "Nature of feedback/complants (& Finding)", "Action Taken", "Start date & time",
                           "Acknowledged date", "Technically completed on", "Status", "Customer / FED Internal"]

    #initialising the dataset
    def greet(self,button):
        self.feedbackinfo_list = CsvReader.read_file()
        for i in self.feedbackinfo_list:
            self.cloudstr += i.company + i.property_name + i.location
        if self.feedbackinfo_list == "Invalid file":
            exit()
        else:
            self.createview()
            self.container.destroy()

    #recreating treeview based on search input
    def search(self, button, desFrame, searchInput):
        self.treeview(searchInput)

    #delete all the child of frame selected and clear all plots
    def deletechild(self,funcFrame):
        for child in funcFrame.winfo_children():
            child.destroy()
        plt.cla()
        plt.clf()
        plt.close('all')

    #A seperate frame for classify to choose
    def classifier(self,button):
        self.funcFrame.destroy()
        self.funcFrame = Frame(self.leftFrame, highlightbackground="blue", highlightcolor="black", highlightthickness=1)
        backButton = Button(self.funcFrame, text="Back", command=lambda: self.basicfuncFrame())
        coyLabel = Label(self.funcFrame, text="Company : \t")
        catLabel = Label(self.funcFrame, text="Category : \t")
        analyseButton = Button(self.funcFrame, text="Analyse", command=lambda: self.creategraph(self,"classifier"))

        #ComboBox
        self.uniqueCoy = list(self.getuniquecoy())
        variable = StringVar(self.master)
        self.coybox = ttk.Combobox(self.funcFrame, textvariable=variable, state='readonly')
        self.coybox['values'] = (self.uniqueCoy)

        # ComboBox
        self.uniquecat = list(self.getuniquecat())
        variable = StringVar(self.master)
        self.catbox = ttk.Combobox(self.funcFrame, textvariable=variable, state='readonly')
        self.catbox['values'] = (self.uniquecat)

        backButton.grid(row=0,column=0,sticky="nw")
        coyLabel.grid(row=1, column=0)
        self.coybox.grid(row=1, column=1)
        catLabel.grid(row=2, column=0)
        self.catbox.grid(row=2,column=1)
        analyseButton.grid(row=3, column=1)

        self.funcFrame.grid(row=1,column=0)

    #A seperate frame for category's frequency
    def catFrequency(self,button):
        self.creategraph(button,"overallfreq")
        self.funcFrame.destroy()
        self.funcFrame = Frame(self.leftFrame, highlightbackground="blue", highlightcolor="black", highlightthickness=1)
        backButton = Button(self.funcFrame, text="Back", command=lambda: self.basicfuncFrame())
        catLabel = Label(self.funcFrame, text="Category : \t")
        goButton = Button(self.funcFrame, text="Go", command=lambda: self.creategraph(self,"specificfreq"))

        # ComboBox
        variable = StringVar(self.master)
        self.combox = ttk.Combobox(self.funcFrame, textvariable=variable, state='readonly')
        self.combox['values'] = ("Completed","Acknowledged")

        # ComboBox
        self.uniquecat = list(self.getuniquecat())
        variable = StringVar(self.master)
        self.catbox = ttk.Combobox(self.funcFrame, textvariable=variable, state='readonly')
        self.catbox['values'] = (self.uniquecat)

        backButton.grid(row=0,column=0,sticky="nw")
        catLabel.grid(row=1, column=0)
        self.catbox.grid(row=1, column=1)
        self.combox.grid(row=2,column=1)
        goButton.grid(row=3, column=1)

        self.funcFrame.grid(row=1,column=0)

    #return a list of unique companies in the dataset
    def getuniquecoy(self):
        output =set()
        for x in self.feedbackinfo_list:
            output.add(x.company)
        return list(output)

    #return a list of unique category in the dataset
    def getuniquecat(self):
        output = set()
        for x in self.feedbackinfo_list:
            output.add(x.category)
        return list(output)

    #An all-in-one function to create graph. What time of graph is based on the value of mode
    def creategraph(self,button,mode):
        self.deletechild(self.rightFrame)
        if mode == "classifier":
            plt = Classifier.get_com_feedback_prob(self.feedbackinfo_list, self.uniqueCoy[self.coybox.current()],
                                                         self.uniquecat[self.catbox.current()])
            if type(plt) is str:
                tkMessageBox.showinfo("Error", plt)
                return
        elif mode == "avgtime":
            plt = AverageCompletionTime.average_completion_time()
        elif mode == "overallfreq":
            plt = CatFrequency.getFrequency(self.feedbackinfo_list)
        elif mode == "specificfreq":
            s =["Completed","Acknowledged"]
            plt = CatFrequency.GenerateHistograph(self.uniquecat[self.catbox.current()], s[self.combox.current()],
                                                  self.feedbackinfo_list)
        elif mode == "numoftype":
            plt = NumberofType.get_request_type(self.feedbackinfo_list)
        else:
            plt = cloud.gencloud(self.cloudstr)

        fig = plt.figure(1)
        canvas = FigureCanvasTkAgg(fig, master=self.rightFrame)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    #Create text. Similar to creategraph(). The different output is dependent of the output s
    def createtxt(self, button, s):
        self.deletechild(self.rightFrame)
        sFrame = Text(self.rightFrame)
        sFrame.pack(expand=YES, fill=BOTH)
        sFrame.insert(END, s)
        sFrame.config(state=DISABLED)

    #Download function. function depends on the value mode
    def download(self, button, mode):
        directory = tkFileDialog.askdirectory() + '/'
        x=[]
        if directory =="/":
            return
        for i in self.resultcount:
            x.append(self.feedbackinfo_list[i])
        if mode == "csv":
            DownloadCsv.get_files_by_property_name(x, directory)
        else:
            DownloadCsv.downloadtxt(x, directory)

    def dlframe(self,button):
        self.funcFrame.destroy()
        self.funcFrame = Frame(self.leftFrame)
        backButton = Button(self.funcFrame, text="Back", command=lambda: self.basicfuncFrame())
        dlLabel = Label(self.funcFrame, text="Download as : \t")
        csvButton = Button(self.funcFrame, text="Csv file", command=lambda: self.download(self, "csv"))
        txtButton = Button(self.funcFrame, text="Txt file", command=lambda: self.download(self, "txt"))

        backButton.grid(row=0,column=0,sticky="nw")
        dlLabel.grid(row=1, column=0)
        csvButton.grid(row=2, column=0, sticky="w")
        txtButton.grid(row=2, column=1, sticky="e")

        self.funcFrame.grid(row=1,column=0, sticky="w")

    def newentry (self,button):
        self.feedbackinfo_list = NewEntry.new_entry(self.feedbackinfo_list)

    def basicfuncFrame(self):
        if hasattr(self, 'funcFrame'):
            self.funcFrame.destroy()
        self.deletechild(self.rightFrame)
        self.funcFrame = Frame(self.leftFrame)

        self.creategraph("","")
        # creating claasify button
        classifyButton = Button(self.funcFrame, text="Predictive Analysis", command=lambda: self.classifier(self),
                                width =25)
        # creating avgComplete Button
        avgComButton = Button(self.funcFrame, text="Avg Completion Time", command=lambda: self.creategraph(self,"avgtime"),
                                width =25)
        # creating getfreq Button
        getfreqButton = Button(self.funcFrame, text="Category Frequency", command=lambda: self.catFrequency(self),
                                width =25)
        # creating numoftype Button
        numoftypeButton = Button(self.funcFrame, text="Number Of Requests", command=lambda: self.creategraph(self,"numoftype"),
                                width =25)
        # creating numoffb Button
        numoffbButton = Button(self.funcFrame, text="Number Of Feedback", command=lambda: self.createtxt(self,
                                                        NumberOfFeedback.get_feedback(self.feedbackinfo_list)),
                                width =25)
        #creating of typefreq Button
        typefreqButton = Button(self.funcFrame, text="Types Of Frequency", command=lambda: self.createtxt(self,
                                                                typefreq.requestfreq(self.feedbackinfo_list)),
                                width =25)
        #creating downnload Button
        printButton = Button(self.funcFrame, text="Download", command=lambda: self.dlframe(self),
                                width =25)
        # creating Merge Button
        mergeButton = Button(self.funcFrame, text="Merge", command=lambda: self.newentry(self), width=25)

        classifyButton.grid(row=0, column=0, sticky="nw")
        avgComButton.grid(row=1, column=0, sticky="nw")
        getfreqButton.grid(row=2, column=0, sticky="nw")
        numoftypeButton.grid(row=3,column=0, sticky="nw")
        numoffbButton.grid(row=4,column=0, sticky="nw")
        typefreqButton.grid(row=5,column=0, sticky="nw")
        printButton.grid(row=6,column=0, sticky="sw")
        mergeButton.grid(row=7,column=0, sticky="sw")

        self.funcFrame.grid(row=1, column=0, sticky="w")

    def treeview(self, searchPara):
        if hasattr(self, 'treeFrame'):
            self.treeFrame.destroy()
        self.treeFrame = Frame(self.masterFrame)
        tree = ttk.Treeview(self.treeFrame)
        self.treeFrame.rowconfigure(0, weight=1)
        self.treeFrame.columnconfigure(0, weight=1)

        # calling the columns and giving them an id
        tree["columns"] = (self.colnames)
        tree.heading("#0", text="")
        tree.column("#0", minwidth=0, width=0)
        for x in range(1, 16):
            tree.heading(str(x), text=self.colnames[x])
            tree.column(str(x), minwidth=0)

        counter = 0
        self.resultcount=[]
        if searchPara != "":
            for x in self.feedbackinfo_list:
                try:
                    if searchPara in x.company or searchPara in x.category or searchPara in x.property_name :
                        tree.insert("", "end", values=(x.report_date_time, x.company, x.requestor, x.property_name,
                                               x.category, x.des_type, x.location, x.if_breakdown,x.description,
                                               x.finding, x.action_taken,x.start_date_time, x.acknowledge_date_time,
                                               x.completed_date_time, x.status, x.customer_type))
                        self.resultcount.append(counter)
                except:
                    pass
                counter += 1
        else:
            try:
                for x in self.feedbackinfo_list:
                    tree.insert("", "end", values=(x.report_date_time, x.company, x.requestor, x.property_name,
                                                x.category, x.des_type, x.location, x.if_breakdown,
                                                x.finding, x.start_date_time, x.acknowledge_date_time,
                                                x.completed_date_time, x.status, x.customer_type))
            except:
                pass

        # implementing the y-bar and x-bar of treeview
        treev = Scrollbar(self.treeFrame, orient=VERTICAL, command=tree.yview)
        treeh = Scrollbar(self.treeFrame, orient=HORIZONTAL, command=tree.xview)

        tree.configure(yscrollcommand=treev.set)
        tree.configure(xscrollcommand=treeh.set)

        tree.grid(row=0, column=0, sticky='nsw')
        treeh.grid(row=1, column=0, sticky='sew')
        treev.grid(row=0, column=1, sticky='nse')
        self.treeFrame.grid(row=1,column=0, columnspan=3, sticky="nsew")

    def createview(self, searchPara=""):
        #creating frame with parent, Tkinter
        self.masterFrame = Frame(self.master)
        #giving z-weight to frame, so that other child frame will resize with respect of this frame
        self.masterFrame.rowconfigure(0, weight=1)
        self.masterFrame.columnconfigure(0, weight=1)

        # create the elements for Search bar
        self.leftFrame = Frame(self.masterFrame)
        searchFrame = Frame(self.leftFrame)

        # creating search button
        searchButton = Button(searchFrame, text="search",
                              command=lambda: self.search(self, self.masterFrame, searchEntry.get()))

        searchLabel = Label(searchFrame, text="Search : \t")
        searchEntry = Entry(searchFrame, bd=10)

        # implement to searchframe
        searchLabel.grid(row=0, column=0)
        searchEntry.grid(row=0,column=1)
        searchButton.grid(row=0, column=2)

        #reqtypeButton.grid(row=4, column=2)
        searchFrame.grid(row=0,column=0)

        # creating func frame with the frame
        self.rightFrame = Frame(self.masterFrame)

        #Create Tree
        self.treeview(searchPara)

        #Create function fram + word cloud
        self.basicfuncFrame()

        # add frames into grid
        #sticky='nsew' is being used to make it stick to which direction you prefer. North = n South =s and etc
        self.leftFrame.grid(row=0, column=0, pady=50, columnspan=2,sticky="nw")
        self.rightFrame.grid(row=0, column=1, pady=50, sticky="ne")

        # pack masterFrame to TKinter
        self.masterFrame.pack(fill=None, expand=False)
