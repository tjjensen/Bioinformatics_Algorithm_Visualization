import wx

class VizMatrix():
    def __init__(self, data, x=0, y=0, title=None, row_titles=None, col_titles=None, cell_colors=None, line_color='#000000', font_color='#000000', cell_size=40, dmatrix=None):
        self.data = data
        self.x = x
        self.y = y
        self.title = title
        self.row_titles = row_titles
        self.col_titles = col_titles
        if not cell_colors:
            cell_colors = [['#ffffff' for i in range(len(data[0]))] for j in range(len(data))]
        self.cell_colors = cell_colors
        self.line_color = line_color
        self.font_color = font_color
        self.cell_size = cell_size
        self.dmatrix = dmatrix
        if self.title:
            self.title_offset = self.cell_size
        else:
            self.title_offset = 0
        if self.row_titles:
            self.row_offset = self.cell_size
        else:
            self.row_offset = 0
        if self.col_titles:
            self.col_offset = self.cell_size
        else:
            self.col_offset = 0

    def getSize(self):
        return self.cell_size*len(self.data[0]) + self.col_offset, self.cell_size*(len(self.data)) + self.title_offset + self.row_offset

    def setCellColor(self, row, col, color):
        self.cell_colors[i][j] = color

    #Drawing methods
    def drawMatrix(self, dc):
        font = dc.GetFont()
        font.SetPixelSize((.5*self.cell_size,self.cell_size))
        font.SetFamily(wx.FONTFAMILY_SWISS)
        dc.SetFont(font)
        dc.SetTextForeground(self.font_color)
        pen = dc.GetPen()
        pen.SetColour(self.line_color)
        self.drawTitle(dc)
        self.drawAxisTitles(dc)
        self.drawColors(dc)
        self.drawData(dc)

    def drawTitle(self, dc):
        if self.title:
            dc.DrawText(self.title, self.x + self.getSize()[0]/2 - .5*self.cell_size*(len(self.title)-1)/2, self.y)

    def drawAxisTitles(self, dc):
        if self.row_titles:
            for idx, row_title in enumerate(self.row_titles):
                font = dc.GetFont()
                font.SetWeight(wx.FONTWEIGHT_LIGHT)
                font.SetPixelSize((.5*self.cell_size/len(row_title),self.cell_size/len(row_title)))
                y_extra = 0
                if len(row_title) == 2:
                    y_extra = .25*self.cell_size
                elif len(row_title) > 2:
                    y_extra = .4*self.cell_size
                dc.SetFont(font)
                dc.DrawText(row_title, self.x + .17*self.cell_size, self.y + self.title_offset + self.row_offset + idx*self.cell_size + y_extra)
        if self.col_titles:
            for idx, col_title in enumerate(self.col_titles):
                font = dc.GetFont()
                font.SetWeight(wx.FONTWEIGHT_LIGHT)
                font.SetPixelSize((.5*self.cell_size/len(col_title),self.cell_size/len(col_title)))
                y_extra = 0
                if len(col_title) == 2:
                    y_extra = .25*self.cell_size
                elif len(col_title) > 2:
                    y_extra = .4*self.cell_size
                dc.SetFont(font)
                dc.DrawText(col_title, self.x + self.col_offset + idx*self.cell_size + .17*self.cell_size, self.y + self.title_offset + y_extra)

    def drawColors(self, dc):
        x = self.x + self.col_offset        
        y = self.y + self.title_offset + self.row_offset
        for i, row_colors in enumerate(self.cell_colors):
            for j, color in enumerate(row_colors):
                dc.SetBrush(wx.Brush(color))
                dc.DrawRectangle(x + j*self.cell_size, y + i *self.cell_size,
                    self.cell_size, self.cell_size)

    def drawData(self, dc):
        x = self.x + self.col_offset
        y = self.y + self.title_offset + self.row_offset
        size = self.getSize()
        for i, row in enumerate(self.data):
            for j, cell in enumerate(row):
                if cell is not None:
                    cell_str = str(cell).rstrip('0').rstrip('.')
                    font = dc.GetFont()
                    font.SetWeight(wx.FONTWEIGHT_LIGHT)
                    font.SetPixelSize((.5*self.cell_size/len(cell_str),self.cell_size/len(cell_str)))
                    y_extra = 0
                    if len(cell_str) == 2:
                        y_extra = .25*self.cell_size
                    elif len(cell_str) > 2:
                        y_extra = .35*self.cell_size
                    dc.SetFont(font)
                    dc.DrawText(cell_str, x + j*self.cell_size + .17*self.cell_size, y + i*self.cell_size + y_extra)