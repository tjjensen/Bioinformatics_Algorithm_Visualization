import wx
import wx.richtext as rt
import pydot


DESCRIPTION = (
    'Ford-Fulkerson Algorithm\n' +
    'The maximum flow problem involves finding a feasible flow through a flow network that is maximal. The Fork-Fulkerson algorithm approaches the problem by creating the flow network and adding reverse edges, drawn here in green, whose capacities are zero. The algorithm starts with a depth first search starting at the source, looking for a path to the sink. When a path with an allowed flow greater than zero is found, the graph is updated so that the flow of each edge in the path is incremented by the allowed flow and the flow of the reverse edge is decremented by the allowed flow. Continuous rounds of depth first search result in a finished graph which has maximal flow.\n'+
    'Maximum flow problem relates to bioinformatics in that an aggregate multiple sequence alignment can be created using maximum flow between pairwise alignments. Maximum flow has also been used to find hot regions of protein interaction networks.\n')

class FlowFrame(wx.Frame):
    def __init__(self, parent, flow_network):
        wx.Frame.__init__(self, parent, title = 'Network Flow', size=(800,700))

        self.panel = FlowDrawingPanel(self, flow_network)
        self.Show(True)

class FlowDrawingPanel(wx.Panel):
    def __init__(self, parent, flow_network):
        wx.Panel.__init__(self, parent)

        self.forward_timer = True
        self.flow_network = flow_network
        self.steps = flow_network.get_steps()
        self.step_index = 0
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timeUpdate, self.timer)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.drawing_panel = DrawingPanel(self, self.flow_network, self.steps[0][:-1])

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.drawing_panel, 1, wx.EXPAND)

        
        vbox2 = wx.BoxSizer(wx.VERTICAL)

        self.description_text = rt.RichTextCtrl(self, size=(300,400), style=rt.RE_READONLY)
        self.description_text.GetCaret().Hide()
        for line in DESCRIPTION.splitlines():
            self.description_text.AddParagraph(line)

        vbox2.Add(self.description_text, 1, wx.EXPAND)
        
        hbox.Add(vbox1, 1, wx.EXPAND)
        hbox.Add(vbox2, 0, wx.EXPAND)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        flow_static_txt =wx.StaticText(self, label='Current Flow:')
        self.flow_txt_ctrl = wx.TextCtrl(self, size=(27,-1))
        self.flow_txt_ctrl.SetEditable(False)
        self.flow_txt_ctrl.SetValue(str(0))

        hbox2.AddSpacer(10)
        hbox2.Add(flow_static_txt, 0, wx.ALL, 5)
        hbox2.Add(self.flow_txt_ctrl, 0, wx.ALL, 2)

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
        vbox.Add(hbox2, 0, wx.EXPAND)
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
        self.drawing_panel.my_plot(self.steps[self.step_index][:-1])
        self.flow_txt_ctrl.SetValue(str(self.steps[self.step_index][-1]))

    def nextTraverse(self, event):
        if self.step_index >= len(self.steps) - 1:
            return
        self.step_index += 1
        self.drawing_panel.my_plot(self.steps[self.step_index][:-1])
        self.flow_txt_ctrl.SetValue(str(self.steps[self.step_index][-1]))

    def restart(self, event):
        self.step_index = 0
        self.drawing_panel.my_plot(self.steps[self.step_index][:-1])
        self.flow_txt_ctrl.SetValue(str(self.steps[self.step_index][-1]))

    def finish(self, event):
        self.step_index = len(self.steps) - 1
        self.drawing_panel.my_plot(self.steps[self.step_index][:-1])
        self.flow_txt_ctrl.SetValue(str(self.steps[self.step_index][-1]))

class DrawingPanel(wx.ScrolledWindow):
    def __init__(self, parent, flow_network, step):
        wx.ScrolledWindow.__init__(self, parent)
        self.bitmap = None
        self.flow_network = flow_network
        self.my_plot(step)
        self.SetBackgroundColour(wx.WHITE)
        self.SetScrollRate(5,5)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def my_plot(self, step):
        graph = pydot.Dot(graph_type='digraph')
        nodes = dict()
        current_node, flows = step
        for name, node in self.flow_network.nodes.iteritems():
            g_node = pydot.Node(name, style='filled', fillcolor='#666666', fontcolor='#000000')
            if self.flow_network.source == name:
                g_node.set_fillcolor('#770000')
                if name == current_node:
                    g_node.set_fillcolor('#FF4500')
                #g_node.set_fontcolor('#FF4500')
            elif self.flow_network.sink == name:
                g_node.set_fillcolor('#000077')
                if name == current_node:
                    g_node.set_fillcolor('#0045CC')
                #g_node.set_fontcolor('#770000')
            elif name == current_node:
                g_node.set_fillcolor('#CCCC00')
                #g_node.set_fontcolor('#CCCC00')
            graph.add_node(g_node)
            nodes[name] = g_node


        for tail, head, flow, capacity, forward in flows:
            g_edge = pydot.Edge(nodes[tail], nodes[head], label=' {0}/{1} '.format(flow, capacity))
            if not forward:
                g_edge.set_color('#008800')
                g_edge.set_constraint(False)
            graph.add_edge(g_edge)

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