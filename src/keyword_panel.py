import wx
import keyword_frame
import dictionary_trie

class KeywordPanel(wx.Panel):
    
    def __init__(self, parent):

        wx.Panel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        left_vbox = wx.BoxSizer(wx.VERTICAL)
        right_vbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(left_vbox, 0, wx.EXPAND)
        hbox.Add(right_vbox, 1, wx.EXPAND)

        #Create and fill sequence box UI
        seq_box = wx.StaticBoxSizer(wx.StaticBox(self, label="Input String"), wx.VERTICAL)
        self.db_static_txt = wx.StaticText(self, label='Input String:')
        self.db_txt_ctrl = wx.TextCtrl(self, size=(200, -1))
        

        self.db_import_btn = wx.Button(self, label='Import from File')
        self.db_import_btn.Bind(wx.EVT_BUTTON, self.importDB)


        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.db_static_txt, flag=wx.LEFT, border=0)
        hbox1.Add(self.db_txt_ctrl, flag=wx.LEFT, border=5)

        seq_box.Add(hbox1, 0, wx.ALL, 2)
        seq_box.Add(self.db_import_btn, 0, wx.LEFT | wx.ALIGN_TOP, 50)
        

        left_vbox.Add(seq_box, 0, wx.ALL | wx.EXPAND, 3)

        list_box = wx.StaticBoxSizer(wx.StaticBox(self, label="Keywords"), wx.VERTICAL)
        self.list_ctrl = wx.ListCtrl(self, size=(400,400), style=wx.LC_REPORT |  wx.LC_NO_HEADER | wx.BORDER_SUNKEN)

        self.list_ctrl.InsertColumn(0, 'Keyword', width=400)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.keyword_delete_btn = wx.Button(self, label='Remove Keywords')
        self.keyword_delete_btn.Bind(wx.EVT_BUTTON, self.keywordDelete)
        self.keyword_clear_btn = wx.Button(self, label='Clear')
        self.keyword_clear_btn.Bind(wx.EVT_BUTTON, self.keywordClear)

        hbox2.Add(self.keyword_delete_btn, 0)
        hbox2.AddSpacer(5)
        hbox2.Add(self.keyword_clear_btn, 0)

        hbox3= wx.BoxSizer(wx.HORIZONTAL)

        keyword_static_txt = wx.StaticText(self, label='Keyword:')
        self.keyword_txt_ctrl = wx.TextCtrl(self, size=(200, -1))
        self.keyword_add_btn = wx.Button(self, label='Add Keyword')
        self.keyword_add_btn.Bind(wx.EVT_BUTTON, self.addKeyword)

        hbox3.Add(keyword_static_txt, 0)
        hbox3.AddSpacer(5)
        hbox3.Add(self.keyword_txt_ctrl, 0)
        hbox3.AddSpacer(10)
        hbox3.Add(self.keyword_add_btn, 0)

        self.keyword_from_file_btn = wx.Button(self, label='Import from File')
        self.keyword_from_file_btn.Bind(wx.EVT_BUTTON, self.importKeyword)

        list_box.Add(self.list_ctrl, 1, wx.EXPAND)
        list_box.AddSpacer(10)
        list_box.Add(hbox2, 0)
        list_box.AddSpacer(5)
        list_box.Add(hbox3, 0)
        list_box.AddSpacer(5)
        list_box.Add(self.keyword_from_file_btn, 0)


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

    def importDB(self, event):
        db = ''
        filetype = self.getFiletype()
        if filetype:
            db = self.getSeq(filetype)
        if db:
            self.db_txt_ctrl.SetValue(db)

    def getFiletype(self):
        filetype = ''
        dlg = wx.SingleChoiceDialog(self, message='Choose a file type.', caption='Choose a file type.', choices=['Plain text', 'FASTA'])
        if dlg.ShowModal() == wx.ID_OK:
            filetype = dlg.GetStringSelection()
        dlg.Destroy()
        return filetype

    def getSeq(self, filetype):
        if filetype == 'Plain text':
            wildcard = 'Text file (*.txt)|*.txt|All files|*'
        else:
            wildcard = 'FASTA File (*.fasta)|*.fasta|All files (*.*)|*'
        seq = ''
        dlg = wx.FileDialog(self, message='Choose a sequence file', defaultFile='', wildcard=wildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            with open(path, 'Ur') as f:
                contents = f.read()
                if filetype == 'Plain text':
                    seq = ''.join(contents.split())
                else:
                    lines = contents.splitlines()
                    start = False
                    seq_list = list()
                    for line in lines:
                        if line[0] == '>':
                            if not start:
                                start = True
                                continue
                            else:
                                break
                        if start:
                            seq_list.append(line)
                    seq = ''.join(seq_list)
        dlg.Destroy()
        return seq

    def keywordDelete(self, event):
        current_item = self.list_ctrl.GetNextSelected(-1)
        while current_item >= 0:
            self.list_ctrl.DeleteItem(current_item)
            current_item = self.list_ctrl.GetNextSelected(-1)
        self.list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def keywordClear(self, event):
        self.list_ctrl.DeleteAllItems()
        self.list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def addKeyword(self, event):
        word = self.keyword_txt_ctrl.GetValue()
        self.list_ctrl.Append([word])
        self.list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def importKeyword(self, event):
        keywords = list()
        multifiletype = self.getMultiFiletype()
        if multifiletype:
            keywords = self.getMultiSeq(multifiletype)
        if keywords:
            for keyword in keywords:
                self.list_ctrl.Append([keyword])
            self.list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def getMultiFiletype(self):
        filetype = ''
        dlg = wx.SingleChoiceDialog(self, message='Choose a multi-sequence file type.', caption='Choose a file type.', choices=['Line Separated Plain Text', 'Multi-FASTA'])
        if dlg.ShowModal() == wx.ID_OK:
            filetype = dlg.GetStringSelection()
        dlg.Destroy()
        return filetype

    def getMultiSeq(self, filetype):
        if filetype == 'Line Separated Plain Text':
            wildcard = 'Text file (*.txt)|*.txt|All files|*'
        else:
            wildcard = 'FASTA File (*.fasta)|*.fasta|All files (*.*)|*'
        seq = ''
        dlg = wx.FileDialog(self, message='Choose a sequence file', defaultFile='', wildcard=wildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            with open(path, 'Ur') as f:
                contents = f.read()
                if filetype == 'Line Separated Plain Text':
                    seqs = contents.splitlines()
                else:
                    lines = contents.splitlines()
                    start = False
                    seqs = list()
                    for line in lines:
                        if line[0] == '>':
                                seqs.append('')
                                continue
                        else:
                            seqs[-1] += ''.join(line.split())
        dlg.Destroy()
        return seqs
    def visualize(self, event):
        database = str(self.db_txt_ctrl.GetValue())

        keywords = list()
        for i in range(self.list_ctrl.GetItemCount()):
            txt = self.list_ctrl.GetItemText(i)
            keywords.append(str(txt))
        alphabet = set()
        for c in database:
            alphabet.add(c)
        for c in ''.join(keywords):
            alphabet.add(c)

        trie = dictionary_trie.DictionaryTrie(list(alphabet), keywords)

        k_frame = keyword_frame.KeywordFrame(self, trie, database)
