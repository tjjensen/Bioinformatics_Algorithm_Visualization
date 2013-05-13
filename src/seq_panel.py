import bio_viz
import wx
import bio_utils
import seqframe
import seq_align
class NeedlemanWunshPanel(bio_viz.AlgoPanel):
    def __init__(self, parent):
        bio_viz.AlgoPanel.__init__(self, parent)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox, 0)
        left_vbox = wx.BoxSizer(wx.VERTICAL)
        right_vbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(left_vbox, 0, wx.EXPAND)
        hbox.Add(right_vbox, 1, wx.EXPAND)

        #Create and fill sequence box UI
        seq_box = wx.StaticBoxSizer( wx.StaticBox(self, label="Sequences" ), wx.VERTICAL) 
        self.seq1_static_txt = wx.StaticText(self, label='Sequence u:')
        self.seq1_txt_ctrl = wx.TextCtrl(self, size=(200, -1))
        

        self.seq1_import_btn = wx.Button(self, label='Import from File')
        self.seq1_import_btn.Bind(wx.EVT_BUTTON, self.import_seq1)


        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.seq1_static_txt, flag=wx.LEFT, border=0)
        hbox1.Add(self.seq1_txt_ctrl, flag=wx.LEFT, border=5)

        self.seq2_static_txt = wx.StaticText(self, label='Sequence v:')
        self.seq2_txt_ctrl = wx.TextCtrl(self, size=(200, -1))
        self.seq2_import_btn = wx.Button(self, label='Import from File')
        self.seq2_import_btn.Bind(wx.EVT_BUTTON, self.import_seq2)

        hbox2= wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.seq2_static_txt, flag=wx.LEFT, border=0)
        hbox2.Add(self.seq2_txt_ctrl, flag=wx.LEFT, border=5)
        seq_box.Add(hbox1, 0, wx.ALL, 2)
        seq_box.Add(self.seq1_import_btn, 0, wx.LEFT | wx.ALIGN_TOP, 50)
        seq_box.Add(hbox2, 0, wx.ALL, 2)
        seq_box.Add(self.seq2_import_btn, 0, wx.LEFT | wx.ALIGN_TOP, 50)
        
        span_box = wx.StaticBoxSizer( wx.StaticBox(self, label="Alignment Span" ), wx.VERTICAL)
        self.global_radio_btn = wx.RadioButton(self, label='Global', style = wx.RB_GROUP)
        self.local_radio_btn = wx.RadioButton(self, label='Local')
        span_box.Add(self.global_radio_btn, 0)
        span_box.Add(self.local_radio_btn, 0)

        left_vbox.Add(seq_box, 0, wx.ALL | wx.EXPAND, 3)
        left_vbox.Add(span_box, 0, wx.ALL | wx.EXPAND, 3)


        self.nb = wx.Notebook(self)

        nucleo_alpha = list(bio_utils.NUCLEOTIDES) + ['-']
        self.nucleotide_page = SeqAlphaPanel(self.nb, nucleo_alpha)

        protein_alpha = list(bio_utils.AMINO_ACIDS) + ['-']
        self.protein_page = SeqAlphaPanel(self.nb, protein_alpha)

        self.nb.AddPage(self.nucleotide_page, 'Nucleotide')
        self.nb.AddPage(self.protein_page, 'Amino Acid')

        right_vbox.Add(self.nb, 1, wx.EXPAND)

        bottom_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.back_btn = wx.Button(self, label='Back')
        self.visualize_btn = wx.Button(self, label = 'Visualize')
        self.visualize_btn.Bind(wx.EVT_BUTTON, self.visualize)
        bottom_hbox.Add(self.back_btn, 0, wx.ALIGN_LEFT | wx.ALIGN_BOTTOM)
        bottom_hbox.Add(wx.BoxSizer(wx.VERTICAL), 1)
        bottom_hbox.Add(self.visualize_btn, 0, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)
        vbox.Add(bottom_hbox, 1, wx.ALIGN_BOTTOM | wx.EXPAND | wx.ALL, 10)

        self.SetSizer(vbox)

    def import_seq1(self, event):
        seq1 = ''
        filetype = self.getFiletype()
        if filetype:
            seq1 = self.get_seq(filetype)
        if seq1:
            self.seq1_txt_ctrl.SetValue(seq1)

    def import_seq2(self, event):
        seq2 = ''
        filetype = self.getFiletype()
        if filetype:
            seq2 = self.get_seq(filetype)
        if seq2:
            self.seq2_txt_ctrl.SetValue(seq2)

    def getFiletype(self):
        filetype = ''
        dlg = wx.SingleChoiceDialog(self, message='Choose a file type.', caption='Choose a file type.', choices=['Plain text', 'FASTA'])
        if dlg.ShowModal() == wx.ID_OK:
            filetype = dlg.GetStringSelection()
        dlg.Destroy()
        return filetype

    def get_seq(self, filetype):
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


    def visualize(self, event):        
        current_page = self.nb.GetCurrentPage()
        seq1 = self.seq1_txt_ctrl.GetValue()
        for c1 in seq1:
            if c1 not in current_page.alphabet:
                dlg = wx.MessageDialog(self, 'Sequence u contains invalid characters.', 'Invalid Sequence', wx.OK | wx.ICON_ERROR)
                dlg.ShowModal() 
                dlg.Destroy()
                return
        seq2 = self.seq2_txt_ctrl.GetValue()
        for c2 in seq2:
            if c2 not in current_page.alphabet:
                dlg = wx.MessageDialog(self, 'Sequence v contains invalid characters.', 'Invalid Sequence', wx.OK | wx.ICON_ERROR)
                dlg.ShowModal() 
                dlg.Destroy()
                return
        local = self.local_radio_btn.GetValue()

        scores = [[0 for i in range(len(current_page.alphabet))] for i in range(len(current_page.alphabet))]
        for i in range(1, len(current_page.alphabet)):
            for j in range(i, len(current_page.alphabet)+1):
                if j >= i:
                    contents = current_page.scoring_grid.FindItemAtPosition((i,j)).GetWindow().GetValue()
                    try:
                        float(contents)
                    except ValueError:
                        dlg = wx.MessageDialog(self, 'Cell ({0},{1}) of the scoring matrix does not contain a valid floating point number.'.format(i,j), 'Invalid Float', wx.OK | wx.ICON_ERROR)
                        dlg.ShowModal() 
                        dlg.Destroy()
                        return
                    scores[i-1][j-1] = float(contents)
        for i in range(len(current_page.alphabet)):
            for j in range(i):
                scores[i][j] = scores[j][i]

        self.seq_matrix = seq_align.SeqAlign(seq1, seq2, scores, current_page.alphabet, local)
        self.viz_frame = seqframe.SeqFrame(self, self.seq_matrix)


