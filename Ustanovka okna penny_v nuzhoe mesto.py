import sys
import wx
from time import clock
import win32ui, win32gui, win32con, win32api
import json

class MyForm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Screenshot Tutorial",size=(600, 300) )

        panel = wx.Panel(self)
        screenshotBtn = wx.Button(panel, label="Place window")
        screenshotBtn.Bind(wx.EVT_BUTTON, self.onPlacewindow)
        wx.StaticText(panel, -1, "Название окна:", pos=(10, 12))  # label статичный текст - "Pos:"
        self.posCtrl = wx.TextCtrl(panel, -1, "penny roulette - william hill casino", pos=(100, 10),size=(350,20) )  # создаем атрибут - окно Edit - текстовое
        # окошко и называем его posCtrl
        printBtn = wx.Button(panel, label="Get Place Window")
        printBtn.Bind(wx.EVT_BUTTON, self.onPlacewindow)
        panel.SetBackgroundColour(wx.WHITE)
        #
        # self.SetTransparent(200)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(screenshotBtn, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(printBtn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(sizer)
        #self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))

    def onPlacewindow(self, event):
        # """

        start1 = clock()
        btn = event.GetEventObject().GetLabel()
        toplist, winlist = [], []  # пустые списки куда будут запихиваться хандлы окон                      #европейская рулетка премиум - william hill casino
        nameWindow = (self.posCtrl.GetValue()).lower()

        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(enum_cb, toplist)
        print(winlist)
        windowToInterest = [(hwnd, title) for hwnd, title in winlist if nameWindow  in title.lower()]  # получение хендла по title
        # just grab the hwnd for first window matching firefox
        print(len(windowToInterest))
        # if len(firefox1)==1:
        hwnd1 = windowToInterest
        print(repr(hwnd1))
        firefox = windowToInterest[0]  # мы тут отсекли название окна
        hwnd = firefox[0]
        print(repr(hwnd))
        # y = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN) # получаем координату Y(начало в данном случае Y=0)
        win32gui.SetForegroundWindow(hwnd)  # выводит на передний план окно
        if btn == 'Get Place Window':
           place = win32gui.GetWindowPlacement(hwnd)
           print('place', place)
           with open('WindowPlace.txt', 'w') as jsonfile: json.dump(place, jsonfile)
        # win32gui.SetWindowPlacement(hwnd,(0, 1, (-1, -1), (-1, -1), (1922, 0, 2720, 474)))
        if btn == 'Place window':
            with open('WindowPlace.txt', 'r') as f:  # извлекаем  из файла
                place = json.load(f)

            win32gui.SetWindowPlacement(hwnd,place)
        end1 = clock()

        print("Result (iterativ): выполняется за " + "\nФункция %1.10f секунд" % (end1 - start1))


# Запустите программу
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
