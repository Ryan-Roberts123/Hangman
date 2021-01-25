from tkinter import *
from PIL import ImageTk, Image
import random
import csv
from tkinter import messagebox
import sys

lost = False

# Tkinter setup
root = Tk()
root.title("Hangman")
root.iconbitmap("icon.ico")


y = 0
file_list = []
# Produces a list of png file names
while y < 8:
    file_name = "Hangman " + str(y) + ".png"
    file_list.append(file_name)
    y = y + 1


def start():
    global i, x, count, tf, prev_answers, answerlist, mainword, charlist, lost, root
    #  Produces empty answerlist and variables
    answerlist = []
    prev_answers = []
    global i
    i = 0
    x = 0
    count = 0

    # Opens csv file and selects a random word
    with open("objects.csv") as f:
        reader = csv.reader(f)
        randomword = str(random.choice(list(reader))).upper()

    # Makes the random word into a list and removes '[]'
    charlist = list(str(randomword))
    charlist.remove("[")
    charlist.remove("'")
    charlist.remove("'")
    charlist.remove("]")

    # Makes final word into a string
    mainword = ''.join(charlist)
    # print(mainword)

    # Fills Answer List with correct number of empty values
    while len(answerlist) < len(charlist):
        answerlist.append(" ")
    update()

# Ends the game
def end():
    root.quit()
    sys.exit()

# Checks if the input letter is in the target word
# Adds corrects letter or adds 1 onto death count
def proccess():
    global i
    global count
    global charlist
    x = False
    while i < len(charlist):
        if letterinput == charlist[int(i)]:
            answerlist[int(i)] = charlist[int(i)]
            i = i + 1
            x = True
        else:
            i = i + 1
    if i == len(charlist) and x == False:
        count = count + 1
    correctanswer()


# Runs if the word is correct and ends the game
def correctanswer():
    global count
    if charlist == answerlist:
        correct = "The word was " + mainword + ".\n Well played.\n Your score was " + str(count)
        messagebox.showinfo("Congratulations", str(correct))
        end()

# Runs when the game is over. Produces a textbox with the correct answer, then closes the game.
def losingmessage():
    global lost, mainword
    if count == 7:
        lost = True
        losingtext = "The word was " + mainword + ".\n You ran out of tries."
        print(losingtext)
        response = messagebox.showerror("Game over!", losingtext)
        end()


# Makes the input uppercase if it isn't already
def lowercase():
    global letterinput
    if letterinput.islower():
        letterinput = str(letterinput).upper()


def buttonpress(event=None):
    global letterinput, answerlist, i, entryBox
    letterinput = str(entryBox.get())
    # Removes the input from the entry box.
    entryBox.delete(0, 'end')
    lowercase()
    # Checks if the first letter is a uppercase. Changes it to lowercase.
    if letterinput.istitle():
        letterinput = letterinput[0].lower() + letterinput[1:]
    lowercase()
    print("Letter input = ", letterinput)
    # Produces a message box if you have already entered an input.
    if letterinput in prev_answers:
        alreadyentered = "You have already entered: " + letterinput
        print(alreadyentered)
        messagebox.showinfo("Repeated input", alreadyentered)
    else:
        # Checks if the player has entered the full word.
        if letterinput == mainword:
            answerlist = charlist
        correctanswer()
        proccess()
        i = 0
        print("Count = ", count)
        prev_answers.append(letterinput)
    update()
    losingmessage()


# Updates the png and answers
def update():
    global count, my_img, label_list, lost, charlist
    # Opens the correct png with width of the length of the charlist
    my_img = ImageTk.PhotoImage(Image.open(file_list[int(count)]))
    pic = Label(image=my_img)
    pic.grid(row=0, column=0, columnspan=int(len(charlist)))

    # Produces a score counter at the bottom.
    scoretext = "Score = " + str(count) + "/7"
    score = Label(root, text=scoretext, bg="red")
    score.grid(row=3, column=0)

    # Produces Labels below the png and inputs the answerlist
    c = 0
    while c < len(charlist):
        label_list = "label_list" + str(c)
        label_list = Label(root, width=15, text="-" + answerlist[c])
        label_list.grid(row=1, column=c)
        c = c + 1


start()
# Defines the entry boxes on the 3rd row
enterLetter = Label(root, text="Enter Letter or word:")
entryBox = Entry(root, width=20, borderwidth=5)
button = Button(root, padx=20, text="Enter", command=buttonpress)

enterLetter.grid(row=2, column=0)
entryBox.grid(row=2, column=1)
button.grid(row=2, column=3)

# Enter key runs the function as well as the button
root.bind('<Return>', buttonpress)

# Makes the Tkinter window stay open
root.mainloop()