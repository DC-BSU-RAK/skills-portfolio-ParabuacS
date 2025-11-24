from tkinter import *
from tkinter import messagebox
import os
from PIL import ImageTk, Image


"""
Constants will use underscoring (VARIABLE_NAME)
Everything else will use camel casing (variableName)
"""

STUDENT_FILE = "studentMarks.txt"

def readStudentRecords(fileName=STUDENT_FILE):
    #will return each student line and parse it later
    with open(fileName, "r") as file:
        lines = file.readlines()
    if not lines:
        return [] #will return empty list if there's nothing
    """
    this next return line will skip the first line in the txt file (the lone number)
    Github Copilot explained that that number represented the number of registered
    students in the records. Thanks to that, I had to get help in modifying this
    function and a few others just to skip that line. However, I feel that it is
    important to address. 
    """
    return lines[1:] #skip the first line representing number of students

def separateStudentInfo(line):
    #all lines will be turned into their own dictionaries
    categories = line.strip().split(",") #using the comma as the divider
    if len(categories) < 6: #this makes sure there are only six categories
        raise ValueError(f"Incorrect line formatting: {line!r}")#this part was made with GitHub Copilot
    subjectOne = int(categories[2].strip())#turning each subject and exam mark into integers for something later
    subjectTwo = int(categories[3].strip())
    subjectThree = int(categories[4].strip())
    exam = int(categories[5].strip())

    totalMark = subjectOne + subjectTwo + subjectThree + exam
    gradePercentage = (totalMark / 160) * 100 #160 points is the overall total, AKA 100% of the grade
    #showing the grade mark the student gets
    if gradePercentage >= 70:#all of these read the grade percentage
        grade = "A"#then it will give corresponding letter
    elif gradePercentage >= 60:
        grade = "B"
    elif gradePercentage >= 50:
        grade = "C"
    elif gradePercentage >= 40:
        grade = "D"
    else:
        grade = "F"

    #after all that, it will return a full library PER STUDENT
    return {
        "id": categories[0].strip(),
        "name": categories[1].strip(),
        "s1": subjectOne,
        "s2": subjectTwo,
        "s3": subjectThree,
        "exam": exam,
        "total": totalMark,
        "grade": grade
    }

def separateStudents(lines):
    #a dictionary is created per studet
    return [separateStudentInfo(line) for line in lines]

def writeToStudentRecords(fileName=STUDENT_FILE):
    #allows adding new student info and updating the number on the first line
    global students
    with open(fileName, "w") as file:
        file.write(str(len(students)) + "\n")
        for newStudent in students:
            line = (
                f"{newStudent['id']},"
                f"{newStudent['name']},"
                f"{newStudent['s1']},"
                f"{newStudent['s2']},"
                f"{newStudent['s3']},"
                f"{newStudent['exam']}\n"
            )
            file.write(line)

def tableOfStudentInfo(mainFrame, studentsList):
    #this is for the table frame that shows all students
    for widget in mainFrame.winfo_children():
        widget.destroy()#clears the table

    categoryHeadings = ["ID", "Name", "S1", "S2", "S3", "Exam", "Total", "Grade"]
    keyWords = ["id", "name", "s1", "s2", "s3", "exam", "total", "grade"]

    for column, header in enumerate(categoryHeadings):
        Label(mainFrame,text=header,font=("Arial", 12, "bold"),borderwidth=1,relief="solid",width=12,bg="#f0f0f0").grid(row=0, column=column, sticky="nsew")

    #this colors the row depending on student grade
    for row, student in enumerate(studentsList, start=1):
        grade = student["grade"]
        if grade == "A":
            rowBG = "#FFF59D"  #yellow row for academic excellence
        elif grade == "F":
            rowBG = "#FFCDD2"  #red for fail
        else:
            rowBG = "#C8E6C9"  #everything else is green for pass

        for column, key in enumerate(keyWords):
            Label(mainFrame,text=str(student[key]),font=("Arial", 11),borderwidth=1,relief="solid",width=12,bg=rowBG).grid(row=row, column=column, sticky="nsew")

    #resizes each column cuz of varying info
    for column in range(len(categoryHeadings)):
        mainFrame.grid_columnconfigure(column, weight=1)

