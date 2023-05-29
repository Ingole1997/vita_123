import pymysql
from tkinter import font
from turtle import width
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

#connection later
def connection():
    conn=pymysql.connect(host='localhost',user='root',password='manager',db='pythondb1')
    return conn

def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    
    for array in read():
        my_tree.insert(parent='',index='end',id=array,text="",values=(array),tags='orow')
    
    my_tree.tag_configure('orow',background='#EEEEEE',font=('Arial',12))
    my_tree.grid(row=8,column=0,columnspan=5,rowspan=11,padx=10,pady=20)
    
#gui
root=Tk()
root.title("student registration system")
root.geometry("1080x720")
my_tree=ttk.Treeview(root)

#functions later

#placeholder for entry
ph1=tk.StringVar()
ph2=tk.StringVar()
ph3=tk.StringVar()
ph4=tk.StringVar()
ph5=tk.StringVar()

#set placeholder values
def setph(word,num):
    if num==1:
        ph1.set(word)
    if num==2:
        ph2.set(word)
    if num==3:
        ph3.set(word)
    if num==4:
        ph4.set(word)
    if num==5:
        ph5.set(word)
    
def read():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM students")
    results=cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def add():
    studid=str(studidEntry.get())
    fname=str(fnameEntry.get())
    lname=str(lnameEntry.get())
    address=str(addressEntry.get())
    phone=str(phoneEntry.get())
    
    if (studid=="" or studid==" ") or (fname=="" or fname==" ") or (lname=="" or lname==" ") or (address=="" or address==" ") or (phone=="" or phone==" "):
        messagebox.showinfo("Error","please fill up the blank entry")
    else:
        try:
            conn=connection()
            cursor=conn.cursor()
            cursor.execute("Insert into students Values ('"+studid+"','"+fname+"','"+lname+"','"+address+"','"+phone+"')")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error","Stud ID already exist")
            return
        
    refreshTable()
    
def reset():
    decision=messagebox.askquestion("Warning!!","Delete all data?")
    if decision != "yes":
        return
    else:
        try:
            conn=connection()
            cursor=conn.cursor()
            cursor.execute("Delete from students")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error","Sorry an error occured")
            return
        
    refreshTable()
    
def delete():
    decision=messagebox.askquestion("Warning!!","Delete selected data?")
    if decision != "yes":
        return
    else:
        selected_item=my_tree.selection()[0]
        deleteData=str(my_tree.item(selected_item)['values'][0])
        try:
            conn=connection()
            cursor=conn.cursor()
            cursor.execute("Delete from students Where studid='"+str(deleteData)+"'")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error","Sorry an error occured")
            return
        
    refreshTable()
    
def select():
        try:
            selected_item=my_tree.selection()[0]
            studid=str(my_tree.item(selected_item)['values'][0])
            fname=str(my_tree.item(selected_item)['values'][1])
            lname=str(my_tree.item(selected_item)['values'][2])
            address=str(my_tree.item(selected_item)['values'][3])
            phone=str(my_tree.item(selected_item)['values'][4])
            
            setph(studid,1)
            setph(fname,2)
            setph(lname,3)
            setph(address,4)
            setph(phone,5)
        except:
            messagebox.showinfo("Error","Please select a data row")

def search():
    studid=str(studidEntry.get())
    fname=str(fnameEntry.get())
    lname=str(lnameEntry.get())
    address=str(addressEntry.get())
    phone=str(phoneEntry.get())
    
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("Select * from students where STUDID='"+studid+"' or FNAME='"+fname+"' or LNAME='"+lname+"' or ADDRESS='"+address+"' or PHONE='"+phone+"' ")
    
    try:
        result=cursor.fetchall()
        for num in range(0,5):
            setph(result[0][num],(num+1))
            
        conn.commit()
        conn.close()
    except:
        messagebox.showinfo("Error","No data found") 
        
