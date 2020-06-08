import tkinter as tk
from User import User
from tkinter import Tk, Label, Button, Entry, W , E, Scale, HORIZONTAL, Frame
from lib.sitepackages import pypyodbc
import datetime



class RegisterPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="azure")
        self.DBfile = '.\\NewsChecker.mdb'
        self.conn = pypyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb)};DBQ='+self.DBfile)
        self.myCursor = self.conn.cursor()
        self.controller = controller
        self.label = tk.Label(self, text="Web Scrape Register",bg="azure", font=controller.title_font)
        self.label.grid(row=0,column=0)

        self.labelName = tk.Label(self, text="Please enter your Name" , bg="azure" ,font='Helvetica 10 bold').grid(row=1,column=0)
        self.entryName = tk.Entry(self, width="50")
        self.entryName.grid(row=1,column=1, pady=20, padx=10)

        self.labelGender =  tk.Label(self, text="Which gender are you? ", bg="azure",font='Helvetica 10 bold').grid(row=2,column=0,pady=10, padx=10)
        self.mOF  =  tk.StringVar()
        self.mOF.set("Male")
        self.option = tk.OptionMenu(self, self.mOF,"Male", "Female", "Divers")
        self.option.grid(row=2, column=1,pady=10, padx=10)

        self.labelStudent =  tk.Label(self, text="Student status: " , bg="azure",font='Helvetica 10 bold').grid(row=3,column=0,pady=10, padx=10)
        self.var = tk.StringVar()
        self.var.set("0")
        self.checkButton = tk.Checkbutton(self, text="Are you a student", variable=self.var, onvalue=-1, offvalue=0, bg="azure" )
        self.checkButton.grid(row=3, column=1, pady=10, padx=10)

        self.labelEmail = tk.Label(self, text="Please enter your email adress", bg="azure" ,font='Helvetica 10 bold').grid(row=4,column=0, pady=10, padx=10)
        self.entryEmail =  tk.Entry(self, width="50")
        self.entryEmail.grid(row=4,column=1)


        self.labelPassword =  tk.Label(self, text="Password (min 6. charackters)", bg="azure",font='Helvetica 10 bold').grid(row=5,column=0, pady=10, padx=10)
        self.entryPassword =  tk.Entry(self,show="*", width="50")
        self.entryPassword.grid(row=5,column=1, pady=10, padx=10)


        self.labelPassword1 =  tk.Label(self, text="Please repeat your Password", bg="azure",font='Helvetica 10 bold').grid(row=6,column=0, pady=10, padx=10)
        self.entryPassword1 =  tk.Entry(self, show="*", width="50")
        self.entryPassword1.grid(row=6,column=1, pady=10, padx=10)


        self.labelText = tk.Label(self,text="Please take care: " , bg="azure",font='Helvetica 10 bold').grid(row=7, column=0, pady=10, padx=10)
        self.txt = tk.Text(self,width="35", height="10")
        self.txt.grid(row=7,column=1, padx=10, pady=10)


        button = tk.Button(self, text="Register", fg="white" , bg="lawn green", width='40', font='Helvetica 10 bold', command=self.registerUser).grid(row=8, column=1, pady=10,padx=10)

        button = tk.Button(self, text="Go to the start page",fg="white" , bg="royal blue", width='40',font='Helvetica 10 bold', command=lambda: controller.show_frame("StartPage"))
        button.grid(row=9, column=1,pady=10,padx=10)
    
    def checkPassword(self): 
        return len(self.entryPassword.get()) >= 6 and (self.entryPassword.get() == self.entryPassword1.get())

    def checkFilled(self):
        return len(self.entryName.get())>0  and len(self.entryEmail.get()) > 0 and len(self.mOF.get()) > 1


    def registerUser(self):
        if (self.checkPassword() and self.checkFilled()):
            self.clearTextField()
        
            date = datetime.datetime.now()
            newUser = User(self.entryName.get(), self.mOF.get(), self.entryEmail.get(),self.entryPassword.get(),self.var.get(),date.strftime('%m/%d/%Y'))


            print(self.var.get())
            print(date.strftime('%m/%d/%Y'))
            
            self.saveUser(newUser)
            
            self.txt.insert(tk.END,"You have successfully registerd your new Account")
            self.txt.insert(tk.END,"\n")
            
            self.clearText()
            
            print('Nice! You registered your Account')
            
        elif (self.checkPassword() and not self.checkFilled()):
            self.clearTextField()
            self.txt.insert(tk.END,'You didnt filled out every reuired field')
        elif (self.checkFilled() and not self.checkPassword()):
            self.clearTextField()
            self.txt.insert(tk.END,"Youre Password doesent have the "  + "\n" + "needed security standards")
        else:
            self.clearTextField()
            self.txt.insert(tk.END,"Please fill out every field and" + "\n" + "youre password must contain"  + "\n" +"atleast 6 letters or digit")
    

    
    def saveUser(self,user):
        self.clearTextField()
        SQL_insert = "insert into user(username,gender,email,password,student,registerDate) values ('"+user.getUserName() +"','"+ user.getGender()+"','" + user.getEmail()+"','" + user.getPassword()+"','" + user.getStudent() +"','" + user.getRegisterDate() + "')"
        self.myCursor.execute(SQL_insert)
        self.myCursor.commit()

    
    def clearText(self):
        self.entryName.delete(0, tk.END)
        self.entryEmail.delete(0, tk.END)
        self.entryPassword.delete(0, tk.END)
        self.entryPassword1.delete(0, tk.END)

    def clearTextField(self):
        self.txt.delete('1.0',tk.END)




    ########VERSION WITHOUT DAO LAYER #################

    def register(self): 
        if (self.checkPassword() and self.checkFilled()):
            self.clearTextField()
            SQL_insert = "insert into user(username,gender,email,password) values ('"+self.entryName.get()+"','"+self.mOF.get()+"','" +self.entryEmail.get()+"','" + self.entryPassword.get()+"')"
            self.myCursor.execute(SQL_insert)
            self.myCursor.commit()            
            self.txt.insert(tk.END,"You have successfully registerd your new Account")           
            self.clearText()
            print('Nice! You registered your Account')
        elif (self.checkPassword() and not self.checkFilled()):
            self.clearTextField()
            self.txt.insert(tk.END,'You didnt filled out every reuired field')
        elif (self.checkFilled() and not self.checkPassword()):
            self.clearTextField()
            self.txt.insert(tk.END,"Youre Password doesent have the needed security standards")
        else:
            self.clearTextField()
            self.txt.insert(tk.END,"Please fill out every field and youre password must containt atleast 6 letters or digit")


