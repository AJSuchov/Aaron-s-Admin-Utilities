import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import os, time, threading
import win32com.shell.shell as shell
import subprocess as sub


def quit():
    quit()

###Fonts###
LARGE_FONT= ("Verdana", 12)
MEDIUM_FONT= ("Verdana", 9)
SMALL_FONT= ("Verdana", 7)

################### This initializes the whole GUI ###################################################
class AJsUtilities(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="A.ico")
        tk.Tk.wm_title(self, "Aaron's Utilities V0.9.2.1")
        
        container = tk.Frame(self,bg='#262626')
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}

        for F in (WelcomeScreen,AJsUtilitiesButtons,FirewallOptions, NetworkTests,PowerOptions, AllowUpdates, IPConfig, MapDrive): 
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

        powerOption = tk.Button(self, text="Power Options",width=26, height=5, font=LARGE_FONT, padx=5,pady=5, bg='#b3001b', fg='white',command=lambda: controller.show_frame(PowerOptions))
        powerOption.grid(row=1,column=0,padx=12,pady=5)

        ipconfig = tk.Button(self, text="Get IP's", width=26, height=5, font=LARGE_FONT, padx=5,pady=5, bg='#b3001b', fg='white',command=lambda: controller.show_frame(IPConfig))
        ipconfig.grid(row=1,column=1,padx=12,pady=5)

        updates = tk.Button(self, text="Windows Updates",width=26, height=5, font=LARGE_FONT, padx=5,pady=5, bg='#b3001b', fg='white',command=lambda: controller.show_frame(AllowUpdates))
        updates.grid(row=2,column=0,padx=12,pady=5)

        mapDrive = tk.Button(self, text="Map Drives",width=26, height=5, font=LARGE_FONT, padx=5,pady=5, bg='#b3001b', fg='white',command=lambda: controller.show_frame(MapDrive))
        mapDrive.grid(row=2,column=1,padx=12,pady=5)


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

        #### Gets IP Information
        pingIP = self.PingAdd.get()
        os.system('ping ' + pingIP + '> "C:\\Users\\Public\\ping.txt"')
        pingResults = open('C:\\Users\\Public\\ping.txt','r')
        pingRE = pingResults.read()
        self.resultsPing.config(text=pingRE)
        self.PingAdd.delete(0,END)
        
        pingResults.close()

        #### Clean up text files by deleting them
        ping_clean = 'DEL ' + 'C:\\Users\\Public\\ping.txt'

        os.system(ping_clean)

    ### Basic one button that calls google.com to see if it can get signal
    def internetTest(self):

        #### Gets IP Information
        os.system('ping www.google.com> "C:\\Users\\Public\\ping.txt"')
        pingResults = open('C:\\Users\\Public\\ping.txt','r')
        pingRE = pingResults.read()
        self.resultsPing.config(text=pingRE)
        self.PingAdd.delete(0,END)
        
        pingResults.close()

        #### Clean up text files by deleting them
        ping_clean = 'DEL ' + 'C:\\Users\\Public\\ping.txt'

        os.system(ping_clean)

