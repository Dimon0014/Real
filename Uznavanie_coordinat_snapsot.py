#!/usr/bin/python

# bitmap.py
import time
import json
import wx
import win32ui, win32gui, win32con, win32api
class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size = (370, 370))
        self.panel = wx.Panel(self, -1)
        self.btn1 = wx.Button(self.panel, label="Сканировать координаты")
        self.bitmap = wx.Bitmap('myImage_frame_r.bmp')
        self.w_img = self.bitmap.GetWidth()
        self.h_img = self.bitmap.GetHeight()
        #wx.EVT_PAINT(self, self.OnPaint)
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Centre()
        self.panel.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn1)
        self.SetTransparent(150)

    def OnButton(self, event):
        """Called when self.btn1 is clicked"""

        # self.panel.BackgroundColour = wx.WHITE
        f = self.coordWindow('framecoordscan')
        pos = self.panel.GetSize()
        self.w_img
        self.h_img
        verhn_lev_ugol_x = self.w_img/2
        verhn_lev_ugol_y = self.h_img/2
        x_cord = pos.x/2 + f[0]  + 9 -  int(verhn_lev_ugol_x)# гдобальная координата х # 7 - похоже на 3+3  или 4+4 бордюры по бокам# сейчас -1 пиксель учитывает красную рамку
        y_cord = pos.y/2 + f[1] + 28 - int(verhn_lev_ugol_y) # гдобальная координата y # 28 - похоже на 30 ширина панели вверху# сейчас -1 пиксель учитывает красную рамку
        #self.posCtrl.SetValue("%s, %s" % (x_cord, y_cord))
        x_cord2 = x_cord +self.w_img
        y_cord2 = y_cord +self.h_img
        x_cord = int(x_cord)
        y_cord = int(y_cord)
        x_cord2 = int(x_cord2)
        y_cord2 = int(y_cord2)
        coordinaty_snap = [x_cord,y_cord,x_cord2,y_cord2]
        with open('coord_snapshot_amount_stavki.txt', 'w') as jsonfile: json.dump(coordinaty_snap, jsonfile)  # сохраняем в файл


        # for i in range(len(self.coord_hlp)):




    def OnSize(self, event):
        self.Refresh(False)


    def OnPaint(self, event):
        dc = wx.PaintDC(self.panel)
        wdx, wdy = self.panel.GetSize()
        ox = (wdx - self.w_img) / 2
        oy = (wdy - self.h_img) / 2
        # print(ox, oy)
        dc.DrawBitmap(self.bitmap,  ox, oy)
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


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'FrameCoordScan')
        frame.Show(True)
        self.SetTopWindow(frame)



        return True

app = MyApp(0)
app.MainLoop()