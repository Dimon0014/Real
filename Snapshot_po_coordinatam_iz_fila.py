import sys
import wx
from time import clock
import win32ui, win32gui, win32con, win32api
import json

class MyForm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Screenshot Tutorial")

        panel = wx.Panel(self)
        screenshotBtn = wx.Button(panel, label="Take Screenshot")
        screenshotBtn.Bind(wx.EVT_BUTTON, self.onTakeScreenShot)
       # printBtn = wx.Button(panel, label="Print Screenshot")
        #printBtn.Bind(wx.EVT_BUTTON, self.onPrint)
        panel.SetBackgroundColour(wx.WHITE)
        self.SetTransparent(200)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(screenshotBtn, 0, wx.ALL | wx.CENTER, 5)
        #sizer.Add(printBtn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(sizer)

    def onTakeScreenShot(self, event):
        # """
        # Делает скриншот выбранного фрагмента экрана
        # Основано на методе, предложенном Андреа Гавана
        start1 = clock()
        with open('coord_snapshot_vhoda.txt', 'r') as f:  # извлекаем  из файла
            data2 = json.load(f)
        print('', data2)
        rect1 = data2 #win32gui.GetWindowRect(hwnd)

       # mfcDC = win32ui.CreateDCFromHandle(hwnd)
        print('rect', rect1)

        rect = self.GetRect() #  получаем координаты своего окна
        rect.x = rect1[0]#+134
        rect.y = rect1[1]#+275
        rect.width = rect1[2]-rect1[0]#+1080)
        rect.height = rect1[3]- rect1[1]#+691)
        #print('координаты', rect.x, rect.y, rect.width, rect.height)
        # Настройка ширины для Linux обнаружено Джоном Торресом
        # http://article.gmane.org/gmane.comp.python.wxpython/67327
        if sys.platform == 'linux2':
            client_x, client_y = self.ClientToScreen((0, 0))
            border_width = client_x - rect.x
            title_bar_height = client_y - rect.y
            rect.width += (border_width * 2)
            rect.height += title_bar_height + border_width

        # Сделать скриншот всей зоны DC (контекста устройства)
        dcScreen = wx.ScreenDC()

        # Создать битмап, в котором сохранится скриншот
        # Учтите, что битмап должен быть достаточно большим, чтобы в него поместился скриншот
        # -1 значит использование текущей стандартной глубины цвета
        bmp = wx.Bitmap(rect.width, rect.height)

        # Создать в памяти DC, который будет использован непосредственно для скриншота
        memDC = wx.MemoryDC()

        # Прикажите DC использовать наш битмап
        # Все изображения из DC теперь переместится в битмап
        memDC.SelectObject(bmp)

        # Blit в данном случае скопируйте сам экран в кэш памяти
        # и, таким образом, он попадёт в битмап
        memDC.Blit(0,  # Скопируйте сюда координат Х
                   0,  # Скопируйте сюда координат Y
                   rect.width,  # Скопируйте эту ширину
                   rect.height,  # Скопируйте эту высоту
                   dcScreen,  # Место, откуда нужно скопировать
                   rect.x,  # Какой офсет у Х в оригинальном DC (контексте устройства)?
                   rect.y  # Какой офсет у Y в оригинальном DC?
                   )

        # Select the Bitmap out of the memory DC by selecting a new
        # uninitialized Bitmap
        memDC.SelectObject(wx.NullBitmap)
        fileName='vhod_3.bmp'



        img = bmp.ConvertToImage()

        img.SaveFile(fileName, wx.BITMAP_TYPE_BMP)

        print('...saving as BMP!')

        end1 = clock()

        print("Result (iterativ): выполняется за " + "\nФункция %1.10f секунд" % (end1 - start1))


# Запустите программу
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
