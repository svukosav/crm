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
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter.ttk import *


tab_w_id = {}

class CRM(Frame):
	def __init__(self, title, master=None):
		Frame.__init__(self, master)

		self.create_db()
		self.load_proj_list()
		self.create_tabs()
		self.pop_tabs()
		self.menu()
		self.pop_sum_tab()
		self.pack(fill="both", expand=1)

	def load_proj_list(self):
		# Generate list of current distinct projects in database
		conn = sqlite3.connect('crmdatabase.sqlite3')
		cur = conn.cursor()

		sql_command = """
			SELECT DISTINCT project FROM tasks;
		"""

		cur.execute(sql_command)
		proj = cur.fetchall()

		self.proj_list = [x[0] for x in proj]

	def dd_mm_yyyy(self):
		# Return current date in dd/mm/yyyy format
		now = datetime.datetime.now()
		return '-'.join(map(str, [now.day, now.month, now.year]))

	def create_db(self):
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
			task_id INTEGER PRIMARY KEY,
			project VARCHAR DEFAULT "Project ID",
			task_name VARCHAR DEFAULT "Task Name",
			date_created TIMESTAMP DEFAULT CURRENT_DATE,
			task_description VARCHAR DEFAULT "Description",
			status VARCHAR DEFAULT "Open",
			UNIQUE (task_id));

		INSERT INTO tasks (project, task_name, date_created, task_description, status) VALUES ('Bow River Bridge', 'Call Tim Chu', '2019-01-01', 'Ask about Bow River Bridge', 'Open');

		INSERT INTO tasks (project, task_name, date_created, task_description, status) VALUES ('Bow River Bridge', 'Call Singbeil this is an extra long text description', '2019-01-05', 'Confirm rams', 'Open');

		INSERT INTO tasks (project, task_name, date_created, task_description, status) VALUES ('Bow River Bridge', 'Call Janox', '2019-04-01', 'Check power supplies', 'Closed');

		INSERT INTO tasks (project, task_name, date_created, task_description, status) VALUES ('Bow River Bridge', 'Call Tim Chu', '2014-01-01', 'Ask about Bow River Bridge', 'Open');

		INSERT INTO tasks (project, task_name, date_created, task_description, status) VALUES ('Bow River Bridge', 'Call Singbeil this is an extra long text description', '2011-01-01', 'Confirm rams', 'Open');

		INSERT INTO tasks (project, task_name, date_created, task_description, status) VALUES ('Bow River Bridge', 'Call Janox', '2019-01-09', 'Check power supplies', 'Closed');

		INSERT INTO tasks (project, task_name, date_created, task_description, status) VALUES ('Bow River Bridge', 'Call Tim Chu', '2019-05-02', 'Ask about Bow River Bridge', 'Open');

		INSERT INTO tasks (project, task_name, date_created, task_description, status) VALUES ('Bow River Bridge', 'Call Janox', '2011-09-01', 'Check power supplies', 'Closed');

		INSERT INTO tasks (project, task_name, date_created, task_description, status) VALUES ('West Calgary Ring Road', 'Call Stefan', '2013-01-01', 'Send emails', 'Open');

		INSERT INTO tasks (project, task_name, task_description, status) VALUES ('Hwy 91 Widening', 'Create drawings for joop', 'use autocad', 'Open');

		INSERT INTO tasks (project, task_name, task_description, status) VALUES ('Hwy 91 Widening', 'another task', 'Another really long used description of text for use autocad', 'Open');

		INSERT INTO tasks (project, task_name, task_description, status) VALUES ('Lynn Valley Twinning', 'Call Fortis', 'Check gas lines', 'Open');
		
		"""
		cur.executescript(sql_command)
		conn.commit()

		conn.close()

	def create_tabs(self):
		self.tab_control = ttk.Notebook(self)

		self.tab = ttk.Frame(self.tab_control)
		self.tab_control.add(self.tab, text="Summary")
		tab_w_id["Summary"] = self.tab

		for x in self.proj_list:
			self.tab = ttk.Frame(self.tab_control)
			self.tab_control.add(self.tab, text=x)
			tab_w_id[x] = self.tab

		self.tab_control.pack(expand=1, fill="both")

	def pop_sum_tab(self):
		print(tab_w_id["Summary"])
		btn = Button(tab_w_id["Summary"], text="New Task", command=self.create_task)
		btn.grid(column = 0, row = 0)

	def pop_tabs(self):
		conn = sqlite3.connect('crmdatabase.sqlite3')
		cur = conn.cursor()
		for proj, tab_obj in tab_w_id.items():
			sql_command = """
				SELECT * FROM tasks WHERE project = ? ORDER BY date_created DESC;
			"""

			# Select data with the id x (specific project)
			cur.execute(sql_command, (proj,))
			resp = cur.fetchall()

			# Populate all data with the given id x (specific project)
			for counter, entry in enumerate(resp):
				text = '\n'.join(["Task: "+str(entry[0]), entry[2], entry[4], entry[3]])
				# Task Name
				nTask = Label(tab_obj, text=text, font=("Helvetica", 9))
				nTask.grid(column=0, row=counter+1, sticky="news", ipadx=5, ipady=5, padx=2, pady=0.5)

				if entry[5] == "Open":
					nTask.configure(background="Green", foreground="White", wraplength=250)
				elif entry[5] == "Closed":
					nTask.configure(background="Red", foreground="White", wraplength=250)

				checkmark = Button(tab_obj, text="Complete Task", command="")
				checkmark.grid(column = 1, row = counter+1, sticky="NE")
				checkmark = Button(tab_obj, text="Modify Task", command="")
				checkmark.grid(column = 2, row = counter+1, sticky="NE")

		conn.close()	

	def menu(self):
		self.menu = Menu(self)
		new_item = Menu(self.menu, tearoff=0)
		new_item.add_command(label="New Task", command="")
		new_item.add_separator()
		new_item.add_command(label="Edit", command="")
		new_item.add_command(label="Readme", command="")
		new_item.add_command(label="Exit", command=quit)
		self.menu.add_cascade(label="File", menu=new_item)
		self.master.config(menu=self.menu)



	def close_task(self):
		# Turn from green to red
		pass

	def modify_task(self):
		# Change name, description, etc
		pass

	def analytics(self):
		# Data points on existing tasks
		pass

	def create_task(self):
		# Create new task
		pass

	def check_task(self):
		# See if task has expired
		# If true, turn orange
		pass







def setup():
	print("Welcome to CRMv1.0.0\n" + 
			"Created with sqlite3 on January 31st 2019\n")
	# Initialization
	root = Tk()
	root.title("Flatiron CRMv1.0.0")
	root.geometry('550x500')
	root.config(background="grey")
	root.resizable(width=False, height=False)
	app = CRM(root)
	root.mainloop()
	
if __name__ == "__main__":
	setup()











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