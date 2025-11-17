from tkinter import *
from random import choice
import pygame

"""
Please note that, while I made both of these audio functions myself,
I decided to use Github Copilot to make it cleaner. the init, music load,
set volume and play were all mine thanks to a bit of research into the
pygame library. However, the try and except blocks were suggested by Copilot
as a way to hunt down errors. In short, it added error-handling as a just in case effect.
"""

def playInitialDrum():
    try:
        #plays the drumroll when it shows the question part of the joke
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load("Drum Roll Sound Effect [High Quality].mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(loops=-1)#it will loop until the punchline drum stops it
    except Exception as e:
        print("playInitialDrum failed:", e)#if anything goes wrong, it will show this

def playPunchLineDrum():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()#this will stop the drumroll sound and queue the punchline drum
        else:
            pygame.mixer.init()
        pygame.mixer.music.load("Joke Drum Sound Effect.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()#this will only play once then stop until the next joke
    except Exception as e:
        print("playPunchLineDrum failed:", e)

def sendJoke(path="randomJokes.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [ln.strip() for ln in f if ln.strip()]#will return a random line
    except FileNotFoundError:
        return ["Joke file not found: randomJokes.txt"]

jokes = sendJoke()

"""
Please note that the separatePunchLine function was made with the help of GitHub Copilot
since I didn't even know that parsing the string line directly from the text file was possible. 
This helped me to make the cancelReveal and showJoke functions and adding the delay
to showing the punchline in the actual tkinter display.
Also, most of the try and except blocks were suggested by Copilot to help with error-handling,
since the original code that I made didn't have error-handlers.
"""

#this will separate the question and punchline using "?" as the tracker
def separatePunchline(line):
    line = line.strip()
    question, separate, rest = line.partition('?') #this will get rid of the question mark
    if separate:
        return (question.strip() + '?', rest.strip()) #returns both of them with the question mark readded

revealAfterDelay = None
currentPunchline = None

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
    revealButton.config(state=NORMAL)#again, same thing

def showJoke(raw, delay=1500):#this is the delaying part of the punchline
    global revealAfterDelay, currentPunchline
    cancelReveal()#calls other function
    question, punchline = separatePunchline(raw)#raw means the whole joke line without being separated yet
    currentPunchline = punchline
    if punchline:
        #shows question first
        JokeText.configure(text=question)
        try:
            playInitialDrum()#plays drumroll while showing the question ONLY
        except Exception:
            pass
        #all buttons except showing the punchline option are disabled
        displayJoke.config(state=DISABLED)
        backButton.config(state=DISABLED)
        revealButton.config(state=NORMAL)
    else:
        #will invert the options and reconfigure the text
        JokeText.configure(text=question)
        displayJoke.config(state=NORMAL)
        backButton.config(state=NORMAL)
        revealButton.config(state=DISABLED)

def revealPunchline(question, punchline):
    global revealAfterDelay
    #wil call the cancel to play punchline drum
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
    revealButton.config(state=DISABLED)

def pickJoke():#grabs the random joke line
    grabJoke = choice(jokes)
    showJoke(grabJoke)
    switchFrames(jokeShowFrame)#switches frames

def onRevealButtonClick():
    global currentPunchline
    questionText = JokeText.cget("text")#reads the current info before updating
    if currentPunchline and questionText:#will show the punchline after the button is pressed
        revealPunchline(questionText, currentPunchline)

def switchFrames(frame):#changes between frames
    cancelReveal()
    frame.tkraise()

root = Tk()#finally starting the tkinter display after ONE HUNDRED LINES!!!
root.title("Alexa's Jokes")
root.geometry("420x250")
root.resizable(False, False)#you cant change the size of the screen

givenAnswer = StringVar()

"""
Please note that the container frame and button frame were made with the help of GitHub Copilot
since at the start, I only tried making the title frame and joke frame, which caused a few errors.
This was the most efficient way of making sure everything was in place without issues.
"""

#this frame stacks everything inside
containerFrame = Frame(root)
containerFrame.grid(row=0, column=0, sticky="nsew")
containerFrame.grid_rowconfigure(0, weight=1)
containerFrame.grid_columnconfigure(0, weight=1)

#initial title frame
titleFrame = Frame(containerFrame, bg="#4CAF50", pady=10)
titleFrame.grid(row=0, column=0, sticky="nsew")

titleLabel = Label(titleFrame, text="Alexa's Jokes", bg="#4CAF50", fg="white", font=("Arial", 16, "bold"))
titleLabel.pack(pady=(8,4))

jokeButton = Button(titleFrame, text="Tell me a joke!", command=pickJoke, bg="#e72cdb", fg="white", font=("Arial", 12))
jokeButton.pack(padx=10, pady=10)

#this is the other frame where the jokes are shown
jokeShowFrame = Frame(containerFrame, bg="#684F17", pady=10)
jokeShowFrame.grid(row=0, column=0, sticky="nsew")

firstJoke = choice(jokes)
JokeText = Message(jokeShowFrame, text=firstJoke, width=380, font=("Arial", 12), bg="#684F17")
JokeText.pack(padx=10, pady=(16,8))

#this is inside the joke frame to store buttons
buttonFrame = Frame(jokeShowFrame, bg="#684F17")
buttonFrame.pack(pady=(0,10))

#option to get another joke
displayJoke = Button(buttonFrame, text="Another!", command=lambda: showJoke(choice(jokes)), bg="#e72cdb")
displayJoke.grid(row=0, column=0, padx=6)

#gives the punchline
revealButton = Button(buttonFrame, text="Send Punchline", command=onRevealButtonClick, state=DISABLED, bg="#e72cdb")
revealButton.grid(row=0, column=1, padx=6)

#return to title frame
backButton = Button(buttonFrame, text="Back", command=lambda: switchFrames(titleFrame), bg="#e72cdb")
backButton.grid(row=0, column=2, padx=6)

#turns off the whole code
stopJokes = Button(buttonFrame, text="Close", command=root.destroy, bg="#e72cdb")
stopJokes.grid(row=0, column=3, padx=6)

#title frame shows first when the code runs
switchFrames(titleFrame)

root.mainloop()