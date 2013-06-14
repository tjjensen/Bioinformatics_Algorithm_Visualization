#!/usr/bin/python
# -*- coding: utf-8 -*- 

import wx
import seq_panel
import de_bruijn_panel
import keyword_panel
import flow_panel
import mean_panel

class VizFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,700))
        
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        menu_item = fileMenu.Append(wx.ID_ANY, 'Main Menu')
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')

        menubar.Append(fileMenu, '&File')

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.toMenu, menu_item)
        self.Bind(wx.EVT_MENU, self.onQuit, fitem)


        self.menu_panel = MenuPanel(self)
        self.nw_panel = seq_panel.NeedlemanWunshPanel(self)
        self.keyword_panel = keyword_panel.KeywordPanel(self)
        self.flow_panel = flow_panel.FlowPanel(self)
        self.mean_panel = mean_panel.MeanPanel(self)
        self.nw_panel.Hide()
        self.keyword_panel.Hide()
        self.flow_panel.Hide()
        self.mean_panel.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.menu_panel, 1, wx.EXPAND)
        self.sizer.Add(self.nw_panel, 1, wx.EXPAND)
        self.sizer.Add(self.keyword_panel, 1, wx.EXPAND)
        self.sizer.Add(self.flow_panel, 1, wx.EXPAND)
        self.sizer.Add(self.mean_panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.current_panel = self.menu_panel
        self.Center()
        self.Show(True)

    def toMenu(self, event):
        self.current_panel.Hide()
        self.current_panel = self.menu_panel
        self.current_panel.Show()
        self.Layout()        


    def toNeedlemanWunsh(self, event):
        self.current_panel.Hide()
        self.current_panel = self.nw_panel
        self.current_panel.Show()
        self.Layout()

    def toKeyword(self, event):
        self.current_panel.Hide()
        self.current_panel = self.keyword_panel
        self.current_panel.Show()
        self.Layout()

    def toFlow(self, event):
        self.current_panel.Hide()
        self.current_panel = self.flow_panel
        self.current_panel.Show()
        self.Layout()

    def toMean(self, event):
        self.current_panel.Hide()
        self.current_panel = self.mean_panel
        self.current_panel.Show()
        self.Layout()

    def onQuit(self, event):
        self.Close()

class MenuPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        title_txt = wx.StaticText(self, label='Bioinformatics Algorithm Visualization')
        title_txt.SetFont(wx.Font(28, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL))

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        lvbox1 = wx.BoxSizer(wx.VERTICAL)
        rvbox1 = wx.BoxSizer(wx.VERTICAL)

        seq_path = './../pics/seq.png'
        seq_img = wx.Image(seq_path, wx.BITMAP_TYPE_ANY).Scale(200,200, wx.IMAGE_QUALITY_HIGH)
        seq_img = seq_img.ConvertToBitmap()
        seq_bm = wx.StaticBitmap(self, bitmap=seq_img)
        self.seq_btn = wx.Button(self, label='Sequence Algorithms')
        self.seq_btn.Bind(wx.EVT_BUTTON, parent.toNeedlemanWunsh)

        lvbox1.Add(seq_bm, 0)
        lvbox1.Add(self.seq_btn, 0, wx.ALIGN_CENTRE | wx.ALL, 4)

        flow_path = './../pics/flow.png'
        flow_img = wx.Image(flow_path, wx.BITMAP_TYPE_ANY).Scale(200,200, wx.IMAGE_QUALITY_HIGH)
        flow_img = flow_img.ConvertToBitmap()
        flow_bm = wx.StaticBitmap(self, bitmap=flow_img)
        self.flow_btn = wx.Button(self, label='Flow Network')
        self.flow_btn.Bind(wx.EVT_BUTTON, parent.toFlow)

        rvbox1.Add(flow_bm, 0, wx.ALL, 4)
        rvbox1.Add(self.flow_btn, 0, wx.ALIGN_CENTRE | wx.ALL, 4)

        hbox1.Add(lvbox1)
        hbox1.Add(rvbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        
        lvbox2 = wx.BoxSizer(wx.VERTICAL)
        rvbox2 = wx.BoxSizer(wx.VERTICAL)

        keyword_path = './../pics/keyword.png'
        keyword_img = wx.Image(keyword_path, wx.BITMAP_TYPE_ANY).Scale(200,200, wx.IMAGE_QUALITY_HIGH)
        keyword_img = keyword_img.ConvertToBitmap()
        keyword_bm = wx.StaticBitmap(self, bitmap=keyword_img)
        self.keyword_btn = wx.Button(self, label='Keyword Search')
        self.keyword_btn.Bind(wx.EVT_BUTTON, parent.toKeyword)

        lvbox2.Add(keyword_bm, 0, wx.ALL, 4)
        lvbox2.Add(self.keyword_btn, 0, wx.ALIGN_CENTRE | wx.ALL, 4)

        mean_path = './../pics/mean.png'
        mean_img = wx.Image(mean_path, wx.BITMAP_TYPE_ANY).Scale(200,200, wx.IMAGE_QUALITY_HIGH)
        mean_img = mean_img.ConvertToBitmap()
        mean_bm = wx.StaticBitmap(self, bitmap=mean_img)
        self.mean_btn = wx.Button(self, label='k-Means')
        self.mean_btn.Bind(wx.EVT_BUTTON, parent.toMean)

        rvbox2.Add(mean_bm, 0, wx.ALL, 4)
        rvbox2.Add(self.mean_btn, 0, wx.ALIGN_CENTRE | wx.ALL, 4)

        hbox2.Add(lvbox2)
        hbox2.Add(rvbox2)

        vbox.Add(title_txt, 0, wx.ALIGN_CENTRE)
        vbox.AddSpacer(15)
        vbox.Add(hbox1, 0, wx.ALIGN_CENTRE)
        vbox.Add(hbox2, 0, wx.ALIGN_CENTRE)
        self.SetSizer(vbox)

   #     seq_path = './../pics/flow.png'
   #     seq_img = wx.Image(seq_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
   #     self.seq_btn = wx.BitmapButton(self, bitmap=seq_img, size=(100,100))
#
   #     #self.seq_btn = wx.Button(self, label='Sequence Algorithms')
   #     self.seq_btn.Bind(wx.EVT_BUTTON, parent.toNeedlemanWunsh)
#
   #     self.network_btn = wx.Button(self, label='Network Flow')
   #     self.network_btn.Bind(wx.EVT_BUTTON, parent.toFlow)
#
   #     self.keyword_btn = wx.Button(self, label='Keyword Matching')
   #     self.keyword_btn.Bind(wx.EVT_BUTTON, parent.toKeyword)
#
   #     self.mean_btn = wx.Button(self, label='k-Means')
   #     self.mean_btn.Bind(wx.EVT_BUTTON, parent.toMean)
#
   #     self.submenu_grid = wx.FlexGridSizer(rows=4, cols=2)
   #      
   #     self.submenu_grid.AddMany([(self.seq_btn, 0),
   #                           (self.network_btn, 0, wx.EXPAND),
   #                           (wx.StaticText(self, label='Sequence Alignment'), 0),
   #                           (wx.StaticText(self, label='Flow Network'), 0),
   #                           (self.keyword_btn, 0, wx.EXPAND),
   #                           (self.mean_btn, 0, wx.EXPAND),
   #                           (wx.StaticText(self, label='Keyword Search'),0),
   #                           (wx.StaticText(self, label='k-Means'),0)])
#
   #     vbox.Add(self.submenu_grid, 1, wx.EXPAND | wx.ALL, 100)
   #     self.SetSizer(vbox)

if __name__ == '__main__':
    app = wx.App(redirect=False) 
    VizFrame(None, 'Bioinformatics Algorithm Visualization')
    app.MainLoop()