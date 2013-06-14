import wx
import lloyd
import matplotlib.pyplot as plt
import wx.richtext as rt

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
DESCRIPTION = (
    'k-means clustering:\n' +
    'The k-means clustering problem involves creating k clusters of a distribution, that best separate the distribution. Lloyd\'s algorithm provides a non-optimal solution by randomly selecting cluster centers, assigning points within the distribution to the clusters, and then reevaluating the clusters so that they equal to the average of their associated points. This is continued until the association of the points no longer changes.\n'+
    'Clustering is widely used in bioinformatics for various problems, such as gene family creation and gene coexpression analysis.\n'+
    'In this visualization, cluster centers are represented with an "X" and points are represented with a dot. Cluster groups and the cluster center are represented in the same color, but if k is greater than seven, then colors are reused.')

class MeanFrame(wx.Frame):
    def __init__(self, parent, k, points):
        wx.Frame.__init__(self, parent, title = 'k-Means', size=(800,700))

        self.panel = MeanDrawingPanel(self, k, points)
        self.Show(True)

class MeanDrawingPanel(wx.Panel):
    def __init__(self, parent, k, points):
        wx.Panel.__init__(self, parent)

        self.forward_timer = True
        self.k = k
        self.points = points
        self.clusters, self.associations = lloyd.lloyd(k, points)
        self.step_index = 0
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timeUpdate, self.timer)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.drawing_panel = DrawingPanel(self, self.points)

        self.description_text = rt.RichTextCtrl(self, size=(300,400), style=rt.RE_READONLY)
        self.description_text.GetCaret().Hide()
        for line in DESCRIPTION.splitlines():
            self.description_text.AddParagraph(line) 

        hbox.Add(self.drawing_panel, 1, wx.EXPAND)
        hbox.Add(self.description_text, 0, wx.EXPAND)

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

        self.drawing_panel.my_plot(self.clusters[0], self.associations[0])

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
        cluster = self.clusters[self.step_index]
        association = self.associations[self.step_index]
        self.drawing_panel.my_plot(cluster, association)
        
    def nextTraverse(self, event):
        if self.step_index >= len(self.clusters) - 1:
            return
        self.step_index += 1
        cluster = self.clusters[self.step_index]
        association = self.associations[self.step_index]
        self.drawing_panel.my_plot(cluster, association)



    def restart(self, event):
        self.step_index = 0
        cluster = self.clusters[self.step_index]
        association = self.associations[self.step_index]
        self.drawing_panel.my_plot(cluster, association)


    def finish(self, event):
        self.step_index = len(self.clusters) - 1
        cluster = self.clusters[self.step_index]
        association = self.associations[self.step_index]
        self.drawing_panel.my_plot(cluster, association)

class DrawingPanel(wx.ScrolledWindow):
    def __init__(self, parent, points):
        wx.ScrolledWindow.__init__(self, parent)
        self.bitmap = None
        self.points = points
        self.SetBackgroundColour(wx.WHITE)
        self.SetScrollRate(5,5)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def my_plot(self, centers, association):
        fig = plt.figure()
        xs = list()
        ys = list()
        for x, y in self.points:
            xs.append(x)
            ys.append(y)
        xc = list()
        yc = list()
        for x, y in centers:
            xc.append(x)
            yc.append(y)
        for a in set(association):
            for i, point in enumerate(self.points):
                if association[i] == a:
                    plt.plot([xs[i]], [ys[i]], colors[a%len(colors)]+'o')
            plt.plot([xc[a]],[yc[a]], colors[a%len(colors)]+'x')
        x_min, x_max = lloyd.getXrange(self.points)
        y_min, y_max = lloyd.getYrange(self.points)
        plt.axis([x_min-.2*(x_max-x_min), x_max+.2*(x_max-x_min), y_min-.2*(y_max-y_min), y_max+.2*(y_max-y_min)])
        plt.title('k-Means')
        img_file = 'test.png'
        plt.savefig(img_file)
        if self.bitmap:
            self.bitmap.Destroy()
        self.bitmap = wx.Image(img_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.Refresh()

    def OnPaint(self, event):
        self.SetVirtualSize(self.bitmap.GetSize())
        dc = wx.PaintDC(self)       
        self.DoPrepareDC(dc)
        dc.DrawBitmap(self.bitmap, 0, 0)