#the next few functions are for sorting the table, function names are self explanatory

def alphabeticalSorting():
    global students
    students = sorted(students, key=lambda student: student["name"])
    reloadAllPages()#will reload to show the sorted view

def ascendingOrderSorting():
    global students
    students = sorted(students, key=lambda student: student["total"])
    tableOfStudentInfo(studentTableFrame, students)#refreshes the table

def descendingOrderSorting():
    global students
    students = sorted(students, key=lambda student: student["total"], reverse=True)
    tableOfStudentInfo(studentTableFrame, students)#same, refreshes the tabl

#this one is for the individual student view frame
def individualStudentView(selected):
    for student in students:
        if student["name"] == selected:
            individualLabel["ID"].config(text=student["id"])
            individualLabel["Name"].config(text=student["name"])
            individualLabel["Subject 1"].config(text=student["s1"])
            individualLabel["Subject 2"].config(text=student["s2"])
            individualLabel["Subject 3"].config(text=student["s3"])
            individualLabel["Exam Mark"].config(text=student["exam"])
            individualLabel["Total"].config(text=student["total"])
            individualLabel["Grade"].config(text=student["grade"])
            break

#reload all the pages whenever big changes are made, like writing to the studentMarks file

def reloadAllPages():
    global students

    rawLine = readStudentRecords()#raw means the entire line, it hasn't been parsed yet
    students = separateStudents(rawLine)#then it will separate the students

    #will reconfigure the menu in individual student view to show new options
    menu = menuButton["menu"]
    menu.delete(0, "end")#delete what's there, then redo it

    for student in students:
        menu.add_command(label=student["name"],command=lambda name=student["name"]: (selectedName.set(name),individualStudentView(name)))

    #same, reloads the delete info option
    menuDelete = deleteStudentMenu["menu"]
    menuDelete.delete(0, "end")

        #reloads the update student menu
    menuUpdate = updateStudentMenu["menu"]
    menuUpdate.delete(0, "end")

    for student in students:
        label = f"{student['name']} ({student['id']})"
        menuUpdate.add_command(label=label,command=lambda lbl=label: updateSelection.set(lbl))

    for student in students:
        label = f"{student['name']} ({student['id']})"
        menuDelete.add_command(label=label,command=lambda lbl=label: deleteSelection.set(lbl))

    #will reload the table to show new student info
    tableOfStudentInfo(studentTableFrame, students)

