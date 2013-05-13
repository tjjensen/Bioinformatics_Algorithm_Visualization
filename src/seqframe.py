import wx
import seq_align
import viz_matrix

class SeqFrame(wx.Frame):
    def __init__(self, parent, align_mat):
        wx.Frame.__init__(self, parent, title = 'Sequence Alignment', size=(600,600))

        self.panel = SeqPanel(self, align_mat)
        self.Show(True)


class SeqPanel(wx.Panel):
    def __init__(self, parent, align_mat):
        wx.Panel.__init__(self, parent)

        self.forward_timer = True
        self.align_mat = align_mat
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timeUpdate, self.timer)

        vbox = wx.BoxSizer(wx.VERTICAL)

        row_titles = list('v' + align_mat.seq2)
        col_titles = list('u' + align_mat.seq1)
        row_titles[0] = 'Seq v'
        col_titles[0] = 'Seq u'
        self.drawing_panel = DrawingPanel(self, align_mat.S, align_mat.D, row_titles, col_titles)


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

        vbox.Add(self.drawing_panel, 1, wx.EXPAND)
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
            success = self.align_mat.proceedBackward()
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
            self.drawing_panel.Refresh()


    def finish(self, event):
        success = self.align_mat.finish()
        if success:
            self.drawing_panel.matrix.data = self.align_mat.S
            self.drawing_panel.matrix.dmatrix = self.align_mat.D
            self.drawing_panel.Refresh()

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
