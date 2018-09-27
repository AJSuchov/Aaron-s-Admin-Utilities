import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import os
import win32com.shell.shell as shell

def quit():
    quit()

###Fonts###
LARGE_FONT= ("Verdana", 12)
MEDIUM_FONT= ("Verdana", 9)

################### This initializes the whole GUI ###################################################
class AJsUtilities(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="A.ico")
        tk.Tk.wm_title(self, "Aaron's Utilities V0.5.1")
        
        container = tk.Frame(self,bg='#262626')
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}

        for F in (WelcomeScreen,AJsUtilitiesButtons,FirewallOptions, NetworkTests): 
            frame = F(container, self) 
            self.frames[F] = frame  
            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(WelcomeScreen)  

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

############# This is the main screen ################################################################
class WelcomeScreen(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self,parent)
            labelThing = tk.Label(self, text="""This application requires the user to know what they are doing
and to have administrator rights. Multiple functions require the user
to be administrator. DO NOT DISTRIBUTE. If there are any errors,
contact Aaron. Below is that you agree or disagree to the terms of
service that Aaron can make at anytime he gets to doing it.""", font=LARGE_FONT, pady=5, fg='white', bg='#262626')
            labelThing.pack(pady=5)

            agreeButton = tk.Button(self, text="I Agree", width=26, height=5, font=LARGE_FONT, padx=5,pady=5, bg='#255c99', fg='white',
                                command=lambda: controller.show_frame(AJsUtilitiesButtons))
            agreeButton.pack()

            disagreeButton = tk.Button(self, text="I Disagree", width=26, height=5, font=LARGE_FONT, padx=5,pady=5, bg = '#b3001b', fg='white', 
                                command=quit)
            disagreeButton.pack(pady=5)


