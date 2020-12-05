from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv
import sys

__version__ = '0.1.2'

def parse_cvs(file, sep=','):
    with open(file) as f:
        data = list(csv.reader(f, delimiter=sep))

    return data

class Table(Frame):
	def __init__(self, parent=None, data=[]):
		assert len(data) > 1

		super().__init__(parent)

		table = ttk.Treeview(self, show="headings", selectmode="browse")
		table["columns"] = tuple(['No.'] + data[0])
		table["displaycolumns"] = tuple(['No.'] + data[0])
		table.column('No.', width=45)

		for head in tuple(['No.'] + data[0]):
			table.heading(head, text=head, anchor=CENTER)
			table.column(head, anchor=CENTER)

		for row in range(len(data[1:])):
			table.insert('', END, values=tuple([row+1] + data[row+1]))

		scrolltabley = ttk.Scrollbar(self, command=table.yview, orient=VERTICAL)
		table.configure(yscrollcommand=scrolltabley.set)
		scrolltabley.pack(fill=Y, side=RIGHT)

		table.pack(expand=YES, fill=BOTH)

		scrolltablex = ttk.Scrollbar(self, command=table.xview, orient=HORIZONTAL)
		table.configure(xscrollcommand=scrolltablex.set)
		scrolltablex.pack(fill=X)

class OpenFileWindow(Toplevel):
	def __init__(self, parent):
		super().__init__()

		self.geometry('+100+100')
		self.title('Open')
		self.resizable(False, False)
		self.transient(parent)
		self.grab_set()
		self.focus_set()

		self.parent = parent
		self.create_widgets()

	def clear(self):
		for widget in self.parent.slaves():
			widget.destroy()

	def overviewer(self):
		file = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
		self.path.delete(0, END)
		self.path.insert(0, file.replace('/', '\\'))

	def open_file(self):
		try:
			table = Table(self.parent, parse_cvs(self.path.get(), sep=self.split.get()))
		except TypeError:
			messagebox.showerror('Error!', 'Invalid separator')
		except FileNotFoundError:
			messagebox.showerror('Error!', 'File not found')
		except OSError:
			messagebox.showerror('Error!', 'Wrong way')
		except AssertionError:
			messagebox.showerror('Error!', 'Empty file')
		except Exception as ex:
			messagebox.showerror('Error!', ex)
		else:
			self.clear()
			table.pack(fill=BOTH, expand=1)
			self.destroy()

	def create_widgets(self):
		ttk.Label(self, text='Way:').grid(row=0, column=0, padx=5, pady=5, sticky=W)

		self.path = ttk.Entry(self, width=40)
		self.path.grid(row=0, column=1, padx=5, pady=5, columnspan=4)

		ttk.Button(self, text='Overview', command=self.overviewer).grid(row=0, column=6, padx=5, pady=5)
		ttk.Label(self, text='Separator:').grid(row=1, column=0, padx=5, pady=5, sticky=W)

		self.split = ttk.Entry(self, width=10)
		self.split.grid(row=1, column=1, padx=5, pady=5, sticky=W)
		self.split.insert(0, ',')

		ttk.Button(self, text='Open', command=self.open_file).grid(row=2, column=0, padx=5, pady=5)
		ttk.Button(self, text='Cancel', command=self.destroy).grid(row=2, column=1, padx=5, pady=5)

class AboutWindow(Toplevel):
	def __init__(self, parent):
		super().__init__()

		self.geometry('+100+100')
		self.title('About')
		self.resizable(False, False)
		self.transient(parent)
		self.grab_set()
		self.focus_set()

		self.create_widgets()

	def create_widgets(self):
		ttk.Label(self, text='CSV Viewer v%s' % __version__).pack()
		ttk.Label(self, text='Author: Ku6iK_Ru6Ika').pack()
		ttk.Label(self, text='Telegram: https://t.me/ku6ik_ru6ika').pack()

class Application(Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.menu = Menu(self.master) 
		self.master.config(menu=self.menu)

		self.file_menu = Menu(self.menu, tearoff=0)
		self.file_menu.add_command(label="Open", command=lambda: OpenFileWindow(self.master))
		self.file_menu.add_command(label="Exit", command=self.master.destroy)

		self.about_menu = Menu(self.menu, tearoff=0)
		self.about_menu.add_command(label="About the program", command=lambda: AboutWindow(self.master))

		self.menu.add_cascade(label="File", menu=self.file_menu)
		self.menu.add_cascade(label="Reference", menu=self.about_menu)

		if len(sys.argv) > 1:
			try:
				self.table = Table(self.master, parse_cvs(sys.argv[1]))
				self.table.pack(fill=BOTH, expand=1)
			except AssertionError:
				messagebox.showerror('Error!', 'Empty file')
				ttk.Label(text='Open CSV file').pack()
		else:
			ttk.Label(text='Open CSV file').pack()

if __name__ == '__main__':
	root = Tk()
	root.title('CSV Viewer')

	root.minsize(400, 300)
	root.maxsize(1200, 500)
	app = Application(master=root)
	app.mainloop()
