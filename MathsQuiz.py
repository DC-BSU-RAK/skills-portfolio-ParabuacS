from tkinter import * #grab everything from tkinter
from random import randint, choice #we only need these two
import pygame #this is used for the background audio

root = Tk() #the overall main frame where everything is in
root.title('Math Quiz')
root.geometry('318x250')
root.config(bg="#DE0C8A")

def playBGM():
    pygame.mixer.init()
    pygame.mixer.music.load("Baldis basics theme song.mp3") #grabs the audio file
    pygame.mixer.music.set_volume(0.7) #optional volume is lowered
    pygame.mixer.music.play(loops=-1) # -1 means it will loop indefinitely

#needed variables and constants
quizQuestion = ""
correctAnswer = 0
difficultyVar = StringVar(value='easy')
MAX_ATTEMPTS = 3 #this is a constant
attemptsLeft = MAX_ATTEMPTS
MAX_QUESTIONS = 10 #also a constant
questionsAsked = 0
totalScore = 0
givenAnswer = StringVar()

#update labels
def updateAttempts():
    attemptsLabel.configure(text=f"Attempts left: {attemptsLeft}")

def updateProgress():
    progressLabel.configure(text=f"Question {questionsAsked}/{MAX_QUESTIONS}")

def updateScore():
    scoreLabel.configure(text=f"Score: {totalScore}")

#starting the quiz
def start(mode):
    global questionsAsked, totalScore
    difficultyVar.set(mode)#picks the difficulty
    questionsAsked = 0
    submitAnswer.config(state=NORMAL)#state normal means it can be used
    userInput.config(state=NORMAL)
    l3.configure(text="")
    generateQuestion()#calls the random question generator
    switchFrames(gameFrame)#moves to main game

def generateQuestion():#uses random to make questions
    global quizQuestion, correctAnswer, attemptsLeft, questionsAsked
    if questionsAsked >= MAX_QUESTIONS:#after finishing ten questions
        questionLabel.configure(text="Mode complete")
        l3.configure(text=f"{difficultyVar.get().capitalize()} mode finished ({MAX_QUESTIONS} questions)", fg="white")#shows that you're done
        submitAnswer.config(state=DISABLED)#state disabled means its not allowed
        userInput.config(state=DISABLED)
        updateProgress()#adds to the questions answered
        return

    questionsAsked += 1
    updateProgress()#will show in the label

    difficulty = difficultyVar.get()#limits as per the brief
    if difficulty == 'easy':#limit for easy
        min, max = 1, 9#variables storing minimum and maximum values
    elif difficulty == 'medium':#limit for medium
        min, max = 10, 99
    else: # limit for hard
        min, max = 1000, 9999

    firstNumber = randint(min, max)#will use the difficulty as a reference
    secondNumber = randint(min, max)
    operator = choice(["+", "-"])#only add and subtract allowed
    if operator == "-" and firstNumber < secondNumber:#prevents negative correct answers
        firstNumber, secondNumber = secondNumber, firstNumber#invert the numbers if negative is the correct answer

    quizQuestion = f"{firstNumber}{operator}{secondNumber}"#shows the question
    correctAnswer = firstNumber + secondNumber if operator == "+" else firstNumber - secondNumber #stores correct answer

    attemptsLeft = MAX_ATTEMPTS #starting number of attempts
    updateAttempts()#will update every time you use an attempt
    questionLabel.configure(text=quizQuestion)#shows question
    givenAnswer.set("")
    userInput.focus_set()#will target the user box
    l3.configure(text="")#placeholder

def checkAnswer():
    global attemptsLeft, totalScore
    try:#input needs to be pure digits
        ans = int(givenAnswer.get())
    except ValueError: #makes sure only numbers are allowed
        l3.configure(text="Please enter a number", fg="#FFA500")
        return

    #points system
    if ans == correctAnswer:
        attemptsUsed = MAX_ATTEMPTS - attemptsLeft + 1
        if attemptsUsed == 1:#if correct on first try, get this
            points = 10
        elif attemptsUsed == 2:#if correct on second try
            points = 5
        elif attemptsUsed == 3:#if correct on third try
            points = 1
        else:#if you run out of attempts
            points = 0
        totalScore += points#add to overall score
        updateScore()#updates the label
        l3.configure(text=f"Correct! (+{points} pts)", fg="#014707")#will show results
        root.after(1000, generateQuestion)#will have a delay to show results before moving to next question
    else:#allows a retry
        attemptsLeft -= 1#if incorrect, minus one attempt
        if attemptsLeft > 0:#makes sure you have attempts left
            l3.configure(text="Incorrect, try again", fg="#5F1414")#displaying that you should retry
            updateAttempts()#update label
            givenAnswer.set("")
            userInput.focus_set()#targets input box
        else:#moves on after three tries
            l3.configure(text=f"Out of attempts (The answer is {correctAnswer})", fg="#5F1414")#shows message before moving questions
            updateAttempts()
            root.after(1000, generateQuestion)

