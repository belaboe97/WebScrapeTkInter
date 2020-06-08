import tkinter as tk    
from tkinter import Tk, Label, Button, Entry, W , E, Scale, HORIZONTAL, Frame , END, Text
from bs4 import BeautifulSoup
import requests
from requests import get
from lib.sitepackages import pypyodbc
import soupsieve



class ScrapePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="azure")
        self.DBfile = '.\\newsChecker.mdb'
        self.conn = pypyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb)};DBQ='+self.DBfile)
        self.myCursor = self.conn.cursor()
        self.controller = controller

        self.label = tk.Label(self, text="Webscrape", font=controller.title_font, bg='azure').grid(row=0,column=0)


        self.linkLabel = tk.Label(self, text="ScrapeLink :", bg='azure', font='Helvetica 10 bold').grid(row=1,column=0)
        self.linkEntry = tk.Entry(self,width=50)
        self.linkEntry.grid(row=1,column=1)

        self.labelDatabase = tk.Label(self, text="Create and Save Table", bg='azure', font='Helvetica 10 bold').grid(row=2,column=0)
        self.tableNameEntry = tk.Entry(self,width=50)
        self.tableNameEntry.grid(row=2,column=1)
        
        self.linkTextLabel = tk.Label(self, text="Choose one Link: ", bg='azure', font='Helvetica 10 bold').grid(row=3,column=0)
        self.textLinks = tk.Text(self, width=50,height=10)
        self.textLinks.grid(row=4,column=0)

        self.textLinks.insert(tk.END,'https://www.learnlaravel.me/getting-started/')
        self.textLinks.insert(tk.END, '\n')
        self.textLinks.insert(tk.END,'https://www.learnlaravel.me/validation-and-business-logic/')
        self.textLinks.insert(tk.END, '\n')
        self.textLinks.insert(tk.END,'https://www.learnlaravel.me/templating-and-views/')
        self.textLinks.insert(tk.END, '\n')
        self.textLinks.insert(tk.END,'https://www.learnlaravel.me/integrating-components/')
        self.textLinks.insert(tk.END, '\n')
        self.textLinks.insert(tk.END,'https://www.learnlaravel.me/security/')
        self.textLinks.insert(tk.END, '\n')


        self.outputText = tk.Text(self, width=40 , height=10)
        self.outputText.grid(row=4,column=1)

        self.getDataButtton  = tk.Button(self , text="Save to existing Table", command=self.saveData, fg="white" , bg="gold", width='40', font='Helvetica 10 bold').grid(row=5,column=1, pady=10,padx=10)
        
        self.createTableBtn =  tk.Button(self, text="Create New Table", command=self.createNewDatabaseTable, fg="white" , bg="dark turquoise", width='40', font='Helvetica 10 bold')
        self.createTableBtn.grid(row=6,column=1, pady=10,padx=10)

        
        self.getTableBtn1 =  tk.Button(self, text="Get All Existing Table Names", command=self.getAllTableNames,fg="white" , bg="brown1", width='40', font='Helvetica 10 bold')
        self.getTableBtn1.grid(row=7,column=1, pady=10,padx=10)

        self.getTableBtn =  tk.Button(self, text="Save new Tablename", command=self.saveTableName, fg="white" , bg="deep pink", width='40', font='Helvetica 10 bold')
        self.getTableBtn.grid(row=8,column=1, pady=10,padx=10)

        
        self.saveNewBtn =  tk.Button(self, text="New Table & Save Data", command=self.saveDataToNewTable, fg="white" , bg="lawn green", width='40', font='Helvetica 10 bold')
        self.saveNewBtn.grid(row=9,column=1, pady=10,padx=10)
        
        
        self.button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"),fg="white" , bg="royal blue", width='40', font='Helvetica 10 bold')

                        
        self.button.grid(row=10,column=1, pady=10,padx=10)

    def saveData(self):
        url = self.linkEntry.get()
        print(url)
        
        self.clearTextField()
        response = get(url)

        html_soup = BeautifulSoup(response.text, 'html.parser')

        content = html_soup.find('div',"entry-content")

        listelements =  content.findAll('li')

        link = content.li

        contentList = []

        for i in listelements:
            name = i.prettify().split('"')[3]
            contentList.append(name)

        try:
            counter = 0
            for content in contentList:
                SQL_insert = "insert into "+ self.tableNameEntry.get() +"(IndexNumber,Linkname) values ('"+str(counter)+"','"+content+"')"
                row = self.myCursor.execute(SQL_insert)
                self.myCursor.commit()
                counter += 1
                
                self.outputText.insert(tk.END,"Saved!")
        except:
            self.clearTextField()
            self.outputText.insert(tk.END,"Data is allready saved")
            
    def createNewDatabaseTable(self):
        try:
            SQL_insert = "CREATE TABLE "+ self.tableNameEntry.get()+"( IndexNumber INTEGER  PRIMARY KEY, LinkName CHAR (100) )"
            self.myCursor.execute(SQL_insert)
            self.outputText.insert(tk.END,"Table created!")
        except:
            self.clearTextField()
            self.outputText.insert(tk.END,"Table allready exist!")

    def saveTableName(self):
        try:
            SQL_insert = "insert into TableNames(Tablenames) values ('"+self.tableNameEntry.get()+"')"
            row = self.myCursor.execute(SQL_insert)
            self.myCursor.commit()
        except:
            self.clearTextField()
            self.outputText.insert(tk.END,'Cant save TableName')

    def getAllTableNames(self): 
        self.clearTextField()
        Sql_table = "Select * FROM TableNames"
        tables = self.myCursor.execute(Sql_table)
        for rows in tables: 
            self.outputText.insert(tk.END,rows[1])
            self.outputText.insert(tk.END,'\n')

    def saveDataToNewTable(self):
        try: 
            self.createNewDatabaseTable()
            self.saveTableName()
            self.saveData()
        except: 
            self.clearTextField()
            self.outputText.insert(tk.END,"Upps, something went wrong!")


    def getTableNamesID(self,tablename):
        Sql_table = "Select ID  from TableNames where Tablenames = '"+ tablename +"'"
        tables = self.myCursor.execute(Sql_table).fetchone()[0]
        self.myCursor.commit()
        return tables

    def clearTextField(self):
        self.outputText.delete('1.0',tk.END)

 













        