def update():
    selectedstudid=""
    try:
        selected_item=my_tree.selection()[0]
        selectedstudid=str(my_tree.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error","Please select a data row")
        
    studid=str(studidEntry.get())
    fname=str(fnameEntry.get())
    lname=str(lnameEntry.get())
    address=str(addressEntry.get())
    phone=str(phoneEntry.get())
    
    if (studid=="" or studid==" ") or (fname=="" or fname==" ") or (lname=="" or lname==" ") or (address=="" or address==" ") or (phone=="" or phone==" "):
        messagebox.showinfo("Error","please fill up the blank entry")
        return
    else:
        try:
            conn=connection()
            cursor=conn.cursor()
            cursor.execute("Update students SET STUDID='"+
                           studid+"', FNAME='"+
                           fname+"', LNAME='"+
                           lname+"', ADDRESS='"+
                           address+"', PHONE='"+
                           phone+"' WHERE STUDID='"+
                           selectedstudid+"' ")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error","Stud ID already exist")
            return
        
    refreshTable()
    
        
#gui
label=Label(root,text="student registration system",font=('Arial Bold',30))
label.grid(row=0,column=0,columnspan=8,rowspan=2,padx=50,pady=40)

studid=Label(root,text="Stud ID",font=('Arial',15))
fname=Label(root,text="First name",font=('Arial',15))
lname=Label(root,text="Last name",font=('Arial',15))
address=Label(root,text="Address",font=('Arial',15))
phone=Label(root,text="Phone",font=('Arial',15))
  
studid.grid(row=3,column=0,columnspan=1,padx=50,pady=5)
fname.grid(row=4,column=0,columnspan=1,padx=50,pady=5)
lname.grid(row=5,column=0,columnspan=1,padx=50,pady=5)
address.grid(row=6,column=0,columnspan=1,padx=50,pady=5)
phone.grid(row=7,column=0,columnspan=1,padx=50,pady=5)

studidEntry=Entry(root,width=55,bd=5,font=('Arial',15),textvariable=ph1)
fnameEntry=Entry(root,width=55,bd=5,font=('Arial',15),textvariable=ph2)
lnameEntry=Entry(root,width=55,bd=5,font=('Arial',15),textvariable=ph3)
addressEntry=Entry(root,width=55,bd=5,font=('Arial',15),textvariable=ph4)
phoneEntry=Entry(root,width=55,bd=5,font=('Arial',15),textvariable=ph5)

studidEntry.grid(row=3,column=1,columnspan=4,padx=5,pady=0)
fnameEntry.grid(row=4,column=1,columnspan=4,padx=5,pady=0)
lnameEntry.grid(row=5,column=1,columnspan=4,padx=5,pady=0)
addressEntry.grid(row=6,column=1,columnspan=4,padx=5,pady=0)
phoneEntry.grid(row=7,column=1,columnspan=4,padx=5,pady=0)

addtn=Button(root,text="add",padx=65,pady=25,width=10,bd=5,font=('Arial',15),bg="#84F894",command=add)
updatetn=Button(root,text="update",padx=65,pady=25,width=10,bd=5,font=('Arial',15),bg="#84E8F8",command=update)
deletetn=Button(root,text="delete",padx=65,pady=25,width=10,bd=5,font=('Arial',15),bg="#FF9999",command=delete)
searchtn=Button(root,text="search",padx=65,pady=25,width=10,bd=5,font=('Arial',15),bg="#F4FE82",command=search)
resettn=Button(root,text="reset",padx=65,pady=25,width=10,bd=5,font=('Arial',15),bg="#F398FF",command=reset) 
selecttn=Button(root,text="select",padx=65,pady=25,width=10,bd=5,font=('Arial',15),bg="#EEEEEE",command=select)

addtn.grid(row=3,column=5,columnspan=1,rowspan=2)
updatetn.grid(row=5,column=5,columnspan=1,rowspan=2)
deletetn.grid(row=7,column=5,columnspan=1,rowspan=2)
searchtn.grid(row=9,column=5,columnspan=1,rowspan=2)
resettn.grid(row=11,column=5,columnspan=1,rowspan=2)
selecttn.grid(row=13,column=5,columnspan=1,rowspan=2)

style=ttk.Style()
style.configure("Treeview.Heading",font=("Arial Bold",11))
my_tree['columns']=("stud ID","first name","last name","address","phone")

my_tree.column("#0",width=0,stretch=NO)
my_tree.column("stud ID",anchor=W,width=170)
my_tree.column("first name",anchor=W,width=150)
my_tree.column("last name",anchor=W,width=150)
my_tree.column("address",anchor=W,width=165)
my_tree.column("phone",anchor=W,width=150)

my_tree.heading("stud ID",text="Student Id",anchor=W)
my_tree.heading("first name",text="First name",anchor=W)
my_tree.heading("last name",text="Last name",anchor=W)
my_tree.heading("address",text="Address",anchor=W)
my_tree.heading("phone",text="Phone",anchor=W)

refreshTable()

root.mainloop()