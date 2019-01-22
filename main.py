import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import pickle
import datetime


class task():


	def __init__(self, task_name, date_created, description):
		self.task_name = task_name
		self.date_created = date_created
		self.description = description
		self.date = dd_mm_yyyy()

	def vars(self):
		return [self.task_name, self.date_created, self.description]

	def summary(self):
		pass


def dd_mm_yyyy():
	# Return current date in dd/mm/yyyy format
	now = datetime.datetime.now()
	return '-'.join(map(str, [now.day, now.month, now.year]))

def load_data():
	# Create str path of data folder based on current directory where python file is located
	data = os.getcwd() + '\data'

	# Create str list of all files inside data folder
	data_files_dir = [f for f in listdir(data) if isfile(join(data, f))]
	
	# Return data if data.pk is in str list
	# Else return None
	# Exceptions return None
	try:
		if 'data.pk' in data_files_dir:
			return pd.read_pickle('.\data\data.pk')
		else:
			return None
	except:
		print("Cannot find directory or data file...\n")
		return None

# No good
def data_output(data = None):
	if data is None:
		dates = pd.date_range('20130101', periods=6)
		df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
		df.to_pickle('.\data\data.pk')
		print("5555")
	else:
		data.to_pickle('.\data\data.pk')

def main(data = None):
	# Check if pickled data file exists in data folder
	if data is None:
		print("No data found...")
	else:
		print("Data found...\n")

	# User input, create new class instance
	# task1 = task('Call subcontractors', dd_mm_yyyy(), 'Call Richard Janox and Hyseco')
	entry = task('Call hyseco', dd_mm_yyyy(), 'Call Enmax')

	# Classifying user input as new instance, modifying existing, or deleting existing
	# Modification of existing class instance
	if entry.task_name in list(data['task_name']):
		pass
	else:
		# Creation of new class instance
		data_in = pd.DataFrame(entry.__dict__, columns = entry.__dict__.keys(), index = [0])
		data_in = pd.DataFrame(entry.__dict__, index = [0])
		data = pd.concat([data, data_in])

		
		file = open('data.pk','wb')
		pickle.dump(data, file)
		file.close()

		file = open('data.pk', 'rb')
		obj_1 = pickle.load(file)
		with pd.option_context('display.max_rows', None, 'display.max_columns', None):
			print(obj_1)
		file.close()



	# User input, modify existing class instance
	# 
	# User input, delete existing class instance
	# 

	# See current dataframe
	with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		print(data)
	

	# data_output(data_in)


def test_dir():
	# Target path for data directory
	data = os.getcwd() + '\data'

	# Create new data folder if doesn't exist
	if not os.path.exists(data):
		os.makedirs('data')
		print("Data directory created...")
	else:
		print("Data directory found...")

def setup():
	print("Welcome to CRMv1.0.0\n" + "Today's Date: " + dd_mm_yyyy() + "\n")
	test_dir()
	
if __name__ == "__main__":
	# Run program setup
	setup()
	# Main loop
	main(load_data())