###################################### Class for choosing a power plan ##############################################################
class PowerOptions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        powersaver = tk.Button(self,text="Power Saver...",width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200, command=self.powerSaver)
        powersaver.grid(row=0,column=0,padx=12,pady=(10,5))
        powerSaveDiscription= tk.Label(self, text="*Saves energy by reducing your computer's performance where possible.", font=SMALL_FONT, wraplength=250)
        powerSaveDiscription.grid(row=1, column=0, pady=(0,20), sticky='N')

        balanced = tk.Button(self,text="Balanced Power.",width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200, command=self.balPow)
        balanced.grid(row=0,column=1,padx=12,pady=(10,5))
        balancedDiscription= tk.Label(self, text="*Automatically balances performance with energy consumption on capable hardware.", font=SMALL_FONT, wraplength=250)
        balancedDiscription.grid(row=1, column=1, pady=(0,20), sticky='N')

        high = tk.Button(self,text="High Performance!",width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200, command=self.highPow)
        high.grid(row=2,column=0,padx=12,pady=5)
        highPerDiscription= tk.Label(self, text="*Favors performance, but may use more energy.", font=SMALL_FONT, wraplength=250)
        highPerDiscription.grid(row=3, column=0, sticky='N')
        
        ultimate = tk.Button(self,text="ULTIMATE PERFORMANCE!!!",width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200, command=self.ultPow)
        ultimate.grid(row=2,column=1,padx=12,pady=5)
        ultimateDiscription= tk.Label(self, text="*Provides ultimate performance on higher end PC's.", font=SMALL_FONT, wraplength=250)
        ultimateDiscription.grid(row=3, column=1, sticky='N')
        
        returnButton = tk.Button(self,text="Back to Options",width=26, height=5, font=MEDIUM_FONT, padx=5,pady=5,bg='#b3001b', fg='white', wraplength=200, command=lambda: controller.show_frame(AJsUtilitiesButtons))
        returnButton.grid(row=8,column=0,padx=12,pady=(120,50))

    ##################### Functions to go with the buttons #########################
    #Enable PowerSaver
    def powerSaver(self):
        os.system('powercfg /l> "C:\\Users\\Public\\poweroptions.txt"')
        with open('C:\\Users\\Public\\poweroptions.txt', 'r') as powerfind:
            for option in powerfind:
                if "Power saver" in option:
                    key_seg = option[19:55]

        new_cmd = 'powercfg /s ' + key_seg
        power_clean = 'DEL ' + 'C:\\Users\\Public\\poweroptions.txt'

        os.system(power_clean)
        os.system(new_cmd)

    #Enable Balanced Power
    def balPow(self):
        os.system('powercfg /l> "C:\\Users\\Public\\poweroptions.txt"')
        with open('C:\\Users\\Public\\poweroptions.txt', 'r') as powerfind:
            for option in powerfind:
                if "Balanced" in option:
                    key_seg = option[19:55]

        new_cmd = 'powercfg /s ' + key_seg
        power_clean = 'DEL ' + 'C:\\Users\\Public\\poweroptions.txt'

        os.system(power_clean)
        os.system(new_cmd)

    #Enable High Performance
    def highPow(self):
        os.system('powercfg /l> "C:\\Users\\Public\\poweroptions.txt"')
        with open('C:\\Users\\Public\\poweroptions.txt', 'r') as powerfind:
            for option in powerfind:
                if "High" in option:
                    key_seg = option[19:55]

        new_cmd = 'powercfg /s ' + key_seg
        power_clean = 'DEL ' + 'C:\\Users\\Public\\poweroptions.txt'

        os.system(power_clean)
        os.system(new_cmd)

    #Enable Ultimate Performance
    def ultPow(self):
        os.system('powercfg /l> "C:\\Users\\Public\\poweroptions.txt"')
        with open('C:\\Users\\Public\\poweroptions.txt', 'r') as powerfind:
            for option in powerfind:
                if "Ultimate" in option:
                    key_seg = option[19:55]

        new_cmd = 'powercfg /s ' + key_seg
        power_clean = 'DEL ' + 'C:\\Users\\Public\\poweroptions.txt'

        os.system(power_clean)
        os.system(new_cmd)

###################################### Windows Updater ##############################################################
class AllowUpdates(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        installUpdates = tk.Button(self, text="Install Updates", command=self.update,width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200)
        installUpdates.grid(row=0, column=0, padx=12,pady=(10,5))

        AllowUpdate = tk.Button(self, text="Enable Automatic Updates", command=self.AllowUpdates,width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200)
        AllowUpdate.grid(row=0, column=1, padx=12,pady=(10,5))

        DenyUpdate = tk.Button(self, text="Disable Automatic Updates", command=self.DenyUpdateAuto,width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200)
        DenyUpdate.grid(row=1, column=0, padx=12,pady=5)

        UpdateAndInst = tk.Button(self, text="Enable Updates and Install Updates", command=self.AllowAndUpdate,width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200)
        UpdateAndInst.grid(row=1, column=1, padx=12,pady=5)

        returnButton = tk.Button(self,text="Back to Options",width=26, height=5, font=MEDIUM_FONT, padx=5,pady=5,bg='#b3001b', fg='white', wraplength=200, command=lambda: controller.show_frame(AJsUtilitiesButtons))
        returnButton.grid(row=8,column=0,padx=12,pady=(120,50))

    ##################### Functions to go with the buttons #########################
    def update(self):
        tk.messagebox.showinfo('Auto Update', 'The update process will begin, another notification will be present when this process is complete and/or your computer will automatically restart.')
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + 'powershell Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force; Install-Module PSWindowsUpdate -Force; Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force; Import-Module PSWindowsUpdate; Add-WUServiceManager -ServiceID 7971f918-a847-4430-9279-4a52d1efe18d -Confirm:$false; Install-WindowsUpdate -AcceptAll -MicrosoftUpdate -AutoReboot')
##        global checkBoxIndic
##        checkBoxIndic = False

