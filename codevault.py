"""
Next to- dos:

	- Check for list box multiple select option
	  Add utility that user can select multiple search results and open all of them with same event bind
	- Design finale flow of the application
	- Add security and robustness of the input widgets
"""

from Tkinter import *
import os, datetime
import json, difflib, tkMessageBox

dirpath = os.path.dirname(__file__)
data_folder = 'data'
datapath = dirpath + data_folder + '/'

class SearchCode(object):
	"""
	window to search all the existing json files
	"""

	def __init__(self):
		self.search_window = Tk()
		self.search_window.title("Get Your Code | Code Vault")

		self.row1 = Frame(self.search_window, pady=15)
		self.row1.pack()

		# Set up dropdown menu to choose from language available
		language_list = self.get_languages_from_files()
		self.languages = StringVar(self.search_window)
		try:
			self.languages.set(language_list[0]) # default value
		except Exception, e:
			# Redirect to save new code page
			# ----- Do something to kill this page
			SaveCode()
			# When language list is empty and no search data is found
			# Show a tkinter msg box about no data found
			tkMessageBox.showerror("No previous data found", "No previously saved code data found. Please save some code snippets First.")

		self.language_lab = Label(self.row1, text='Language : ')
		self.language_lab.pack(side='left')
		self.language_ent = OptionMenu(self.row1, self.languages, *language_list)
		self.language_ent.pack(side='left')


		self.title_lab = Label(self.row1, text='Title : ', padx=15)
		self.title_lab.pack(side='left')
		self.title_ent = Entry(self.row1, width = 30 )
		self.title_ent.pack(side='left')

		self.row2 = Frame(self.search_window, pady=15,padx=15)
		self.row2.pack()

		self.search_bu = Button(self.row2, text="Search",command=self.search_code)
		self.search_bu.pack(side="left")
		self.cancel_bu = Button(self.row2, text="Cancel",command=self.search_code)
		self.cancel_bu.pack(side="left")

		self.row3 = Frame(self.search_window)
		self.row3.pack()

		self.result_box = Listbox(self.row3, width=60)

		self.search_window.geometry("900x600")
		self.search_window.mainloop()

	def get_languages_from_files(self):
		"""
		Used to fill options menu with languages
		"""
		datafile_names = os.listdir(datapath)
		clean_names = []
		for filename in datafile_names:
			if filename.endswith('.json'):
				clean_names.append(filename[:-5])
		return clean_names


	def get_file_data(self):
		"""
		Get json data from a file

		Takes language input from language entry widget and
		opens appropreate language file. Returns language data
		as a dictionary
		"""
		filepath = datapath + self.languages.get() + ".json"
		try:
			with open( filepath ) as data_file:
				data = json.load( data_file )
		except Exception, e:
			data = []
		return data

	def search_code(self):
		"""
		Function called by search Button

		Takes input from title entry widget and compares it with
		all titles available in data file of that language
		shows all data that match nearly 45% and show it on a list box
		"""
		title = self.title_ent.get()
		data = self.get_file_data()
		self.search_data = []
		self.result_box.delete(0, END)

		compare = difflib.SequenceMatcher()
		compare.set_seq1(title)

		for snippet in data:
			compare.set_seq2(snippet['title'])
			rate = compare.ratio()
			if rate > 0.45:
				self.search_data.append(snippet)
		# import pdb; pdb.set_trace()
		# Show this data on a clickable format
		if not self.result_box.winfo_manager():
			self.result_box.pack()
		
		for data_fragment in self.search_data:
			self.result_box.insert(END, data_fragment['title'])

		self.result_box.bind("<Double-Button-1>", self.open_search_item)

	def open_search_item(self, event):
		"""
		Function called on double click to an item on list box

		gets preciese data that was clicked and shows it
		on a new Toplevel window, that has facility to copy codes
		on Button click
		"""
		# get index of the element that was clicked
		clicked_on = self.result_box.curselection()[0]
		selected = self.search_data[clicked_on]
		# selected containes the data to be shown
		# Show it in another top level window
		self.top = Toplevel(height=200, width=150)
		self.top.title(selected['title'])

		top_frame = Frame(self.top)
		top_frame.pack()

		code_lab = Label( top_frame, text='Code : ', pady=10)
		code_lab.pack(side='top')
		code_box = Text( top_frame, width=120, height=10, background="#555555", foreground="white", wrap = "word", pady=10, padx=5 )
		code_box.pack(side='top')
		code_box.insert(0.0, selected['code'])

		code_bu = Button(top_frame, text='Copy Code',padx=10, pady=20,width=15, command=lambda:self.copy_to_clipboard(selected['code']))
		code_bu.pack(side='top')

		example_lab = Label( top_frame, text='Example Code : ', pady=10)
		example_lab.pack(side='top')
		example_ent = Text( top_frame, width=120, height=10, background="#555555", foreground="white", wrap = "word", pady=10, padx=5 )
		example_ent.pack(side='top')
		example_ent.insert(0.0, selected['example'])

		example_bu = Button(top_frame, text='Copy Example Code',padx=10, pady=20,width=15, command=lambda:self.copy_to_clipboard(selected['example']))
		example_bu.pack(side='top')

	def copy_to_clipboard(self,data):
		self.search_window.clipboard_clear()
		self.search_window.clipboard_append(data)

		

