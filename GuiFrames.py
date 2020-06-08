import tkinter as tk                
from tkinter import font  as tkfont 
from startpage import StartPage
from register import RegisterPage
from ScrapePage import ScrapePage



class ScraperApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for frames in (StartPage, RegisterPage, ScrapePage):
            page_name = frames.__name__
            frame = frames(parent=container, controller=self)
            self.frames[page_name] = frame

  
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()






if __name__ == "__main__":
    app = ScraperApp()
    app.mainloop()
