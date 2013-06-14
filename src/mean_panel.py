import wx
import mean_frame
import lloyd

class MeanPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        left_vbox = wx.BoxSizer(wx.VERTICAL)
        right_vbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(left_vbox, 0, wx.EXPAND)
        hbox.Add(right_vbox, 1, wx.EXPAND)

        k_box = wx.StaticBoxSizer(wx.StaticBox(self, label="k-Value"), wx.VERTICAL)
        self.k_static_txt = wx.StaticText(self, label='k:')
        self.k_txt_ctrl = wx.TextCtrl(self, size=(200, -1))

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.k_static_txt, flag=wx.LEFT, border=0)
        hbox1.Add(self.k_txt_ctrl, flag=wx.LEFT, border=5)

        k_box.Add(hbox1, 0, wx.ALL, 2)

        left_vbox.Add(k_box, 0, wx.ALL | wx.EXPAND, 3)

        list_box = wx.StaticBoxSizer(wx.StaticBox(self, label="Points"), wx.VERTICAL)
        self.list_ctrl = wx.ListCtrl(self, size=(400,400), style=wx.LC_REPORT | wx.BORDER_SUNKEN)

        self.list_ctrl.InsertColumn(0, 'x-value', width=190)
        self.list_ctrl.InsertColumn(1, 'y-value', width=190)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.point_delete_btn = wx.Button(self, label='Remove Points')
        self.point_delete_btn.Bind(wx.EVT_BUTTON, self.pointDelete)
        self.point_clear_btn = wx.Button(self, label='Clear')
        self.point_clear_btn.Bind(wx.EVT_BUTTON, self.pointClear)

        hbox2.Add(self.point_delete_btn, 0)
        hbox2.AddSpacer(5)
        hbox2.Add(self.point_clear_btn, 0)

        hbox3= wx.BoxSizer(wx.HORIZONTAL)

        x_static_txt = wx.StaticText(self, label='x Value:')
        self.x_txt_ctrl = wx.TextCtrl(self, size=(30, -1))
        y_static_txt = wx.StaticText(self, label='y Value:')
        self.y_txt_ctrl = wx.TextCtrl(self, size=(30, -1))
        self.point_add_btn = wx.Button(self, label='Add Keyword')
        self.point_add_btn.Bind(wx.EVT_BUTTON, self.addPoint)

        hbox3.Add(x_static_txt, 0)
        hbox3.AddSpacer(5)
        hbox3.Add(self.x_txt_ctrl, 0)
        
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(y_static_txt, 0)
        hbox4.AddSpacer(5)
        hbox4.Add(self.y_txt_ctrl, 0)

        list_box.Add(self.list_ctrl, 1, wx.EXPAND)
        list_box.AddSpacer(10)
        list_box.Add(hbox2, 0)
        list_box.AddSpacer(5)
        list_box.Add(hbox3, 0)
        list_box.AddSpacer(5)
        list_box.Add(hbox4, 0)
        list_box.AddSpacer(5)
        list_box.Add(self.point_add_btn)


        right_vbox.Add(list_box, 1, wx.EXPAND)

        bottom_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.back_btn = wx.Button(self, label='Back')
        self.back_btn.Bind(wx.EVT_BUTTON, self.GetParent().toMenu)
        self.visualize_btn = wx.Button(self, label = 'Visualize')
        self.visualize_btn.Bind(wx.EVT_BUTTON, self.visualize)
        bottom_hbox.Add(self.back_btn, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM)
        bottom_hbox.AddStretchSpacer()
        bottom_hbox.Add(self.visualize_btn, 0, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)
        vbox.Add(hbox, 0)
        vbox.Add(bottom_hbox, 1, wx.ALIGN_BOTTOM | wx.EXPAND | wx.ALL, 10)

        self.SetSizer(vbox)

        self.Layout()

    def pointDelete(self, event):
        current_item = self.list_ctrl.GetNextSelected(-1)
        while current_item >= 0:
            self.list_ctrl.DeleteItem(current_item)
            current_item = self.list_ctrl.GetNextSelected(-1)

    def pointClear(self, event):
        self.list_ctrl.DeleteAllItems()

    def addPoint(self, event):
        x = self.x_txt_ctrl.GetValue()
        y = self.y_txt_ctrl.GetValue()
        try:
            float(x)
        except ValueError:
            dlg = wx.MessageDialog(self, 'x-value must be an floating point number.', 'Invalid x-value', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return
        try:
            float(y)
        except ValueError:
            dlg = wx.MessageDialog(self, 'y-value must be an floating point number.', 'Invalid y-value', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        self.list_ctrl.Append([x,y])

    def visualize(self, event):
        k = self.k_txt_ctrl.GetValue()
        try:
            k = int(k)
        except ValueError:
            dlg = wx.MessageDialog(self, 'k must be an integer.', 'Invalid k', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        points = list()
        for i in range(self.list_ctrl.GetItemCount()):
            x = float(self.list_ctrl.GetItem(i, 0).GetText())
            y = float(self.list_ctrl.GetItem(i, 1).GetText())
            points.append((x,y))
        if not points:
            dlg = wx.MessageDialog(self, 'No points were found.', 'No Points', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        m_frame = mean_frame.MeanFrame(self, k, points)