##        def checkBox():
##            global checkBoxIndic
##            while(checkBoxIndic):
##                time.sleep(10)
##                try:
##                    with open('C:\\Users\\Public\\Update.txt', 'r') as works:
##                        for confirmation in works:
##                            if "Done" in confirmation:
##                                tk.messagebox.showinfo('Auto Update', 'Updates have concluded, your computer may or may not restart.')
##                                checkBoxIndic = True
##                            else:
##                                print('This file has something wrong')
##                except:
##                    print('Test')
##                    pass

    def AllowUpdates(self):
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + 'sc config wuauserv start=auto & reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU')
        
    def DenyUpdateAuto(self):
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + 'sc config wuauserv start=disabled & reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update" /v AUOptions /t REG_DWORD /d 1 /f')

    def AllowAndUpdate(self):
        tk.messagebox.showinfo('Auto Update', 'The update process will begin, another notification will be present when this process is complete and/or your computer will automatically restart.')
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c' + 'sc config wuauserv start=auto & reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU & powershell Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force; Install-Module PSWindowsUpdate -Force; Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force; Import-Module PSWindowsUpdate; Add-WUServiceManager -ServiceID 7971f918-a847-4430-9279-4a52d1efe18d -Confirm:$false; Install-WindowsUpdate -AcceptAll -MicrosoftUpdate -AutoReboot')

