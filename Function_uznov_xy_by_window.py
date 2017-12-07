import wx
import win32ui, win32gui, win32con, win32api


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "My Frame", size=(300, 300))
        self.panel = wx.Panel(self,
                              -1)  # панель на которой распалагаются элементы управления, Frame - это просто рамка, -1 это индификатор через который панель и фрейм соеденяются
        self.panel.SetBackgroundColour('#FF6400')
        self.panel.SetBackgroundColour(wx.WHITE)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.onClick)
        # self.panel.Bind(wx.EVT_MOTION, self.OnMove) # связываем панель и событие MOTION(движение мыши по панели)
        # с обработчиком OnMove()
        wx.StaticText(self.panel, -1, "Pos:", pos=(10, 12))  # label статичный текст - "Pos:"
        self.posCtrl = wx.TextCtrl(self.panel, -1, "333", pos=(40, 10))  # создаем атрибут - окно Edit - текстовое
        # окошко и называем его posCtrl
        # https://www.youtube.com/watch?v=cp1ZeMisTNo&list=PLejTrt5hn2r1uzZ53GDeUElXRkRFbUmQd&index=2
        button = wx.Button(self.panel, label='Exit', pos=(170, 10), size=(60, 30))  # создали кнопку

        # self.SetTransparent(150)

    def OnMove(self, event):  # Передаем функции событие(event) в данном случае wx.EVT_MOTION
        pos = event.GetPosition()
        self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))

    def onClick(self, event):
        # self.panel.BackgroundColour = wx.WHITE
        f = self.coordWindow('my frame')
        pos = event.GetPosition()
        x_cord = pos.x + f[0] + 4  # гдобальная координата х
        y_cord = pos.y + f[1] + 4  # гдобальная координата y
        self.posCtrl.SetValue("%s, %s" % (x_cord, y_cord))
        print('координаты клика на экране', x_cord, y_cord)
        print('координаты окна My Frame', f)
        # for i in range(len(self.coord_hlp)):

    #  if self.coord_hlp[i] == 0:
    # 	 x = pos.x
    # 	 y = pos.y
    # 	 list = [self.coord_name[i], (x, y)]
    # 	 self.coord.append(list)
    # 	 self.coord_hlp[i] = 1
    # 	 print('coordinat_hlp', 'i=', i)
    #
    # 	 self.i += 1
    # 	 if self.i < len(self.coord_hlp):
    # 		 msg2 = "Кликните по координате %s" % self.coord_name[self.i]
    # 		 self.instructions.SetLabel(msg2)
    # 	 # msg3 = "Кликните на кнопке запуска снова"
    # 	 # self.instructions.SetLabel(msg3)
    # 	 if self.i == len(self.coord_hlp):
    # 		 print(self.coord)
    # 		 with open('xy_coord.txt', 'w') as jsonfile: json.dump(self.coord, jsonfile)
    # 	 break

    def coordWindow(self, title_name):
        toplist, winlist = [], []  # пустые списки куда будут запихиваться хандлы окон                      #европейская рулетка премиум - william hill casino

        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(enum_cb, toplist)
        print(winlist)
        my_window = [(hwnd, title) for hwnd, title in winlist if
                     title_name in title.lower()]  # получение хендла по title
        print('len my_window', len(my_window))
        hwnd1 = my_window
        print('repr', repr(hwnd1))

        my_window = my_window[0]  # мы тут отсекли название(вернее хандл по названию) окна из кучи всех названий
        hwnd = my_window[0]  # мы тут отсекли название (вернее хандл по названию)окна из кучи всех названий

        print(repr(hwnd))
        # y = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN) # получаем координату Y(начало в данном случае Y=0)
        # win32gui.SetForegroundWindow(hwnd)  # выводит на передний план окно
        hwndD = win32gui.GetWindowRect(hwnd)  # Returns the rectangle for a window in screen coordinates
        return hwndD


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()