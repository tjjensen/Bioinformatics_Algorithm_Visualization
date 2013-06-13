import wx
import flow_frame
import flow_network

class FlowPanel(wx.Panel):
    
    def __init__(self, parent):

        wx.Panel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        left_vbox = wx.BoxSizer(wx.VERTICAL)
        right_vbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(left_vbox, 0, wx.EXPAND)
        hbox.Add(right_vbox, 1, wx.EXPAND)

        node_box = wx.StaticBoxSizer(wx.StaticBox(self, label="Nodes"), wx.VERTICAL)
        self.node_list = wx.ListCtrl(self, size=(250,250), style=wx.LC_REPORT |  wx.LC_NO_HEADER | wx.BORDER_SUNKEN)

        self.node_list.InsertColumn(0, 'Node', width=245)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.node_source_btn = wx.Button(self, label='Set as Source')
        self.node_source_btn.Bind(wx.EVT_BUTTON, self.setSource)
        self.node_sink_btn = wx.Button(self, label='Set as Sink')
        self.node_sink_btn.Bind(wx.EVT_BUTTON, self.setSink)
        self.node_delete_btn = wx.Button(self, label='Remove Nodes')
        self.node_delete_btn.Bind(wx.EVT_BUTTON, self.nodeDelete)
        self.node_clear_btn = wx.Button(self, label='Clear')
        self.node_clear_btn.Bind(wx.EVT_BUTTON, self.nodeClear)

        hbox1.Add(self.node_source_btn, 0)
        hbox1.AddSpacer(5)
        hbox1.Add(self.node_sink_btn, 0)
        hbox1.AddSpacer(5)
        hbox1.Add(self.node_delete_btn, 0)
        hbox1.AddSpacer(5)
        hbox1.Add(self.node_clear_btn, 0)

        hbox2= wx.BoxSizer(wx.HORIZONTAL)

        node_static_txt = wx.StaticText(self, label='Node:')
        self.node_txt_ctrl = wx.TextCtrl(self, size=(200, -1))
        self.node_add_btn = wx.Button(self, label='Add Node')
        self.node_add_btn.Bind(wx.EVT_BUTTON, self.addNode)

        hbox2.Add(node_static_txt, 0)
        hbox2.AddSpacer(5)
        hbox2.Add(self.node_txt_ctrl, 0)
        hbox2.AddSpacer(10)
        hbox2.Add(self.node_add_btn, 0)


        source_static_text = wx.StaticText(self, label='Source Node:')
        self.source_text_ctrl = wx.TextCtrl(self, size=(100, -1))

        sink_static_text = wx.StaticText(self, label='Sink Node:')
        self.sink_text_ctrl = wx.TextCtrl(self, size=(100, -1))

        node_box.Add(self.node_list, 1, wx.EXPAND)
        node_box.AddSpacer(10)
        node_box.Add(hbox1, 0)
        node_box.AddSpacer(7)
        node_box.Add(hbox2, 0)
        node_box.AddSpacer(5)
        node_box.Add(source_static_text, 0)
        node_box.AddSpacer(5)
        node_box.Add(self.source_text_ctrl, 0)
        node_box.AddSpacer(5)
        node_box.Add(sink_static_text, 0)
        node_box.AddSpacer(5)
        node_box.Add(self.sink_text_ctrl, 0)

        left_vbox.Add(node_box, 0, wx.ALL | wx.EXPAND, 3)
        
        edge_box = wx.StaticBoxSizer(wx.StaticBox(self, label="Edges"), wx.VERTICAL)
        self.edge_list = wx.ListCtrl(self, size=(400,400), style=wx.LC_REPORT | wx.BORDER_SUNKEN)

        self.edge_list.InsertColumn(0, 'Tail Node', width=150)
        self.edge_list.InsertColumn(1, 'Head Node', width=150)
        self.edge_list.InsertColumn(2, 'Capacity', width=90)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.edge_add_btn = wx.Button(self, label='Add Edge')
        self.edge_add_btn.Bind(wx.EVT_BUTTON, self.addEdge)
        self.edge_delete_btn = wx.Button(self, label='Remove Edges')
        self.edge_delete_btn.Bind(wx.EVT_BUTTON, self.edgeDelete)
        self.edge_clear_btn = wx.Button(self, label='Clear')
        self.edge_clear_btn.Bind(wx.EVT_BUTTON, self.edgeClear)

        hbox3.Add(self.edge_add_btn, 0)
        hbox3.AddSpacer(5)
        hbox3.Add(self.edge_delete_btn, 0)
        hbox3.AddSpacer(5)
        hbox3.Add(self.edge_clear_btn, 0)

        edge_box.Add(self.edge_list, 1, wx.EXPAND)
        edge_box.AddSpacer(10)
        edge_box.Add(hbox3, 0)
        edge_box.AddSpacer(7)

        right_vbox.Add(edge_box, 0, wx.ALL | wx.EXPAND, 3)

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

    def setSource(self, event):
        if self.node_list.GetSelectedItemCount() > 1:
            dlg = wx.MessageDialog(self, 'Select a single node in ordert to set the source or sink.', 'More than one Item Selected', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return
        elif self.node_list.GetSelectedItemCount() == 0:
            return
        current_item = self.node_list.GetNextSelected(-1)
        self.source_text_ctrl.SetValue(self.node_list.GetItemText(current_item))

    def setSink(self, event):
        if self.node_list.GetSelectedItemCount() > 1:
            dlg = wx.MessageDialog(self, 'Select a single node in ordert to set the source or sink.', 'More than one Item Selected', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return
        elif self.node_list.GetSelectedItemCount() == 0:
            return
        current_item = self.node_list.GetNextSelected(-1)
        self.sink_text_ctrl.SetValue(self.node_list.GetItemText(current_item))

    def nodeDelete(self, event):
        current_item = self.node_list.GetNextSelected(-1)
        while current_item >= 0:
            node = self.node_list.GetItemText(current_item)
            edges = self.getEdges()
            del_edges = list()
            for i, edge in enumerate(edges):
                if node == edge[0] or node == edge[1]:
                    del_edges.append(i)
            del_edges.reverse()
            for edge in del_edges:
                self.edge_list.DeleteItem(edge)
            self.node_list.DeleteItem(current_item)
            current_item = self.node_list.GetNextSelected(-1)


        self.node_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def nodeClear(self, event):
        self.node_list.DeleteAllItems()
        self.node_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.edge_list.DeleteAllItems()

    def addNode(self, event):
        word = self.node_txt_ctrl.GetValue()
        if not word:
            return
        if word in self.getNodes():
            dlg = wx.MessageDialog(self, 'Node with that name already exists.', 'Invalid Node Name', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return
        self.node_list.Append([word])
        self.node_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def edgeDelete(self, event):
        current_item = self.edge_list.GetNextSelected(-1)
        while current_item >= 0:
            self.edge_list.DeleteItem(current_item)
            current_item = self.edge_list.GetNextSelected(-1)

    def edgeClear(self, event):
        self.edge_list.DeleteAllItems()

    def addEdge(self, event):
        if not self.getNodes():
            dlg = wx.MessageDialog(self, 'No nodes present in graph.', 'No Nodes Found', wx.OK| wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        edge_dlg = AddEdgeDialog(self, self.getNodes())
        if edge_dlg.ShowModal() == wx.ID_OK:
            edge_info = edge_dlg.getEdge()
            if edge_info:
                exists = False
                for i, edge in enumerate(self.getEdges()):
                    if edge_info[0] == edge[0] and edge_info[1] == edge[1]:
                        exists = True
                        self.edge_list.SetStringItem(i, 2, edge_info[2])
                if not exists:
                    self.edge_list.Append(edge_info)
        self.getEdges()
        edge_dlg.Destroy()

    def getNodes(self):
        nodes = list()
        for i in range(self.node_list.GetItemCount()):
            txt = self.node_list.GetItemText(i)
            nodes.append(str(txt))
        return nodes

    def getEdges(self):
        edges = list()
        for i in range(self.edge_list.GetItemCount()):
            edges.append((str(self.edge_list.GetItem(i, 0).GetText()), str(self.edge_list.GetItem(i, 1).GetText()), str(self.edge_list.GetItem(i, 2).GetText())))
        return edges

    def visualize(self, event):
        nodes = self.getNodes()
        edges = self.getEdges()
        source = str(self.source_text_ctrl.GetValue())
        sink = str(self.sink_text_ctrl.GetValue())

        #TEST VALUES#
        #nodes = ('a', 'b', 'c', 'd')
        #edges = (('a', 'b', 10), ('b', 'c', 1), ('b', 'd', 10), ('a', 'c', 10), ('c', 'd', 10))
        #source = 'a'
        #sink = 'd'

        if not nodes:
            dlg = wx.MessageDialog(self, 'You must add nodes to the graph.', 'No Nodes', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return
        if not edges:
            dlg = wx.MessageDialog(self, 'You must add edges to the graph.', 'No Edges', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return
        if source not in nodes:
            dlg = wx.MessageDialog(self, 'Source node not found in list of nodes.', 'Invalid Source', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return
        if sink not in nodes:
            dlg = wx.MessageDialog(self, 'Sink node not found in list of nodes.', 'Invalid Sink', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return

        network = flow_network.FlowNetwork(nodes, edges, source, sink)
        fframe = flow_frame.FlowFrame(self, network)



class AddEdgeDialog(wx.Dialog):
    def __init__(self, parent, nodes):
        wx.Dialog.__init__(self, parent)
        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.tail_list = wx.ListCtrl(self, size=(100,150), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL)
        self.tail_list.InsertColumn(0, 'Tail Node', width=100)
        self.head_list = wx.ListCtrl(self, size=(100,150), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL)
        self.head_list.InsertColumn(0, 'Head Node', width=100)

        for node in nodes:
            self.tail_list.Append([node])
            self.head_list.Append([node])
        if nodes and len(max(nodes, key=len)) > 11:
            self.tail_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.head_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        hbox.Add(self.tail_list, 1, wx.EXPAND)
        hbox.AddSpacer(5)
        hbox.Add(self.head_list, 1, wx.EXPAND)

        capacity_static_txt = wx.StaticText(self, label='Edge Capacity:')
        self.capacity_txt_ctrl = wx.TextCtrl(self, size=(50,-1))

        btn_sizer = self.CreateButtonSizer(wx.CANCEL|wx.OK)
        sizer.Add(hbox, 0, wx.EXPAND)
        sizer.Add(capacity_static_txt, 0, wx.ALL, 3)
        sizer.Add(self.capacity_txt_ctrl, 0, wx.ALL, 3)
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 5)
        self.SetSizer(sizer)

    def getEdge(self):
        if self.tail_list.GetSelectedItemCount() != 1:
            dlg = wx.MessageDialog(self, 'No tail node was selected.', 'No Tail Node Selected', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return False
        if self.head_list.GetSelectedItemCount() != 1:
            dlg = wx.MessageDialog(self, 'No head node was selected.', 'No Head Node Selected', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return False
        try:
            int(self.capacity_txt_ctrl.GetValue())
        except ValueError:
            dlg = wx.MessageDialog(self, 'Edge capacity must be an integer.', 'Invalid Capacity', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return False
        tail_node = self.tail_list.GetItemText(self.tail_list.GetNextSelected(-1))
        head_node = self.head_list.GetItemText(self.head_list.GetNextSelected(-1))
        if tail_node == head_node:
            dlg = wx.MessageDialog(self, 'Tail node must differ from head node.', 'Invalid Nodes', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return False

        capacity = self.capacity_txt_ctrl.GetValue()
        return (tail_node, head_node, capacity)


 