class SeqAlphaPanel(wx.Panel):
    def __init__(self, parent, alphabet):
        wx.Panel.__init__(self, parent)
        self.alphabet = alphabet

        vbox = wx.BoxSizer(wx.VERTICAL)
        matrix_box = wx.StaticBoxSizer( wx.StaticBox(self, label="Scoring Matrix" ), wx.VERTICAL)

        self.scoring_grid = wx.GridBagSizer()
        for i in range(len(self.alphabet)):
            for j in range(len(self.alphabet) + 1):
                if i == 0:
                    if j == 0:
                        self.scoring_grid.Add(wx.StaticText(self), (i,j), flag=wx.EXPAND)
                    else:
                        self.scoring_grid.Add(wx.StaticText(self, label=self.alphabet[j-1]), (i,j), flag=wx.ALIGN_CENTER)
                elif j == 0:
                    self.scoring_grid.Add(wx.StaticText(self, label=self.alphabet[i-1]), (i,j), flag=wx.EXPAND)
                elif j>=i:
                    self.scoring_grid.Add(wx.TextCtrl(self, size = (35, -1)), (i,j), flag=wx.EXPAND)
                else:
                    self.scoring_grid.Add(wx.StaticText(self), (i,j), flag=wx.EXPAND)

        self.import_btn = wx.Button(self, label = 'Import from File')


        match_txt = wx.StaticText(self, label='Update Match Score:')
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.match_score_txt = wx.TextCtrl(self, size=(35, -1))
        self.match_btn = wx.Button(self, label='Update')
        self.match_btn.Bind(wx.EVT_BUTTON, self.updateMatch)
        hbox1.Add(self.match_score_txt, 0, wx.LEFT, 5)
        hbox1.Add(self.match_btn, 0, wx.LEFT, 10)

        mismatch_txt = wx.StaticText(self, label='Update Mismatch Score:')
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.mismatch_score_txt = wx.TextCtrl(self, size=(35, -1))
        self.mismatch_btn = wx.Button(self, label='Update')
        self.mismatch_btn.Bind(wx.EVT_BUTTON, self.updateMismatch)
        hbox2.Add(self.mismatch_score_txt, 0, wx.LEFT, 5)
        hbox2.Add(self.mismatch_btn, 0, wx.LEFT, 10)

        indel_txt = wx.StaticText(self, label='Update Indel Score:')
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.indel_score_txt = wx.TextCtrl(self, size=(35, -1))
        self.indel_btn = wx.Button(self, label='Update')
        self.indel_btn.Bind(wx.EVT_BUTTON, self.updateIndel)
        hbox3.Add(self.indel_score_txt, 0, wx.LEFT, 5)
        hbox3.Add(self.indel_btn, 0, wx.LEFT, 10)

        matrix_box.Add(self.scoring_grid, 0)

        vbox.Add(matrix_box, 0, wx.EXPAND)
        vbox.Add(self.import_btn, 0, wx.ALL, 5)
        vbox.Add(match_txt, 0)
        vbox.Add(hbox1, 0, wx.EXPAND)
        vbox.Add(mismatch_txt, 0, wx.TOP, 5)
        vbox.Add(hbox2, 0, wx.EXPAND)
        vbox.Add(indel_txt, 0, wx.TOP, 5)
        vbox.Add(hbox3, 0, wx.EXPAND)

        self.SetSizer(vbox)

    def updateMatch(self, event):
        match_score = self.match_score_txt.GetValue()
        try:
            float(match_score)
        except ValueError:
            dlg = wx.MessageDialog(self, 'Please enter a valid floating point number.', 'Invalid Float', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return
        for i in range(1, len(self.alphabet)):
            self.scoring_grid.FindItemAtPosition((i,i)).GetWindow().SetValue(match_score)

    def updateMismatch(self, event):
        mismatch_score = self.mismatch_score_txt.GetValue()
        try:
            float(mismatch_score)
        except ValueError:
            dlg = wx.MessageDialog(self, 'Please enter a valid floating point number.', 'Invalid Float', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return
        for i in range(1, len(self.alphabet)):
            for j in range(i+1, len(self.alphabet)):
                self.scoring_grid.FindItemAtPosition((i,j)).GetWindow().SetValue(mismatch_score)

    def updateIndel(self, event):
        indel_score = self.indel_score_txt.GetValue()
        try:
            float(indel_score)
        except ValueError:
            dlg = wx.MessageDialog(self, 'Please enter a valid floating point number.', 'Invalid Float', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal() 
            dlg.Destroy()
            return
        for i in range(1, len(self.alphabet)):
            self.scoring_grid.FindItemAtPosition((i,len(self.alphabet))).GetWindow().SetValue(indel_score)