import time
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
task_w_id = {}

class CRM(tk.Frame):
	def __init__(self, title, master=None):
		tk.Frame.__init__(self, master)
		self.colours()
		self.create_db()
		self.load_proj_list()
		self.create_tabs()
		self.pop_tabs()
		self.menu()
		self.pop_sum_tab()
		self.pack(fill="both", expand=True)

	def colours(self):
		# Bootstrap Colors
		# Main colors
		self.bg = "#F8F9FA" #off-white
		self.fg = "#343A40" # off-black 52, 58, 64

		# Misc colors
		self.dark_grey = "#6C757D" #dark grey
		self.blue = "#007BFF" # blue 0,123,255
		self.green = "#28A745" # green 40,167,69
		self.red = "#DC3545" # red 220, 53, 69
		self.yellow = "#FFC107" # yellow 255, 193, 7
		self.turquoise = "#17A2B8" # turquoise 23, 162, 184
		


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

		conn.close()

	def yyyy_mm_dd(self):
		# Return current date in dd/mm/yyyy format
		now = datetime.datetime.now()
		return str('-'.join(map(str, [now.year, now.month, now.day])))

	def create_db(self):
		# Creates a sample database for debugging and testing the app. <<Will eventually be deleted>>
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
			date_completed TIMESTAMP DEFAULT "Date Completed",
			UNIQUE (task_id));

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
		# Creates the project tabs for the app
		self.tab_control = ttk.Notebook(self)
		self.tab_control.enable_traversal()

		# Creates the summary tab which is manually added and prepended to tab_w_id
		self.tab = ttk.Frame(self.tab_control)
		self.tab_control.add(self.tab, text="Summary")
		tab_w_id["Summary"] = self.tab

		# Project tabs are dynamically added based on database entries and stored in tab_w_id
		for x in self.proj_list:
			self.tab = ttk.Frame(self.tab_control)
			self.tab_control.add(self.tab, text=x)
			tab_w_id[x] = self.tab

		self.tab_control.pack(expand=1, fill="both")

	def update_tabs(self, projName):
		self.tab = ttk.Frame(self.tab_control)
		self.tab_control.add(self.tab, text=projName)
		tab_w_id[projName] = self.tab


	def pop_sum_tab(self):
		title = Label(tab_w_id["Summary"], text="CRM v1.0.0", font=("Helvetica Neue", 18))
		title.grid(column=0, row=0, sticky="w", columnspan=2)

		lblActions = Label(tab_w_id["Summary"], text="Actions", font=("Helvetica Neue", 15))
		lblActions.grid(column=0, row=1, sticky="w")

		btn = tk.Button(tab_w_id["Summary"], text="New Task", command=self.create_task, background=self.green, foreground=self.bg, padx=50, pady=10, relief="groove", font=("Helvetica Neue", 11))
		btn.grid(column = 0, row = 2, columnspan=3, sticky="news")

		# Create GUI
		lblTitle = Label(tab_w_id["Summary"], text="Analytics", font=("Helvetica Neue", 15))
		lblTitle.grid(column=0, row=3, sticky="w")

		# Completed tasks
		lblCompTasks = Label(tab_w_id["Summary"], text="Completed Tasks", font=("Helvetica Neue", 11, "bold"))
		lblCompTasks.grid(column=0, row=4, sticky="w")

		self.compTasks = Label(tab_w_id["Summary"], text="", font=("Helvetica Neue", 11))
		self.compTasks.grid(column=1, row=4, sticky="w")

		# Tasks outstanding
		lblOutTasks = Label(tab_w_id["Summary"], text="Tasks Outstanding", font=("Helvetica Neue", 11, "bold"))
		lblOutTasks.grid(column=0, row=5, sticky="w")

		self.outTasks = Label(tab_w_id["Summary"], text="", font=("Helvetica Neue", 11))
		self.outTasks.grid(column=1, row=5, sticky="w")

		# Total tasks
		lblCompTasks = Label(tab_w_id["Summary"], text="Total Tasks", font=("Helvetica Neue", 11, "bold"))
		lblCompTasks.grid(column=0, row=6, sticky="w")
		
		self.totTasks = Label(tab_w_id["Summary"], text="", font=("Helvetica Neue", 11))
		self.totTasks.grid(column=1, row=6, sticky="w")
		
		# Projects
		lblProj = Label(tab_w_id["Summary"], text="Summary of Projects", font=("Helvetica Neue", 11, "bold"))
		lblProj.grid(column=0, row=7, sticky="Nw")
		
		self.lblProj = Label(tab_w_id["Summary"], text="", font=("Helvetica Neue", 11))
		self.lblProj.grid(column=1, row=7, sticky="NW")	

		self.analytics()

	def analytics(self):
			# Analytics on the database
			# Get data from the database
			conn = sqlite3.connect('crmdatabase.sqlite3')
			cur = conn.cursor()

			sql_command = """
				SELECT COUNT(*) FROM tasks;
			"""

			cur.execute(sql_command)
			data = cur.fetchall()
			taskTotal = data[0][0]

			sql_command = """
				SELECT COUNT(*) FROM tasks WHERE status='Open';
			"""

			cur.execute(sql_command)
			data = cur.fetchall()
			taskOpen = data[0][0]

			sql_command = """
				SELECT COUNT(*) FROM tasks WHERE status='Closed';
			"""

			cur.execute(sql_command)
			data = cur.fetchall()
			taskClosed = data[0][0]

			sql_command = """
				SELECT COUNT(DISTINCT project) FROM tasks;
			"""

			cur.execute(sql_command)
			data = cur.fetchall()
			uniqueProj = data[0][0]

			sql_command = """
				SELECT project, COUNT(project) FROM tasks GROUP BY project;
			"""

			cur.execute(sql_command)
			data = cur.fetchall()
			projectInfo = dict(data)
			# print(taskTotal, taskOpen, taskClosed, uniqueProj, projectInfo)
			conn.close()

			# Change values in summary tab
			self.compTasks.config(text=str(taskClosed))
			self.outTasks.config(text=str(taskOpen))
			self.totTasks.config(text=str(taskTotal))
			self.lblProj.config(text='\n'.join([x for x in projectInfo]))

	def pop_tabs(self):
		# Populates tabs with data in the database
		# Connects to database
		conn = sqlite3.connect('crmdatabase.sqlite3')
		cur = conn.cursor()

		# Iterates through tabs
		for proj, tab_obj in tab_w_id.items():
			sql_command = """
				SELECT * FROM tasks WHERE project = ? ORDER BY date_created DESC;
			"""

			# Select data with the project id (specific project)
			cur.execute(sql_command, (proj,))
			resp = cur.fetchall()

			# Populate all data with the given project id (specific project)
			for counter, entry in enumerate(resp):
				text = '\n'.join(["Task: "+str(entry[0]), entry[2], entry[4], entry[3], entry[5], str(entry[6])])
				# Task Name
				nTask = Label(tab_obj, text=text, font=("Helvetica", 9))
				nTask.grid(column=0, row=counter+1, sticky="news", ipadx=5, ipady=5, padx=2, pady=0.5)

				# Store task id in task_w_id
				task_w_id[entry[0]] = nTask

				if entry[5] == "Open":
					nTask.config(background=self.green, foreground=self.fg, wraplength=250)
				elif entry[5] == "Closed":
					nTask.config(background=self.red, foreground=self.fg, wraplength=250)

				checkmark = tk.Button(tab_obj, text="Complete Task", command=lambda x=(nTask, entry[0]): self.close_task(x), background=self.green, foreground=self.fg, relief="groove", takefocus=False)
				checkmark.grid(column = 1, row = counter+1, sticky="news")
				checkmark = tk.Button(tab_obj, text="Modify Task", command="", background=self.yellow, foreground=self.fg, relief="groove", takefocus=False)
				checkmark.grid(column = 2, row = counter+1, sticky="news")

		conn.close()

	def menu(self):
		self.menu = Menu(self)
		new_item = Menu(self.menu, tearoff=0)
		new_item.add_command(label="New Task", command=self.create_task)
		new_item.add_separator()
		new_item.add_command(label="Edit", command="")
		new_item.add_command(label="Readme", command="")
		new_item.add_command(label="Exit", command=quit)
		self.menu.add_cascade(label="File", menu=new_item)
		self.master.config(menu=self.menu)

	def close_task(self, entry):
		# Unpack entry tuple
		lblTask = entry[0]
		taskId = entry[1]
		date_completed = datetime.datetime.now()

		# Update database
		conn = sqlite3.connect('crmdatabase.sqlite3')
		cur = conn.cursor()

		sql_command = """
			UPDATE tasks SET status='Closed', date_completed=CURRENT_DATE WHERE task_id=?;
		"""

		cur.execute(sql_command, (taskId,))
		conn.commit()

		# Turn task from "Open" to "Close" (from green to red) locally. Global update of all colors occurs when new task is inserted.
		self.pop_tabs()
		self.analytics()

		

	def modify_task(self):
		# Change name, description, etc
		pass

	def create_task(self):
		# Create new task
		self.win2 = tk.Toplevel(self)
		self.win2.title("New Task")
		self.win2.config(background=self.bg)
		self.win2.resizable(width=False, height=False)

		self.lblTask = tk.Label(self.win2, text="Task Name", background=self.bg, foreground=self.fg)
		self.lblTask.grid(column=0, row=0, sticky="w")
		self.entTask = tk.Entry(self.win2)
		self.entTask.grid(column=0, row=1, padx=5, pady=5, sticky="w")
		self.entTask.focus()

		self.lblDate = tk.Label(self.win2, text="Date Created (Y/M/D)", background=self.bg, foreground=self.fg)
		self.lblDate.grid(column=1, row=0, sticky="w")
		self.lblDateText = tk.Label(self.win2, text=str(self.yyyy_mm_dd()), background=self.bg)
		self.lblDateText.grid(column=1, row=1, sticky="w")

		self.alert = tk.Label(self.win2, text="", background=self.bg, foreground=self.red)
		self.alert.grid(column=2, row=1, sticky="news")
		self.alert_msg = tk.Label(self.win2, text="", background=self.bg, foreground=self.red)
		self.alert_msg.grid(column=2, row=2, sticky="news")
		
		self.lblProjName = tk.Label(self.win2, text="New Project Name", background=self.bg, foreground=self.fg, state=DISABLED)
		self.lblProjName.grid(column=0, row=2, sticky="w")
		self.entProjName = tk.Entry(self.win2, state=DISABLED)
		self.entProjName.grid(column=0, row=3, padx=5, pady=5, sticky="w")

		self.chk_state = BooleanVar()
		self.chk_state.set(True)
		self.chk = tk.Checkbutton(self.win2, text="Select existing", var=self.chk_state, command=self.change_state, background=self.bg, foreground=self.fg, selectcolor=self.bg)
		self.chk.grid(column=2, row=3)

		self.curProjList = tk.Label(self.win2, text="Current Projects", background=self.bg, foreground=self.fg)
		self.curProjList.grid(column=1, row=2, sticky="W")
		self.comboCurProjList = ttk.Combobox(self.win2, foreground=self.fg, background=self.bg, state="readonly")
		self.comboCurProjList['values'] = [""] + self.proj_list
		self.comboCurProjList.current(0)
		self.comboCurProjList.grid(column=1, row=3, sticky="W")

		self.lblTaskDesc = tk.Label(self.win2, text="Task Description", background=self.bg, foreground=self.fg)
		self.lblTaskDesc.grid(column=0, row= 4, sticky="w")
		self.entTaskDesc = tk.Text(self.win2, width=50, height=5)
		self.entTaskDesc.grid(column=0, row=5, padx=5, pady=5, sticky="w", columnspan=3)

		self.submitNewTask = tk.Button(self.win2, text="Submit", command=self.get_input, background=self.green, foreground=self.bg, relief="groove", font=("Helvetica", 11))
		self.submitNewTask.grid(column=0, row=6, sticky="nesw", padx=100, columnspan=3)

	def change_state(self):
		if self.chk_state.get() == True:
			self.curProjList.config(state=NORMAL)
			self.comboCurProjList.config(state=NORMAL)
			self.entProjName.delete(0, END)
			self.lblProjName.config(state=DISABLED)
			self.entProjName.config(state=DISABLED)
		elif self.chk_state.get() == False:
			self.curProjList.config(state=DISABLED)
			self.comboCurProjList.config(state=DISABLED)
			self.comboCurProjList.current(0)
			self.lblProjName.config(state=NORMAL)
			self.entProjName.config(state=NORMAL,)

	def get_input(self):
		if not self.entTask.get():
			self.alert.config(text="Warning")
			self.alert_msg.config(text="Missing Task")
			self.lblTask.config(foreground=self.red)
			self.win2.after(3000, lambda: (self.alert.config(text=""), self.alert_msg.config(text=""), self.lblTask.config(foreground=self.fg)))
		elif not self.entProjName.get() and not self.comboCurProjList.get():
			self.alert.config(text="Warning")
			self.alert_msg.config(text="Missing Project")
			self.win2.after(3000, lambda: (self.alert.config(text=""), self.alert_msg.config(text="")))
		elif len(self.entTaskDesc.get("1.0", "end-1c")) == 0:
			self.alert.config(text="Warning")
			self.alert_msg.config(text="Missing Text")
			self.lblTaskDesc.config(foreground=self.red)
			self.win2.after(3000, lambda: (self.alert.config(text=""), self.alert_msg.config(text=""), self.lblTaskDesc.config(foreground=self.fg)))
		else:
			if self.entProjName.get() and not self.comboCurProjList.get():
				project_name = self.entProjName.get()
			elif not self.entProjName.get() and self.comboCurProjList.get():
				project_name = self.comboCurProjList.get()			

			task_name = self.entTask.get()
			task_description = self.entTaskDesc.get(1.0, END).rstrip()

			# Connect to database and add entry
			conn = sqlite3.connect('crmdatabase.sqlite3')
			cur = conn.cursor()

			sql_command = """
				INSERT INTO tasks (project, task_name, task_description, status) VALUES (?, ?, ?, 'Open');
			"""
			cur.execute(sql_command, (project_name, task_name, task_description,))
			conn.commit()
			conn.close()

			# Close window
			self.win2.destroy()
			# update tabs
			if project_name not in self.proj_list:
				self.update_tabs(project_name)
			self.load_proj_list()
			self.pop_tabs()
			self.analytics()

	def check_task(self):
		# See if task has expired
		# If true, turn orange
		pass

def setup():
	print("Welcome to CRMv1.0.0\n" + 
			"Created with sqlite3 on January 31st 2019\n")
	# Initialization
	root = tk.Tk()
	root.title("Flatiron CRMv1.0.0")
	root.geometry('550x500')
	root.resizable(width=False, height=False)
	app = CRM("CRM Prototype", master=root)
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