"""
#
# File : CODEVAULT PY
# @author : Dishant Chavda
# date : 11-01-2016
#
"""

from Tkinter import *
import os, datetime
import json, difflib, tkMessageBox

from entry_auto_complete import AutocompleteEntry

dirpath = os.path.dirname(__file__)
data_folder = 'data'
datapath = dirpath + data_folder + '/'

# Variable used to takle first time save of code snippet
no_data_yet = False
# Main utility is for updating language options on search window when
# new language code is saved from save window
main_window = None

def get_languages_from_files():
	"""
	Used to fill options menu with languages
	"""
	datafile_names = os.listdir(datapath)
	clean_names = []
	for filename in datafile_names:
		if filename.endswith('.json'):
			clean_names.append(filename[:-5])
	return clean_names

language_list = []

class SearchCode(object):
	"""
	window to search all the existing json files
	"""

	def __init__(self, master):
		global no_data_yet, language_list, main_window

		main_window = self

		self.search_window = master
		self.search_window.title("Get Your Code | Code Vault")

		# Set up dropdown menu to choose from language available
		self.language = StringVar(self.search_window)   # variable to save the state of option menu for languages
		try:
			self.language.set(language_list[0]) # default value
		except Exception, e:
			# Redirect to save new code page
			no_data_yet = True   # This is a first time code save event
			SaveCode(master)
			# When language list is empty and no search data is found
			# Go to the savecode page with master argument
			return

		self.row1 = Frame(self.search_window, pady=15)
		self.row1.pack()

		self.language_lab = Label(self.row1, text='Language : ')
		self.language_lab.pack(side='left')
		self.language_ent = OptionMenu(self.row1, self.language, *language_list)
		self.language_ent.pack(side='left')


		self.title_lab = Label(self.row1, text='Title : ', padx=15)
		self.title_lab.pack(side='left')
		self.title_ent = Entry(self.row1, width = 30 )
		self.title_ent.pack(side='left')

		self.tag_frame = Frame(self.search_window, pady=15,padx=15)
		self.tag_frame.pack()

		self.tags_lab = Label(self.tag_frame, text='Tags : ')
		self.tags_lab.pack(side='left')
		self.tags_ent = Entry(self.tag_frame, width = 50 )
		self.tags_ent.pack(side='left')

		self.row2 = Frame(self.search_window, pady=15,padx=15)
		self.row2.pack()

		self.show_all_bu = Button(self.row2, text="Show All Codes",command=self.show_all_code)
		self.show_all_bu.pack(side="left")

		self.search_bu = Button(self.row2, text="Search",command=self.search_code)
		self.search_bu.pack(side="left")

		self.cancel_bu = Button(self.row2, text="Clear",command=self.clear_all_widgets)
		self.cancel_bu.pack(side="left")

		self.row3 = Frame(self.search_window)
		self.row3.pack()

		self.result_box = Listbox(self.row3, width=60)

		self.bot = Frame(self.search_window, pady=15,padx=15)
		self.bot.pack(side="bottom")

		self.quit = Button(self.bot, text="Quit", padx=10, pady=20,width=15,command=self.search_window.destroy)
		self.quit.pack(side='left')
		self.add_code = Button(self.bot, text="Save New Code", padx=10, pady=20,width=15,command=lambda:SaveCode())
		self.add_code.pack(side="left")

		self.search_window.geometry("900x600")
		self.search_window.mainloop()


	def get_file_data(self):
		"""
		Get json data from a file

		Takes language input from language entry widget and
		opens appropreate language file. Returns language data
		as a dictionary
		"""
		filepath = datapath + self.language.get() + ".json"
		try:
			with open( filepath ) as data_file:
				data = json.load( data_file )
		except Exception, e:
			data = []
		return data

	def show_all_code(self):
		self.result_box.delete(0, END)
		# Show this data on a clickable format
		if not self.result_box.winfo_manager():
			self.result_box.pack()

		self.data = self.get_file_data()

		self.search_data = self.data
		
		for data_fragment in self.search_data:
			tag_str = '] ['.join([ x.title() for x in data_fragment['tags'] ])
			self.result_box.insert(END, data_fragment['title'].title() + " : [" + tag_str + "]")

		self.result_box.bind("<Double-Button-1>", self.open_search_item)

	def search_code(self):
		"""
		Function called by search Button

		Takes input from title entry widget and compares it with
		all titles available in data file of that language
		shows all data that match nearly 45% and show it on a list box
		"""
		title = self.title_ent.get()
		tags = [ x.strip().lower() for x in self.tags_ent.get().split(',') ]
		self.data = self.get_file_data()
		tags_search_data = []
		title_search_data = []

		if title == "" and tags == [""]:
			tkMessageBox.showerror("Data input error", "To search from the code vault please enter TAGS or TITLE that you need to search")
			return

		if tags != [""]:
			# tags are added as search parameters
			for snippet in self.data:
				for each_tag in tags:
					if each_tag in snippet['tags']:
						tags_search_data.append(snippet)
						break

		if title != "":
			# compare title of code snippets and get matching
			compare = difflib.SequenceMatcher()
			compare.set_seq1(title.lower())
			if tags_search_data != []:
				# search only in data found with tag matching
				self.data = tags_search_data
			for snippet in self.data:
				compare.set_seq2(snippet['title'].lower())
				rate = compare.ratio()
				if rate > 0.45:
					title_search_data.append(snippet)
		
		self.result_box.delete(0, END)
		# Show this data on a clickable format
		if not self.result_box.winfo_manager():
			self.result_box.pack()

		if title_search_data != []:
			self.search_data = title_search_data
		else:
			self.search_data = tags_search_data + title_search_data
		
		for data_fragment in self.search_data:
			tag_str = '] ['.join([ x.title() for x in data_fragment['tags'] ])
			self.result_box.insert(END, data_fragment['title'].title() + " : [" + tag_str + "]")

		self.result_box.bind("<Double-Button-1>", self.open_search_item)

	def highlight_keywords(self, widget):
		import keyword

		widget.tag_configure("keywords", foreground="yellow")

		kw_list = keyword.kwlist
		for kws in kw_list:
			index = widget.search(kws,"1.0", stopindex="end")
			if index != "":
				widget.tag_add("keywords", index, "%s+%dc" %(index,len(kws)))


	def open_search_item(self, event):
		"""
		Function called on double click to an item on list box

		gets preciese data that was clicked and shows it
		on a new Toplevel window, that has facility to copy codes
		on Button click
		"""
		# get index of the element that was clicked
		try:
			clicked_on = self.result_box.curselection()[0]
		except Exception, e:
			tkMessageBox.showerror("Data input error", "No code snippet found")
			return
		
		selected = self.search_data[clicked_on]
		# selected containes the data to be shown
		# Show it in another top level window
		self.top = Toplevel()
		self.top.title(selected['title'])

		top_frame = Frame(self.top)
		top_frame.pack()

		code_lab = Label( top_frame, text='Code : ', pady=10)
		code_lab.pack(side='top')
		code_box = Text( top_frame, width=120, height=10, background="#555555", foreground="white", wrap = "word", pady=10, padx=5 )
		code_box.pack(side='top')
		code_box.insert(0.0, selected['code'])

		# self.highlight_keywords(code_box)

		code_bu = Button(top_frame, text='Copy Code',padx=10, pady=20,width=15, command=lambda:self.copy_to_clipboard(selected['code']))
		code_bu.pack(side='top')

		example_lab = Label( top_frame, text='Example Code : ', pady=10)
		example_lab.pack(side='top')
		example_ent = Text( top_frame, width=120, height=10, background="#555555", foreground="white", wrap = "word", pady=10, padx=5 )
		example_ent.pack(side='top')
		example_ent.insert(0.0, selected['example'])

		example_bu = Button(top_frame, text='Copy Example Code',padx=10, pady=20,width=15, command=lambda:self.copy_to_clipboard(selected['example']))
		example_bu.pack(side='top')

		bot_frame = Frame(self.top)
		bot_frame.pack()

		save_change = Button(bot_frame, text="Save Changes", padx=10, pady=20,width=15,command=lambda:self.update_data(selected,code_box,example_ent))
		save_change.pack(side='left')

		quit = Button(bot_frame, text="Close", padx=10, pady=20,width=15,command=self.top.destroy)
		quit.pack(side='left')

		self.top.geometry("900x600")

	def update_data(self,old_data,code_box,example_ent):
		filepath = datapath + self.language.get() + ".json"
		try:
			self.data.remove( old_data )
		except Exception, e:
			# Raised due to 2 reasons
			# 1 - File do not exist and no data
			# 2 - old_data is not in data
			pass

		new_data = {
			'title' : old_data['title'],
			'tags' : old_data['tags'],
			"code" : code_box.get(0.0,END),
			"example" : example_ent.get(0.0,END),
		}
		
		if new_data not in self.data:
			self.data.append( new_data )
		# write new updated data back to the file
		try:
			jsonfile = open( filepath, 'w' )
			jsonfile.write( json.dumps( self.data, indent = 4 ) )
			jsonfile.close()
		except Exception, e:
			print e
		self.top.destroy()
		self.clear_all_widgets()


	def copy_to_clipboard(self,data):
		self.search_window.clipboard_clear()
		self.search_window.clipboard_append(data)

	def clear_all_widgets(self):
		self.title_ent.delete(0,END)
		self.tags_ent.delete(0,END)
		self.result_box.pack_forget()

	def refresh_languages(self):
		global language_list
		import Tkinter as tk

		# clear all current options from options menu
		self.language_ent['menu'].delete(0, 'end')
		# Insert list of new options (tk._setit hooks them up to var)
		for lang in language_list:
			self.language_ent['menu'].add_command(label=lang, command=tk._setit(self.language, lang))

		