################################### IP Config ##################################################################################
class IPConfig(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        GetIP = tk.Button(self, text="Get IP Addresses", command=self.getIP,width=26, height=5, font=LARGE_FONT, padx=5,pady=5,bg='#b3001b', fg='white',wraplength=200)
        GetIP.grid(row=0, column=0, sticky='E', pady=(10,5), padx=(0,28))

        scrollbar = Scrollbar(self, width = 16)
        scrollbar.grid(row=1, column = 1, pady=(20,20))

        self.resultsIP = tk.Listbox(self, yscrollcommand=scrollbar.set, width=55,height=20)
        self.resultsIP.grid(row=1, column=0, padx=(125,0), pady=(20,20))

        scrollbar.config(command = self.resultsIP.yview)

        returnButton = tk.Button(self,text="Back to Options",width=26, height=5, font=MEDIUM_FONT, padx=5,pady=5,bg='#b3001b', fg='white', wraplength=200, command=lambda: controller.show_frame(AJsUtilitiesButtons))
        returnButton.grid(row=8,column=0,padx=12,pady=(0,50),sticky='W')

    ##################### Functions to go with the buttons #########################
    def getIP(self):
        os.system('ipconfig> "C:\\Users\\Public\\ips.txt"')
        with open('C:\\Users\\Public\\ips.txt', 'r') as ipInfo:
            for line in ipInfo:
                self.resultsIP.insert(END, line)
        
        ip_clean = 'DEL ' + 'C:\\Users\\Public\\ips.txt'
        os.system(ip_clean)


################################### Map Drives ##################################################################################
class MapDrive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        description = tk.Label(self, text="Choose to either map a drive or delete a mapped drive.", font=LARGE_FONT, wraplength=600)
        description.grid(row=0, column=0, columnspan=4, padx = (55,0), pady=(10,10))

        returnButton = tk.Button(self,text="Back to Options",width=26, height=5, font=MEDIUM_FONT, padx=5,pady=5,bg='#b3001b', fg='white', wraplength=200, command=lambda: controller.show_frame(AJsUtilitiesButtons))
        returnButton.grid(row=8,column=0,padx=12,pady=(20,50))

        deleteDriveLabel = tk.Label(self, text="Delete a drive", font=MEDIUM_FONT)
        deleteDriveLabel.grid(row=1, column=2, columnspan=2)
        
        mapDriveLabel = tk.Label(self, text="Map a drive", font=MEDIUM_FONT)
        mapDriveLabel.grid(row=1, column=0, columnspan=2)

        chooseDriveDelLabel = tk.Label(self, text="Choose Drive:", font=MEDIUM_FONT)
        chooseDriveDelLabel.grid(row=2, column=2)

        deleteDriveButton= tk.Button(self, text="DELETE!!", command=self.deleteDrive, font=MEDIUM_FONT, padx=5,pady=5,bg='#b3001b', fg='white', wraplength=200)
        deleteDriveButton.grid(row=3, column=2, columnspan = 2)

        CreateDriveButton= tk.Button(self, text="MAP!", command=self.mapDrive, font=MEDIUM_FONT, padx=5,pady=5,bg='#b3001b', fg='white', wraplength=200)
        CreateDriveButton.grid(row=3, column=0, columnspan=2)

        diskInfo = tk.Button(self, text='Details for Drives', command=self.diskInfo, font=LARGE_FONT, bg='#b3001b', fg='white', wraplength=200)
        diskInfo.grid(row=4, columnspan=4, pady=(10,0), padx=(60,0))

        scrollbarx = Scrollbar(self, width = 16)
        scrollbarx.grid(row=6, column = 0, columnspan=4,sticky='N', padx=(70,0), pady=(0,20))

        scrollbary = Scrollbar(self, width = 16)
        scrollbary.grid(row=5, column = 3, pady=(20,20),sticky='W')
        
        self.resultsDrive = tk.Listbox(self, xscrollcommand=scrollbarx.set, yscrollcommand=scrollbary.set, width=55,height=15)
        self.resultsDrive.grid(row=5, column=0, padx=(125,0), pady=(20,0), columnspan=3)

        scrollbarx.config(command = self.resultsDrive.xview, orient=HORIZONTAL)
        scrollbary.config(command = self.resultsDrive.yview)
        
        self.address = tk.Entry(self,width=40)
        self.address.grid(row=2, column=0)
        

        ##This is for the drop down menu's for the drives
        optionList = MapDrive.listAvailableDrives()
        self.v = tk.StringVar(parent)
        self.v.set(optionList[0])
        self.om = tk.OptionMenu(self,self.v,*optionList)
        self.om.grid(row=2,column=1, sticky='W')

        deleteList = MapDrive.findMappedDrives()
        self.v1 = tk.StringVar(parent)
        self.v1.set(deleteList[0])
        self.om1 = tk.OptionMenu(self,self.v1,*deleteList)
        self.om1.grid(row=2,column=3)
        
    ##################### Functions to go with the buttons #########################
    def mapDrive(self):
        driveToMap = self.v.get()
        addressOfDrive = self.address.get()
        os.system('net use ' + driveToMap + ' ' + addressOfDrive)
        MapDrive.reset(self)
        self.address.delete(0,END)
        #print('net use ' + driveToMap + ' ' + addressOfDrive)

    def deleteDrive(self):
        driveToDelete = self.v1.get()
        os.system('net use ' + driveToDelete + ' /delete')
        #print('net use ' + driveToDelete + ' /delete')
        MapDrive.reset(self)
        
    def findMappedDrives():
        os.system('fsutil fsinfo drives> "C:\\Users\\Public\\drives.txt"')
        findDrives = open('C:\\Users\\Public\\drives.txt', 'r')
        allDrives = findDrives.read().split(' ')
        allDrives.remove(allDrives[-1])
        allDrives.remove(allDrives[0])
        
        holder = [] #Holds new list of options
        for option in allDrives:
            holder.append(option[0:2])

        return holder


        findDrives.close()
        drive_clean = 'DEL ' + 'C:\\Users\\Public\\drives.txt'
        os.system(drive_clean)

    def listAvailableDrives():
        allLetterDrives = ['A:', 'B:', 'C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']

        holder = MapDrive.findMappedDrives()
        for x in holder:
            for y in allLetterDrives:
                if x == y:
                    allLetterDrives.remove(y)

        return allLetterDrives

    def reset(self):
        optionList = []
        deleteList = []
        self.om.children['menu'].delete(0,"end")
        self.om1.children['menu'].delete(0,"end")
        optionList = MapDrive.listAvailableDrives()
        deleteList = MapDrive.findMappedDrives()
        
        for ava in optionList:
            self.om.children['menu'].add_command(label=ava, command= lambda ma=ava: self.v.set(ma))
        self.v.set(optionList[0])
        
        for use in deleteList:
            self.om1.children['menu'].add_command(label=use, command= lambda u=use: self.v1.set(u))
        self.v1.set(deleteList[0])

    def diskInfo(self):
        os.system('wmic logicaldisk get caption,description,providername>"C:\\Users\\Public\\drivesInfo.txt"')
        with open('C:\\Users\\Public\\drivesInfo.txt', 'r') as driveInfo:
            self.resultsDrive.delete(0,END)
            for line in driveInfo:
                self.resultsDrive.insert(END, line)

        #### Clean up text files by deleting them
        drive_clean = 'DEL ' + 'C:\\Users\\Public\\drivesInfo.txt'
        os.system(drive_clean)
        
        

#Continuously has gui up.

app = AJsUtilities()
app.geometry("600x600")
app.mainloop()