class SaveCode(object):
	"""
	Create a new window to save new code snippet
	"""

	# appHighlightFont = font.Font(family='Helvetica', size=12, weight='bold')

	def __init__(self):
		self.save_window = Tk()
		self.save_window.title("Save Your Code | Code Vault")


		# First row that containes language and title boxes
		self.row1 = Frame(self.save_window, pady=15)
		self.row1.pack()

		self.language_lab = Label(self.row1, text='Language : ')
		self.language_lab.pack(side='left')
		self.language_ent = Entry(self.row1, width = 10 )
		self.language_ent.pack(side='left')

		self.title_lab = Label(self.row1, text='Title : ')
		self.title_lab.pack(side='left')
		self.title_ent = Entry(self.row1, width = 30 )
		self.title_ent.pack(side='left')

		# Second row with tags information
		self.row2 = Frame(self.save_window)
		self.row2.pack()

		self.tags_lab = Label(self.row2, text='Tags : ')
		self.tags_lab.pack(side='left')
		self.tags_ent = Entry(self.row2, width = 50 )
		self.tags_ent.pack(side='left')

		# Third box frame for code text box
		self.row3 = Frame(self.save_window)
		self.row3.pack()

		self.code_lab = Label(self.row3, text='Enter Your Code : ', pady=10)
		self.code_lab.pack(side='top')
		self.code_box = Text( self.row3, width=120, height=10, background="#555555", foreground="white", wrap = "word", pady=10, padx=5 )
		self.code_box.pack(side='top')

		self.example_lab = Label(self.row3, text='Example Code : ', pady=10)
		self.example_lab.pack(side='top')
		self.example_ent = Text( self.row3, width=120, height=10, background="#555555", foreground="white", wrap = "word", pady=10, padx=5 )
		self.example_ent.pack(side='top')

		# row 4 for buttons
		self.row4 = Frame(self.save_window)
		self.row4.pack()

		self.save_but = Button(self.row4, text='Save',padx=10, pady=20,width=15, command=self.save_code)
		self.save_but.pack(side='left')

		self.save_but = Button(self.row4, text='Cancel',padx=10, pady=20,width=15, command=self.clear_all_widgets)
		self.save_but.pack(side='left')
		
		self.save_window.geometry("900x600")

		self.save_window.mainloop()


	def save_code(self):
		filepath = datapath + self.language_ent.get() + ".json"
		# read data from file if available
		try:
			with open( filepath ) as data_file:
				data = json.load( data_file )
		except Exception, e:
			data = []
		# Add current data to existing data

		tags = self.tags_ent.get().split(',')  # Remove white space from tags --------------
		# Check for required and empty fields ------------------
		new_data = {
			'title' : self.title_ent.get(),
			'tags' : tags,
			"code" : self.code_box.get(0.0,END),
			"example" : self.example_ent.get(0.0,END),
		}
		data.append(new_data)
		# write new updated data back to the file
		try:
			jsonfile = open( filepath, 'w' )
			jsonfile.write( json.dumps( data, indent = 4 ) )
			jsonfile.close()
		except Exception, e:
			print e

		self.clear_all_widgets()


	def clear_all_widgets(self):
		# clear all widgets and make them ready for new entry
		self.code_box.delete(0.0, END)
		self.example_ent.delete(0.0, END)
		self.language_ent.delete(0, END)
		self.title_ent.delete(0, END)
		self.tags_ent.delete(0, END)


if __name__ == '__main__':
	appStarter = SearchCode()



