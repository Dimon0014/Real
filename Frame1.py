#Boa:Frame:Frame1

import wx
import wx.lib.buttons

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1BUTTON2, wxID_FRAME1BUTTON3, 
 wxID_FRAME1BUTTON4, wxID_FRAME1BUTTON5, wxID_FRAME1BUTTON6, 
 wxID_FRAME1GENBUTTON1, wxID_FRAME1NOTEBOOK1, wxID_FRAME1PANEL1, 
 wxID_FRAME1PANEL2, wxID_FRAME1PANEL3, wxID_FRAME1PANEL4, wxID_FRAME1PANEL5, 
 wxID_FRAME1STATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(15)]

class Frame1(wx.Frame):
    def _init_coll_notebook1_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel2, select=True, text='Pages0')
        parent.AddPage(imageId=-1, page=self.panel3, select=False,
              text='Pages1')
        parent.AddPage(imageId=-1, page=self.panel4, select=False,
              text='Pages2')
        parent.AddPage(imageId=-1, page=self.panel5, select=False,
              text='Pages3')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(755, 331), size=wx.Size(400, 358),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self.SetClientSize(wx.Size(384, 320))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(384, 320),
              style=wx.TAB_TRAVERSAL)

        self.notebook1 = wx.Notebook(id=wxID_FRAME1NOTEBOOK1, name='notebook1',
              parent=self.panel1, pos=wx.Point(0, 0), size=wx.Size(384, 320),
              style=0)

        self.panel2 = wx.Panel(id=wxID_FRAME1PANEL2, name='panel2',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(376, 294),
              style=wx.TAB_TRAVERSAL)

        self.panel3 = wx.Panel(id=wxID_FRAME1PANEL3, name='panel3',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(376, 294),
              style=wx.TAB_TRAVERSAL)

        self.panel4 = wx.Panel(id=wxID_FRAME1PANEL4, name='panel4',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(376, 294),
              style=wx.TAB_TRAVERSAL)

        self.panel5 = wx.Panel(id=wxID_FRAME1PANEL5, name='panel5',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(376, 294),
              style=wx.TAB_TRAVERSAL)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label='button1',
              name='button1', parent=self.panel5, pos=wx.Point(8, 16),
              size=wx.Size(75, 23), style=0)

        self.button2 = wx.Button(id=wxID_FRAME1BUTTON2, label='button2',
              name='button2', parent=self.panel5, pos=wx.Point(8, 48),
              size=wx.Size(75, 23), style=0)

        self.button3 = wx.Button(id=wxID_FRAME1BUTTON3, label='button3',
              name='button3', parent=self.panel4, pos=wx.Point(8, 16),
              size=wx.Size(75, 23), style=0)

        self.button4 = wx.Button(id=wxID_FRAME1BUTTON4, label='button4',
              name='button4', parent=self.panel4, pos=wx.Point(8, 48),
              size=wx.Size(75, 23), style=0)

        self.button5 = wx.Button(id=wxID_FRAME1BUTTON5, label='button5',
              name='button5', parent=self.panel4, pos=wx.Point(8, 80),
              size=wx.Size(75, 23), style=0)

        self.button6 = wx.Button(id=wxID_FRAME1BUTTON6, label='button6',
              name='button6', parent=self.panel3, pos=wx.Point(8, 24),
              size=wx.Size(75, 23), style=0)

        self.genButton1 = wx.lib.buttons.GenButton(id=wxID_FRAME1GENBUTTON1,
              label='genButton1', name='genButton1', parent=self.panel2,
              pos=wx.Point(8, 32), size=wx.Size(76, 25), style=0)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label='staticText1', name='staticText1', parent=self.panel2,
              pos=wx.Point(16, 16), size=wx.Size(56, 13), style=0)

        self._init_coll_notebook1_Pages(self.notebook1)

    def __init__(self, parent):
        self._init_ctrls(parent)

  


if __name__ == '__main__':
    app = wx.App()
    frame = create(None)
    frame.Show()

    app.MainLoop()
