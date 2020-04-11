import tkinter as tk
from tkinter import ttk
import sqlite3 as sql
import winsound
import itertools
from PIL import ImageTk,Image
from functools import partial
im_num = 1
im_pic = 1
correct_ans = 1
total=0
player=''

'''functions'''    
    
#function for inserting picture of character
def initImage(path):
    img = Image.open(str(path)+".png")
    img = img.resize((400,400), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    top.configure(image=img)
    m2.image = img
    m2.add(top)  

#event handler for option buttons
def clicked(num,id):
    global im_num
    im_num+=1
    global im_pic
    if grade(id):
        im_pic+=1
        num = im_pic
        if num<7:
            initImage(num)  
    l1.configure(text=getques())  

#function for points calculation
def grade(ans):
    global total
    total += 1
    if(ans==correct_ans):
        return False
    total -= 1
    return True

#function to retrieve questions, options and correct answer from database
def getques():
    ls=[]
    options=[]
    global correct_ans
    if im_num<5:
        try:
            conn=sql.connect('Questions.db')
            query = "SELECT * FROM Ques WHERE Qno = " + str(im_num)
            cur=conn.cursor()
            cur.execute(query)
            record = cur.fetchall()
            ls=list(itertools.chain(*record))
            options=ls[2].split(',')
            correct_ans = ls[3]
            conn.commit()
            cur.close()
        except sql.Error as err:
            print("Error:",err)
        finally:
            if conn:
                conn.close()
        if im_num>1:
            b1.configure(text=options[0])
            b2.configure(text=options[1])
            b3.configure(text=options[2])
            b4.configure(text=options[3])
        return ls[1]
    #when questions are exhausted the option buttons are un-placed and question label is re-packed
    #to display score. 
    #b5 button for replay is packed
    b1.place_forget()
    b2.place_forget()
    b3.place_forget()
    b4.place_forget()
    l1.place_forget()
    l1.pack()    
    b6.pack()
    b5.pack()
    if total==0:
        return "Game Over"
    elif total==4:
        initImage(6)
        return "New High Score"
    else:
        return "Your score: "+str(total)

#event-handler for replay button. sets widgets and global variables to initial values  
def Replay():
    global total, im_num, correct_ans
    global im_pic, player
    name.delete(0, 'end')
    l1.pack_forget()
    b5.pack_forget()
    b6.pack_forget() 
    m2.pack_forget()
    l1.place_forget()
    b1.place_forget()
    b2.place_forget()
    b3.place_forget()
    b4.place_forget()
    im_num = 1
    im_pic = 1
    correct_ans = 1
    total=0
    player=''
    b1.configure(text="Rice")
    b2.configure(text="Wheat")
    b3.configure(text="Sugarcane")
    b4.configure(text="Maize")
    initImage(1)
    l1.configure(text=getques())    
    winsound.PlaySound('1-01 Doki Doki Literature Club!.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
    main()

# new window definition
def new_winF():
    newwin = tk.Toplevel(root)
    newwin.title("Score Board")
    newwin.geometry("600x200")
    newwin['bg']='#42f5ef'
    label = tk.Label(newwin, text="High Scores", font=('Comic Sans MS',30),background='#42f5ef')
    label.pack()
    # create Treeview with 3 columns
    cols = ('Position', 'Name', 'Score')
    listBox = ttk.Treeview(newwin, columns=cols, show='headings',height=5)
    # set column headings
    for col in cols:
        listBox.heading(col, text=col) 
    tempList=[]
    try:
        conn=sql.connect('Questions.db')
        query = "INSERT INTO scoreboard VALUES('"+player+"',"+str(total)+")"
        cur=conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
    except sql.Error as err:
        pass
    finally:
        if conn:
            conn.close()
    try:
        conn=sql.connect('Questions.db')
        query = '''SELECT * FROM scoreboard ORDER BY score DESC'''
        cur=conn.cursor()
        cur.execute(query)
        record = cur.fetchall()
        i=0
        for rec in record:
            i+=1
            if i==6:
                break
            tempList.append(list(rec))
        conn.commit()
        cur.close()
    except sql.Error as err:
        print("Error:",err)
    finally:
        if conn:
            conn.close()
    for i, (name, score) in enumerate(tempList, start=1):
        listBox.insert("", "end", values=(i, name, score))    
    listBox.pack()    

#function to add widgets of game    
def gamewid(): 
    global player
    player=name.get()
    lb.place_forget()
    name.place_forget()
    go.place_forget()
    m2.pack(fill=tk.BOTH,expand=1)
    m2.add(top)    
    m2.add(bottom)
    l1.place(x=300,y=50)
    b1.place(x=400,y=200)
    b2.place(x=600,y=200)
    b3.place(x=800,y=200)
    b4.place(x=1000,y=200) 
    
'''end of functions'''

'''global gui widgets'''    
#bg music
winsound.PlaySound('1-01 Doki Doki Literature Club!.wav', winsound.SND_LOOP + winsound.SND_ASYNC)

#window   
root=tk.Tk()
root.title("Quiz")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d" % (w, h))
root['bg']='#42f5ef'

#player name prompt
lb=tk.Label(root,text="Enter player name: ", font = ('Comic Sans MS',30),background='#42f5ef')
name=tk.Entry(root)
go=tk.Button(root,text="Enter",font = ('Comic Sans MS',15),command=gamewid,bg='#FFC0CB')

#base pane
m2 = tk.PanedWindow(root, orient=tk.VERTICAL)

#top label for picture
top = tk.Label(m2)
top['bg']='#FFC0CB'

#setting first image
initImage(1)

#bottom pane
bottom = tk.PanedWindow(m2)
bottom['bg']='#42f5ef'

#label for questions
l1=tk.Label(bottom,text=getques(), font = ('Comic Sans MS',30),background='#42f5ef',fg='white')

#option buttons
b1=tk.Button(bottom,text="Rice",font = ('Comic Sans MS',15),command=partial(clicked, 1,1),bg='#FFC0CB')
b2=tk.Button(bottom,text="Wheat",font = ('Comic Sans MS',15),command=partial(clicked, 1,2),bg='#FFC0CB')
b3=tk.Button(bottom,text="Sugarcane",font = ('Comic Sans MS',15),command=partial(clicked, 1,3),bg='#FFC0CB')
b4=tk.Button(bottom,text="Maize",font = ('Comic Sans MS',15),command=partial(clicked, 1,4),bg='#FFC0CB')

#replay button
b5=tk.Button(bottom,text="Replay?",font = ('Comic Sans MS',15),command=Replay,bg='#FFC0CB')

#scoreboard button
b6 = tk.Button(bottom, text ="Scoreboard",font = ('Comic Sans MS',15), command =new_winF,bg='#FFC0CB')
'''end of global gui widgets'''    


#main function to add widgets to get player name
def main():
    global w,h
    cr=int(h/2)
    cc=int(w/2)
    lb.place(x=cc-150,y=cr-100)
    name.place(x=cc-125,y=cr,width=290, height=25)
    go.place(x=cc-20,y=cr+50)
    root.mainloop()
    winsound.PlaySound(None, winsound.SND_LOOP | winsound.SND_ASYNC) 
main()