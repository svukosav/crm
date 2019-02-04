import os
import time
from os import listdir
from os import path
from os.path import isfile, join
import pandas as pd
import numpy as np
import pickle
import datetime
import sqlite3
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter.ttk import *

def dd_mm_yyyy():
	# Return current date in dd/mm/yyyy format
	now = datetime.datetime.now()
	return '-'.join(map(str, [now.day, now.month, now.year]))

def db():
	# Connect to database or create if non existant
	conn = sqlite3.connect('crmdatabase.sqlite3')
	cur = conn.cursor()

	# Load existing tables
	cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
	current_tables = cur.fetchall()

	# Create task table if non existant and add data to task table
	sql_command = """

	DROP TABLE IF EXISTS tasks;

	CREATE TABLE IF NOT EXISTS tasks (
		id INTEGER PRIMARY KEY,
		project VARCHAR DEFAULT "Project ID",
		task_name VARCHAR DEFAULT "Task Name",
		task_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		task_description VARCHAR DEFAULT "Description",
		UNIQUE (id));

	INSERT INTO tasks (project, task_name, task_description) VALUES ('Bow River Bridge', 'Call Tim Chu', 'Ask about Bow River Bridge');

	INSERT INTO tasks (project, task_name, task_description) VALUES ('Bow River Bridge', 'Call Singbeil', 'Confirm rams');

	INSERT INTO tasks (project, task_name, task_description) VALUES ('Bow River Bridge', 'Call Janox', 'Check power supplies');

	INSERT INTO tasks (project, task_name, task_description) VALUES ('West Calgary Ring Road', 'Call Stefan', 'Send emails');

	INSERT INTO tasks (project, task_name, task_description) VALUES ('Hwy 91 Widening', 'Create drawings for joop', 'use autocad');

	INSERT INTO tasks (project, task_name, task_description) VALUES ('Lynn Valley Twinning', 'Call Fortis', 'Check gas lines');
	
	"""
	cur.executescript(sql_command)
	conn.commit()

	# Select data
	cur.execute('SELECT * FROM tasks')
	data = cur.fetchall()
	print(data)
	conn.close()



def window_setup():

	def pop_tabs(lt):
		conn = sqlite3.connect('crmdatabase.sqlite3')
		cur = conn.cursor()
		for x in lt:
			sql_command = """
				SELECT * FROM tasks WHERE project = ?;
			"""

			cur.execute(sql_command, (x,))
			resp = cur.fetchall()

			for counter, entry in enumerate(resp):
				print(counter)
				text = "Task Name: " + entry[2] + "\nDescription: " + entry[4] + "\nDate Created: " + entry[3]
				# Task Name
				nTask = Label(lt[entry[1]], text=text, font="Helvetica 10")
				nTask.grid(column=0, row=counter*2+1, sticky='w')


	def tab_projects():
		conn = sqlite3.connect('crmdatabase.sqlite3')
		cur = conn.cursor()

		sql_command = """
			SELECT DISTINCT project FROM tasks;
		"""

		cur.execute(sql_command)
		proj = cur.fetchall()
		
		tab_control = ttk.Notebook(window)

		# Create Summary tab
		summary = ttk.Frame(tab_control)
		tab_control.add(summary, text="Summary")
		lblCurProj = Label(summary, text= "Current Projects:", font="Helvetica 10 bold")
		lblCurProj.grid(column=0, row=0, sticky='w')
		lblProjList = Label(summary, text= "")
		lblProjList.grid(column=0, row=1, sticky="w")

		# List current projects
		l = [x[0] for x in proj]
		lblProjList.configure(text='\n'.join(l), font="Helvetica 9 italic")
		
		# Summary of upcoming tasks
		lblTaskSum = Label(summary, text="Upcoming Tasks", font="Helvetica 10 bold")
		lblTaskSum.grid(column=0, row=2, sticky="w")

		# Create project tabs
		tabs_id = []
		for entry in proj:
			text1 = entry[0]
			frame = ttk.Frame(tab_control)
			tab_control.add(frame, text=text1)
			lbl1 = Label(frame, text= "Current Tasks:", font="Helvetica 10 bold")
			lbl1.grid(column=0, row=0, sticky='w')
			tabs_id.append(frame)

		# Tabs dict with project keys and tkinter object values
		lt = dict(zip(l, tabs_id))

		tab_control.pack(expand=1, fill="both")

		return lt

	def list_projects():
		conn = sqlite3.connect('crmdatabase.sqlite3')
		cur = conn.cursor()

		sql_command = """
			SELECT DISTINCT project FROM tasks;
		"""

		cur.execute(sql_command)
		proj = cur.fetchall()
		
		conn.close()
		tab_control = ttk.Notebook(window)
		proj_sum = Label(ttk.Frame(tab_control), text="Active Projects")
		proj_sum.grid(column=0, row=0)
		


	# window initialization
	window = Tk()
	window.title("Flatiron CRMv1.0.0")
	window.geometry('550x500')

	# Create menu
	def menu():
		menu = Menu(window)
		new_item = Menu(menu, tearoff=0)
		new_item.add_command(label="New Project", command="")
		new_item.add_separator()
		new_item.add_command(label="Edit", command="")
		menu.add_cascade(label="File", menu=new_item)
		window.config(menu=menu)

	lt = tab_projects()
	menu()
	pop_tabs(lt)
	list_projects()


	window.mainloop()

	

