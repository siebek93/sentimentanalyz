"""
Imports

"""
import newspaper
from newspaper import Article
import nltk
from textblob import TextBlob
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext, filedialog
import PIL.Image,  PIL.ImageTk
import argparse
from io import BytesIO

import urllib.request



class Analyzer(object):
    def __init__(self,url):
    
            
        #getting the article from argparse with help from newspaper
        if args.url:
            self.article = Article(args.url,language='nl') #url if it does work
            self.article.download()

        elif args.offlinetext:
            with open(args.offlinetext,"r") as f:
                 #get offline text if url doesn't work
                self.article = Article('', language='nl')
                self.article.download(input_html=f.read())
        

        self.article.parse() #parse article for NLP
        self.article.nlp() #natural language processing of the article

        
        self.master_window = Tk()

        # Parent widget for the buttons
        self.buttons_frame = Frame(self.master_window)
        self.buttons_frame.grid(row=0, column=0, sticky=W+E)    

        self.btn_File = Button(self.buttons_frame, text='Save as', command=self.save)
        self.btn_File.grid(row=0, column=1, padx=(10), pady=10) #sizes

        #configuring buttoms and setting colors
        self.btn_File = Button(self.buttons_frame, text='Summary', command = self.get_summary, activebackground='red')
        self.btn_File.grid(row=0, column=2, padx=(10), pady=10) #sizes

        self.btn_File = Button(self.buttons_frame, text='Sentiment', command = self.get_sentiment, activebackground='blue')
        self.btn_File.grid(row=0, column=3, padx=(10), pady=10) #sizes

        self.btn_File = Button(self.buttons_frame, text='Exit', command = self.exits, background='lightblue', activebackground="red")
        self.btn_File.grid(row=0, column=4, padx=(10), pady=10) #sizes


        # Group1 Frame ----------------------------------------------------
        self.group1 = LabelFrame(self.master_window, text="Article", padx=5, pady=5)
        self.group1.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=E+W+N+S)

        self.master_window.columnconfigure(0, weight=1)
        self.master_window.rowconfigure(1, weight=1)

        self.group1.rowconfigure(0, weight=1)
        self.group1.columnconfigure(0, weight=1)

        # Create the textbox for the downloaded text & set the sizes
        txtbox = scrolledtext.ScrolledText(self.group1, width=80, height=20)
        txtbox.insert(INSERT, self.article.text)
        txtbox.grid(row=0, column=0,   sticky=E+W+N+S)

        mainloop()


    def get_summary(self):

        #getting the summary of the text and setting it in the frame
        txtbox = scrolledtext.ScrolledText(self.group1, width=80, height=20)
        txtbox.insert(INSERT, self.article.summary)
        txtbox.grid(row=0, column=0,sticky=E+W+N+S)
        btn_File = Button(self.buttons_frame, text='Full article', command = self.get_article, activebackground='red')
        btn_File.grid(row=0, column=2, padx=(10), pady=10)


    def get_article(self):
        txtbox = scrolledtext.ScrolledText(self.group1, width=80, height=20)
        txtbox.insert(INSERT, self.article.text)
        txtbox.grid(row=0, column=0,sticky=E+W+N+S)
        btn_File = Button(self.buttons_frame, text='Summary ', command = self.get_summary, activebackground='green')
        btn_File.grid(row=0, column=2, padx=(10), pady=10)


    def get_sentiment(self):
        #get the sentiment
        #Create a textblob object to analyze
        text_obj = TextBlob(self.article.summary) #processing summary instead of 
        sentiment = text_obj.sentiment.polarity
        #return a value between 1 (good) and -1 (bad) 0 = neutral
    ##    txtbox = scrolledtext.ScrolledText(group1, width=80, height=20)

        if sentiment == 0: #if 0 then neutral
            
            #setting photo's (need to be in the same folder to display)
            window = tk.Toplevel()
            try:
                with urllib.request.urlopen("https://i.pinimg.com/originals/59/84/64/5984646f336cca7e9446eff1bf4538f0.jpg") as picture_url:
                    s = picture_url.read()
                photo = PIL.ImageTk.PhotoImage(PIL.Image.open(BytesIO(s))) 
            except Exception as e:
                photo = PIL.ImageTk.PhotoImage(PIL.Image.open("neutral.jpg"))
            w = Label(window, image=photo, text=f"The sentiment is neutral {text_obj.sentiment.polarity}", compound=tk.BOTTOM)
            w.photo = photo
            w.pack()

        elif sentiment > 0: #if higher then zero positive
            try:
                with urllib.request.urlopen("https://i.pinimg.com/originals/95/7e/80/957e806e153ab4f3cdf21b7c366bfdfb.png") as picture_url:
                    s = picture_url.read()
                photo = PIL.ImageTk.PhotoImage(PIL.Image.open(BytesIO(s)))  
            except Exception as e:
                photo = PIL.ImageTk.PhotoImage(PIL.Image.open("positive.jpg")) 
            
           
            window = tk.Toplevel()
            w = Label(window, image=photo, text=f"The sentiment is positive {text_obj.sentiment.polarity}", compound=tk.BOTTOM)
            w.photo = photo
            w.pack()

        
        elif sentiment < 0: # if lower then 0 then negative
            try:
                with urllib.request.urlopen("https://i.pinimg.com/originals/b0/41/75/b04175fd1ffbefdc02d90136c262a6e3.jpg") as picture_url:
                    s = picture_url.read() ## getting image from online source
                photo = PIL.ImageTk.PhotoImage(PIL.Image.open(BytesIO(s))) ## converting to bytes and reading image
            except Exception as e:
                photo = PIL.ImageTk.PhotoImage(PIL.Image.open("negative.jpg")) 
            
            window = tk.Toplevel()
            w = Label(window, image=photo, text=f"The sentiment is negative {text_obj.sentiment.polarity}", compound=tk.BOTTOM)
            w.photo = photo
            w.pack()

        
        #save the file and catch exception if no file name given
    def save(self):
        try:
            name = filedialog.asksaveasfilename(defaultextension=".doc",
                                filetypes=[("Text files",".txt"),
                                            ("Word files",".doc")],
                                initialdir="dir",
                                title="Save as")
            with open(name, "w") as data:
                data.write(article.text)
            
        except FileNotFoundError as e:
            print(e)
            pass

    #exit the program
    def exits(self):
       self.master_window.destroy()



# main part to initialize class and get argument for processing url
if __name__ == "__main__":
        
    try:
		#parsing argument and gives printing option/ options to get different stocks/bitcoin
        parser = argparse.ArgumentParser(description='program to display sentiment + summary')
        parser.add_argument('-u', "--url" , type=str,
                        help='url to analyze', default="https://www.nu.nl/coronavirus/6099844/30000-medewerkers-acute-zorg-krijgen-vaccin-op-korte-termijn.html")
        parser.add_argument('-o', "--offlinetext" , type=str,
                        help='offline text HTML to analyze', default="voorbeeldtext.txt")

        args = parser.parse_args()
        e = Analyzer(args.url if args.url else args.offlinetext)


        #catch exception if you want to exit the program via terminal
    except KeyboardInterrupt:
                sys.exit(0)



