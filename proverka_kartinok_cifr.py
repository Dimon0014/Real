# snapshot и сравнивает с картинкой из файла
import json
import sys
import wx
from time import clock
import win32ui, win32gui, win32con, win32api


class MyForm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Proverka_cifr")

        panel = wx.Panel(self)
        screenshotBtn = wx.Button(panel, label="Proverka cifr")
        screenshotBtn.Bind(wx.EVT_BUTTON, self.proverkaCifr)
       # printBtn = wx.Button(panel, label="Print Screenshot")
        #printBtn.Bind(wx.EVT_BUTTON, self.onPrint)
        panel.SetBackgroundColour(wx.WHITE)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(screenshotBtn, 0, wx.ALL | wx.CENTER, 5)
        #sizer.Add(printBtn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(sizer)

    def pix_to_pix(self):
        print('вызов pix_to_pix')
        for i in range(0, 38):
            for k in range(0, 38):
                name =str(i)+'.bmp'
                bmp01 = wx.Image(name, type=wx.BITMAP_TYPE_ANY)
                name = str(k) + '.bmp'
                bmp02 = wx.Image(name, type=wx.BITMAP_TYPE_ANY)
                p01 = bmp01.GetData()
                p02 = bmp02.GetData()
                if p01 == p02:
                    print('Совпадение: i =', i, 'k =', k)
                    #break
    def proverkaCifr(self, event):
        start1 = clock()
        self.pix_to_pix()

        end1 = clock()

        print("Result (iterativ): выполняется за " + "\nФункция %1.10f секунд" % (end1 - start1))


        # Запустите программу


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()