class SaveCode(object):
	"""
	Create a new window to save new code snippet
	"""

	# appHighlightFont = font.Font(family='Helvetica', size=12, weight='bold')

	def __init__(self, master=None):
		import ttk

		if master:
			self.save_window = master
		else:
			self.save_window = Toplevel()

		self.save_window.title("Save Your Code | Code Vault")


		# First row that containes language and title boxes
		self.row1 = Frame(self.save_window, pady=15)
		self.row1.pack()

		self.language_lab = Label(self.row1, text='Language : ')
		self.language_lab.pack(side='left')
		# self.language_ent = AutocompleteEntry(language_list, self.row1)
		self.language_ent = ttk.Combobox(self.row1, width = 10 )
		self.language_ent.pack(side='left')
		self.language_ent['values'] = language_list

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

		self.save_but = Button(self.row4, text='Save To Vault',padx=10, pady=20,width=15, command=self.save_code)
		self.save_but.pack(side='left')

		self.cancel_but = Button(self.row4, text='Cancel',padx=10, pady=20,width=15, command=self.clear_all_widgets)
		self.cancel_but.pack(side='left')

		if not no_data_yet:
			# Don't show the button to go to the search window when there is no data to search
			self.search_but = Button(self.save_window, text='Search Vault',padx=10, pady=20,width=15, command=self.open_search_window)
			self.search_but.pack(side='bottom')

		self.quit = Button(self.row4, text="Quit", padx=10, pady=20,width=15,command=self.save_window.destroy)
		self.quit.pack(side='bottom')
		
		self.save_window.geometry("900x650")

		if master:
			# Main loop of master will run from this window only when first time code
			# creation is done and master argument is handeled by this window
			self.save_window.mainloop()


	def save_code(self):
		global no_data_yet,language_list, main_window

		language = self.language_ent.get()
		if language == "":
			tkMessageBox.showerror("Data input error", "Enter language name of the code snippet")
			return

		title = self.title_ent.get()
		if title == "":
			tkMessageBox.showerror("Data input error", "Enter Title of the code snippet which will be used to search it in the future.")
			return

		filepath = datapath + language + ".json"
		# read data from file if available
		try:
			with open( filepath ) as data_file:
				data = json.load( data_file )
		except Exception, e:
			data = []
		# Add current data to existing data

		tags = [ x.strip().lower() for x in self.tags_ent.get().split(',') ]
		# Check for required and empty fields ------------------
		new_data = {
			'title' : title,
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

		# import pdb; pdb.set_trace()
		if no_data_yet:
			# First time data saved , enable search button now
			no_data_yet = False
			self.search_but = Button(self.save_window, text='Search Vault',padx=10, pady=20,width=15, command=self.open_search_window)
			self.search_but.pack(side="bottom")
			language_list.append(language)
			self.language_ent['values'] = language_list
		else:
			# Refresh options menu in search window if code for new language added
			if language not in language_list:
				language_list.append(language)
				self.language_ent['values'] = language_list
				main_window.refresh_languages()

		self.clear_all_widgets()

	def open_search_window(self):
		self.save_window.destroy()
		root = Tk()
		SearchCode(root)


	def clear_all_widgets(self):
		# clear all widgets and make them ready for new entry
		self.code_box.delete(0.0, END)
		self.example_ent.delete(0.0, END)
		self.language_ent.delete(0, END)
		self.title_ent.delete(0, END)
		self.tags_ent.delete(0, END)


if __name__ == '__main__':
	global language_list

	if not os.path.exists(datapath):
		# Create new data directory if it does not exist
		os.makedirs(datapath)
	else:
		language_list = get_languages_from_files()

	root = Tk()
	SearchCode(root)

