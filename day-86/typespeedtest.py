import time
import tkinter as tk

import requests 



class TypeSpeed(): 
    
    def __init__(self):
        
        #--------------------Vars----------------#
        self.time = 0




        #---------------------------- GUI SETUP ----------------------------------#
        
        self.window = tk.Tk()
        self.window.geometry("700x500")
        self.window.resizable(False, False)
        self.window.config(bg="#2E2E2E")
        self.window.title("Type speed test")



        title = tk.Label(self.window, 
                 text="Type Speed Test", 
                 font=("Times New Roman", 20, "bold italic"),  
                 bg="#2E2E2E", 
                 fg="#F5F5F5")
        
        title.place(x = 265, y = 30)

        self.instrs = tk.Label(self.window, 
                                 text="Instructions:\n1. Press 'Start' to begin.\n2. A random text will appear on the screen, and you need to type it in the text box.\n3. When you're done typing, press Enter.",
                                 font=("Arial", 12), 
                                 bg="#f0f0f0",  
                                 fg="#333333",  
                                 bd=2,  
                                 relief="solid", 
                                 padx=10, pady=10,  
                                 width=40, height=8,  
                                 wraplength=350)  

        
        self.instrs.place(relx=0.5, rely=0.2, anchor="n")

        self.start_button = tk.Button(self.window, 
                                 text="Start", 
                                 font=("Arial", 14), 
                                 bg="#4CAF50", 
                                 fg="white", 
                                 relief="flat", 
                                 padx=20, pady=10, 
                                 width=10, 
                                 height=2, 
                                 bd=0, 
                                 highlightthickness=0, 
                                 activebackground="#45a049", 
                                 activeforeground="white", 
                                 command= self.start)
        self.start_button.place(relx=0.5, y=350, anchor="n")

        self.window.mainloop()
    
    def start(self):
        #....type speed test...#
        
        self.instrs.destroy()
        self.start_button.destroy()

        self.randomText = self.getRandomtext() 
        print(self.randomText)
        self.textlb = tk.Label(self.window, 
                                 text=f"Text:\n{self.randomText}",
                                 font=("Arial", 10), 
                                 bg="#f0f0f0",  
                                 fg="#333333",  
                                 bd=2,  
                                 relief="solid", 
                                 padx=10, pady=10,  
                                 width=44, height=20,  
                                 wraplength=300)  
        
        self.textlb.place(x = 180, rely=0.2, anchor="n")

        self.text_area = tk.Text(self.window, 
                             font=("Arial", 10), 
                             width=44, height=21, 
                             wrap="word", 
                             bd=2, relief="solid")
        
        self.initialtime = time.time()


        self.text_area.place(x= 525, rely=0.2, anchor="n") 
        self.text_area.bind("<Return>", self.on_enter)

        
        

    def on_enter(self, event): 
        user_input = self.text_area.get("1.0", "end")
        elapsedTime = time.time() - self.initialtime
        words_list = user_input.split()
        randList = self.randomText.split()
        
        j = 0
        for i, word in enumerate(words_list): 
            if word  == randList[i]: 
                j+= 1
        print(j/elapsedTime*60) 

        self.text_area.destroy()
        self.textlb.destroy()

        wpm = (j / elapsedTime) * 60 
        print(f"Palabras por minuto: {wpm}")

       
        self.final_message = tk.Label(self.window, 
                                      text=f"test finished!\nYour type speed is: {wpm:.2f} words per minute", 
                                      font=("Arial", 16, "bold"), 
                                      fg="#4CAF50",  
                                      bg="#f0f0f0", 
                                      pady=20)
        self.final_message.place(x=350, rely=0.4, anchor="n")

       
        self.close_button = tk.Button(self.window, 
                                      text="X", 
                                      font=("Arial", 12), 
                                      fg="white", 
                                      bg="red", 
                                      command= self.window.quit
                                      )
        self.close_button.place(x=350, rely=0.65, anchor="n")





    def getRandomtext(self): 
        words = requests.get("https://random-word-api.herokuapp.com/word?number=60").json()
        text = ""
        for word in words: 
            text = text + " " + word
        return text
         

    

typeSpeed = TypeSpeed()

