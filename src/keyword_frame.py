import wx
import wx.richtext as rt
import pydot


DESCRIPTION = (
    'Aho-Corasick Keyword Search\n' +
    'Keyword search involves finding keywords with a given input string. The Aho-Corasick string matching algorithm allows for multiple keywords to be processed on single input string in linear time by using a modified dictionary trie. The trie is modified such that each node within the trie has a failiure transition to its longest suffix in the trie and the failure transition, represented here in green, is taken if the current node does not have a child corresponding to the current letter.\n' +
    'String matching is utilized in bioinformatics as a fast means of string comparison. BLAST utilizes string matching in order to greatly improve speed with a modest decrease in sensitivity while performing alignments.\n')
class KeywordFrame(wx.Frame):
    def __init__(self, parent, trie, database):
        wx.Frame.__init__(self, parent, title = 'Keyword Matching', size=(800,700))

        self.panel = KeywordDrawingPanel(self, trie, database)
        self.Show(True)

class KeywordDrawingPanel(wx.Panel):
    def __init__(self, parent, trie, database):
        wx.Panel.__init__(self, parent)

        self.forward_timer = True
        self.trie = trie
        self.database = database
        self.steps = trie.getAllStepwise(database)
        self.step_index = 0
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timeUpdate, self.timer)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.drawing_panel = DrawingPanel(self, self.trie)
        self.string_panel = StringPanel(self, self.database)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.drawing_panel, 1, wx.EXPAND)

        vbox1.Add(self.string_panel, 0, wx.EXPAND)

        vbox2 = wx.BoxSizer(wx.VERTICAL)

        self.description_text = rt.RichTextCtrl(self, size=(200,400), style=rt.RE_READONLY)
        self.description_text.GetCaret().Hide()
        for line in DESCRIPTION.splitlines():
            self.description_text.AddParagraph(line) 
        self.list_ctrl = wx.ListCtrl(self, size=(300,400), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Keyword', width=200)
        self.list_ctrl.InsertColumn(1, 'Index', width=90)
        vbox2.Add(self.description_text, 1, wx.EXPAND)
        vbox2.Add(self.list_ctrl, 1, wx.EXPAND)

        hbox.Add(vbox1, 1, wx.EXPAND)
        hbox.Add(vbox2, 0, wx.EXPAND)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.pause_resume_btn = wx.Button(self, label='Start')
        self.pause_resume_btn.Bind(wx.EVT_BUTTON, self.pauseResume)
        time_static_txt = wx.StaticText(self, label='Interval (ms):')
        self.time_txt_ctrl = wx.TextCtrl(self, size=(40, -1))
        self.time_txt_ctrl.SetValue('1000')


        self.previous_btn = wx.Button(self, label='Previous')
        self.previous_btn.Bind(wx.EVT_BUTTON, self.previousTraverse)
        self.next_btn = wx.Button(self, label='Next')
        self.next_btn.Bind(wx.EVT_BUTTON, self.nextTraverse)
        self.restart_btn = wx.Button(self, label='Restart')
        self.restart_btn.Bind(wx.EVT_BUTTON, self.restart)
        self.finish_btn = wx.Button(self, label='Finish')
        self.finish_btn.Bind(wx.EVT_BUTTON, self.finish)

        hbox1.Add(self.pause_resume_btn, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)
        hbox1.Add(time_static_txt, 0, wx.LEFT | wx.BOTTOM | wx.ALIGN_BOTTOM, 10)
        hbox1.Add(self.time_txt_ctrl, 0, wx.BOTTOM | wx.LEFT | wx.ALIGN_BOTTOM, 6)
        hbox1.AddStretchSpacer()

        hbox1.Add(self.previous_btn, 0,  wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 5)
        hbox1.Add(self.next_btn, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 5)
        hbox1.AddSpacer(10)
        hbox1.Add(self.restart_btn, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 5)
        hbox1.Add(self.finish_btn, 0,  wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 5)

        vbox.Add(hbox, 1, wx.EXPAND)
        vbox.Add(hbox1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        self.SetSizer(vbox)

    def timeUpdate(self, event):
        if self.forward_timer:
            self.nextTraverse(None)
        else:
            self.previousTraverse(None)

    def pauseResume(self, event):
        if self.timer.IsRunning():
            self.timer.Stop()
            self.pause_resume_btn.SetLabel('Resume')
            self.time_txt_ctrl.Enable()

        else:
            speed = self.time_txt_ctrl.GetValue()
            try:
                speed = int(speed)
            except ValueError:
                dlg = wx.MessageDialog(self, 'Please enter a valid integer.', 'Invalid Integer', wx.OK | wx.ICON_ERROR)
                dlg.ShowModal() 
                dlg.Destroy()
                return
            if speed < 0:
                self.forward_timer = False
                speed = abs(speed)
            else:
                self.forward_timer = True
            self.timer.Start(speed)
            self.pause_resume_btn.SetLabel('Pause')
            self.time_txt_ctrl.Disable()

    def previousTraverse(self, event):
        if self.step_index <= 0:
            return
        self.step_index -= 1
        startOfString, endOfString, currentNode, match_indices = self.steps[self.step_index]
        self.string_panel.set_value(self.database, startOfString, endOfString)
        self.drawing_panel.my_plot(currentNode)
        self.list_ctrl.DeleteAllItems()
        for match in match_indices:
            num_items = self.list_ctrl.GetItemCount()
            self.list_ctrl.InsertStringItem(num_items, match[1])
            self.list_ctrl.SetStringItem(num_items, 1, str(match[0]))

    def nextTraverse(self, event):
        if self.step_index >= len(self.steps) - 1:
            return
        self.step_index += 1
        startOfString, endOfString, currentNode, match_indices = self.steps[self.step_index]
        self.string_panel.set_value(self.database, startOfString, endOfString)
        self.drawing_panel.my_plot(currentNode)
        self.list_ctrl.DeleteAllItems()
        for match in match_indices:
            num_items = self.list_ctrl.GetItemCount()
            self.list_ctrl.InsertStringItem(num_items, match[1])
            self.list_ctrl.SetStringItem(num_items, 1, str(match[0]))


    def restart(self, event):
        self.step_index = 0
        startOfString, endOfString, currentNode, match_indices = self.steps[self.step_index]
        self.string_panel.set_value(self.database, startOfString, endOfString)
        self.drawing_panel.my_plot(currentNode)
        self.list_ctrl.DeleteAllItems()
        for match in match_indices:
            num_items = self.list_ctrl.GetItemCount()
            self.list_ctrl.InsertStringItem(num_items, match[1])
            self.list_ctrl.SetStringItem(num_items, 1, str(match[0]))

    def finish(self, event):
        self.step_index = len(self.steps) - 1
        startOfString, endOfString, currentNode, match_indices = self.steps[self.step_index]
        self.string_panel.set_value(self.database, startOfString, endOfString)
        self.drawing_panel.my_plot(currentNode)
        self.list_ctrl.DeleteAllItems()
        for match in match_indices:
            num_items = self.list_ctrl.GetItemCount()
            self.list_ctrl.InsertStringItem(num_items, match[1])
            self.list_ctrl.SetStringItem(num_items, 1, str(match[0]))

class StringPanel(wx.Panel):
    def __init__(self, parent, string):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.static_text = rt.RichTextCtrl(self, size=(2000, 60),style= rt.RE_READONLY)
        self.static_text.GetCaret().Hide()

        sizer.Add(self.static_text, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.set_value(string, 0, 0)


    def set_initial(self, string):
        self.static_text.Clear()
        self.static_text.WriteText('Database String:')
        self.static_text.Newline()
        self.static_text.BeginFontSize(16)
        self.static_text.WriteText(string)
        self.static_text.EndFontSize()

    def set_value(self, string, start, end):
        self.static_text.Clear()
        self.static_text.WriteText('Database String:')
        self.static_text.Newline()
        self.static_text.BeginFontSize(16)
        if string[:start]:
            self.static_text.WriteText(string[:start])
        if start == len(string):
            self.static_text.EndFontSize()
            return
        if start == end:
            self.static_text.BeginTextColour(wx.BLUE)
            self.static_text.WriteText(string[start])
            self.static_text.EndTextColour()
            if string[start+1:]:
                self.static_text.WriteText(string[start+1:])
            self.static_text.EndFontSize()
            return
        self.static_text.BeginTextColour('#006400')
        self.static_text.WriteText(string[start])
        self.static_text.EndTextColour()
        if start < end-1:
            if string[start+1:end-1]:
                self.static_text.BeginUnderline()
                self.static_text.WriteText(string[start+1:end-1])
                self.static_text.EndUnderline()
            self.static_text.BeginTextColour('#660000')
            self.static_text.WriteText(string[end-1])
            self.static_text.EndTextColour()

            if string[end:]:
                self.static_text.BeginTextColour(wx.BLUE)
                self.static_text.WriteText(string[end])
                self.static_text.EndTextColour()
            if string[end+1:]:
                self.static_text.WriteText(string[end+1:])
        else:
            if string[start+1:]:
                self.static_text.BeginTextColour(wx.BLUE)
                self.static_text.WriteText(string[start+1])
                self.static_text.EndTextColour()
            if string[start+2:]:
                self.static_text.WriteText(string[start+2:])
        self.static_text.EndFontSize()

class DrawingPanel(wx.ScrolledWindow):
    def __init__(self, parent, trie):
        wx.ScrolledWindow.__init__(self, parent)
        self.bitmap = None
        self.trie = trie
        self.my_plot(0)
        self.SetBackgroundColour(wx.WHITE)
        self.SetScrollRate(5,5)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def my_plot(self, current_node):
        graph = pydot.Dot(graph_type='digraph')
        nodes = list()
        for i in range(len(self.trie.node_list)):
            node = pydot.Node(str(i), style='filled', fillcolor='#666666', fontcolor='#666666')
            if self.trie.node_list[i].terminal and i == current_node:
                node.set_fillcolor('#FF4500')
                node.set_fontcolor('#FF4500')
            elif self.trie.node_list[i].terminal:
                node.set_fillcolor('#770000')
                node.set_fontcolor('#770000')
            elif i == current_node:
                node.set_fillcolor('#CCCC00')
                node.set_fontcolor('#CCCC00')
            graph.add_node(node)
            nodes.append(node)
        for edge in self.trie.edges:
            graph.add_edge(pydot.Edge(nodes[edge[0]], nodes[edge[1]], label=str(self.trie.node_list[edge[1]].previous_edge)))#, labelfontcolor='#FFFFFF', fontsize='10,0', color='#FFFFFF'))

        for back_edge in self.trie.back_edges:
            edge = pydot.Edge(nodes[back_edge[0]], nodes[back_edge[1]], color='#006400')
            edge.set_constraint(False)
            graph.add_edge(edge)
        img_file = 'test.png'
        graph.write_png(img_file)
        if self.bitmap:
            self.bitmap.Destroy()
        self.bitmap = wx.Image(img_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.Refresh()

    def OnPaint(self, event):
        self.SetVirtualSize(self.bitmap.GetSize())
        dc = wx.PaintDC(self)       
        self.DoPrepareDC(dc)
        dc.DrawBitmap(self.bitmap, 0, 0)