"""
small reflection, I'm nearing 200 lines
and we're nowhere near done with the logic.
send help :')
"""
#this is for the writing to txt file and then adding to the system
def addNewStudent():
    global students
    #user will manually input each item
    studentID = userInputID.get().strip()
    studentName = userInputName.get().strip()
    subjectOne = userInputS1.get().strip()
    subjectTwo = userInputS2.get().strip()
    subjectThree = userInputS3.get().strip()
    exam = userInputExam.get().strip()

    #these are validations
    if not studentID.isdigit() or len(studentID) != 4:#makes sure the ID is only four digits
        messagebox.showerror("Invalid ID", "Student ID must be exactly 4 digits.")
        return

    if any(student["id"] == studentID for student in students):#makes sure it's not an existing ID
        messagebox.showerror("Duplicate ID", "A student with that ID already exists.")
        return

    if not studentName:#makes sure you actually wrote a name
        messagebox.showerror("Invalid Name", "Student name cannot be empty.")
        return #I did not decide to do a 'wrong spelling' or anything

    #converting the subject and exam marks into integers for total grade later
    try:
        s1Converted = int(subjectOne)
        s2Converted = int(subjectTwo)
        s3Converted = int(subjectThree)
        examConverted = int(exam)
    except ValueError:#makes sure the marks are numerical
        messagebox.showerror("Invalid Marks", "Marks must be integers.")
        return

    #subject marks must be out of 20 and at least 0, this makes sure of it
    if not (0 <= s1Converted <= 20 and 0 <= s2Converted <= 20 and 0 <= s3Converted <= 20):
        messagebox.showerror("Invalid Marks", "Subject marks must be between 0 and 20.")
        return

    if not (0 <= examConverted <= 100):#exam marks are out of 100
        messagebox.showerror("Invalid Exam", "Exam mark must be between 0 and 100.")
        return

    #this is for the overall total grade, which determines the color of their row
    total = s1Converted + s2Converted + s3Converted + examConverted
    percentage = (total / 160) * 100

    if percentage >= 70:
        grade = "A"#this one will show the row to be yellow
    elif percentage >= 60:#all the elifs will show green color
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:#this will show red as fail
        grade = "F"

    newStudent = {#new dictionary for the new student
        "id": studentID,
        "name": studentName,
        "s1": s1Converted,
        "s2": s2Converted,
        "s3": s3Converted,
        "exam": examConverted,
        "total": total,
        "grade": grade
    }

    #this will write to the studentMarks file
    students.append(newStudent)
    writeToStudentRecords()

    #refreshes everything to make way for the new info
    reloadAllPages()

    #after adding, the info in the forms is removed
    userInputID.delete(0, END)
    userInputName.delete(0, END)
    userInputS1.delete(0, END)
    userInputS2.delete(0, END)
    userInputS3.delete(0, END)
    userInputExam.delete(0, END)

    #will confirm to the user that it has been done
    messagebox.showinfo("Added", f"Student {studentName} ({studentID}) added successfully.")


def deleteStudentInfo():
    #will allow you to delete an existing student's information
    global students

    selectedStudent = deleteSelection.get()#will grab the selected student from the form

    if not selectedStudent:#makes sure you actually picked a student
        messagebox.showerror("No selection", "Please choose a student to delete.")
        return

    if "(" not in selectedStudent or ")" not in selectedStudent:##will hunt down for parentheses
        messagebox.showerror("Bad selection", "Unexpected selection format.")
        return#shows that you did something wrong

    #takes the ID of the selected student
    studentID = selectedStudent.split("(")[-1].split(")")[0].strip()

    #then it will ask you to confirm that you want to delete the student
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student ID {studentID}?")
    if not confirm:#askyesno makes the message box a yes or no option for the user
        return  

    #grabs the student ID from the system the deletes it
    newStudents = [student for student in students if student["id"] != studentID]

    #this is for the sake of showing that the selected ID doesn't exist in the system
    if len(newStudents) == len(students):
        messagebox.showerror("Not found", f"No student with ID {studentID} was found.")
        return

    #saves the progress, writes to the file to delete the student info line, then refresh pages
    students = newStudents
    writeToStudentRecords()

    reloadAllPages()
    #confirms that it's done
    messagebox.showinfo("Deleted", f"Student ID {studentID} deleted.")

