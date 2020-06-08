import tkinter as tk    
from tkinter import Tk, Label, Button, Entry, W , E, Scale, HORIZONTAL, Frame
from lib.sitepackages import pypyodbc
from User import User


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='azure')
        self.DBfile = '.\\newsChecker.mdb'
        self.conn = pypyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb)};DBQ='+self.DBfile)
        self.myCursor = self.conn.cursor()
        self.controller = controller
        self.labelHeader = tk.Label(self, text="Login Web Scraper",bg='azure', font=controller.title_font)
        self.labelHeader.grid(column=0, row= 0, pady=5)

        self.emailLabel = tk.Label(self, text="Please enter your email adress", bg='azure', font='Helvetica 10 bold',).grid(column=0,row=1, pady=20)
        self.emailEntry = tk.Entry(self,width=50)
        self.emailEntry.grid(column=1,row=1, pady=20)


        self.passwordLabel = tk.Label(self,text="Please enter your password",bg='azure', font='Helvetica 10 bold',).grid(column=0,row=2, pady=10)
        self.passwordEntry = tk.Entry(self,show="*",width=50)
        self.passwordEntry.grid(column=1,row=2, pady=10)

        self.txt =  tk.Text(self,width=40,height=10, pady=10)
        self.txt.grid(column=1,row=3, pady=5)
        
        self.button1 = tk.Button(self, text="Login", width='40', bg="royal blue",fg='white' ,font='Helvetica 10 bold',command=self.login) # Login DevMode for no login
        self.button1.grid(column=1, row=4, pady=15 )
        self.button2 = tk.Button(self, text="Register new account ",width='40', fg='white', bg="lawn green", font='Helvetica 10 bold',
                            command=lambda: controller.show_frame("RegisterPage"))
        self.button2.grid(column=1, row=5,  pady=10)

    def loginDevMode(self):
        self.controller.show_frame("ScrapePage")

    def login(self):
        password="placeholder for the problem before assaigning a variable, password issue isnt fixed so far but this password as standardpassword is to 99.9999 % not used"
        SQL = "SELECT * FROM user WHERE email='"+self.emailEntry.get()+"'"
        print(SQL)
        userAttributes = []
        user = self.myCursor.execute(SQL)   
        print(user)
        for data in user:
            password = data[3]
        if password == self.passwordEntry.get():
            self.controller.show_frame("ScrapePage")
        else:
            self.clearTextField()
            self.txt.insert(tk.END,' password or  email dont match')
       
    def clearTextField(self):
        self.txt.delete('1.0',tk.END)
            


