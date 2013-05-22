#!/usr/bin/python

import wx
import seq_panel
import de_bruijn_panel
import keyword_panel
import flow_panel

class VizFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.menu_panel = MenuPanel(self)
        self.seq_submenu = SeqMenuPanel(self)
        self.nw_panel = seq_panel.NeedlemanWunshPanel(self)
        self.graph_submenu = GraphMenuPanel(self)
        self.bruijn_panel = de_bruijn_panel.DeBruijnPanel(self)
        self.keyword_panel = keyword_panel.KeywordPanel(self)
        self.flow_panel = flow_panel.FlowPanel(self)
        self.seq_submenu.Hide()
        self.nw_panel.Hide()
        self.graph_submenu.Hide()
        self.bruijn_panel.Hide()
        self.keyword_panel.Hide()
        self.flow_panel.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.menu_panel, 1, wx.EXPAND)
        self.sizer.Add(self.seq_submenu, 1, wx.EXPAND)
        self.sizer.Add(self.nw_panel, 1, wx.EXPAND)
        self.sizer.Add(self.graph_submenu, 1, wx.EXPAND)
        self.sizer.Add(self.bruijn_panel, 1, wx.EXPAND)
        self.sizer.Add(self.keyword_panel, 1, wx.EXPAND)
        self.sizer.Add(self.flow_panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.current_panel = self.menu_panel
        self.Center()
        self.Show(True)

    def toMenu(self, event):
        self.current_panel.Hide()
        self.current_panel = self.menu_panel
        self.current_panel.Show()
        self.Layout()        

    def toSequenceSubmenu(self, event):
        self.current_panel.Hide()
        self.current_panel = self.seq_submenu
        self.current_panel.Show()
        self.Layout()

    def toGraphSubmenu(self, event):
        self.current_panel.Hide()
        self.current_panel = self.graph_submenu
        self.current_panel.Show()
        self.Layout()

    def toNeedlemanWunsh(self, event):
        self.current_panel.Hide()
        self.current_panel = self.nw_panel
        self.current_panel.Show()
        self.Layout()

    def toBruijn(self, event):
        self.current_panel.Hide()
        self.current_panel = self.bruijn_panel
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

class MenuPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.seq_btn = wx.Button(self, label='Sequence Algorithms')
        self.seq_btn.Bind(wx.EVT_BUTTON, parent.toSequenceSubmenu)

        self.network_btn = wx.Button(self, label='Network Flow')
        self.network_btn.Bind(wx.EVT_BUTTON, parent.toFlow)

        self.keyword_btn = wx.Button(self, label='Keyword Matching')
        self.keyword_btn.Bind(wx.EVT_BUTTON, parent.toKeyword)

        self.submenu_grid = wx.GridSizer(rows=2, cols=2)
         
        self.submenu_grid.AddMany([(self.seq_btn, 0, wx.EXPAND),
                              (self.network_btn, 0, wx.EXPAND),
                              (self.keyword_btn, 0, wx.EXPAND),
                              (wx.Button(self, label='Sequence4 Algorithms'), 0, wx.EXPAND)])

        vbox.Add(self.submenu_grid, 1, wx.EXPAND | wx.ALL, 100)
        self.SetSizer(vbox)



class SubmenuPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class SeqMenuPanel(SubmenuPanel):
    def __init__(self, parent):
        SubmenuPanel.__init__(self, parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.nw_btn = wx.Button(self, label='Needleman-Wunsh Algorithm')
        self.nw_btn.Bind(wx.EVT_BUTTON, parent.toNeedlemanWunsh)

        self.submenu_grid = wx.GridSizer(rows=2, cols=2)
        
        self.submenu_grid.AddMany([(self.nw_btn, 0, wx.EXPAND),
                              (wx.Button(self, label='Sequence Algorithm2'), 0, wx.EXPAND),
                              (wx.Button(self, label='Sequence3 Algorithm3'), 0, wx.EXPAND),
                              (wx.Button(self, label='Sequence4 Algorithm4'), 0, wx.EXPAND)])

        vbox.Add(self.submenu_grid, 1, wx.EXPAND | wx.ALL, 100)
        self.SetSizer(vbox)

class GraphMenuPanel(SubmenuPanel):
    def __init__(self, parent):
        SubmenuPanel.__init__(self, parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.bruijn_btn = wx.Button(self, label='De Bruijn Reassembly')
        self.bruijn_btn.Bind(wx.EVT_BUTTON, parent.toBruijn)

        self.submenu_grid = wx.GridSizer(rows=2, cols=2)
        
        self.submenu_grid.AddMany([(self.bruijn_btn, 0, wx.EXPAND),
                              (wx.Button(self, label='Graph Algorithm2'), 0, wx.EXPAND),
                              (wx.Button(self, label='Graph Algorithm3'), 0, wx.EXPAND),
                              (wx.Button(self, label='Graph Algorithm4'), 0, wx.EXPAND)])

        vbox.Add(self.submenu_grid, 1, wx.EXPAND | wx.ALL, 100)
        self.SetSizer(vbox)

class AlgoPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)



if __name__ == '__main__':
    app = wx.App(redirect=False) 
    VizFrame(None, 'Bioinformatics Algorithm Visualization')
    app.MainLoop()