def updateStudentInfo():
    #will allow you to update an existing student's marks
    global students

    selected = updateSelection.get()  #this will get the student chosen for update

    if not selected:  #makes sure something was actually chosen
        messagebox.showerror("No selection", "Please choose a student to update.")
        return

    if "(" not in selected or ")" not in selected:  #same parentheses check as the delete function
        messagebox.showerror("Bad selection", "Unexpected selection format.")
        return

    studentID = selected.split("(")[-1].split(")")[0].strip()

    #the inputs are used as the marks
    newS1 = updateInputS1.get().strip()
    newS2 = updateInputS2.get().strip()
    newS3 = updateInputS3.get().strip()
    newExam = updateInputExam.get().strip()

    #validations for integer marks
    try:#will convert the inputted marks into integers for grading system
        newS1Conv = int(newS1)
        newS2Conv = int(newS2)
        newS3Conv = int(newS3)
        newExamConv = int(newExam)
    except ValueError:#will force you to use whole numbers
        messagebox.showerror("Invalid Marks", "Marks must be integers.")
        return

    #the same range check as the other student info
    if not (0 <= newS1Conv <= 20 and 0 <= newS2Conv <= 20 and 0 <= newS3Conv <= 20):
        messagebox.showerror("Invalid Marks", "Subject marks must be between 0 and 20.")
        return

    if not (0 <= newExamConv <= 100):
        messagebox.showerror("Invalid Exam", "Exam mark must be between 0 and 100.")
        return

    #update in students list
    found = False
    for student in students:
        if student["id"] == studentID:
            student["s1"] = newS1Conv
            student["s2"] = newS2Conv
            student["s3"] = newS3Conv
            student["exam"] = newExamConv

            #calculating like the other function
            total = newS1Conv + newS2Conv + newS3Conv + newExamConv
            percentage = (total / 160) * 100
            #again, this is for the row color coding
            if percentage >= 70:
                grade = "A"
            elif percentage >= 60:
                grade = "B"
            elif percentage >= 50:
                grade = "C"
            elif percentage >= 40:
                grade = "D"
            else:
                grade = "F"
            #shows the total points and grade
            student["total"] = total
            student["grade"] = grade
            #the student is then found by the system
            found = True
            break

    if not found:#this is an error handler
        messagebox.showerror("Not found", f"No student with ID {studentID} was found.")
        return

    #save updated information
    writeToStudentRecords()

    #refresh the full system
    reloadAllPages()

    #clear the content you put in the form
    updateInputS1.delete(0, END)
    updateInputS2.delete(0, END)
    updateInputS3.delete(0, END)
    updateInputExam.delete(0, END)

    #confirmation
    messagebox.showinfo("Updated", f"Student ID {studentID} marks updated successfully.")

#FINALLY STARTING THE TKINTER GUI OMG

root = Tk()
root.title("Student Info Manager")
root.geometry("1100x650")

#this is for the icon
img = Image.open("StudentManagerIcon.png")
img = img.resize((32, 32))
icon = ImageTk.PhotoImage(img)
root.iconphoto(True, icon)

