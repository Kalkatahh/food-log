import tkinter
from tkinter.ttk import Label

import cv2
import time
from pyzbar import pyzbar
from tkinter import *
from tkinter import messagebox as mb
import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user="root",
    password="",
    database="food_log"
)

mycursor = db.cursor()
#mycursor.execute("CREATE TABLE User (name VARCHAR(25), age int UNSIGNED, person_id int PRIMARY KEY AUTO_INCREMENT) ")
#
mycursor.execute("INSERT INTO User (name, age) VALUES (%s, %s)", ("Cristiano", 26))
# db.commit()

mycursor.execute("SELECT * FROM User")

for x in mycursor:
    print(x)

used_codes = []
foods = {}
addFood = False
root = Tk()
root.geometry("600x300")
root.title("Sim's Food App")


def initialize():
    global addFood
    newFood = Label(root, text="Enter new food:", font=('bold', 10))
    newFood.place(x=20, y=30)

    e_newFood = Entry()
    e_newFood.place(x=150, y=30)

    insert = Button(root, text="Scan barcode", font=('italic', 10), bg="white", command=lambda: start_camera(e_newFood.get()))
    insert.place(x=400, y=35)

    printFoods = Button(root, text="Print your foods", font=('italic', 10), bg="white", command=print_list)
    printFoods.place(x=20, y=180)

    root.mainloop()


def print_list():
    global foods
    newRoot = Tk()
    newRoot.title("List of foods")
    newRoot.geometry("300x300")
    if len(used_codes) == 0:
        b = Label(newRoot, text="No foods")
        b.place(x=100, y=30)
    # for i in range(len(used_codes)):  # Rows
    #     b = Label(newRoot, text=used_codes[i])
    #     b.grid(row=i)
    for i in foods:
        j = 0
        b= Label(newRoot, text=(i, foods[i]))
        b.grid(row=j)
        j = j + 1

def start_camera(newFoodItem):

    global addFood
    global foods
    setFood = Label(root, text="", font=('bold', 30))
    setFood.place(x=300, y=70)
    open_camera()
    if addFood:
        if not newFoodItem or len(newFoodItem) == 0:
            setFood['text'] = 'Enter a food item first'
            used_codes.pop()
            addFood = False
        else:
            foods[newFoodItem] = used_codes[-1]
            setFood['text'] = 'SUCCESSFULLY ADDED'
            addFood = False


def open_camera():
    global foods
    global addFood
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # 3- width
    cap.set(4, 480)  # 4 - height
    while cap.isOpened():
        success, frame = cap.read()
        cv2.imshow("Scan food - press 'q' to quit", frame)
        for code in pyzbar.decode(frame):
            if code.data.decode('utf-8') not in used_codes:
                used_codes.append({code.data.decode('utf-8'): 1})
                addFood = True
                cap.release()
                cv2.destroyAllWindows()
                mb.showinfo("Message", "Successfully added new food")
            elif code.data.decode('utf-8') in used_codes:
                used_codes.append({code.data.decode('utf-8'): 0})

                time.sleep(5)
            # print(code.type)
            # print(code.data.decode('utf-8'))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    if not addFood:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    initialize()
