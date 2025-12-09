# -*- coding: utf-8 -*-

#--------------------------------------------------------------------------
# Python code generated with wxFormBuilder (version 3.9.0 Jun 14 2020)
# http://www.wxformbuilder.org/
#
# PLEASE DO *NOT* EDIT THIS FILE!
#--------------------------------------------------------------------------

import wx
import wx.xrc

import gettext
_ = gettext.gettext

#--------------------------------------------------------------------------
#  Class MyFrame1
#---------------------------------------------------------------------------

class MyFrame1 ( wx.Frame ):

	def __init__(self, parent):
		wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = _(u"阅读 v0.1"), pos = wx.DefaultPosition, size = wx.Size( 1178,730 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
		self.SetBackgroundColour(wx.Colour( 239, 235, 235 ))

		self.m_menubar1 = wx.MenuBar(0)
		self.m_menu1 = wx.Menu()
		self.m_menuItem1 = wx.MenuItem(self.m_menu1, wx.ID_ANY, _(u"导入本地文件"), wx.EmptyString, wx.ITEM_NORMAL)
		self.m_menu1.Append(self.m_menuItem1)

		self.m_menubar1.Append(self.m_menu1, _(u"文件"))

		self.m_menu2 = wx.Menu()
		self.m_menuItem2 = wx.MenuItem(self.m_menu2, wx.ID_ANY, _(u"导入Reader源"), wx.EmptyString, wx.ITEM_NORMAL)
		self.m_menu2.Append(self.m_menuItem2)

		self.m_menuItem7 = wx.MenuItem(self.m_menu2, wx.ID_ANY, _(u"导入阅读源"), wx.EmptyString, wx.ITEM_NORMAL)
		self.m_menu2.Append(self.m_menuItem7)

		self.m_menuItem8 = wx.MenuItem(self.m_menu2, wx.ID_ANY, _(u"导入自定义源"), wx.EmptyString, wx.ITEM_NORMAL)
		self.m_menu2.Append(self.m_menuItem8)

		self.m_menuItem3 = wx.MenuItem(self.m_menu2, wx.ID_ANY, _(u"编辑源"), wx.EmptyString, wx.ITEM_NORMAL)
		self.m_menu2.Append(self.m_menuItem3)

		self.m_menubar1.Append(self.m_menu2, _(u"编辑"))

		self.m_menu3 = wx.Menu()
		self.m_menuItem4 = wx.MenuItem(self.m_menu3, wx.ID_ANY, _(u"检查更新"), wx.EmptyString, wx.ITEM_NORMAL)
		self.m_menu3.Append(self.m_menuItem4)

		self.m_menuItem5 = wx.MenuItem(self.m_menu3, wx.ID_ANY, _(u"关于"), wx.EmptyString, wx.ITEM_NORMAL)
		self.m_menu3.Append(self.m_menuItem5)

		self.m_menubar1.Append(self.m_menu3, _(u"设置"))

		self.m_menu4 = wx.Menu()
		self.m_menuItem6 = wx.MenuItem(self.m_menu4, wx.ID_ANY, _(u"代理设置"), wx.EmptyString, wx.ITEM_NORMAL)
		self.m_menu4.Append(self.m_menuItem6)

		self.m_menubar1.Append(self.m_menu4, _(u"工具"))

		self.m_menu5 = wx.Menu()
		self.m_menuItem9 = wx.MenuItem(self.m_menu5, wx.ID_ANY, _(u"加载Reader源"), wx.EmptyString, wx.ITEM_NORMAL)
		self.m_menu5.Append(self.m_menuItem9)

		self.m_menuItem10 = wx.MenuItem(self.m_menu5, wx.ID_ANY, _(u"加载阅读源"), wx.EmptyString, wx.ITEM_NORMAL)
		self.m_menu5.Append(self.m_menuItem10)

		self.m_menuItem11 = wx.MenuItem(self.m_menu5, wx.ID_ANY, _(u"加载自定义源"), wx.EmptyString, wx.ITEM_NORMAL)
		self.m_menu5.Append(self.m_menuItem11)

		self.m_menubar1.Append(self.m_menu5, _(u"加载"))

		self.SetMenuBar(self.m_menubar1)

		bSizer1 = wx.BoxSizer(wx.VERTICAL)

		bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer2.Add(self.m_textCtrl1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		self.m_button1 = wx.Button(self, wx.ID_ANY, _(u"搜索"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer2.Add(self.m_button1, 0, wx.ALL, 5)

		m_comboBox1Choices = []
		self.m_comboBox1 = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboBox1Choices, 0)
		bSizer2.Add(self.m_comboBox1, 0, wx.ALL, 5)


		bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)

		bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

		m_comboBox2Choices = []
		self.m_comboBox2 = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboBox2Choices, 0)
		bSizer3.Add(self.m_comboBox2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		self.m_button2 = wx.Button(self, wx.ID_ANY, _(u"下载"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer3.Add(self.m_button2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)


		bSizer1.Add(bSizer3, 0, wx.EXPAND, 5)

		bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

		m_listBox1Choices = []
		self.m_listBox1 = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox1Choices, wx.LB_SINGLE)
		bSizer4.Add(self.m_listBox1, 0, wx.ALL|wx.EXPAND, 5)

		self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_RICH2)
		bSizer4.Add(self.m_textCtrl2, 1, wx.ALL|wx.EXPAND, 5)


		bSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

		bSizer5 = wx.BoxSizer(wx.VERTICAL)

		self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText1.Wrap(-1)

		bSizer5.Add(self.m_staticText1, 1, wx.ALL|wx.ALIGN_RIGHT, 5)


		bSizer1.Add(bSizer5, 0, wx.EXPAND, 5)


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre(wx.BOTH)

		# Connect Events
		self.Bind(wx.EVT_MENU, self.Selereader, id = self.m_menuItem2.GetId())
		self.Bind(wx.EVT_MENU, self.load_reader, id = self.m_menuItem9.GetId())
		self.m_button1.Bind(wx.EVT_BUTTON, self.Search)
		self.m_comboBox1.Bind(wx.EVT_COMBOBOX, self.change_rule)
		self.m_comboBox2.Bind(wx.EVT_COMBOBOX, self.change_book)
		self.m_listBox1.Bind(wx.EVT_LISTBOX_DCLICK, self.get_content)

	def __del__( self ):
		# Disconnect Events
		self.Unbind(wx.EVT_MENU, id = self.m_menuItem2.GetId())
		self.Unbind(wx.EVT_MENU, id = self.m_menuItem9.GetId())
		self.m_button1.Unbind(wx.EVT_BUTTON, None)
		self.m_comboBox1.Unbind(wx.EVT_COMBOBOX, None)
		self.m_comboBox2.Unbind(wx.EVT_COMBOBOX, None)
		self.m_listBox1.Unbind(wx.EVT_LISTBOX_DCLICK, None)


	# Virtual event handlers, overide them in your derived class
	def Selereader( self, event ):
		event.Skip()

	def load_reader( self, event ):
		event.Skip()

	def Search( self, event ):
		event.Skip()

	def change_rule( self, event ):
		event.Skip()

	def change_book( self, event ):
		event.Skip()

	def get_content( self, event ):
		event.Skip()


