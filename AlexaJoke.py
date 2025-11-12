from tkinter import *
from random import choice
import pygame

def playInitialDrum():
    try:
        #plays the drumroll when it shows the question part of the joke
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load("Drum Roll Sound Effect [High Quality].mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(loops=-1)#it will loop until the punchline drum stops it
    except Exception as e:
        print("playInitialDrum failed:", e) #if anything goes wrong, it will show this

def playPunchLineDrum():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop() #this will stop the drumroll sound and queue the punchline drum
        else:
            pygame.mixer.init()
        pygame.mixer.music.load("Joke Drum Sound Effect.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play() #this will only play once then stop until the next joke
    except Exception as e:
        print("playPunchLineDrum failed:", e) #same thing, any error will show this

def sendJoke(path="randomJokes.txt"): #this opens the jokes file
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [ln.strip() for ln in f if ln.strip()] #will return a random line
    except FileNotFoundError:
        return ["Joke file not found: randomJokes.txt"]

jokes = sendJoke()

#this will separate the question and punchline using "?" as the tracker
def separatePunchline(line):
    line = line.strip()
    question, separate, rest = line.partition('?') #this will get rid of the question mark
    if separate:
        return (question.strip() + '?', rest.strip()) #returns both of them with the question mark readded

revealAfterDelay = None

def cancelReveal():#this will help in putting a delay to revealing the punchline
    global revealAfterDelay
    if revealAfterDelay is not None:
        try:
            root.after_cancel(revealAfterDelay)#if the delay is not needed, this will cancel it
        except Exception:
            pass
        revealAfterDelay = None
    try:#the punchline drum will not play if the user cancels reveal
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except Exception:
        pass
    displayJoke.config(state=NORMAL)#this will enable usage of the button
    backButton.config(state=NORMAL)#same thing

def showJoke(raw, delay=1500):#this is the actual delay of the punchline
    global revealAfterDelay
    cancelReveal()#calls the other function
    question, punchline = separatePunchline(raw)#raw means the entire, non-separated joke
    if punchline:
        #show question first
        JokeText.configure(text=question)
        #play drumroll while waiting for punchline
        try:
            playInitialDrum()#this is the inital drumroll
        except Exception:
            pass
        #you cant use the buttons while waiting for the reveal
        displayJoke.config(state=DISABLED)
        backButton.config(state=DISABLED)
        #this will set the time between the question and punchline reveal
        revealAfterDelay = root.after(delay, lambda: revealPunchline(question, punchline))
    else:#the whole joke will show as normal if the punchline isn't found
        JokeText.configure(text=question)
        displayJoke.config(state=NORMAL)
        backButton.config(state=NORMAL)

def revealPunchline(question, punchline):#pausing the initial drumroll
    global revealAfterDelay
    #calls the cancel to then play the punchline drum
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except Exception:
        pass
    JokeText.configure(text=f"{question}\n\n{punchline}")
    try:
        playPunchLineDrum()
    except Exception:
        pass
    revealAfterDelay = None
    displayJoke.config(state=NORMAL)
    backButton.config(state=NORMAL)

def pickJoke():#grabs the random joke from the text file
    showJoke(choice(jokes))
    switchFrames(jokeShowFrame)#switches to the joke frame

def switchFrames(frame):#switches between both frames
    cancelReveal()
    frame.tkraise()

root = Tk()#starting the actual tkinter display
root.title("Alexa's Jokes")
root.geometry("420x200")
root.resizable(False, False)#you cant increase or decrease the window manually

givenAnswer = StringVar()

#this frame stacks all other frames inside it
containerFrame = Frame(root)
containerFrame.grid(row=0, column=0, sticky="nsew")
containerFrame.grid_rowconfigure(0, weight=1)
containerFrame.grid_columnconfigure(0, weight=1)

#this is the inital frame
titleFrame = Frame(containerFrame, bg="#4CAF50", pady=10)
titleFrame.grid(row=0, column=0, sticky="nsew")

titleLabel = Label(titleFrame, text="Alexa's Jokes", bg="#4CAF50", fg="white", font=("Arial", 16, "bold"))
titleLabel.pack(pady=(8,4))

jokeButton = Button(titleFrame, text="Tell me a joke!", command=pickJoke, bg="#388E3C", fg="white", font=("Arial", 12))
jokeButton.pack(padx=10, pady=10)

#this is the frame where the jokes are shown
jokeShowFrame = Frame(containerFrame, bg="#E8F5E9", pady=10)
jokeShowFrame.grid(row=0, column=0, sticky="nsew")

#firstJoke shows the inital joke after pressing the button in title frame
firstJoke = choice(jokes)
JokeText = Message(jokeShowFrame, text=firstJoke, width=380, font=("Arial", 12), bg="#E8F5E9")
JokeText.pack(padx=10, pady=(16,8))

#this inside the joke frame
buttonFrame = Frame(jokeShowFrame, bg="#E8F5E9")
buttonFrame.pack(pady=(0,10))

#gives you the option for another joke
displayJoke = Button(buttonFrame, text="Another!", command=lambda: showJoke(choice(jokes)))
displayJoke.grid(row=0, column=0, padx=6)

#returns to title screen
backButton = Button(buttonFrame, text="Back", command=lambda: switchFrames(titleFrame))
backButton.grid(row=0, column=1, padx=6)

#stops the whole code from running
stopJokes = Button(buttonFrame, text="Close", command=root.destroy)
stopJokes.grid(row=0, column=2, padx=6)

#title frame will show first
switchFrames(titleFrame)


root.mainloop()