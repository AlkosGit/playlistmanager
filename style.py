from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *

class MyFrame(Frame):
    def __init__(self, parent, **config):
        Frame.__init__(self, parent, **config)
        self.config(background='#444444')

class MyMenu(Menu):
    def __init__(self, parent, **config):
        Menu.__init__(self, parent, **config)
        self.config(background='#444444', 
            foreground='white', 
            activebackground='#555555', 
            activeforeground='#FFFFFF', 
            tearoff=0)

class MyLabel(Label):
    def __init__(self, parent, **config):
        Label.__init__(self, parent, **config)
        self.config(background='#444444', 
            foreground='white')

class MyEntry(Entry):
    def __init__(self, parent, **config):
        Entry.__init__(self, parent, **config)
        self.config(background='#444444', 
            foreground='white', 
            highlightcolor='white', 
            insertbackground='white', 
            disabledbackground='#444444',
            relief='flat')

class MyCheckbutton(Checkbutton):
    def __init__(self, parent, **config):
        Checkbutton.__init__(self, parent, **config)
        self.config(activebackground='#444444',
            highlightbackground='#444444', 
            foreground='#444444', 
            background='#444444', 
            highlightcolor='white', 
            relief='flat')

class MyText(Text):
    def __init__(self, parent, **config):
        Text.__init__(self, parent, **config)
        self.config(background='#444444',
            foreground='white', 
            highlightcolor='white', 
            insertbackground='white',
            relief='flat')

class MyScrolledText(ScrolledText):
    def __init__(self, parent, **config):
        ScrolledText.__init__(self, parent, **config)
        self.config(background='#444444',
            foreground='white', 
            highlightcolor='white', 
            insertbackground='white',
            relief='flat')

class MyScrollbar(Scrollbar):
    def __init__(self, parent, **config):
        Scrollbar.__init__(self, parent, **config)
        self.config(background='#444444', 
            activebackground='#333333',
            relief='flat')

class MyButton(Button):
    def __init__(self, parent, **config):
        Button.__init__(self, parent, **config)
        self.config(background='#444444', 
            foreground='white', 
            activebackground='#333333', 
            activeforeground='white', 
            relief='flat')

class MyCombobox(ttk.Combobox):
    def __init__(self, parent, **config):
        ttk.Combobox.__init__(self, parent, **config)
        self.option_add('*TCombobox*Listbox.background', '#444444')
        self.option_add('*TCombobox*Listbox.foreground', 'white')
        self.option_add('*TCombobox*Listbox.selectbackground', '#444444')
        self.option_add('*TCombobox*Listbox.selectforeground', '#444444')
            
