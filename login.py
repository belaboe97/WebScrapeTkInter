import tkinter as tk    
from tkinter import Tk, Label, Button, Entry, W , E, Scale, HORIZONTAL, Frame , END, Text
from bs4 import BeautifulSoup
import requests
from requests import get
from lib.sitepackages import pypyodbc
import soupsieve



class ScrapePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.DBfile = '.\\newsChecker.mdb'
        self.conn = pypyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb)};DBQ='+self.DBfile)
        self.myCursor = self.conn.cursor()
        self.controller = controller

        self.label = tk.Label(self, text="This is page 2", font=controller.title_font)

        self.linkEntry = tk.Entry(self,width=50)
        self.linkEntry.pack()

        self.outputText = tk.Text(self, width=20 , height=10)
        self.outputText.pack()

        self.getDataButtton  = tk.Button(self, width=30, fg="white" , bg="black" , command=self.getData).pack()
        
        self.label.pack(side="top", fill="x", pady=10)

        self.tableNameEntry = tk.Entry(self,width=50)
        self.tableNameEntry.pack()
        
        self.createTableBtn =  tk.Button(self, text="Create New Table", command=self.createNewDatabaseTable)
        self.createTableBtn.pack()

        self.getTableBtn =  tk.Button(self, text="Create New Table", command=self.getTableNames)
        self.getTableBtn.pack()
        
        
        self.button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))

                        
        self.button.pack()

    def getData(self):
        url = self.linkEntry.get()
        print(url)
        
        self.outputText.insert(tk.END,url)
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
                SQL_insert = "insert into tabletest(IndexNumber,Linkname) values ('"+str(counter)+"','"+content+"')"
                row = self.myCursor.execute(SQL_insert)
                self.myCursor.commit()
                counter += 1
        except:
            print("Data is allready saved")
            
    def createNewDatabaseTable(self):
        try:
             SQL_insert = "CREATE TABLE "+ self.tableNameEntry.get()+"( IndexNumber  INTEGER  PRIMARY KEY, LinkName CHAR (100));"
             self.myCursor.execute(SQL_insert)
        except:
            print("Table already exists")

    def getTableNames(self):
        SQL_insert =  "SELECT MSysObjects.Name AS table_name FROM MSysObjects WHERE (((Left([Name],1))<>'~') AND ((Left([Name],4))<>'MSys') AND ((MSysObjects.Type) In (1,4,6)) AND ((MSysObjects.Flags)=0)) order by MSysObjects.Name"
        tableNames = self.myCursor.execute(SQL_insert)
        print(tableNames)














        
