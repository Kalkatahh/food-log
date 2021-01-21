import time
from tkinter import *
from tkinter import messagebox as mb
from tkinter.ttk import Label

import cv2
import mysql.connector
from pyzbar import pyzbar

db = mysql.connector.connect(
    host='localhost',
    user="root",
    password="",
    database="food_log"
)
#
# mycursor = db.cursor()
# #mycursor.execute("CREATE TABLE User (name VARCHAR(25), age int UNSIGNED, person_id int PRIMARY KEY AUTO_INCREMENT) ")
#
# mycursor.execute("INSERT INTO User (name, age) VALUES (%s, %s)", ("Cristiano", 26))
# # db.commit()
#
# mycursor.execute("SELECT * FROM User")
#
# for x in mycursor:
#     print(x)

used_codes = []
foods = {}
addFood = False
root = Tk()
root.geometry("600x300")
root.title("Sim's Food App")


def initialize():
    global addFood
    newFood = Label(root, text="Enter new food:")
    newFood.grid(row=0, column=0)

    e_newFood = Entry()
    e_newFood.grid(row=0, column=1, columnspan=3)

    insert = Button(root, text="Scan barcode", command=lambda: start_camera(e_newFood.get(), addedLabel))
    insert.grid(row=0, column=4)

    addedLabel = Label(root, text="")
    addedLabel.grid(row=1, column=0)

    printFoods = Button(root, text="Print your foods", command=print_list)
    printFoods.grid(row=2, column=0)

    root.mainloop()


def print_list():
    global foods
    newRoot = Tk()
    newRoot.title("List of foods")
    newRoot.geometry("300x300")
    if len(used_codes) == 0:
        b = Label(newRoot, text="No foods")
        b.grid(row=0, column=0, columnspan=3)
    # for i in range(len(used_codes)):  # Rows
    #     b = Label(newRoot, text=used_codes[i])
    #     b.grid(row=i)
    for i in foods:
        j = 0
        b = Label(newRoot, text=(i, foods[i]))
        b.grid(row=j)
        j = j + 1


def start_camera(new_food_item, addedLabel):
    global addFood
    global foods

    open_camera(addedLabel)
    if addFood:
        if not new_food_item or len(new_food_item) == 0:
            addedLabel['text'] = 'Enter a food item first'
            used_codes.pop()
            addFood = False
        else:
            foods[new_food_item] = used_codes[-1]
            addedLabel['text'] = 'SUCCESSFULLY ADDED'
            addFood = False


def open_camera(addedLabel):
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
                if addedLabel.get():
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