#################################### This section has all of the "Main Menu" buttons and options that take to other pages #######################################
class AJsUtilitiesButtons(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        fireWallOpt = tk.Button(self,text="Firewall Options", width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white', command=lambda: controller.show_frame(FirewallOptions))
        fireWallOpt.grid(row=0,column=0,padx=12,pady=5)

        pingTesting = tk.Button(self, text="Connection Tests",width=26, height=5, font=LARGE_FONT, padx=5,pady=5, bg='#b3001b', fg='white',command=lambda: controller.show_frame(NetworkTests))
        pingTesting.grid(row=0,column=1,padx=12,pady=5)


##################################### Class for the firewall activation and deactivation #####################################################
class FirewallOptions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        enAllFire = tk.Button(self,text="Enable All Firewalls",width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200, command=self.enableFireWallAll)
        enAllFire.grid(row=0,column=0,padx=12,pady=5)

        disAllFire = tk.Button(self,text="Disable All Firewalls",width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200, command=self.disFireWallAll)
        disAllFire.grid(row=0,column=1,padx=12,pady=5)

        enDomFire = tk.Button(self,text="Enable Domain Network Firewalls",width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200, command=self.enableFireWallDom)
        enDomFire.grid(row=1,column=0,padx=12,pady=5)

        disDomFire = tk.Button(self,text="Disable Domain Network Firewalls",width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200, command=self.disFireWallDom)
        disDomFire.grid(row=1,column=1,padx=12,pady=5)

        enPrivFire = tk.Button(self,text="Enable Private Network Firewalls",width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200, command=self.enableFireWallPriv)
        enPrivFire.grid(row=2,column=0,padx=12,pady=5)

        disPrivFire = tk.Button(self,text="Disable Private Network Firewalls",width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200, command=self.disFireWallPriv)
        disPrivFire.grid(row=2,column=1,padx=12,pady=5)

        enPubFire = tk.Button(self,text="Enable Public and Guest Network Firewalls",width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200, command=self.enableFireWallPub)
        enPubFire.grid(row=3,column=0,padx=12,pady=5)

        disPubFire = tk.Button(self,text="Disable Public and Guest Network Firewalls",width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white', wraplength=200, command=self.disFireWallPub)
        disPubFire.grid(row=3,column=1,padx=12,pady=5)

        returnButton = tk.Button(self,text="Back to Options",width=26, height=5, font=MEDIUM_FONT, padx=5,pady=5,bg='#b3001b', fg='white', wraplength=200, command=lambda: controller.show_frame(AJsUtilitiesButtons))
        returnButton.grid(row=4,column=0,padx=12,pady=5)

    ######Functions that are connected to buttons ########
    #Disable all firewalls
    def disFireWallAll(self):
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + 'netsh advfirewall set allprofiles state off')

    #enable all firewalls
    def enableFireWallAll(self):
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + 'netsh advfirewall set allprofiles state on')

    #Disable Domain network firewalls
    def disFireWallDom(self):
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + 'netsh advfirewall set domainprofiles state off')

    #enable Domain network firewalls
    def enableFireWallDom(self):
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + 'netsh advfirewall set domainprofiles state on')

    #Disable Private network firewalls
    def disFireWallPriv(self):
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + 'netsh advfirewall set privateprofiles state off')

    #enable Private network firewalls
    def enableFireWallPriv(self):
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + 'netsh advfirewall set privateprofiles state on')

    #Disable Public and Guest network firewalls
    def disFireWallPub(self):
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + 'netsh advfirewall set publicprofiles state off')

    #enable Public and Guest network firewalls
    def enableFireWallPub(self):
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + 'netsh advfirewall set publicprofiles state on')

        
########################################## This section is for the testing of internet connection and network connection i.e. pinging servers ############################################
class NetworkTests(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        genLabel = tk.Label(self, text="Test to see if computer can connect to network or can contact another computer.", font=LARGE_FONT, wraplength=600)
        genLabel.grid(row=0, columnspan=2)
        
        pingLabel = tk.Label(self, text="Input IP address or Computer Name on same network to test contact i.e. ping.", font=LARGE_FONT, wraplength=600)
        pingLabel.grid(row=1, columnspan=2, pady=15)

        inputLabel= tk.Label(self, text="IP to Ping", font=MEDIUM_FONT)
        inputLabel.grid(row=2, column=0, pady=3)

        self.PingAdd = tk.Entry(self)
        self.PingAdd.grid(row=3, column=0, pady=2)

        pingConnectButton= tk.Button(self, text="Test Connection!", command=self.pingOtherComp, font=MEDIUM_FONT, padx=5,pady=5,bg='#b3001b', fg='white', wraplength=200)
        pingConnectButton.grid(row=4, column=0)

        basicInternetTest= tk.Button(self, text="Basic Internet Test", command=self.internetTest, font=LARGE_FONT, bg='#b3001b', fg='white', wraplength=200)
        basicInternetTest.grid(row=2, rowspan=3, column=1)

        self.resultsPing = tk.Label(self, text = "", wraplength=600)
        self.resultsPing.grid(row=5, columnspan=2)
        
        returnButton = tk.Button(self,text="Back to Options",width=26, height=5, font=MEDIUM_FONT, padx=5,pady=5,bg='#b3001b', fg='white', wraplength=200, command=lambda: controller.show_frame(AJsUtilitiesButtons))
        returnButton.grid(row=7,column=0,padx=12,pady=5)


    ######## Functions for the button commands ############
    ### Function for pinging a certain IP or domain 
    def pingOtherComp(self):
        #### Gets Username
        any_user = 'echo %username% > C:\\Users\\Public\\user.txt'
        os.system(any_user)
        with open('C:\\Users\\Public\\user.txt', 'r') as username:
            for name in username:
                main_name = name[0:len(name)-2]

        #### Gets IP Information
        pingIP = self.PingAdd.get()
        os.system('ping ' + pingIP + '> "C:\\Users\\Public\\ping.txt"')
        pingResults = open('C:\\Users\\Public\\ping.txt','r')
        pingRE = pingResults.read()
        self.resultsPing.config(text=pingRE)
        self.PingAdd.delete(0,END)
        
        pingResults.close()

        #### Clean up text files by deleting them
        user_clean = 'DEL ' + 'C:\\Users\\Public\\user.txt'
        ping_clean = 'DEL ' + 'C:\\Users\\Public\\ping.txt'

        os.system(user_clean)
        os.system(ping_clean)

    ### Basic one button that calls google.com to see if it can get signal
    def internetTest(self):
        #### Gets Username
        any_user = 'echo %username% > C:\\Users\\Public\\user.txt'
        os.system(any_user)
        with open('C:\\Users\\Public\\user.txt', 'r') as username:
            for name in username:
                main_name = name[0:len(name)-2]

        #### Gets IP Information
        os.system('ping www.google.com> "C:\\Users\\Public\\ping.txt"')
        pingResults = open('C:\\Users\\Public\\ping.txt','r')
        pingRE = pingResults.read()
        self.resultsPing.config(text=pingRE)
        self.PingAdd.delete(0,END)
        
        pingResults.close()

        #### Clean up text files by deleting them
        user_clean = 'DEL ' + 'C:\\Users\\Public\\user.txt'
        ping_clean = 'DEL ' + 'C:\\Users\\Public\\ping.txt'

        os.system(user_clean)
        os.system(ping_clean)


#Continuously has gui up.

app = AJsUtilities()
app.geometry("600x600")
app.mainloop()
