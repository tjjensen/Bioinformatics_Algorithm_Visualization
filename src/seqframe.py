import wx
import wx.richtext as rt
import seq_align
import viz_matrix

DESCRIPTION = ('Pairwise Sequence Alignment\n' +
    'Sequence alignment is used in bioinformatics to access the functional, structural, and evolutionary relationship between sequences of DNA, RNA, and protein. The Needleman-Wunsch algorithm attempts to find a global alignment, which include every residue of the aligned sequences. It does so by computing an alignment matrix row by row. The matrix and the decisions made while filling the matrix are then used to back-trace the alignment between the two sequences. The Smith-Waterman algorithm works similarly for local alignments.\n' +
    'In this visualization, The alignment matrix fills up rowwise, with arrows indicating the different choices at an step of the alignment. After the matrix is filled, a  path is traced using the arrows to develop the resulting alignment.')

class SeqFrame(wx.Frame):
    def __init__(self, parent, align_mat):
        wx.Frame.__init__(self, parent, title = 'Sequence Alignment', size=(800,700))

        self.panel = SeqPanel(self, align_mat)
        self.Show(True)


class SeqPanel(wx.Panel):
    def __init__(self, parent, align_mat):
        wx.Panel.__init__(self, parent)

        self.align_count = 0
        self.forward_timer = True
        self.align_mat = align_mat
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timeUpdate, self.timer)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        row_titles = list('v' + align_mat.seq2)
        col_titles = list('u' + align_mat.seq1)
        row_titles[0] = 'Seq v'
        col_titles[0] = 'Seq u'

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.drawing_panel = DrawingPanel(self, align_mat.S, align_mat.D, row_titles, col_titles)
        alignment_static_txt = wx.StaticText(self, label='Alignment:')
        self.alignment_txt = wx.TextCtrl(self, size=(-1, 60),style=wx.TE_READONLY | wx.HSCROLL | wx.TE_MULTILINE)
        font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL, False)
        self.alignment_txt.SetFont(font)
        self.alignment_txt.SetValue('Sequence u:\nSequence v:')
        vbox1.Add(self.drawing_panel, 1, wx.EXPAND)
        vbox1.Add(alignment_static_txt, 0, wx.ALL, 4)
        vbox1.Add(self.alignment_txt, 0, wx.EXPAND)


        self.description_text = rt.RichTextCtrl(self, size=(300,400), style=rt.RE_READONLY)
        self.description_text.GetCaret().Hide()
        for line in DESCRIPTION.splitlines():
            self.description_text.AddParagraph(line)

        hbox1.Add(vbox1, 1, wx.EXPAND)
        hbox1.Add(self.description_text, 0, wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
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

        hbox.Add(self.pause_resume_btn, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)
        hbox.Add(time_static_txt, 0, wx.LEFT | wx.BOTTOM | wx.ALIGN_BOTTOM, 10)
        hbox.Add(self.time_txt_ctrl, 0, wx.BOTTOM | wx.LEFT | wx.ALIGN_BOTTOM, 6)
        hbox.AddStretchSpacer()

        hbox.Add(self.previous_btn, 0,  wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 5)
        hbox.Add(self.next_btn, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 5)
        hbox.AddSpacer(10)
        hbox.Add(self.restart_btn, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 5)
        hbox.Add(self.finish_btn, 0,  wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 5)

        vbox.Add(hbox1, 1, wx.EXPAND)
        vbox.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        self.SetSizer(vbox)

    def timeUpdate(self, event):
        self.matrixUpdate(self.forward_timer)

    def matrixUpdate(self, is_forward):
        if is_forward:
            success = self.align_mat.proceedForward()
            if success:
                self.drawing_panel.matrix.data = self.align_mat.S
                self.drawing_panel.matrix.dmatrix = self.align_mat.D
                self.drawing_panel.Refresh()
            else:
                alignment = self.align_mat.getAlignment()
                if self.align_count > len(alignment) - 1:
                    return
                self.align_count = self.align_count + 1
                cell_colors = [['#ffffff' for i in range(len(self.align_mat.S[0]))] for j in range(len(self.align_mat.S))]
                for i in range(self.align_count):
                    cell_colors[alignment[i][0]][alignment[i][1]] = '#cccccc'
                self.drawing_panel.matrix.cell_colors = cell_colors
                self.drawing_panel.Refresh()
                seq1 = ''
                seq2 = ''
                prev_align = alignment[0]
                for i in range(1, len(alignment)):
                    current_align = alignment[i]
                    if prev_align[1] == current_align[1]:
                        seq1 += '-'
                        seq2 += self.align_mat.seq2[prev_align[0]-1]
                    elif prev_align[0] == current_align[0]:
                        seq1 += self.align_mat.seq1[prev_align[1]-1]
                        seq2 += '-'
                    else:
                        seq1 += self.align_mat.seq1[prev_align[1]-1]
                        seq2 += self.align_mat.seq2[prev_align[0]-1]
                    prev_align = current_align
                self.alignment_txt.SetValue('Sequence u: {0}\nSequence v: {1}'.format(seq1[self.align_count-1::-1], seq2[self.align_count-1::-1]))

        else:
            if self.align_count > 0:
                alignment = self.align_mat.getAlignment()
                self.align_count -= 1
                cell_colors = [['#ffffff' for i in range(len(self.align_mat.S[0]))] for j in range(len(self.align_mat.S))]
                for i in range(self.align_count):
                    cell_colors[alignment[i][0]][alignment[i][1]] = '#cccccc'
                self.drawing_panel.matrix.cell_colors = cell_colors
                self.drawing_panel.Refresh()
                seq1 = ''
                seq2 = ''
                prev_align = alignment[0]
                for i in range(1, len(alignment)):
                    current_align = alignment[i]
                    if prev_align[1] == current_align[1]:
                        seq1 += '-'
                        seq2 += self.align_mat.seq2[prev_align[0]-1]
                    elif prev_align[0] == current_align[0]:
                        seq1 += self.align_mat.seq1[prev_align[1]-1]
                        seq2 += '-'
                    else:
                        seq1 += self.align_mat.seq1[prev_align[1]-1]
                        seq2 += self.align_mat.seq2[prev_align[0]-1]
                    prev_align = current_align
                if self.align_count > 0:

                    self.alignment_txt.SetValue('Sequence u: {0}\nSequence v: {1}'.format(seq1[self.align_count-1::-1], seq2[self.align_count-1::-1]))
                else:
                    self.alignment_txt.SetValue('Sequence u:\nSequence v:')

            else:
                success = self.align_mat.proceedBackward()
                self.alignment_txt.SetValue('Sequence u:\nSequence v:')
                if success:
                    self.drawing_panel.matrix.data = self.align_mat.S
                    self.drawing_panel.matrix.dmatrix = self.align_mat.D
                    self.drawing_panel.Refresh()


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
        self.matrixUpdate(False)

    def nextTraverse(self, event):
        self.matrixUpdate(True)

    def restart(self, event):
        success = self.align_mat.restart()
        if success:
            self.drawing_panel.matrix.data = self.align_mat.S
            self.drawing_panel.matrix.dmatrix = self.align_mat.D
            self.align_count = 0
            self.drawing_panel.matrix.cell_colors = [['#ffffff' for i in range(len(self.align_mat.S[0]))] for j in range(len(self.align_mat.S))]
            self.drawing_panel.Refresh()
            self.alignment_txt.SetValue('Sequence u:\nSequence v:')


    def finish(self, event):
        success = self.align_mat.finish()
        if success:
            self.drawing_panel.matrix.data = self.align_mat.S
            self.drawing_panel.matrix.dmatrix = self.align_mat.D
            alignment = self.align_mat.getAlignment()
            self.align_count = len(alignment) - 1
            cell_colors = [['#ffffff' for i in range(len(self.align_mat.S[0]))] for j in range(len(self.align_mat.S))]
            for i in range(self.align_count):
                cell_colors[alignment[i][0]][alignment[i][1]] = '#cccccc'
            self.drawing_panel.matrix.cell_colors = cell_colors
            self.drawing_panel.Refresh()
            seq1 = ''
            seq2 = ''
            prev_align = alignment[0]
            for i in range(1, len(alignment)):
                current_align = alignment[i]
                if prev_align[1] == current_align[1]:
                    seq1 += '-'
                    seq2 += self.align_mat.seq2[prev_align[0]-1]
                elif prev_align[0] == current_align[0]:
                    seq1 += self.align_mat.seq1[prev_align[1]-1]
                    seq2 += '-'
                else:
                    seq1 += self.align_mat.seq1[prev_align[1]-1]
                    seq2 += self.align_mat.seq2[prev_align[0]-1]
                prev_align = current_align
            self.alignment_txt.SetValue('Sequence u: {0}\nSequence v: {1}'.format(seq1[::-1], seq2[::-1]))
                

class DrawingPanel(wx.ScrolledWindow):
    X_SCROLL_SPEED = 10
    Y_SCROLL_SPEED = 10
    EXTRA_SIZE = 20
    def __init__(self, parent, matrix, direction_matrix, row_titles, col_titles):
        wx.ScrolledWindow.__init__(self, parent)
        self.dmatrix = direction_matrix
        self.matrix = viz_matrix.VizMatrix(matrix, row_titles=row_titles, col_titles=col_titles, dmatrix=self.dmatrix)
        self.SetBackgroundColour('white')
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetScrollbars(DrawingPanel.X_SCROLL_SPEED, DrawingPanel.Y_SCROLL_SPEED, 0, 0)

    def OnPaint(self, event):
        self.SetVirtualSize(self.get_expected_size())
        dc = wx.PaintDC(self)       
        self.DoPrepareDC(dc)
        self.matrix.drawMatrix(dc)

    def get_expected_size(self):
        return self.matrix.getSize()[0] + DrawingPanel.EXTRA_SIZE, self.matrix.getSize()[1] + DrawingPanel.EXTRA_SIZE

if __name__ == '__main__':

    app = wx.App(redirect=False) 
    SeqFrame(None)
    app.MainLoop()
