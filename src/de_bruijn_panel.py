import wx


class DeBruijnPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		vbox = wx.BoxSizer(wx.VERTICAL)

		self.SetSizer(vbox)