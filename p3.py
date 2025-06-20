from tkinter import *
from tkinter.messagebox import *
from PIL import Image, ImageTk 
from sqlite3 import *
import re

root=Tk()
root.geometry("600x700+300+50")
root.title("Contact Book")
root.iconbitmap("contact.ico")

bg_image = Image.open("contactbg.png")
bg_image = bg_image.resize((600, 700))
bg = ImageTk.PhotoImage(bg_image)

#defining functionality

def add():
	con=None
	try:
		con=connect("Contact.db")
		cursor=con.cursor()
		cursor.execute("Create table if not exists contact(name text not null,phone text unique key,email text unique key)")

		name=ent_name.get().strip()
		phone=ent_phone.get().strip()
		email=ent_email.get().strip()
		if not name:
			showwarning("Invalid Input", "Name cannot be empty!")
			return
		if not phone.isdigit() or len(phone) != 10:
			showwarning("Invalid Phone", "Phone number must be exactly 10 digits and only numbers.")
			return
		if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
			showwarning("Invalid Email", "Please enter a valid @gmail.com email address.")
			return

		sql="insert into contact values(?,?,?)"	
		cursor.execute(sql, (name,phone,email))
		con.commit()
		showinfo("Congratulations","Contact Addded Successfully")
		ent_name.delete(0,END)
		ent_phone.delete(0,END)
		ent_email.delete(0,END)
		ent_name.focus()

		

	except Exception as e:
		con.rollback()
		showerror("Issue ",e)
		ent_name.delete(0,END)
		ent_phone.delete(0,END)
		ent_email.delete(0,END)
		ent_name.focus()
		

	finally:
		if con is not None:
			con.close()
def view():
	con=None
	try:
		con=connect("Contact.db")
		cursor=con.cursor()
		sql="select * from contact"
		cursor.execute(sql)
		data=cursor.fetchall()
		listbox.delete(0, END)  # Clear listbox before inserting

		for d in data:
			msg = f"{d[0]} | {d[1]} | {d[2]}"
			listbox.insert(END, msg)

	except Exception as e:			
		showerror("Issue",e)


	finally:
		if con is not None:
			con.close()


def update():
    con = None
    try:
        selected = listbox.curselection()
        if not selected:
            showwarning("No Selection", "Please select a contact to update.")
            return

        # Original contact details (for WHERE clause)
        original_contact = listbox.get(selected[0])
        original_name = original_contact.split("|")[0].strip()

        # New values from entries
        name = ent_name.get().strip()
        phone = ent_phone.get().strip()
        email = ent_email.get().strip()

        # Validation
        if not name:
            showwarning("Invalid Input", "Name cannot be empty!")
            return
        if not phone.isdigit() or len(phone) != 10:
            showwarning("Invalid Phone", "Phone number must be exactly 10 digits and only numbers.")
            return
        if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
            showwarning("Invalid Email", "Please enter a valid @gmail.com email address.")
            return

        con = connect("Contact.db")
        cursor = con.cursor()

        cursor.execute("UPDATE contact SET name=?, phone=?, email=? WHERE name=?", (name, phone, email, original_name))
        con.commit()

        showinfo("Updated", f"Contact '{original_name}' updated successfully.")
        view()

        # Optional: Clear the entry fields
        ent_name.delete(0, END)
        ent_phone.delete(0, END)
        ent_email.delete(0, END)
        ent_name.focus()

    except Exception as e:
        if con:
            con.rollback()
        showerror("Issue", str(e))
    finally:
        if con:
            con.close()

		
	
def delete():
	con=None
	try:
		selected=listbox.curselection()
		if not selected:
			showwarning("No seletion","Please select a contact to delete")
			return

		contact=listbox.get(selected[0])
		name = contact.split("|")[0].strip()

		if not askyesno("Confirm please",f"Are you sure you want to delete '{name}'?"):
			return
		con=connect("Contact.db")
		cursor=con.cursor()
		cursor.execute("delete from contact where name=?",(name,))
		con.commit()

		listbox.delete(selected[0])
		showinfo("Deleted",f"Contact '{name}' deleted successfully.")
	except Exception as e:		
		con.rollback()
		showerror("Issue ",str(e))
		
	finally:
		if con is not None:
			con.close()


def clear():
	con=None
	try:

		if not askyesno("Confirm please","Are you sure you want to delete all the contacts?"):
			return
		con=connect("Contact.db")
		cursor=con.cursor()
		cursor.execute("delete from contact")
		con.commit()

		listbox.delete(0,END)
		showinfo("Deleted","All contacts have been deleted successfully.")
	except Exception as e:		
		con.rollback()
		showerror("Issue ",str(e))
		
	finally:
		if con is not None:
			con.close()

def exit():
	if askyesno("Exit","Do you really want to exit"):
		root.destroy()
			

# Create background label
bg_label = Label(root, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

label_title=Label(root,text="📒 Contact Book 📒",font=("Arial",30,"bold"),bg="#E3F2FD",fg="#0D47A1")
label_title.pack(pady=5)

label_name=Label(root,text="Enter Name:",font=("Arial",20,"bold"),fg="white",bg="black")
label_name.place(x=30,y=100)
ent_name=Entry(root,font=("Arial",20,"bold"))
ent_name.place(x=240,y=100)

label_phone=Label(root,text="Enter Phone:",font=("Arial",20,"bold"),fg="white",bg="black")
label_phone.place(x=30,y=170)
ent_phone=Entry(root,font=("Arial",20,"bold"))
ent_phone.place(x=240,y=170)

label_email=Label(root,text="Enter EmailId:",font=("Arial",20,"bold"),fg="white",bg="black")
label_email.place(x=30,y=250)
ent_email=Entry(root,font=("Arial",20,"bold"))
ent_email.place(x=240,y=250)

btn_add=Button(root,text="ADD",font=("Arial",15,"bold"),bg="#4CAF50",fg="black",command=add)
btn_add.place(x=50,y=320)
btn_view=Button(root,text="view",font=("Arial",15,"bold"),bg="#4CAF50",fg="black",command=view)
btn_view.place(x=130,y=320)
btn_update=Button(root,text="update",font=("Arial",15,"bold"),bg="#4CAF50",fg="black",command=update)
btn_update.place(x=210,y=320)
btn_delete=Button(root,text="delete",font=("Arial",15,"bold"),bg="#4CAF50",fg="black",command=delete)
btn_delete.place(x=310,y=320)
btn_clear=Button(root,text="clear",font=("Arial",15,"bold"),bg="#4CAF50",fg="black",command=clear)
btn_clear.place(x=400,y=320)
btn_exit=Button(root,text="exit",font=("Arial",15,"bold"),bg="#4CAF50",fg="black",command=exit)
btn_exit.place(x=490,y=320)

listbox=Listbox(root,font=("Arial",20,"bold"),width=40,height=8,bg="black",fg="white",selectbackground="pink",selectforeground="blue",highlightthickness=0,activestyle='none')
listbox.place(x=0,y=380)
scrollbar=Scrollbar(root)
scrollbar.place(x=580,y=380,height=235)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)



root.mainloop()
