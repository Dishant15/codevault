from Tkinter import *
import os, datetime
import json

dirpath = os.path.dirname(__file__)
data_folder = 'data'
datapath = dirpath + data_folder + '/'

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
	appStarter = SaveCode()