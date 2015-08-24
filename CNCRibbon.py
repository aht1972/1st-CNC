#!/usr/bin/python
# -*- coding: latin1 -*-
# $Id$
#
# Author: vvlachoudis@gmail.com
# Date: 18-Jun-2015

__author__ = "Vasilis Vlachoudis"
__email__  = "vvlachoudis@gmail.com"

try:
	from Tkinter import *
except ImportError:
	from tkinter import *

import Ribbon
import tkExtra

#===============================================================================
# Link to main app
#===============================================================================
class _LinkApp:
	def __init__(self, app):
		self.app = app

	#----------------------------------------------------------------------
	# Add a widget in the widgets list to enable disable during the run
	#----------------------------------------------------------------------
	def addWidget(self, widget):
		self.app.widgets.append(widget)

	#----------------------------------------------------------------------
	# Send a command to Grbl
	#----------------------------------------------------------------------
	def sendGrbl(self, cmd):
		self.app.sendGrbl(cmd)

	#----------------------------------------------------------------------
	# Accept the user key if not editing any text
	#----------------------------------------------------------------------
	def acceptKey(self, skipRun=False):
#		if self.getActivePage() == "Editor": return False
		if not skipRun and self.app.running: return False
		focus = self.focus_get()
		if isinstance(focus, Entry) or \
		   isinstance(focus, Spinbox) or \
		   isinstance(focus, Text): return False
		return True

#===============================================================================
# Button Group, a group of widgets that will be placed in the ribbon
#===============================================================================
class ButtonGroup(Ribbon.LabelGroup, _LinkApp):
	def __init__(self, master, name, app):
		Ribbon.LabelGroup.__init__(self, master, name)
		_LinkApp.__init__(self, app)

#===============================================================================
# Button Group, a group of widgets that will be placed in the ribbon
#===============================================================================
class ButtonMenuGroup(Ribbon.MenuGroup, _LinkApp):
	def __init__(self, master, name, app):
		Ribbon.MenuGroup.__init__(self, master, name)
		_LinkApp.__init__(self, app)

#===============================================================================
# Page, Frame
#===============================================================================
class PageFrame(Frame, _LinkApp):
	def __init__(self, master, name, app):
		Frame.__init__(self, master)
		_LinkApp.__init__(self, app)
		self.name = name

#===============================================================================
# Page, LabelFrame
#===============================================================================
class PageLabelFrame(LabelFrame, _LinkApp):
	def __init__(self, master, name, app):
		LabelFrame.__init__(self, master, text=name, foreground="DarkBlue")
		_LinkApp.__init__(self, app)
		self.name = name

#===============================================================================
# Page, ExLabelFrame
#===============================================================================
class PageExLabelFrame(tkExtra.ExLabelFrame, _LinkApp):
	def __init__(self, master, name, app):
		tkExtra.ExLabelFrame.__init__(self, master, text=name, foreground="DarkBlue")
		_LinkApp.__init__(self, app)
		self.name = name

#===============================================================================
# CNC Page interface between the basic Page class and the bCNC class
#===============================================================================
class Page(Ribbon.Page):
	groups = {}
	frames = {}

	def __init__(self, master, app, **kw):
		self.app = app
		Ribbon.Page.__init__(self, master, **kw)
		self.register()

	#----------------------------------------------------------------------
	# Should be overridden with the groups and frames to register
	#----------------------------------------------------------------------
	def register(self):
		pass

	#----------------------------------------------------------------------
	# Register groups
	#----------------------------------------------------------------------
	def _register(self, groups, frames):
		if groups:
			for g in groups:
				w = g(self.master._ribbonFrame, self.app)
				Page.groups[w.name] = w

		if frames:
			for f in frames:
				w = f(self.master._pageFrame, self.app)
				Page.frames[w.name] = w

	#----------------------------------------------------------------------
	# Add a widget in the widgets list to enable disable during the run
	#----------------------------------------------------------------------
	def addWidget(self, widget):
		self.app.widgets.append(widget)

	#----------------------------------------------------------------------
	# Send a command to Grbl
	#----------------------------------------------------------------------
	def sendGrbl(self, cmd):
		self.app.sendGrbl(cmd)

	#----------------------------------------------------------------------
	def addRibbonGroup(self, name, **args):
		if not args: args = {"side":LEFT, "fill":BOTH}
		self.ribbons.append((Page.groups[name], args))

	#----------------------------------------------------------------------
	def addPageFrame(self, name, **args):
		if not args: args = {"side":TOP, "fill":BOTH}
		if isinstance(name,str):
			self.frames.append((Page.frames[name], args))
		else:
			self.frames.append((name, args))