#this will contain all the frames
container = Frame(root, width=1000, height=600)
container.grid(row=0, column=0, sticky="nsew")
container.grid_propagate(True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

"""
The frames were generated with Copilot, but the logic is all mine.
The lambda part was added because grabbing the function by itself
didn't work.
"""
#making the frames
titleFrame = Frame(container, bg="#ddeeff")
individualView = Frame(container, bg="#eef")
tableView = Frame(container, bg="#ffe")
addAndDeleteView = Frame(container, bg="#f7f7f7")

for frame in (titleFrame, individualView, tableView, addAndDeleteView):
    frame.grid(row=0, column=0, sticky="nsew")

Label(titleFrame, text="Student Information System",font=("Arial", 28, "bold"),bg="#ddeeff").pack(expand=True)

individualStudentFrame = Frame(individualView, bg="#eef")
individualStudentFrame.pack(pady=20)

Label(individualStudentFrame,text="Individual Student Information",font=("Arial", 18, "bold"),bg="#eef").grid(row=0, column=0, columnspan=2, pady=(0,20))

Label(individualStudentFrame,text="Select a student:",font=("Arial", 12),bg="#eef").grid(row=1, column=0, sticky="e")

selectedName = StringVar()#this is for the selecting students part
selectedName.set("Choose a student")

menuButton = OptionMenu(individualStudentFrame, selectedName, ())#its a dropdown menu
menuButton.grid(row=1, column=1, sticky="w", pady=5)

#it will grab the info and display it to the user
individualLabel = {}
individualCategories = ["ID", "Name", "Subject 1", "Subject 2", "Subject 3", "Exam Mark", "Total", "Grade"]

for i, category in enumerate(individualCategories, start=2):
    Label(individualStudentFrame,text=f"{category}:",font=("Arial", 12, "bold"),bg="#eef").grid(row=i, column=0, sticky="e")
    individualLabel[category] = Label(individualStudentFrame,text="",font=("Arial", 12),bg="#eef")
    individualLabel[category].grid(row=i, column=1, sticky="w")

sortingOptions = Frame(tableView, bg="#ffe")
sortingOptions.pack(pady=(10,0))

Button(sortingOptions,text="Sort A → Z (Name)",width=20,command=alphabeticalSorting).grid(row=0, column=0, padx=5)

Button(sortingOptions,text="Sort by Total ↑",width=20,command=ascendingOrderSorting).grid(row=0, column=1, padx=5)

Button(sortingOptions,text="Sort by Total ↓",width=20,command=descendingOrderSorting).grid(row=0, column=2, padx=5)

#this will contain the table itself, not the buttons
studentTableFrame = Frame(tableView, bg="white")
studentTableFrame.pack(fill="both", expand=True, padx=10, pady=10)

#this is for the adding and deleting of info
recordsManagingFrame = Frame(addAndDeleteView, bg="#f7f7f7")
recordsManagingFrame.pack(pady=10, padx=10, fill="both", expand=True)

addingInfo = LabelFrame(recordsManagingFrame, text="Add New Student", padx=10, pady=10, bg="#f7f7f7")
addingInfo.pack(fill="x", padx=10, pady=(0,10))

#the following are different entry points for each field
Label(addingInfo, text="Student ID (4 digits):", bg="#f7f7f7").grid(row=0, column=0, sticky="e", padx=5, pady=2)
userInputID = Entry(addingInfo, width=20)
userInputID.grid(row=0, column=1, pady=2, padx=5)

Label(addingInfo, text="Full Name:", bg="#f7f7f7").grid(row=1, column=0, sticky="e", padx=5, pady=2)
userInputName = Entry(addingInfo, width=40)
userInputName.grid(row=1, column=1, pady=2, padx=5)

Label(addingInfo, text="Subject 1 (0-20):", bg="#f7f7f7").grid(row=2, column=0, sticky="e", padx=5, pady=2)
userInputS1 = Entry(addingInfo, width=10)
userInputS1.grid(row=2, column=1, sticky="w", pady=2, padx=5)

Label(addingInfo, text="Subject 2 (0-20):", bg="#f7f7f7").grid(row=3, column=0, sticky="e", padx=5, pady=2)
userInputS2 = Entry(addingInfo, width=10)
userInputS2.grid(row=3, column=1, sticky="w", pady=2, padx=5)

Label(addingInfo, text="Subject 3 (0-20):", bg="#f7f7f7").grid(row=4, column=0, sticky="e", padx=5, pady=2)
userInputS3 = Entry(addingInfo, width=10)
userInputS3.grid(row=4, column=1, sticky="w", pady=2, padx=5)

Label(addingInfo, text="Exam Mark (0-100):", bg="#f7f7f7").grid(row=5, column=0, sticky="e", padx=5, pady=2)
userInputExam = Entry(addingInfo, width=10)
userInputExam.grid(row=5, column=1, sticky="w", pady=2, padx=5)

Button(addingInfo,text="Add Student",command=addNewStudent,bg="#2E8B57",fg="white").grid(row=6, column=0, columnspan=2, pady=8)

#delete options
deleteBox = LabelFrame(recordsManagingFrame, text="Delete Student", padx=10, pady=10, bg="#f7f7f7")
deleteBox.pack(fill="x", padx=10, pady=(0,10))

Label(deleteBox, text="Select student to delete:", bg="#f7f7f7").grid(row=0, column=0, sticky="e", padx=5, pady=2)

deleteSelection = StringVar()
deleteSelection.set("Choose...")

deleteStudentMenu = OptionMenu(deleteBox, deleteSelection, ())
deleteStudentMenu.grid(row=0, column=1, sticky="w", padx=5, pady=2)

Button(deleteBox,text="Delete Selected",command=deleteStudentInfo,bg="#B22222",fg="white").grid(row=1, column=0, columnspan=2, pady=8)

#update options
updateBox = LabelFrame(recordsManagingFrame, text="Update Student Marks", padx=10, pady=10, bg="#f7f7f7")
updateBox.pack(fill="x", padx=10, pady=(0,10))

Label(updateBox, text="Select student to update:", bg="#f7f7f7").grid(row=0, column=0, sticky="e", padx=5, pady=2)

#this section allows the user to grab a student's name and ID then update their existing marks. 
#overall grade, color of their row, and total marks will update as required.
updateSelection = StringVar()
updateSelection.set("Choose...")

updateStudentMenu = OptionMenu(updateBox, updateSelection, ())
updateStudentMenu.grid(row=0, column=1, sticky="w", padx=5, pady=2)

Label(updateBox, text="New Subject 1 (0-20):", bg="#f7f7f7").grid(row=1, column=0, sticky="e", padx=5, pady=2)
updateInputS1 = Entry(updateBox, width=10)
updateInputS1.grid(row=1, column=1, sticky="w", padx=5, pady=2)

Label(updateBox, text="New Subject 2 (0-20):", bg="#f7f7f7").grid(row=2, column=0, sticky="e", padx=5, pady=2)
updateInputS2 = Entry(updateBox, width=10)
updateInputS2.grid(row=2, column=1, sticky="w", padx=5, pady=2)

Label(updateBox, text="New Subject 3 (0-20):", bg="#f7f7f7").grid(row=3, column=0, sticky="e", padx=5, pady=2)
updateInputS3 = Entry(updateBox, width=10)
updateInputS3.grid(row=3, column=1, sticky="w", padx=5, pady=2)

Label(updateBox, text="New Exam Mark (0-100):", bg="#f7f7f7").grid(row=4, column=0, sticky="e", padx=5, pady=2)
updateInputExam = Entry(updateBox, width=10)
updateInputExam.grid(row=4, column=1, sticky="w", padx=5, pady=2)

Button(updateBox,text="Update Student",command=updateStudentInfo,bg="#1E90FF",fg="white").grid(row=5, column=0, columnspan=2, pady=8)

rawLines = readStudentRecords()#makes raw lines of non-parsed info
students = separateStudents(rawLines)#then separates them by calling the function

#reloads the menu
menu = menuButton["menu"]
menu.delete(0, "end")

for student in students:
    menu.add_command(label=student["name"],command=lambda name=student["name"]: (selectedName.set(name),individualStudentView(name)))

#delete option
deleteMenu = deleteStudentMenu["menu"]
deleteMenu.delete(0, "end")

for student in students:
    entryLabel = f"{student['name']} ({student['id']})"
    deleteMenu.add_command(label=entryLabel,command=lambda lbl=entryLabel: deleteSelection.set(lbl))

#appending option for existing student info
updateMenu = updateStudentMenu["menu"]
updateMenu.delete(0, "end")

for student in students:
    entryLabel = f"{student['name']} ({student['id']})"
    updateMenu.add_command(label=entryLabel, command=lambda lbl=entryLabel: updateSelection.set(lbl))


#this is the INITIAL table when you first run the code
tableOfStudentInfo(studentTableFrame, students)

#this frame is for all common buttons seen in ALL frames
navFrame = Frame(root)
navFrame.grid(row=1, column=0, pady=5)

Button(navFrame, text="Main Title", width=12,command=lambda: titleFrame.tkraise()).grid(row=0, column=0, padx=5)

Button(navFrame, text="Individual", width=12,command=lambda: individualView.tkraise()).grid(row=0, column=1, padx=5)

Button(navFrame, text="Table", width=12,command=lambda: tableView.tkraise()).grid(row=0, column=2, padx=5)

Button(navFrame, text="Manage Records", width=16,command=lambda: addAndDeleteView.tkraise()).grid(row=0, column=3, padx=5)

Button(navFrame, text="Exit", width=12,command=root.destroy).grid(row=0, column=4, padx=5)

titleFrame.tkraise()#shows title frame first
root.mainloop()#I'M FINALLY DONE