def main():
	window_setup()
	

def setup():
	print("Welcome to CRMv1.0.0\n" + 
			"Created with sqlite3 on January 31st 2019\n"+ 
			"Today's Date: " + dd_mm_yyyy() + "\n")
	db()
	
if __name__ == "__main__":
	# Run program setup
	setup()
	# Main loop
	main()











"""
window = Tk()

	window.title("Welcome to Flatiron")
	window.geometry('550x200')


	lbl = Label(window, text="Text Box 1: " + "\n" + "Combobox: ", font=("Arial Bold", 12))
	lbl.grid(column = 0, row = 0)

	txt1 = Entry(window, width=10)
	txt1.grid(column=0, row=1)
	txt1.focus()

	txt2 = Entry(window, width=10, state="disabled")
	txt2.grid(column=1, row=1)

	combo = Combobox(window)
	combo['values'] = (1,2,3,4,5,"Text")
	combo.current(0)
	combo.grid(column=2,row=1)

	chk_state = BooleanVar()
	chk_state.set(False)
	chk = Checkbutton(window, text="I agree to terms", var=chk_state)
	chk.grid(column=3, row=3)

	selected = IntVar()
	rad1 = Radiobutton(window, text="Option 1", value=1, variable=selected, command="")
	rad2 = Radiobutton(window, text="Option 2", value=2, variable=selected, command="")
	rad3 = Radiobutton(window, text="Option 3", value=3, variable=selected, command="")
	rad1.grid(column=0, row=3)
	rad2.grid(column=1, row=3)
	rad3.grid(column=2, row=3)

	txt = scrolledtext.ScrolledText(window,width=40,height=10)
	txt.grid(column=0, row=5)
	txt.insert(INSERT, "temporary text and description")
	
	var = IntVar()
	var.set(50)
	spin1 = Spinbox(window, from_=0, to=100, width=5, textvariable=var)
	spin1.grid(column=2,row=4)

	spin2 = Spinbox(window, value=(3, 8, 11), width=5)
	spin2.grid(column=2, row=5)

	# bar = Progressbar(window, length=100)
	# for x in range(0, 110,10):
	# 	bar['value'] = x
	# 	window.update_idletasks()
	# 	time.sleep(0.5)
	# 	bar.grid(column=1, row=0)

	# Multiple files, returns path
	# file = filedialog.askopenfilenames()
	# Single file, returns path
	# file = filedialog.askopenfilename(filetypes = (("Text files","*.txt"),("All files","*.*")), initialdir = path.dirname(__file__))

	menu = Menu(window)
	new_item = Menu(menu, tearoff=0)
	new_item.add_command(label="New", command="")
	new_item.add_separator()
	new_item.add_command(label="Edit", command="")
	# menu.add_command(label="File")
	menu.add_cascade(label="File", menu=new_item)
	window.config(menu=menu)

	# # Adding additional tabs
	# tab_control = ttk.Notebook(window)
	# tab1 = ttk.Frame(tab_control)
	# tab2 = ttk.Frame(tab_control)
	
	# tab_control.add(tab1, text="First")
	# tab_control.add(tab2, text="Second")

	# lbl1 = Label(tab1, text= "Label1")
	# lbl1.grid(column=0, row=0)
	
	# lbl2 = Label(tab2, text= "Label2")
	# lbl2.grid(column=0, row=0)

	# tab_control.pack(expand=1, fill="both")

	def submit():
		# lbl.configure(text="Button was clicked")
		res = "Text Box 1: " + txt1.get() + "\n" + "Combobox: " + combo.get()
		lbl.configure(text=res)
		print(selected.get())

		# messagebox.showinfo("Temporary Title", "temporary text and description")
		# messagebox.showwarning("Temporary Warning", "temporary warning text and description")
		# messagebox.showerror("Temporary Error", "temporary error text and description")

		# Returns yes or no
		# inp = messagebox.askquestion("Question 1", "Question content")
		# Returns true or false
		# inp = messagebox.askyesno("Question 2", "Question content")
		# Returns true or false or none
		# inp = messagebox.askyesnocancel("Question 3", "Question content")
		# Returns true or false
		# inp = messagebox.askokcancel("Question 4", "Question content")
		# Returns true or false
		# inp = messagebox.askretrycancel("Question 5", "Question content")
		txt.delete(1.0, END)

	btn = Button(window, text="Submit", command=submit)
	btn.grid(column = 2, row = 3)

	window.mainloop()


"""