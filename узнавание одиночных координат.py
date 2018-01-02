import wx
import time
import json
import win32ui, win32gui, win32con, win32api

class OtherFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "win scan x y", size=wx.Size(600, 400))
        self.panel = wx.Panel(self)
        # Собственно меняющийся текст подсказка
        msg = "Кликните на кнопке запуска"
        self.instructions = wx.StaticText(self.panel, label=msg)

        self.msgTxt = wx.TextCtrl(self.panel, value="000")
        # self.posCtrl = wx.TextCtrl(self.panel, -1, "пусто", pos=(40, 10))
        closeBtn = wx.Button(self.panel, label="Запуск сканера")
        closeBtn.Bind(wx.EVT_BUTTON, self.Run_loop)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.onClick)
        self.SetTransparent(160)
        sizer = wx.BoxSizer(wx.VERTICAL)
        flags = wx.ALL | wx.CENTER
        sizer.Add(self.instructions, 0, flags, 2)
        sizer.Add(self.msgTxt, 0, flags, 2)  # тут у едита сайзер есть!
        # так что абсолютные значения позиционирования не нужны
        sizer.Add(closeBtn, 0, flags, 2)
        self.panel.SetSizer(sizer)

        self.coord_hlp = [0] * 2

        self.coord_name = ['vibor perv clika', 'vibor vtor clika']
       # print('6-',self.coord_name[6])
        self.coord = []
        self.i = 0

    def onClick(self, event):
        # self.panel.BackgroundColour = wx.WHITE

        #pos = event.GetPosition()
        f = self.coordWindow('win scan x y')
        pos = event.GetPosition()
        pos.x = pos.x + f[0] + 8  # гдобальная координата х
        pos.y = pos.y + f[1] + 30  # гдобальная координата y
        self.msgTxt.SetValue("%s, %s" % (pos.x, pos.y))
        for i in range(len(self.coord_hlp)):
            if self.coord_hlp[i] == 0:
                x = pos.x
                y = pos.y
                list = [self.coord_name[i], (x, y)]
                self.coord.append(list)
                self.coord_hlp[i] = 1
                print('coordinat_hlp', 'i=', i)

                self.i += 1
                if self.i < len(self.coord_hlp):
                    msg2 = "Кликните по координате %s" % self.coord_name[self.i]
                    self.instructions.SetLabel(msg2)
                # msg3 = "Кликните на кнопке запуска снова"
                # self.instructions.SetLabel(msg3)
                if self.i == len(self.coord_hlp):
                    #print(self.coord)
                    with open('xy_coord_snjatia_stavki.txt', 'w') as jsonfile: json.dump(self.coord, jsonfile)
                break

    # ----------------------------------------------------------------------
    def Run_loop(self, event):
        """
        Send a message and close frame
        """
        print(self.coord_hlp)

        if self.coord_hlp[self.i] == 0:
            msg2 = "Кликните по координате %s" % self.coord_name[self.i]

            self.instructions.SetLabel(msg2)
            print('i в лупе =', self.i)
            # time.sleep(2)
            #  my_string = "Я люблю %s" % "Python"
            # '%d %s, %d %s' % (6, 'bananas', 10, 'lemons')
            # msg = self.msgTxt.GetValue()

            # self.Close()
    def coordWindow(self, title_name):
        toplist, winlist = [], []  # пустые списки куда будут запихиваться хандлы окон                      #европейская рулетка премиум - william hill casino

        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(enum_cb, toplist)
        #print(winlist)
        my_window = [(hwnd, title) for hwnd, title in winlist if
                     title_name in title.lower()]  # получение хендла по title
        #print('len my_window', len(my_window))
        hwnd1 = my_window
        #print('repr', repr(hwnd1))

        my_window = my_window[0]  # мы тут отсекли название(вернее хандл по названию) окна из кучи всех названий
        hwnd = my_window[0]  # мы тут отсекли название (вернее хандл по названию)окна из кучи всех названий

        #print(repr(hwnd))
        # y = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN) # получаем координату Y(начало в данном случае Y=0)
        # win32gui.SetForegroundWindow(hwnd)  # выводит на передний план окно
        hwndD = win32gui.GetWindowRect(hwnd)  # Returns the rectangle for a window in screen coordinates
        return hwndD



########################################################################
class MainPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent

        # Publisher().subscribe(self.showFrame, ("show.mainframe"))

        self.pubsubText = wx.TextCtrl(self, value="")
        xyBtn = wx.Button(self, label="Окно сканирования(x,y)")
        xyBtn.Bind(wx.EVT_BUTTON, self.hideFrame)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.pubsubText, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(xyBtn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(sizer)

    # ----------------------------------------------------------------------
    def hideFrame(self, event):
        """"""
        # self.frame.Hide()
        new_frame = OtherFrame()
        new_frame.Show()

    # ----------------------------------------------------------------------
    def showFrame(self, msg):
        """
        Shows the frame and shows the message sent in the
        text control

        """
        self.pubsubText.SetValue(msg.data)
        frame = self.GetParent()
        frame.Show()


########################################################################
class MainFrame(wx.Frame):
    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Pubsub Tutorial")
        panel = MainPanel(self)


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