"""
Please note that the frames were made with the help of Github Copilot
due to massive issues with adding all the items inside each frame.
However, most of the functionality above this comment was made with minimal
assistance from AI. Apart from root.after and the min max difficulty numbers,
the rest of the code was made with research, a lot of messing around, and my own knowledge.
Again, take note, I tried to make the frames myself, but with huge errors, I resorted
to getting help from Copilot to fix it and make sure the code is under 250 lines.
"""

#frame switching function
def switchFrames(frame):
    frame.tkraise()#allows movement between each frame

#ALL FRAMES ARE STACKED inside of the root frame, which is the window itself
quizWindow = Frame(root)#quizWindow is a frame inside root window
quizWindow.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)#adjusting to resize
root.grid_columnconfigure(0, weight=1)#same as the other one

#main menu
mainFrame = Frame(quizWindow, bg="#DE0C8A")#put inside container quizWindow
mainFrame.grid(row=0, column=0, sticky="nsew")

titleLabel = Label(mainFrame, text="Math Quiz", font=("arial",20), bg="#DE0C8A")#same principle of overlaying
titleLabel.pack(pady=(20,10))

diffLabel = Label(mainFrame, text="Choose your difficulty (10 questions each):", font=("arial",12), bg="#DE0C8A")
diffLabel.pack(pady=(10,8))

buttonFrame = Frame(mainFrame, bg="#DE0C8A")
buttonFrame.pack(pady=6)

#all buttons are inside the button frame
easyMode = Button(buttonFrame, text="Easy (10)", command=lambda: start('easy'), bg="#0D5C2F", fg="white", width=12)#lambda will refer to difficulty option
easyMode.grid(row=0, column=0, padx=6)

mediumMode = Button(buttonFrame, text="Medium (10)", command=lambda: start('medium'), bg="#BB8E1D", fg="white", width=12)
mediumMode.grid(row=0, column=1, padx=6)

hardMode = Button(buttonFrame, text="Hard (10)", command=lambda: start('hard'), bg="#B30808", fg="white", width=12)
hardMode.grid(row=0, column=2, padx=6)

#for the quiz itself
gameFrame = Frame(quizWindow, bg="#DE0C8A")
gameFrame.grid(row=0, column=0, sticky="nsew")#sticky helps to position

#top menu
menubarFrame = Frame(gameFrame, bg="#DE0C8A")
menubarFrame.pack(fill='x', pady=(8,0), padx=10)
scoreLabel = Label(menubarFrame, text=f"Score: {totalScore}", font=("arial",12), bg='#DE0C8A', fg="white")
scoreLabel.pack(side='right')#positions the label
backButton = Button(menubarFrame, text="Back", command=lambda: switchFrames(mainFrame))
backButton.pack(side='left')#same positioning

#all the labels for the quiz
#each label updates via functions
questionLabel = Label(gameFrame, text=quizQuestion, font=("arial",20), bg='#DE0C8A', fg="white")
questionLabel.pack(pady=(20,10))

progressLabel = Label(gameFrame, text=f"Question {questionsAsked}/{MAX_QUESTIONS}", font=("arial",12), bg='#DE0C8A', fg="white")
progressLabel.pack()

attemptsLabel = Label(gameFrame, text=f"Attempts left: {MAX_ATTEMPTS}", font=("arial",12), bg='#DE0C8A', fg="white")
attemptsLabel.pack(pady=(6,0))

#placeholder label
l3 = Label(gameFrame, text = "", bg='#DE0C8A',fg="white",font=("arial",15))
l3.pack(pady=(10,0))

#user input
inputFrame = Frame(gameFrame, bg="#DE0C8A")
inputFrame.pack(pady=(16,0))
userInput = Entry(inputFrame, textvariable=givenAnswer, font=("arial",15))#answer itself
userInput.grid(row=0, column=0, padx=(0,8))
submitAnswer = Button(inputFrame, text="Submit", font=("arial", 15), command=checkAnswer)#submitting answers
submitAnswer.grid(row=0, column=1)

#running the code will show main frame first
switchFrames(mainFrame)
playBGM() #will play the BGM no matter what frame you're on

root.mainloop()