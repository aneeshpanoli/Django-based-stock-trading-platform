from tkinter import *
import subprocess
import psutil
import Forex1RealtimeIB
import threading


class StockTrader:
    def __init__(self, window):
        self.window = window
        self.window.wm_title("Stock Trading - Aneesh Panoli") # window title
        self.window.minsize(width=600, height=400) # window minimum size
        self.window.configure(background="black") # window background
        # frames inside main window
        self.topFrame = Frame(self.window)
        self.topFrame.pack() # packing side can be specified inside the (side=LEFT)

        self.forex_ticker1 = StringVar()
        self.real_time_button5_entry = None


    def menubar(self):
        pass

    def label(self):
        #===============Start Here=======================
        launch_IB_tws_label = Label(self.topFrame, text=" START HERE ")
        launch_IB_tws_label.grid(row=9, column=8)
        #------------------------REAL TIME QUOTES--------------------------------------
        fetch_real_time_label = Label(self.topFrame, text="FETCH REAL TIME QUOTES", bg="white")# Section label
        fetch_real_time_label.grid(row=9, column=9, columnspan=3) # section label
        real_time_button1_label = Label(self.topFrame, text="Enter the stock ticker : ", bg="white")
        real_time_button2_label = Label(self.topFrame, text="Enter the stock ticker : ", bg="white")
        real_time_button3_label = Label(self.topFrame, text="Enter the stock ticker : ", bg="white")
        real_time_button4_label = Label(self.topFrame, text="Enter the stock ticker : ", bg="white")
        real_time_button5_label = Label(self.topFrame, text="Enter the Forex ticker : ", bg="white")

        real_time_button1_label.grid(row=10, column=10)
        real_time_button2_label.grid(row=11, column=10)
        real_time_button3_label.grid(row=12, column=10)
        real_time_button4_label.grid(row=13, column=10)
        real_time_button5_label.grid(row=14, column=10)

        #---------------------------TRADE EXECUTION-----------------------------------------------
        trade_label = Label(self.topFrame, text="TRADE EXECUTION", bg="white")
        trade_label.grid(row=9, column=23)
        trade_label_ticker = Label(self.topFrame, text="Enter stock ticker :", bg="white")
        trade_label_ticker.grid(row=10, column=23)

    def entry(self):
        #------------------------REAL TIME QUOTES--------------------------------------
        real_time_button1_entry = Entry(self.topFrame)
        real_time_button2_entry = Entry(self.topFrame)
        real_time_button3_entry = Entry(self.topFrame)
        real_time_button4_entry = Entry(self.topFrame)
        self.real_time_button5_entry = Entry(self.topFrame, textvariable=self.forex_ticker1)

        real_time_button1_entry.grid(row=10, column=11)
        real_time_button2_entry.grid(row=11, column=11)
        real_time_button3_entry.grid(row=12, column=11)
        real_time_button4_entry.grid(row=13, column=11)
        self.real_time_button5_entry.grid(row=14, column=11)
        #---------------------------TRADE EXECUTION-----------------------------------------------
        trade_button1_entry = Entry(self.topFrame)
        trade_button1_entry.grid(row=11, column=23)

    def button(self):
        #=====================START HERE=============================
        if "tws.exe" in (p.name() for p in psutil.process_iter()):
            self.launch_IB_tws_button = Button(self.topFrame, text=" TWS is \n Running! "\
                                    , fg="black", bg="#ecad9f", command=self.launchTws)
            self.launch_IB_tws_button.grid(row=10, column=8, rowspan=2)
        else:
            self.launch_IB_tws_button = Button(self.topFrame, text=" Lauch \n TWS "\
                                    , fg="black", bg="green", command=self.launchTws)
            self.launch_IB_tws_button.grid(row=10, column=8, rowspan=2)
        #=====================RESTART APP=============================
        restart_app_button = Button(self.topFrame, text="Restart"\
                                , fg="white", bg="Red", command=self.restartFn)
        restart_app_button.grid(row=12, column=8, rowspan=2)
        #========================REAL TIME QUOTES==============================
        real_time_button1 = Button(self.topFrame, text="Submit", fg="blue", bg="green")
        real_time_button2 = Button(self.topFrame, text="Submit", fg="blue",  bg="green")
        real_time_button3 = Button(self.topFrame, text="Submit", fg="blue",  bg="green")
        real_time_button4 = Button(self.topFrame, text="Submit", fg="blue",  bg="green")
        real_time_button5 = Button(self.topFrame, text="Submit", fg="blue",  bg="green",\
                                    command=self.handleToExternal)
        # real_time_button1.pack(side=LEFT)
        real_time_button1.grid(row=10, column=12)
        real_time_button2.grid(row=11, column=12)
        real_time_button3.grid(row=12, column=12)
        real_time_button4.grid(row=13, column=12)
        real_time_button5.grid(row=14, column=12)

        #-----chart buttons--------------
        real_time_chart_button1 = Button(self.topFrame, text="Chart", fg="black", bg="yellow")
        real_time_chart_button2 = Button(self.topFrame, text="Chart", fg="black", bg="yellow")
        real_time_chart_button3 = Button(self.topFrame, text="Chart", fg="black", bg="yellow")
        real_time_chart_button4 = Button(self.topFrame, text="Chart", fg="black", bg="yellow")
        real_time_chart_button5 = Button(self.topFrame, text="Chart", fg="black", bg="yellow")
        #pack
        real_time_chart_button1.grid(row=10, column=13)
        real_time_chart_button2.grid(row=11, column=13)
        real_time_chart_button3.grid(row=12, column=13)
        real_time_chart_button4.grid(row=13, column=13)
        real_time_chart_button5.grid(row=14, column=13)

        #=========================TRADE EXECUTION====================================
        trade_button1 = Button(self.topFrame, text="Start Trading", fg="blue", bg="green")
        trade_button1.grid(row=12, column=23)
    def footer(self):
        pass
#============================================================================================
#======================BUTTON FUNCTIONS========================================================
    def launchTws(self):
        if "tws.exe" in (p.name() for p in psutil.process_iter()):
            self.launch_IB_tws_button = Button(self.topFrame, text=" TWS is \n Running! "\
                                    , fg="black", bg="#ecad9f", command=self.launchTws)
            self.launch_IB_tws_button.grid(row=10, column=8, rowspan=2)
        else:
            subprocess.Popen(['C:\\Jts\\tws.exe'])
    def restartFn(self):
        # will not work if the directory is wrong aka move machines
        subprocess.Popen(['E:\\ProgramData\\Anaconda3\\python.exe'\
                    , 'E:\\ProgramData\\Anaconda3\\Scripts\\mysite\\static\\py\\StockTrader_GUI.py'])
        self.window.destroy()

    def handleToExternal(self):
        self.forex_ticker1 = self.real_time_button5_entry.get()
        f = Forex1RealtimeIB.main(self.forex_ticker1)

    def main(self):
        buttons = self.button()
        entries = self.entry()
        labels = self.label()



window = Tk() #main window
stockTrader = StockTrader(window)
run = stockTrader.main()
window.mainloop() # keep window on
